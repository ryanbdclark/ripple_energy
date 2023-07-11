"""The Owlet Smart Sock integration."""
from __future__ import annotations

import asyncio
import logging

from pyrippleapi.api import RippleAPI
from pyrippleapi.exceptions import (
    RippleConnectionError,
    RippleAuthenticationError,
    RippleDevicesError,
)
from pyrippleapi.generation_asset import GenerationAsset

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_API_TOKEN,
    CONF_SCAN_INTERVAL,
    CONF_EMAIL,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .coordinator import RippleCoordinator

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Owlet Smart Sock from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    ripple_api = RippleAPI(
        auth_token=entry.data[CONF_API_TOKEN], session=async_get_clientsession(hass)
    )

    try:
        assets = await ripple_api.request()

    except RippleAuthenticationError as err:
        _LOGGER.error("API Key not valid, setup ripple energy again")
        raise ConfigEntryAuthFailed(
            f"Credentials expired for {entry.data[CONF_EMAIL]}"
        ) from err

    except RippleConnectionError as err:
        raise ConfigEntryNotReady("Error connecting to ripple") from err

    except RippleDevicesError:
        _LOGGER.error("No ripple devices found to set up")
        return False

    assets = {
        asset["name"]: GenerationAsset(ripple_api, asset, assets["email"])
        for asset in assets["generation_assets"]
    }

    scan_interval = entry.options.get(CONF_SCAN_INTERVAL)
    coordinators = {
        name: RippleCoordinator(hass, asset, scan_interval)
        for (name, asset) in assets.items()
    }

    await asyncio.gather(
        *(
            coordinator.async_config_entry_first_refresh()
            for coordinator in list(coordinators.values())
        )
    )

    hass.data[DOMAIN][entry.entry_id] = coordinators

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

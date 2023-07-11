"""Owlet integration coordinator class."""
from __future__ import annotations

from datetime import timedelta
import logging

from pyrippleapi.exceptions import RippleConnectionError, RippleError
from pyrippleapi.generation_asset import GenerationAsset

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class RippleCoordinator(DataUpdateCoordinator):
    """Coordinator is responsible for querying the device at a specified route."""

    def __init__(self, hass: HomeAssistant, asset: GenerationAsset, interval) -> None:
        """Initialise a custom coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=asset.name,
            update_interval=timedelta(seconds=interval),
        )
        assert self.config_entry is not None
        self.config_entry: ConfigEntry
        self.asset = asset
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, asset.name)}, name=asset.name
        )

    async def _async_update_data(self) -> None:
        """Fetch the data from the device."""
        try:
            await self.asset.update_data()
        except (RippleError, RippleConnectionError) as err:
            raise UpdateFailed(err) from err

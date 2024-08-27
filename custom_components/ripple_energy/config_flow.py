"""Config flow for Owlet Smart Sock integration."""
from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import voluptuous as vol
from homeassistant import config_entries, exceptions
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_TOKEN, CONF_SCAN_INTERVAL
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from pyrippleapi.api import RippleAPI
from pyrippleapi.exceptions import (
    RippleAuthenticationError,
    RippleConnectionError,
    RippleDevicesError,
    RippleError,
)
from pyrippleapi.generation_asset import GenerationAsset

from .const import DOMAIN, POLLING_INTERVAL, ASSETS

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("api_token"): str,
    }
)


class RippleConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ripple Energy."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialise config flow."""
        self._entry: ConfigEntry
        self._api_key: str
        self._devices: dict[str, GenerationAsset]
        self.reauth_entry: ConfigEntry | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            self._api_key = user_input[CONF_API_TOKEN]

            ripple_api = RippleAPI(
                auth_token=self._api_key,
                session=async_get_clientsession(self.hass),
            )
            try:
                data = await ripple_api.request(assets=ASSETS)

            except RippleDevicesError:
                errors["base"] = "no_devices"
            except RippleAuthenticationError:
                errors["base"] = "invalid_api_token"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

            else:
                await self.async_set_unique_id(data["email"])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=data["email"],
                    data={CONF_API_TOKEN: self._api_key},
                    options={CONF_SCAN_INTERVAL: POLLING_INTERVAL},
                )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlowHandler:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_reauth(self, user_input: Mapping[str, Any]) -> FlowResult:
        """Handle reauth."""
        self.reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Dialog that informs the user that reauth is required."""
        assert self.reauth_entry is not None
        errors: dict[str, str] = {}

        if user_input is not None:
            entry_data = self.reauth_entry.data
            ripple_api = RippleAPI(
                user_input[CONF_API_TOKEN],
                session=async_get_clientsession(self.hass),
            )
            try:
                await ripple_api.request()

                await self.hass.config_entries.async_reload(self.reauth_entry.entry_id)

                return self.async_abort(reason="reauth_successful")

            except RippleAuthenticationError:
                errors["base"] = "invalid_api_token"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Error reauthenticating")

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({vol.Required(CONF_API_TOKEN): str}),
            errors=errors,
        )


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a options flow for ripple energy."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialise options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle options flow."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_SCAN_INTERVAL,
                    default=self.config_entry.options.get(CONF_SCAN_INTERVAL),
                ): vol.All(vol.Coerce(int), vol.Range(min=10)),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""

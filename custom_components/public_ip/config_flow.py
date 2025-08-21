"""Adds config flow for Public API."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    PublicIPClient,
    PublicIPClientCommunicationError,
    PublicIPClientError,
)
from .const import CONF_NAME, DOMAIN, LOGGER


class ConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Public API."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_connection()
            except PublicIPClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except PublicIPClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME,
                        default=(user_input or {}).get(CONF_NAME, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_connection(self) -> None:
        """Validate connection."""
        client = PublicIPClient(
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()

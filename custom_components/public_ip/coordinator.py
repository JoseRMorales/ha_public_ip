"""Coordinator for the Public IP integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    PublicIPClientError,
)

if TYPE_CHECKING:
    from .data import PublicDataConfigEntry


class PublicIPDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: PublicDataConfigEntry

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self.config_entry.runtime_data.client.async_get_data()
        except PublicIPClientError as exception:
            raise UpdateFailed(exception) from exception

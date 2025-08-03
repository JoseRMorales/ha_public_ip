"""Public IP for Home Assistant integration."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import PublicIPClient
from .const import DOMAIN, LOGGER
from .coordinator import PublicIPDataUpdateCoordinator
from .data import PublicIPData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import PublicDataConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PublicDataConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = PublicIPDataUpdateCoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=timedelta(minutes=5),
    )
    entry.runtime_data = PublicIPData(
        client=PublicIPClient(
            session=async_get_clientsession(hass),
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: PublicDataConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: PublicDataConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)

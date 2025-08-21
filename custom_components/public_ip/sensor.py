"""Sensor platform for Public IP."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    ENTITY_ID_FORMAT,
    SensorEntity,
    SensorEntityDescription,
)

from .const import DOMAIN
from .entity import PublicIPEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import PublicIPDataUpdateCoordinator
    from .data import PublicDataConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="public_ip",
        icon="mdi:ip",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: PublicDataConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        PublicIPSensor(
            title=entry.title,
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class PublicIPSensor(PublicIPEntity, SensorEntity):
    """Public IP Sensor class."""

    def __init__(
        self,
        title: str,
        coordinator: PublicIPDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self._attr_name = f"{title}"
        self.entity_id = ENTITY_ID_FORMAT.format(f"{DOMAIN}_{title}")
        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data

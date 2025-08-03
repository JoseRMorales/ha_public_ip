"""Custom types for Public API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import PublicIPClient
    from .coordinator import PublicIPDataUpdateCoordinator


type PublicDataConfigEntry = ConfigEntry[PublicIPData]


@dataclass
class PublicIPData:
    """Data for the Public IP integration."""

    client: PublicIPClient
    coordinator: PublicIPDataUpdateCoordinator
    integration: Integration

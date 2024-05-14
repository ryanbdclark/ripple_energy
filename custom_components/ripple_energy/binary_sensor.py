"""Support for Ripple binary sensors."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import RippleCoordinator
from .entity import RippleBaseEntity


@dataclass(kw_only=True)
class RippleBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Represent the Ripple binary sensor entity description."""


SENSORS: tuple[RippleBinarySensorEntityDescription, ...] = (
    RippleBinarySensorEntityDescription(
        key="status",
        translation_key="generating",
        device_class=BinarySensorDeviceClass.POWER,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Ripple sensors from config entry."""

    coordinators: RippleCoordinator = hass.data[DOMAIN][config_entry.entry_id].values()

    sensors = []

    for coordinator in coordinators:
        for sensor in SENSORS:
            sensors.append(RippleBinarySensor(coordinator, sensor))

    async_add_entities(sensors)


class RippleBinarySensor(RippleBaseEntity, BinarySensorEntity):
    """Representation of an Ripple binary sensor."""

    def __init__(
        self,
        coordinator: RippleCoordinator,
        sensor_description: RippleBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = sensor_description
        self._attr_unique_id = (
            f"{self.asset.name}-{self.entity_description.translation_key}"
        )

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""

        if self.entity_description.key == "status":
            state = True if self.asset.status == "Operational" else False

        return state

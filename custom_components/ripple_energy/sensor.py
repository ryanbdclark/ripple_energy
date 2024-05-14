"""Support for Ripple sensors."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower, UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN
from .coordinator import RippleCoordinator
from .entity import RippleBaseEntity


@dataclass(kw_only=True)
class RippleSensorEntityDescription(SensorEntityDescription):
    """Represent the Ripple sensor entity description."""


MEMBER_SENSORS: tuple[RippleSensorEntityDescription, ...] = (
    RippleSensorEntityDescription(
        key="member_capacity",
        translation_key="membercapacity",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    RippleSensorEntityDescription(
        key="member_expected_annual_generation",
        translation_key="memeberexpectedannualgeneration",
        native_unit_of_measurement=UnitOfEnergy.MEGA_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:meter-electric",
    ),
)

SENSORS: tuple[RippleSensorEntityDescription, ...] = (
    RippleSensorEntityDescription(
        key="latest_generated",
        translation_key="generatedlatest",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="latest_earned",
        translation_key="earnedlatest",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:currency-gbp",
    ),
    RippleSensorEntityDescription(
        key="today_generated",
        translation_key="generatedtoday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="today_earned",
        translation_key="earnedtoday",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:currency-gbp",
    ),
    RippleSensorEntityDescription(
        key="yesterday_generated",
        translation_key="generatedyesterday",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="yesterday_earned",
        translation_key="earnedyesterday",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:currency-gbp",
    ),
    RippleSensorEntityDescription(
        key="this_week_generated",
        translation_key="generatedthisweek",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="this_week_earned",
        translation_key="earnedthisweek",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:currency-gbp",
    ),
    RippleSensorEntityDescription(
        key="last_week_generated",
        translation_key="generatedlastweek",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:meter-electric",
        entity_registry_enabled_default=False,
    ),
    RippleSensorEntityDescription(
        key="last_week_earned",
        translation_key="earnedlastweek",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:currency-gbp",
        entity_registry_enabled_default=False,
    ),
    RippleSensorEntityDescription(
        key="this_month_generated",
        translation_key="generatedthismonth",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="this_month_earned",
        translation_key="earnedthismonth",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:currency-gbp",
    ),
    RippleSensorEntityDescription(
        key="last_month_generated",
        translation_key="generatedlastmonth",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:meter-electric",
        entity_registry_enabled_default=False,
    ),
    RippleSensorEntityDescription(
        key="last_month_earned",
        translation_key="earnedlastmonth",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:currency-gbp",
        entity_registry_enabled_default=False,
    ),
    RippleSensorEntityDescription(
        key="this_year_generated",
        translation_key="generatedthisyear",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="this_year_earned",
        translation_key="earnedthisyear",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:currency-gbp",
    ),
    RippleSensorEntityDescription(
        key="last_year_generated",
        translation_key="generatedlastyear",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:meter-electric",
        entity_registry_enabled_default=False,
    ),
    RippleSensorEntityDescription(
        key="last_year_earned",
        translation_key="earnedlastyear",
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:currency-gbp",
        entity_registry_enabled_default=False,
    ),
    RippleSensorEntityDescription(
        key="total_generated",
        translation_key="generatedtotal",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="total_earned",
        translation_key="earnedtotal",
        state_class=SensorStateClass.TOTAL,
        icon="mdi:currency-gbp",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Ripple sensors from config entry."""

    coordinators: list[RippleCoordinator] = list(
        hass.data[DOMAIN][config_entry.entry_id].values()
    )

    sensors = []

    for coordinator in coordinators:
        for sensor in SENSORS:
            if sensor.key in coordinator.asset.generation_data:
                sensors.append(RippleSensor(coordinator, sensor))
        for sensor in MEMBER_SENSORS:
            sensors.append(RippleMemberSensor(coordinator, sensor))

    async_add_entities(sensors)


class RippleSensor(RippleBaseEntity, SensorEntity):
    """Representation of an Ripple sensor."""

    def __init__(
        self,
        coordinator: RippleCoordinator,
        sensor_description: RippleSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description: RippleSensorEntityDescription = sensor_description
        self._attr_unique_id = (
            f"{self.asset.name}-{self.entity_description.translation_key}"
        )

    @property
    def native_value(self) -> StateType:
        """Return sensor value."""

        return self.asset.generation_data[self.entity_description.key]


class RippleMemberSensor(RippleSensor):
    def __init__(
        self,
        coordinator: RippleCoordinator,
        sensor_description: RippleSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, sensor_description)

    @property
    def native_value(self) -> StateType:
        """Return sensor value."""
        return getattr(self.asset, self.entity_description.key)

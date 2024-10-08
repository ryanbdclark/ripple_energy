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
from homeassistant.const import (
    UnitOfPower,
    UnitOfEnergy,
    UnitOfSpeed,
    UnitOfTemperature,
    REVOLUTIONS_PER_MINUTE,
    DEGREE,
)
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

TELEMETRY_SENSORS: tuple[RippleSensorEntityDescription, ...] = (
    RippleSensorEntityDescription(
        key="wind_speed_avg",
        translation_key="wind_speed",
        native_unit_of_measurement=UnitOfSpeed.MILES_PER_HOUR,
        device_class=SensorDeviceClass.WIND_SPEED,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:weather-windy",
    ),
    RippleSensorEntityDescription(
        key="generator_speed_avg",
        translation_key="generator_speed",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:turbine",
    ),
    RippleSensorEntityDescription(
        key="blade_angle_avg",
        translation_key="blade_angle",
        native_unit_of_measurement=DEGREE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:wind-turbine",
        entity_registry_enabled_default=False,
    ),
    RippleSensorEntityDescription(
        key="nacelle_position",
        translation_key="nacelle_position",
        native_unit_of_measurement=DEGREE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:wind-turbine",
        entity_registry_enabled_default=False,
    ),
    RippleSensorEntityDescription(
        key="tower_base_temp_avg",
        translation_key="tower_base_temp",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    RippleSensorEntityDescription(
        key="ambient_temp_max",
        translation_key="ambient_temp",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
)

SENSORS: tuple[RippleSensorEntityDescription, ...] = (
    RippleSensorEntityDescription(
        key="latest_generated",
        translation_key="generatedlatest",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="latest_earned",
        translation_key="earnedlatest",
        native_unit_of_measurement="GBP",
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
        native_unit_of_measurement="GBP",
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
        native_unit_of_measurement="GBP",
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
        native_unit_of_measurement="GBP",
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
        native_unit_of_measurement="GBP",
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
        native_unit_of_measurement="GBP",
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
        native_unit_of_measurement="GBP",
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
        native_unit_of_measurement="GBP",
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
        native_unit_of_measurement="GBP",
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
        native_unit_of_measurement="GBP",
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
        for sensor in TELEMETRY_SENSORS:
            if sensor.key in coordinator.asset.latest_telemetry:
                sensors.append(RippleTelemetrySensor(coordinator, sensor))

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


class RippleTelemetrySensor(RippleSensor):
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
        return self.asset.latest_telemetry[self.entity_description.key]

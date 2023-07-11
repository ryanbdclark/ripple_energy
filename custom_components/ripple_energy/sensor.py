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
    POWER_WATT,
    POWER_KILO_WATT,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN
from .coordinator import RippleCoordinator
from .entity import RippleBaseEntity


@dataclass
class RippleSensorEntityDescriptionMixin:
    """Ripple sensor description mix in."""

    element: str


@dataclass
class RippleSensorEntityDescription(
    SensorEntityDescription, RippleSensorEntityDescriptionMixin
):
    """Represent the Ripple sensor entity description."""


SENSORS: tuple[RippleSensorEntityDescription, ...] = (
    RippleSensorEntityDescription(
        key="membercapacity",
        translation_key="membercapacity",
        native_unit_of_measurement=POWER_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        element="member_capacity",
    ),
    RippleSensorEntityDescription(
        key="memeberexpectedannualgeneration",
        translation_key="memeberexpectedannualgeneration",
        native_unit_of_measurement="MWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="member_expected_annual_generation",
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="generatedlatest",
        translation_key="generatedlatest",
        native_unit_of_measurement="kWh",
        state_class=SensorStateClass.MEASUREMENT,
        element="latest_generated",
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="earnedlatest",
        translation_key="earnedlatest",
        state_class=SensorStateClass.MEASUREMENT,
        element="latest_earned",
        icon="mdi:currency-gbp",
    ),
    RippleSensorEntityDescription(
        key="generatedtoday",
        translation_key="generatedtoday",
        native_unit_of_measurement="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="today_generated",
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="earnedtoday",
        translation_key="earnedtoday",
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="today_earned",
        icon="mdi:currency-gbp",
    ),
    RippleSensorEntityDescription(
        key="generatedyesterday",
        translation_key="generatedyesterday",
        native_unit_of_measurement="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="yesterday_generated",
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="earnedyesterday",
        translation_key="earnedyesterday",
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="yesterday_earned",
        icon="mdi:currency-gbp",
    ),
    RippleSensorEntityDescription(
        key="generatedthisweek",
        translation_key="generatedthisweek",
        native_unit_of_measurement="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="this_week_generated",
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="earnedthisweek",
        translation_key="earnedthisweek",
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="this_week_earned",
        icon="mdi:currency-gbp",
    ),
    RippleSensorEntityDescription(
        key="generatedlastweek",
        translation_key="generatedlastweek",
        native_unit_of_measurement="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="last_week_generated",
        icon="mdi:meter-electric",
        entity_registry_enabled_default=False,
    ),
    RippleSensorEntityDescription(
        key="earnedlastweek",
        translation_key="earnedlastweek",
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="last_week_earned",
        icon="mdi:currency-gbp",
        entity_registry_enabled_default=False,
    ),
    RippleSensorEntityDescription(
        key="generatedthismonth",
        translation_key="generatedthismonth",
        native_unit_of_measurement="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="this_month_generated",
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="earnedthismonth",
        translation_key="earnedthismonth",
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="this_month_earned",
        icon="mdi:currency-gbp",
    ),
    RippleSensorEntityDescription(
        key="generatedlastmonth",
        translation_key="generatedlastmonth",
        native_unit_of_measurement="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="last_month_generated",
        icon="mdi:meter-electric",
        entity_registry_enabled_default=False,
    ),
    RippleSensorEntityDescription(
        key="earnedlastmonth",
        translation_key="earnedlastmonth",
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="last_month_earned",
        icon="mdi:currency-gbp",
        entity_registry_enabled_default=False,
    ),
    RippleSensorEntityDescription(
        key="generatedthisyear",
        translation_key="generatedthisyear",
        native_unit_of_measurement="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="this_year_generated",
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="earnedthisyear",
        translation_key="earnedthisyear",
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="this_year_earned",
        icon="mdi:currency-gbp",
    ),
    RippleSensorEntityDescription(
        key="generatedlastyear",
        translation_key="generatedlastyear",
        native_unit_of_measurement="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="last_year_generated",
        icon="mdi:meter-electric",
        entity_registry_enabled_default=False,
    ),
    RippleSensorEntityDescription(
        key="earnedlastyear",
        translation_key="earnedlastyear",
        state_class=SensorStateClass.TOTAL_INCREASING,
        element="last_year_earned",
        icon="mdi:currency-gbp",
        entity_registry_enabled_default=False,
    ),
    RippleSensorEntityDescription(
        key="generatedtotal",
        translation_key="generatedtotal",
        native_unit_of_measurement="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL,
        element="total_generated",
        icon="mdi:meter-electric",
    ),
    RippleSensorEntityDescription(
        key="earnedtotal",
        translation_key="earnedtotal",
        state_class=SensorStateClass.TOTAL,
        element="total_earned",
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

    async_add_entities(
        RippleSensor(coordinator, sensor)
        for coordinator in coordinators
        for sensor in SENSORS
    )


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

        if self.entity_description.element in [
            "member_capacity",
            "member_expected_annual_generation",
        ]:
            return getattr(self.asset, self.entity_description.element)

        return self.asset.generation_data[self.entity_description.element]

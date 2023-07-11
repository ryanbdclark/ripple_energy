"""Base class for Owlet entities."""

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import RippleCoordinator


class RippleBaseEntity(CoordinatorEntity[RippleCoordinator], Entity):
    """Base class for ripple generation asset entities."""

    def __init__(
        self,
        coordinator: RippleCoordinator,
    ) -> None:
        """Initialize the base entity."""
        super().__init__(coordinator)
        self.asset = coordinator.asset
        self._attr_device_info = coordinator.device_info
        self._attr_has_entity_name = True

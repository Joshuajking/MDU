from enum import Enum
from typing import Optional, Dict, Type

from sqlmodel import SQLModel, Field, MetaData

from dual_universe.src.models.base_model_mixin import BaseModelMixin

metadata = MetaData()


def get_enum_value(enum_class, enum_string):
    """Converts string to Enum if the string represents a valid Enum value."""
    # Extract just the Enum key (e.g., "LOGIN_SCREEN") from "ImageLocation.LOGIN_SCREEN"
    enum_name = enum_string.split(".")[-1]

    # Use getattr to access the enum value dynamically
    return getattr(enum_class, enum_name, None)


class ImageLocation(str, Enum):
    ACTIVE_TAKEN_MISSIONS_SCREEN = "active_taken_missions_screen"
    FLIGHT_SCREEN = "flight_screen"
    CONFIRMATION_SCREEN = "confirmation_screen"
    IN_GAME_SCREEN = "in_game_screen"
    LOGIN_SCREEN = "login_screen"
    LOGOUT_SCREEN = "logout_screen"
    MAP_SCREEN = "map_screen"
    MISSION_DETAILS_SCREEN = "mission_details_screen"
    RETRIEVE_DELIVER_DETAILS_SCREEN = "retrieve_deliver_mission_details_screen"
    NOTIFICATIONS_SCREEN = "notifications_screen"
    SEARCH_FOR_MISSIONS_SCREEN = "search_for_missions_screen"
    GEFORCE_NOW_SCREEN = "geforce_screen"
    WALLET_SCREEN = "wallet_screen"


class Image(SQLModel, BaseModelMixin, table=True):
    __table_args__ = {"extend_existing": True}

    image_name: str = Field(nullable=False)
    image_location: Optional[ImageLocation] = None
    image_url: str = Field(nullable=False)
    left: int = Field(default=None, nullable=True)
    top: int = Field(default=None, nullable=True)
    right: int = Field(default=None, nullable=True)
    bottom: int = Field(default=None, nullable=True)
    region: str = Field(default=None, nullable=True)
    center_x: int = Field(default=None, nullable=True)
    center_y: int = Field(default=None, nullable=True)


model_mapping: Dict[str, Type[SQLModel]] = {
    "image": Image,
}

from enum import Enum
from typing import Optional, Dict, Type

from sqlmodel import SQLModel, Field, MetaData

from dual_universe.src.models.base_model_mixin import BaseModelMixin

metadata = MetaData()


class SearchAreaLocation(str, Enum):
    ACTIVE_TAKEN_MISSIONS = "activeTakenMissions"
    AVAILABLE_MISSIONS = "availableMissions"
    RETRIEVE_DELIVERY_STATUS = "retrieveDeliveryStatus"
    FULL_ACTIVEMISSION_AREA = "fullActiveMissionArea"

    WARP_TARGET_DEST = "warpTargetDestination"
    GAME_CONSOLE_WINDOW = "gameConsoleWindow"
    ORBITAL_HUD_LANDED = "orbitalHudLanded"
    SPACE_FUEL = "spaceFuel"
    ATMO_FUEL = "atmoFuel"

    ABANDON_MISSION = "abandonMission"

    ORIGIN_POS = "originPos"
    DEST_POS = "destPos"

    TITLE_INFO = "titleInfo"
    SAFE_ZONE = "safeZone"
    DISTANCE = "distance"
    RIDE = "ride"
    STATUS = "status"
    ORIGIN_INFO = "originInfo"
    MASS = "mass"
    VOLUME = "volume"
    REWARD_INFO = "rewardInfo"
    DEST_INFO = "destInfo"


class SearchArea(BaseModelMixin, SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    region_name: Optional[SearchAreaLocation] = None
    left: int = Field(default=None, nullable=False)
    top: int = Field(default=None, nullable=False)
    right: int = Field(default=None, nullable=False)
    bottom: int = Field(default=None, nullable=False)
    center_x: int = Field(default=None, nullable=False)
    center_y: int = Field(default=None, nullable=False)
    region: str = Field(default=None, nullable=True)


model_mapping: Dict[str, Type[SQLModel]] = {
    "searcharea": SearchArea,
}

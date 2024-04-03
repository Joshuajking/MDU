import uuid
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, Field


def format_uuid(uuid_value: uuid.UUID) -> str:
	return str(uuid_value)


class BaseModelMixin(BaseModel):
	id: str = Field(default_factory=lambda: format_uuid(uuid.uuid4()), primary_key=True, index=True)
	created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
	updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

	class Config:
		from_attributes = True


class MissionMetadata(BaseModelMixin, SQLModel, table=True):
	round_trips: int = Field(default=0)
	flight_time: float = Field(default=0.0)
	package_percentage: float = Field(default=0.0)


class SearchAreaLocation(str, Enum):
	ACTIVE_TAKEN_MISSIONS = "activeTakenMissions"
	AVAILABLE_MISSIONS = "availableMissions"
	RETRIEVE_DELIVERY_STATUS = "retrieveDeliveryStatus"

	WALLET_CURRENCY = "walletCurrency"
	WALLET_RECIPIENT_LIST = "walletRecipientList"
	RECIPIENT_SEARCH_AREA = "recipeSearchArea"

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
	region_name: Optional[SearchAreaLocation] = None
	left: int = Field(default=None, nullable=False)
	top: int = Field(default=None, nullable=False)
	right: int = Field(default=None, nullable=False)
	bottom: int = Field(default=None, nullable=False)
	center_x: int = Field(default=None, nullable=False)
	center_y: int = Field(default=None, nullable=False)
	region: str = Field(default=None, nullable=True)


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
	WALLET_SCREEN = "wallet_screen"


class Image(SQLModel, BaseModelMixin, table=True):
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


class Character(SQLModel, BaseModelMixin, table=True):
	username: str = Field(nullable=False)
	email: str = Field(nullable=False)
	password: str = Field(nullable=False)
	has_package: bool = Field(default=False, nullable=False)
	has_gametime: bool = Field(default=True, nullable=False)
	active: bool = Field(default=True, nullable=False)


class Mission(SQLModel, BaseModelMixin, table=True):
	title: str = Field(max_length=30, nullable=True)
	safe_zone: bool = Field(default=None, nullable=True)
	distance: float = Field(default=None, nullable=True)
	ride: float = Field(default=None, nullable=True)
	mass: float = Field(default=None, nullable=True)
	volume: float = Field(default=None, nullable=True)
	reward: float = Field(default=None, nullable=True)
	planet_origin: str = Field(default=None, nullable=True)
	planet_destination: str = Field(default=None, nullable=True)
	origin_pos: str = Field(default=None, nullable=True)
	destination_pos: str = Field(default=None, nullable=True)
	character_id: str = Field(default=None, foreign_key="character.id")

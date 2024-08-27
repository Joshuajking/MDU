from sqlmodel import SQLModel, Field

from dual_universe.src.models.base_model_mixin import BaseModelMixin


class MissionMetadata(BaseModelMixin, SQLModel, table=True):
    round_trips: int = Field(default=0)
    flight_time: float = Field(default=0.0)
    package_percentage: float = Field(default=0.0)


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

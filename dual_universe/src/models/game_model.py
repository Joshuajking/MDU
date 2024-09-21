from typing import Dict, Type

from sqlmodel import SQLModel, Field, MetaData

from dual_universe.src.models.base_model_mixin import BaseModelMixin

metadata = MetaData()


class Game(BaseModelMixin, SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    name: str = Field(default="")
    app_path: str = Field(default="")
    game_clients: list[str] = Field(default=[])


model_mapping: Dict[str, Type[SQLModel]] = {
    "Game": Game,
}

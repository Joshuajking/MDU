from typing import Dict, Type

from sqlmodel import SQLModel, Field

from dual_universe.src.models.base_model_mixin import BaseModelMixin


class Game(BaseModelMixin, SQLModel, table=True):
    name: str = Field(default="")
    app_path: str = Field(default="")
    game_clients: list[str] = Field(default=[])


model_mapping: Dict[str, Type[SQLModel]] = {
    "Game": Game,
}

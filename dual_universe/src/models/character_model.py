from typing import Dict, Type

from sqlmodel import SQLModel, Field

from dual_universe.src.models.base_model_mixin import BaseModelMixin


class Character(SQLModel, BaseModelMixin, table=True):
    username: str = Field(nullable=False)
    email: str = Field(nullable=False)
    password: str = Field(nullable=False)
    has_package: bool = Field(default=False, nullable=False)
    has_gametime: bool = Field(default=True, nullable=False)
    active: bool = Field(default=True, nullable=False)


model_mapping: Dict[str, Type[SQLModel]] = {
    "character": Character,
}

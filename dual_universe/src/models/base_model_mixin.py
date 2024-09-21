import uuid
from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field


def format_uuid(uuid_value: uuid.UUID) -> str:
    return str(uuid_value)


class BaseModelMixin(BaseModel):
    id: str = Field(
        default_factory=lambda: format_uuid(uuid.uuid4()), primary_key=True, index=True
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    class Config:
        from_attributes = True

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()

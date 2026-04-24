from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class CategoryModel(BaseModel):
    id: int = Field(ge=0)
    name: str = Field(min_length=1)


class TagModel(BaseModel):
    id: int
    name: str


class PetStatus(str, Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"


class PetModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore"
    )

    id: Optional[int] = None
    name: str = Field(min_length=1)
    category: Optional[CategoryModel] = None
    photo_urls: List[str] = Field(default_factory=list)
    tags: List[TagModel] = Field(default_factory=list)
    status: Optional[PetStatus] = PetStatus.AVAILABLE

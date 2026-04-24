from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from pydantic.alias_generators import to_camel


class ConduitUserModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore"
    )

    username: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=8)
    bio: Optional[str] = None
    image: Optional[str] = None

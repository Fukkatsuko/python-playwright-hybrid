from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel


class PetUserModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore"
    )

    id: Optional[int] = Field(None, ge=0)
    username: str = Field(min_length=3)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    password: str = Field(min_length=8, exclude=True)
    phone: Optional[str] = None
    user_status: int = 0

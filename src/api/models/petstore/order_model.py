from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class OrderStatus(str, Enum):
    PLACED = "placed"
    APPROVED = "approved"
    DELIVERED = "delivered"


class OrderModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="ignore"
    )

    id: Optional[int] = Field(None, ge=0)
    pet_id: int = Field(ge=0)
    quantity: int = Field(default=1, ge=1)
    ship_date: Optional[datetime] = None
    status: OrderStatus = OrderStatus.PLACED
    complete: bool = False

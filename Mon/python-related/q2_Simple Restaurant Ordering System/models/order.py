from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum
from decimal import Decimal
import re
from db.memory import menu_db

class OrderStatus(str, Enum):
    pending = "pending"
    preparing = "preparing"
    ready = "ready"
    delivered = "delivered"
    cancelled = "cancelled"

class Customer(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: str
    phone: str

    @validator("phone")
    def valid_phone(cls, v):
        if not re.fullmatch(r"\d{10}", v):
            raise ValueError("Phone must be 10 digits")
        return v

class OrderItem(BaseModel):
    item_id: int
    quantity: int = Field(..., ge=1)

class Order(BaseModel):
    id: Optional[int]
    customer: Customer
    items: List[OrderItem]
    status: OrderStatus = OrderStatus.pending

    @property
    def total_price(self) -> Decimal:
        total = Decimal("0.00")
        for item in self.items:
            menu_item = menu_db.get(item.item_id)
            if menu_item:
                total += Decimal(menu_item["price"]) * item.quantity
        return round(total, 2)

    @validator("items")
    def must_have_items(cls, v):
        if not v:
            raise ValueError("Order must contain at least one item")
        return v

from pydantic import BaseModel, Field, validator
from enum import Enum
from decimal import Decimal
from typing import List, Optional
import re

class FoodCategory(str, Enum):
    starter = "starter"
    main_course = "main_course"
    dessert = "dessert"
    beverage = "beverage"

class FoodItem(BaseModel):
    id: Optional[int]
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    category: FoodCategory
    price: Decimal = Field(..., ge=1.00, le=100.00, decimal_places=2)
    is_available: bool = True
    preparation_time: int = Field(..., ge=1, le=120)
    ingredients: List[str] = Field(..., min_items=1)
    calories: Optional[int] = Field(None, gt=0)
    is_vegetarian: bool = False
    is_spicy: bool = False

    @property
    def price_category(self):
        if self.price < 10:
            return "Budget"
        elif self.price <= 25:
            return "Mid-range"
        else:
            return "Premium"

    @property
    def dietary_info(self):
        info = []
        if self.is_vegetarian:
            info.append("Vegetarian")
        if self.is_spicy:
            info.append("Spicy")
        return info

    @validator("name")
    def name_only_letters_spaces(cls, v):
        if not re.fullmatch(r"[A-Za-z ]+", v):
            raise ValueError("Name must contain only letters and spaces")
        return v

    @validator("is_spicy")
    def dessert_beverage_cannot_be_spicy(cls, v, values):
        if v and values.get("category") in {"dessert", "beverage"}:
            raise ValueError("Desserts and beverages cannot be spicy")
        return v

    @validator("calories")
    def vegetarian_calories_limit(cls, v, values):
        if v is not None and values.get("is_vegetarian") and v >= 800:
            raise ValueError("Vegetarian items must have less than 800 calories")
        return v

    @validator("preparation_time")
    def beverage_prep_time(cls, v, values):
        if values.get("category") == "beverage" and v > 10:
            raise ValueError("Beverages must have preparation time ≤ 10 minutes")
        return v

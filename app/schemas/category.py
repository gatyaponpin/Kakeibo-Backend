from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    user_group_id: Optional[int] = None
    category_name: str = Field(..., max_length=100)
    balance_kind: int = 0
    month_budget: int = 0  # ← DBの「月予算額」

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    user_group_id: Optional[int] = None
    category_name: Optional[str] = Field(None, max_length=100)
    balance_kind: Optional[int] = None
    month_budget: Optional[int] = None

class Category(CategoryBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

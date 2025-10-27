from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class KakeiboBase(BaseModel):
    user_group_id: Optional[int] = None
    category_id: Optional[int] = None  # SET NULL 運用
    balance_kind: int = 0
    balance_name: Optional[str] = Field(default=None, max_length=20)
    amount: int = 0
    memo: Optional[str] = Field(default=None, max_length=256)
    occur_date: date

class KakeiboCreate(KakeiboBase):
    pass

class KakeiboUpdate(BaseModel):
    user_group_id: Optional[int] = None
    category_id: Optional[int] = None
    balance_kind: Optional[int] = None
    balance_name: Optional[str] = Field(default=None, max_length=20)
    amount: Optional[int] = None
    memo: Optional[str] = Field(default=None, max_length=256)
    occur_date: Optional[date] = None

class Kakeibo(KakeiboBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

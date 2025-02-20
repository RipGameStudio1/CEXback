from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class License(BaseModel):
    type: str  # "free", "basic", "pro"
    expires_at: datetime
    features: List[str]  # список доступных функций
    is_active: bool = True
    purchase_date: datetime = Field(default_factory=datetime.utcnow)

class UserSettings(BaseModel):
    selected_coins: List[str] = []
    buy_exchanges: List[str] = []
    sell_exchanges: List[str] = []
    update_interval: int = 1

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    telegram_id: str
    username: str
    settings: UserSettings
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}

class ActivePair(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    buy_exchange: str
    sell_exchange: str
    coin_pair: str
    network: str
    buy_price: float
    sell_price: float
    spread: float
    commission: float
    last_updated: datetime = Field(default_factory=datetime.utcnow)

class PinnedPair(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    pair_id: PyObjectId
    pinned_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

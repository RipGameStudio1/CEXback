# app/routes/users.py

from fastapi import APIRouter, HTTPException
from ..database import get_database
from ..models import UserSettings, License
from datetime import datetime, timedelta
from bson import json_util
import json

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{telegram_id}")
async def get_user(telegram_id: str):
    try:
        db = await get_database()
        user = await db.users.find_one({"telegram_id": telegram_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return json.loads(json_util.dumps(user))
    except Exception as e:
        print(f"Error getting user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{telegram_id}")
async def create_user(telegram_id: str, username: str):
    try:
        db = await get_database()
        
        # Проверяем существующего пользователя
        existing_user = await db.users.find_one({"telegram_id": telegram_id})
        if existing_user:
            return json.loads(json_util.dumps(existing_user))

        # Создаем базовую лицензию
        default_license = {
            "type": "Free",
            "expires_at": datetime.utcnow() + timedelta(days=7),  # 7-дневный пробный период
            "is_active": True,
            "purchase_date": datetime.utcnow()
        }

        new_user = {
            "telegram_id": telegram_id,
            "username": username,
            "settings": {
                "selected_coins": [],
                "buy_exchanges": [],
                "sell_exchanges": [],
                "update_interval": 1
            },
            "license": default_license,
            "created_at": datetime.utcnow(),
            "last_active": datetime.utcnow()
        }

        result = await db.users.insert_one(new_user)
        created_user = await db.users.find_one({"_id": result.inserted_id})
        return json.loads(json_util.dumps(created_user))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{telegram_id}/settings")
async def update_user_settings(telegram_id: str, settings: UserSettings):
    try:
        db = await get_database()
        result = await db.users.update_one(
            {"telegram_id": telegram_id},
            {"$set": {"settings": settings.dict()}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Получаем обновленного пользователя
        updated_user = await db.users.find_one({"telegram_id": telegram_id})
        return json.loads(json_util.dumps(updated_user))
    except Exception as e:
        print(f"Error updating settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{telegram_id}/license")
async def get_user_license(telegram_id: str):
    try:
        db = await get_database()
        user = await db.users.find_one({"telegram_id": telegram_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return json.loads(json_util.dumps(user.get("license")))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{telegram_id}/license")
async def update_user_license(telegram_id: str, license: License):
    try:
        db = await get_database()
        result = await db.users.update_one(
            {"telegram_id": telegram_id},
            {"$set": {
                "license": license.dict(),
                "last_active": datetime.utcnow()
            }}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException
from ..database import get_database
from datetime import datetime
from typing import Optional
from bson import json_util, ObjectId
import json

router = APIRouter(prefix="/pairs", tags=["pairs"])

@router.get("/")
async def get_pairs(user_id: Optional[str] = None):
    try:
        db = await get_database()
        
        # Получаем активные пары
        active_pairs_cursor = db.active_pairs.find()
        active_pairs = await active_pairs_cursor.to_list(None)

        if not user_id:
            # Если user_id не указан, возвращаем все активные пары
            return {"active_pairs": json.loads(json_util.dumps(active_pairs))}
        
        # Получаем закрепленные пары пользователя
        pinned_pairs_cursor = db.pinned_pairs.find({"user_id": user_id})
        pinned_pairs = await pinned_pairs_cursor.to_list(None)

        # Возвращаем все активные пары и закрепленные пары
        response = {
            "pinned_pairs": json.loads(json_util.dumps(pinned_pairs)),
            "active_pairs": json.loads(json_util.dumps(active_pairs))  # Возвращаем все активные пары
        }
        
        return response

    except Exception as e:
        print(f"Error in get_pairs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{pair_id}/pin")
async def pin_pair(pair_id: str, user_id: str):
    try:
        db = await get_database()
        
        # Проверяем существование пары
        pair = await db.active_pairs.find_one({"_id": ObjectId(pair_id)})
        if not pair:
            raise HTTPException(status_code=404, detail="Pair not found")
        
        # Создаем или обновляем закрепленную пару
        pinned_pair = {
            "user_id": user_id,
            "pair_id": ObjectId(pair_id),
            "pinned_at": datetime.utcnow(),
            "is_active": True
        }
        
        await db.pinned_pairs.update_one(
            {"user_id": user_id, "pair_id": ObjectId(pair_id)},
            {"$set": pinned_pair},
            upsert=True
        )
        
        return {"status": "success", "message": "Pair pinned successfully"}

    except Exception as e:
        print(f"Error in pin_pair: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{pair_id}/pin")
async def unpin_pair(pair_id: str, user_id: str):
    try:
        db = await get_database()
        result = await db.pinned_pairs.delete_one({
            "user_id": user_id,
            "pair_id": ObjectId(pair_id)
        })
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Pinned pair not found")
            
        return {"status": "success", "message": "Pair unpinned successfully"}

    except Exception as e:
        print(f"Error in unpin_pair: {e}")
        raise HTTPException(status_code=500, detail=str(e))

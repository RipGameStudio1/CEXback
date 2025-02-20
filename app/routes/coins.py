from fastapi import APIRouter, HTTPException
from ..database import get_database
from bson import json_util
import json

router = APIRouter(prefix="/coins", tags=["coins"])

@router.get("/")
async def get_coins():
    try:
        db = await get_database()
        coins = await db.coins.find({"is_active": True}).to_list(None)
        return json.loads(json_util.dumps(coins))
    except Exception as e:
        print(f"Error in get_coins: {e}")
        raise HTTPException(status_code=500, detail=str(e))

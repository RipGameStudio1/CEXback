from fastapi import APIRouter, HTTPException
from ..database import get_database
from bson import json_util
import json

router = APIRouter(prefix="/exchanges", tags=["exchanges"])

@router.get("/")
async def get_exchanges():
    try:
        db = await get_database()
        exchanges = await db.exchanges.find({"is_active": True}).to_list(None)
        # Преобразуем BSON в JSON
        return json.loads(json_util.dumps(exchanges))
    except Exception as e:
        print(f"Error in get_exchanges: {e}")  # Для отладки
        raise HTTPException(status_code=500, detail=str(e))

from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

async def init_database():
    mongodb_url = os.getenv("MONGODB_URL")
    client = AsyncIOMotorClient(mongodb_url)
    db = client.scanner_db

    # Начальные данные для бирж
    exchanges = [
        {"name": "Binance", "symbol": "BINANCE", "is_active": True},
        {"name": "Kraken", "symbol": "KRAKEN", "is_active": True},
        {"name": "KuCoin", "symbol": "KUCOIN", "is_active": True},
        {"name": "Bybit", "symbol": "BYBIT", "is_active": True},
        {"name": "OKX", "symbol": "OKX", "is_active": True},
        {"name": "Gate.io", "symbol": "GATEIO", "is_active": True}
    ]

    # Начальные данные для монет
    coins = [
        {"name": "Bitcoin", "symbol": "BTC", "is_active": True},
        {"name": "Ethereum", "symbol": "ETH", "is_active": True},
        {"name": "Binance Coin", "symbol": "BNB", "is_active": True},
        {"name": "Ripple", "symbol": "XRP", "is_active": True},
        {"name": "Cardano", "symbol": "ADA", "is_active": True},
        {"name": "Solana", "symbol": "SOL", "is_active": True},
        {"name": "Polkadot", "symbol": "DOT", "is_active": True},
        {"name": "Dogecoin", "symbol": "DOGE", "is_active": True},
        {"name": "Polygon", "symbol": "MATIC", "is_active": True},
        {"name": "Chainlink", "symbol": "LINK", "is_active": True},
        {"name": "Avalanche", "symbol": "AVAX", "is_active": True},
        {"name": "Uniswap", "symbol": "UNI", "is_active": True}
    ]

    try:
        # Создаем коллекции если они не существуют
        await db.create_collection("exchanges")
        await db.create_collection("coins")
        await db.create_collection("users")
        await db.create_collection("active_pairs")
        await db.create_collection("pinned_pairs")
        
        print("Коллекции созданы успешно")

        # Очищаем существующие данные
        await db.exchanges.delete_many({})
        await db.coins.delete_many({})
        
        # Вставляем начальные данные
        if exchanges:
            result = await db.exchanges.insert_many(exchanges)
            print(f"Добавлено {len(result.inserted_ids)} бирж")
        
        if coins:
            result = await db.coins.insert_many(coins)
            print(f"Добавлено {len(result.inserted_ids)} монет")

        # Создаем индексы
        await db.users.create_index("telegram_id", unique=True)
        await db.active_pairs.create_index("last_updated")
        await db.pinned_pairs.create_index([("user_id", 1), ("pair_id", 1)], unique=True)
        
        print("Индексы созданы успешно")

    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(init_database())

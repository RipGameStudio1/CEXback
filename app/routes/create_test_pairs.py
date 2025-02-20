from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
from datetime import datetime
from bson import ObjectId

async def add_test_pairs():
    client = AsyncIOMotorClient("mongodb+srv://TestDB:TestDBpass@cluster0.ancth.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.scanner_db

    # Тестовые пары
    test_pairs = [
        {
            "buy_exchange": "BINANCE",
            "sell_exchange": "KRAKEN",
            "coin_pair": "BTC/USDT",
            "network": "BTC",
            "buy_price": 50000.0,
            "sell_price": 50200.0,
            "spread": 0.4,
            "commission": 0.001,
            "last_updated": datetime.utcnow()
        },
        {
            "buy_exchange": "KUCOIN",
            "sell_exchange": "BINANCE",
            "coin_pair": "ETH/USDT",
            "network": "ETH",
            "buy_price": 2800.0,
            "sell_price": 2815.0,
            "spread": 0.5,
            "commission": 0.001,
            "last_updated": datetime.utcnow()
        }
    ]

    try:
        # Очищаем существующие пары
        await db.active_pairs.delete_many({})
        
        # Добавляем новые пары
        result = await db.active_pairs.insert_many(test_pairs)
        print(f"Added {len(result.inserted_ids)} test pairs")
        print("Pair IDs:", [str(id) for id in result.inserted_ids])
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

async def check_pairs():
    client = AsyncIOMotorClient("mongodb+srv://TestDB:TestDBpass@cluster0.ancth.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.scanner_db
    
    pairs = await db.active_pairs.find().to_list(None)
    print("\nCurrent pairs in database:")
    for pair in pairs:
        print(f"Pair: {pair['coin_pair']}, Buy: {pair['buy_exchange']}, Sell: {pair['sell_exchange']}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_test_pairs())
    asyncio.run(check_pairs())

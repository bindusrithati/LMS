
import sys
import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy import text

# Explicitly add LMS path
lms_path = r"f:\LMS"
if lms_path not in sys.path:
    sys.path.append(lms_path)

# Load env from LMS folder
load_dotenv(os.path.join(lms_path, ".env"))

from app.connectors.database_connector import get_database
from app.utils.redis_client import redis_client

async def inspect_key():
    print("Inspecting Redis Key for python-batch...")
    session = None
    try:
        session = get_database()
        # Find python batch id
        query = text("SELECT id, name FROM batches WHERE name ILIKE '%python%' LIMIT 1")
        batch = session.execute(query).fetchone()
        
        if not batch:
            print("Python batch not found in DB.")
            return

        print(f"Batch found: {batch.name} (ID: {batch.id})")
        
        cache_key = f"cache:batch:{batch.id}"
        print(f"Checking Redis Key: {cache_key}")
        
        value = await redis_client.get(cache_key)
        ttl = await redis_client.ttl(cache_key)
        
        print(f"TTL: {ttl} seconds")
        print(f"Value: {value}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if session:
            session.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(inspect_key())


import sys
import os
from datetime import datetime

# Add project root to sys.path
sys.path.append(os.getcwd())

try:
    print("1. Testing Imports...")
    from app.entities.chat import ChatMessage
    from app.models.batch_models import GetChatMessageResponse
    from app.connectors.database_connector import get_database
    print("   Imports successful.")
except Exception as e:
    print(f"   FATAL: Import failed: {e}")
    sys.exit(1)

try:
    print("2. Testing Database Connection & Persistence...")
    db = get_database()
    print("   DB Session created.")
    
    # Check if we can query (even empty)
    count = db.query(ChatMessage).count()
    print(f"   Current message count: {count}")
    
    # Try creating a dummy message (rollback after)
    # We need valid batch_id and user_id. We'll try finding existing ones.
    from app.entities.user import User
    from app.entities.batch import Batch
    
    user = db.query(User).first()
    batch = db.query(Batch).first()
    
    if user and batch:
        print(f"   Found User ID: {user.id}, Batch ID: {batch.id}")
        msg = ChatMessage(
            batch_id=batch.id,
            user_id=user.id,
            message="Debug message",
            timestamp=datetime.now()
        )
        db.add(msg)
        db.flush() # Check for constraints
        print("   Message added and flushed successfully.")
        db.rollback()
        print("   Rollback successful.")
    else:
        print("   Skipping insert test (no user/batch found).")
        
    db.close()
    print("   DB Test successful.")
    
except Exception as e:
    print(f"   FATAL: Database error: {e}")
    import traceback
    traceback.print_exc()


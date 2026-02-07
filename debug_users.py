
import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from app.connectors.database_connector import get_db
from app.entities.user import User
from app.utils.enums import Roles
from sqlalchemy import text

def debug_users():
    db = next(get_db())
    print("Checking users...")
    
    # Check raw values first
    result = db.execute(text("SELECT id, name, role FROM users"))
    for row in result:
        print(f"User ID: {row[0]}, Name: {row[1]}, Raw Role ID: {row[2]}")
        try:
            role_enum = Roles(row[2])
            print(f"  -> Valid Enum: {role_enum.name}")
        except ValueError:
            print(f"  -> INVALID ROLE ID! Value: {row[2]}")

    print("-" * 20)
    print("Checking via ORM...")
    
    try:
        users = db.query(User).all()
        for user in users:
            print(f"User {user.id}: {user.name}")
            print(f"  Role Property: {user.role}")
    except Exception as e:
        print(f"ORM Query Failed: {e}")

if __name__ == "__main__":
    debug_users()

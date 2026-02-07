
import sys
import os
from dotenv import load_dotenv
from sqlalchemy import text

# Explicitly add LMS path
lms_path = r"f:\LMS"
if lms_path not in sys.path:
    sys.path.append(lms_path)

# Load env from LMS folder
load_dotenv(os.path.join(lms_path, ".env"))

from app.connectors.database_connector import get_database

def check_python_batch():
    print("Checking for 'python' batches...")
    session = None
    try:
        session = get_database()
        
        # Find batch
        query = text("SELECT id, name FROM batches WHERE name ILIKE '%python%'")
        batches = session.execute(query).fetchall()
        
        if not batches:
            print("No batch found with name containing 'python'")
            return

        for b in batches:
            print(f"Checking Batch: {b.name} (ID: {b.id})")
            
            # Check students
            s_query = text(f"""
                SELECT bs.id, u.name, u.email 
                FROM batch_students bs
                JOIN students s ON bs.student_id = s.id
                JOIN users u ON s.user_id = u.id
                WHERE bs.batch_id = {b.id}
            """)
            students = session.execute(s_query).fetchall()
            
            if students:
                print(f"  Found {len(students)} students:")
                for s in students:
                    print(f"    - {s.name} ({s.email})")
            else:
                print("  No students assigned to this batch in the database.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if session:
            session.close()

if __name__ == "__main__":
    check_python_batch()

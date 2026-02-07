
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

def debug_batches():
    print("Starting debug...")
    session = None
    try:
        session = get_database()
        print("Session created.")

        print("--- Batches ---")
        batches = session.execute(text("SELECT id, name FROM batches")).fetchall()
        for b in batches:
            print(f"Batch ID: {b.id}, Name: {b.name}")
            
            # Check batch_students table
            students = session.execute(text(f"SELECT * FROM batch_students WHERE batch_id = {b.id}")).fetchall()
            if students:
                print(f"  Found {len(students)} students in batch_students:")
                for s in students:
                    print(f"    - Mapping ID: {s.id}, Student ID: {s.student_id}, User ID (implied via Student): ?")
                    
                    # join to get user details
                    query = text(f"""
                        SELECT u.id, u.name, u.email 
                        FROM students st
                        JOIN users u ON st.user_id = u.id
                        WHERE st.id = {s.student_id}
                    """)
                    user = session.execute(query).fetchone()
                    if user:
                        print(f"      -> User: {user.name} ({user.email}) ID: {user.id}")
                    else:
                        print(f"      -> User not found for Student ID {s.student_id}")
            else:
                print("    No students found in batch_student table.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if session:
            session.close()

if __name__ == "__main__":
    debug_batches()

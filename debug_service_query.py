
import sys
import os
import asyncio
from dotenv import load_dotenv
from sqlalchemy.orm import aliased, Session

# Explicitly add LMS path
lms_path = r"f:\LMS"
if lms_path not in sys.path:
    sys.path.append(lms_path)

# Load env from LMS folder
load_dotenv(os.path.join(lms_path, ".env"))

from app.connectors.database_connector import get_database
from app.entities.student import Student
from app.entities.batch_student import BatchStudent
from app.entities.user import User
from app.utils.helpers import get_all_users_dict

def debug_query():
    print("Starting Service Logic Debug...")
    session = None
    try:
        session = get_database()
        batch_id = 25  # python-batch
        
        print(f"Querying for Batch ID: {batch_id}")

        StudentUser = aliased(User)
        query = (
            session.query(Student, StudentUser, BatchStudent)
            .join(BatchStudent, Student.id == BatchStudent.student_id)
            .join(StudentUser, Student.user_id == StudentUser.id)
            .filter(BatchStudent.batch_id == batch_id)
        )
        
        print("Generated SQL:")
        print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))
        
        results = query.all()
        
        print(f"Results Count: {len(results)}")
        
        if results:
            for student, user, batch_student in results:
                print(f"  - Student: {student.id}, User: {user.name} ({user.email}), BatchStudent: {batch_student.id}")
        else:
            print("  No results found via ORM query.")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if session:
            session.close()

if __name__ == "__main__":
    debug_query()

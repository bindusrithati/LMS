from dataclasses import dataclass
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
import json

from app.connectors.database_connector import get_db
from app.entities.syllabus import Syllabus
from app.models.base_response_model import SuccessMessageResponse
from app.models.syllabus_models import GetSyllabusResponse, SyllabusRequest
from app.utils.constants import (
    SYLLABUS_CREATED_SUCCESSFULLY,
    SYLLABUS_DELETED_SUCCESSFULLY,
    SYLLABUS_NAME_ALREADY_EXISTS,
    SYLLABUS_NOT_FOUND,
)
from app.utils.db_queries import get_all_syllabus, get_syllabus, get_syllabus_by_name
from app.utils.helpers import get_all_users_dict
from app.utils.validation import validate_data_exits, validate_data_not_found
from app.utils.redis_client import redis_client


@dataclass
class SyllabusService:
    db: Session = Depends(get_db)

    # ---------------- CREATE ----------------
    def create_syllabus(
        self, request: SyllabusRequest, logged_in_user_id: int
    ) -> SuccessMessageResponse:
        existing_syllabus = get_syllabus_by_name(self.db, request.name)
        validate_data_exits(existing_syllabus, SYLLABUS_NAME_ALREADY_EXISTS)

        syllabus = Syllabus(
            name=request.name,
            topics=list(set(request.topics)),
            created_by=logged_in_user_id,
            updated_by=logged_in_user_id,
        )

        self.db.add(syllabus)
        self.db.commit()

        # 🔥 cache invalidation
        redis_client.delete("cache:syllabus:all")

        return SuccessMessageResponse(message=SYLLABUS_CREATED_SUCCESSFULLY)

    # ---------------- HELPER ----------------
    def get_syllabus_response(
        self,
        syllabus: Syllabus,
    ) -> GetSyllabusResponse:
        users = get_all_users_dict(self.db)

        return GetSyllabusResponse(
            id=syllabus.id,
            name=syllabus.name,
            topics=syllabus.topics,
            created_at=syllabus.created_at,
            created_by=users.get(syllabus.created_by),
            updated_at=syllabus.updated_at,
            updated_by=users.get(syllabus.updated_by),
        )

    # ---------------- GET ALL SYLLABUS (CACHED) ----------------
    def get_all_syllabus(self) -> list[GetSyllabusResponse]:
        cache_key = "cache:syllabus:all"
        cached = redis_client.get(cache_key)

        if cached:
            return [GetSyllabusResponse(**item) for item in json.loads(cached)]

        syllabus_list = get_all_syllabus(self.db)
        response = [self.get_syllabus_response(syllabus) for syllabus in syllabus_list]

        redis_client.setex(cache_key, 120, json.dumps([r.dict() for r in response]))
        return response

    # ---------------- GET SYLLABUS BY ID (CACHED) ----------------
    def get_syllabus_by_id(self, syllabus_id: int) -> GetSyllabusResponse:
        cache_key = f"cache:syllabus:{syllabus_id}"
        cached = redis_client.get(cache_key)

        if cached:
            return GetSyllabusResponse(**json.loads(cached))

        syllabus = get_syllabus(self.db, syllabus_id)
        validate_data_not_found(syllabus, SYLLABUS_NOT_FOUND)

        response = self.get_syllabus_response(syllabus)

        redis_client.setex(cache_key, 120, json.dumps(response.dict()))
        return response

    # ---------------- VALIDATION ----------------
    def validate_update_fields(
        self, syllabus: Syllabus, request: SyllabusRequest
    ) -> None:
        if syllabus.name != request.name:
            existing_syllabus = get_syllabus_by_name(self.db, request.name)
            validate_data_exits(existing_syllabus, SYLLABUS_NAME_ALREADY_EXISTS)

    # ---------------- UPDATE ----------------
    def update_syllabus_by_id(
        self, syllabus_id: int, request: SyllabusRequest, logged_in_user_id: int
    ) -> SuccessMessageResponse:
        syllabus = get_syllabus(self.db, syllabus_id)
        validate_data_not_found(syllabus, SYLLABUS_NOT_FOUND)
        self.validate_update_fields(syllabus, request)

        syllabus.name = request.name
        syllabus.topics = list(set(request.topics))
        syllabus.updated_at = func.now()
        syllabus.updated_by = logged_in_user_id

        self.db.commit()

        # 🔥 cache invalidation
        redis_client.delete("cache:syllabus:all")
        redis_client.delete(f"cache:syllabus:{syllabus_id}")

        return SuccessMessageResponse(message=SYLLABUS_CREATED_SUCCESSFULLY)

    # ---------------- DELETE ----------------
    def delete_syllabus_by_id(self, syllabus_id: int) -> SuccessMessageResponse:
        syllabus = get_syllabus(self.db, syllabus_id)
        validate_data_not_found(syllabus, SYLLABUS_NOT_FOUND)

        self.db.delete(syllabus)
        self.db.commit()

        # 🔥 cache invalidation
        redis_client.delete("cache:syllabus:all")
        redis_client.delete(f"cache:syllabus:{syllabus_id}")

        return SuccessMessageResponse(message=SYLLABUS_DELETED_SUCCESSFULLY)

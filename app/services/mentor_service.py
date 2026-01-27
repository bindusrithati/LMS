from dataclasses import dataclass
from typing import Dict

from fastapi import Depends
from sqlalchemy.orm import Session

from app.connectors.database_connector import get_db
from app.entities.mentor import MentorProfile
from app.entities.user import User
from app.models.base_response_model import SuccessMessageResponse
from app.models.mentor_models import (
    MentorProfileRequest,
    GetMentorProfileResponse,
)
from app.utils.constants import (
    MENTOR_PROFILE_CREATED_SUCCESSFULLY,
    MENTOR_PROFILE_ALREADY_EXISTS,
    MENTOR_PROFILE_NOT_FOUND,
    USER_NOT_MENTOR,
)
from app.utils.db_queries import get_user_by_id
from app.utils.helpers import get_all_users_dict
from app.utils.validation import validate_data_exits, validate_data_not_found


@dataclass
class MentorService:
    db: Session = Depends(get_db)

    # ---------------- CREATE ----------------
    def create_mentor_profile(
        self, request: MentorProfileRequest, logged_in_user_id: int
    ) -> SuccessMessageResponse:

        mentor_user = get_user_by_id(self.db, request.user_id)
        validate_data_not_found(mentor_user, USER_NOT_MENTOR)

        if mentor_user.role != "Mentor":
            validate_data_not_found(None, USER_NOT_MENTOR)

        existing = (
            self.db.query(MentorProfile)
            .filter(MentorProfile.user_id == request.user_id)
            .first()
        )
        validate_data_exits(existing, MENTOR_PROFILE_ALREADY_EXISTS)

        mentor_profile = MentorProfile(
            user_id=request.user_id,
            expertise=request.expertise,
            experience_years=request.experience_years,
            bio=request.bio,
        )

        self.db.add(mentor_profile)
        self.db.commit()
        self.db.refresh(mentor_profile)

        return SuccessMessageResponse(message=MENTOR_PROFILE_CREATED_SUCCESSFULLY)

    # ---------------- GET BY USER ID ----------------
    def get_mentor_profile_by_user_id(self, user_id: int) -> GetMentorProfileResponse:

        mentor_profile = (
            self.db.query(MentorProfile)
            .filter(MentorProfile.user_id == user_id)
            .first()
        )
        validate_data_not_found(mentor_profile, MENTOR_PROFILE_NOT_FOUND)

        users_dict: Dict[int, str] = get_all_users_dict(self.db)
        mentor_user = self.db.query(User).filter(User.id == user_id).first()

        return GetMentorProfileResponse(
            id=mentor_profile.id,
            name=mentor_user.name,
            email=mentor_user.email,
            expertise=mentor_profile.expertise,
            experience_years=mentor_profile.experience_years,
            bio=mentor_profile.bio,
            is_available=mentor_profile.is_available,
            created_at=mentor_profile.created_at,
        )

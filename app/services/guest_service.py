from dataclasses import dataclass
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app.connectors.database_connector import get_db
from app.entities.guest import Guest
from app.models.base_response_model import SuccessMessageResponse
from app.models.guest_models import GuestRequest, GetGuestResponse
from app.utils.constants import (
    GUEST_CREATED_SUCCESSFULLY,
    GUEST_NOT_FOUND,
)
from app.utils.validation import validate_data_not_found


@dataclass
class GuestService:
    db: Session = Depends(get_db)

    # ---------------- CREATE ----------------
    def create_guest(self, request: GuestRequest) -> SuccessMessageResponse:

        guest = Guest(
            name=request.name,
            email=request.email,
            phone_number=request.phone_number,
            purpose=request.purpose,
        )

        self.db.add(guest)
        self.db.commit()

        return SuccessMessageResponse(message=GUEST_CREATED_SUCCESSFULLY)

    # ---------------- GET ALL ----------------
    def get_all_guests(self) -> List[GetGuestResponse]:
        guests = self.db.query(Guest).all()

        return [
            GetGuestResponse(
                id=g.id,
                name=g.name,
                email=g.email,
                phone_number=g.phone_number,
                purpose=g.purpose,
                created_at=g.created_at,
            )
            for g in guests
        ]

    # ---------------- GET BY ID ----------------
    def get_guest_by_id(self, guest_id: int) -> GetGuestResponse:
        guest = self.db.query(Guest).filter(Guest.id == guest_id).first()
        validate_data_not_found(guest, GUEST_NOT_FOUND)

        return GetGuestResponse(
            id=guest.id,
            name=guest.name,
            email=guest.email,
            phone_number=guest.phone_number,
            purpose=guest.purpose,
            created_at=guest.created_at,
        )

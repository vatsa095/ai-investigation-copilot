from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.person import get_person_by_id

router = APIRouter(
    prefix="/suspects",
    tags=["Suspects"]
)


@router.get("/{person_id}")
def get_suspect(person_id: int, db: Session = Depends(get_db)):

    person = get_person_by_id(db, person_id)

    if not person:
        return {
            "message": "Suspect not found"
        }

    return person
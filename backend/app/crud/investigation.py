from sqlalchemy.orm import Session
from app.models import Investigation


# -----------------------------
# CREATE INVESTIGATION NOTE
# -----------------------------
def create_investigation(db: Session, investigation):

    new_note = Investigation(
        case_id=investigation.case_id,
        officer_name=investigation.officer_name,
        notes=investigation.notes,
        next_step=investigation.next_step
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


# -----------------------------
# GET INVESTIGATION BY CASE
# -----------------------------
def get_investigation(db: Session, case_id: int):

    return db.query(Investigation).filter(
        Investigation.case_id == case_id
    ).all()


# -----------------------------
# DELETE INVESTIGATION
# -----------------------------
def delete_investigation(db: Session, investigation_id: int):

    note = db.query(Investigation).filter(
        Investigation.id == investigation_id
    ).first()

    if not note:
        return False

    db.delete(note)
    db.commit()

    return True
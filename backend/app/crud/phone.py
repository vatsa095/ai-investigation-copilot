from sqlalchemy.orm import Session
from app.models import Phone


# -----------------------------
# CREATE PHONE
# -----------------------------
def create_phone(db: Session, phone):

    new_phone = Phone(
        phone_number=phone.phone_number,
        person_id=phone.person_id
    )

    db.add(new_phone)
    db.commit()
    db.refresh(new_phone)

    return new_phone


# -----------------------------
# GET PHONE BY ID
# -----------------------------
def get_phone_by_id(db: Session, phone_id: int):

    return db.query(Phone).filter(
        Phone.id == phone_id
    ).first()


# -----------------------------
# GET PHONE NUMBER
# -----------------------------
def get_phone_number(db: Session, number: str):

    return db.query(Phone).filter(
        Phone.phone_number == number
    ).first()


# -----------------------------
# GET ALL PHONES OF A PERSON
# -----------------------------
def get_person_phones(db: Session, person_id: int):

    return db.query(Phone).filter(
        Phone.person_id == person_id
    ).all()


# -----------------------------
# DELETE PHONE
# -----------------------------
def delete_phone(db: Session, phone_id: int):

    phone = get_phone_by_id(db, phone_id)

    if not phone:
        return False

    db.delete(phone)
    db.commit()

    return True
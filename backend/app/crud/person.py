from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models import Person


# -----------------------------
# CREATE PERSON
# -----------------------------
def create_person(db: Session, person):

    new_person = Person(
        full_name=person.full_name,
        alias=person.alias,
        gender=person.gender,
        dob=person.dob,
        address=person.address
    )

    db.add(new_person)
    db.commit()
    db.refresh(new_person)

    return new_person


# -----------------------------
# GET PERSON BY ID
# -----------------------------
def get_person_by_id(db: Session, person_id: int):

    return db.query(Person).filter(
        Person.id == person_id
    ).first()


# -----------------------------
# GET PERSON BY NAME
# -----------------------------
def get_person_by_name(db: Session, name: str):

    return db.query(Person).filter(
        Person.full_name.ilike(f"%{name}%")
    ).all()


# -----------------------------
# SEARCH PERSON
# -----------------------------
def search_person(db: Session, keyword: str):

    return db.query(Person).filter(

        or_(
            Person.full_name.ilike(f"%{keyword}%"),
            Person.alias.ilike(f"%{keyword}%"),
            Person.address.ilike(f"%{keyword}%")
        )

    ).all()


# -----------------------------
# UPDATE PERSON
# -----------------------------
def update_person(db: Session, person_id: int, data):

    person = get_person_by_id(db, person_id)

    if not person:
        return None

    person.full_name = data.full_name
    person.alias = data.alias
    person.gender = data.gender
    person.dob = data.dob
    person.address = data.address

    db.commit()
    db.refresh(person)

    return person


# -----------------------------
# DELETE PERSON
# -----------------------------
def delete_person(db: Session, person_id: int):

    person = get_person_by_id(db, person_id)

    if not person:
        return False

    db.delete(person)
    db.commit()

    return True
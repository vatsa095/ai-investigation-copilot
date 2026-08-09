from sqlalchemy.orm import Session
from app.models import Associate


# -----------------------------
# CREATE ASSOCIATE
# -----------------------------
def create_associate(db: Session, associate):

    new_associate = Associate(
        person1_id=associate.person1_id,
        person2_id=associate.person2_id,
        relationship_type=associate.relationship_type
    )

    db.add(new_associate)
    db.commit()
    db.refresh(new_associate)

    return new_associate


# -----------------------------
# GET ASSOCIATES OF A PERSON
# -----------------------------
def get_associates(db: Session, person_id: int):

    return db.query(Associate).filter(
        (Associate.person1_id == person_id) |
        (Associate.person2_id == person_id)
    ).all()


# -----------------------------
# DELETE ASSOCIATE
# -----------------------------
def delete_associate(db: Session, associate_id: int):

    associate = db.query(Associate).filter(
        Associate.id == associate_id
    ).first()

    if not associate:
        return False

    db.delete(associate)
    db.commit()

    return True
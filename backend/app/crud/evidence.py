from sqlalchemy.orm import Session
from app.models import Evidence


# -----------------------------
# CREATE EVIDENCE
# -----------------------------
def create_evidence(db: Session, evidence):

    new_evidence = Evidence(
        evidence_type=evidence.evidence_type,
        description=evidence.description,
        case_id=evidence.case_id
    )

    db.add(new_evidence)
    db.commit()
    db.refresh(new_evidence)

    return new_evidence


# -----------------------------
# GET EVIDENCE BY ID
# -----------------------------
def get_evidence_by_id(db: Session, evidence_id: int):

    return db.query(Evidence).filter(
        Evidence.id == evidence_id
    ).first()


# -----------------------------
# GET ALL EVIDENCE OF A CASE
# -----------------------------
def get_case_evidence(db: Session, case_id: int):

    return db.query(Evidence).filter(
        Evidence.case_id == case_id
    ).all()


# -----------------------------
# DELETE EVIDENCE
# -----------------------------
def delete_evidence(db: Session, evidence_id: int):

    evidence = get_evidence_by_id(db, evidence_id)

    if not evidence:
        return False

    db.delete(evidence)
    db.commit()

    return True
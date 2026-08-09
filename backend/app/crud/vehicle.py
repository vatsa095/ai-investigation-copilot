from sqlalchemy.orm import Session
from app.models import Vehicle


# -----------------------------
# CREATE VEHICLE
# -----------------------------
def create_vehicle(db: Session, vehicle):

    new_vehicle = Vehicle(
        vehicle_number=vehicle.vehicle_number,
        vehicle_type=vehicle.vehicle_type,
        person_id=vehicle.person_id
    )

    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)

    return new_vehicle


# -----------------------------
# GET VEHICLE BY ID
# -----------------------------
def get_vehicle_by_id(db: Session, vehicle_id: int):

    return db.query(Vehicle).filter(
        Vehicle.id == vehicle_id
    ).first()


# -----------------------------
# GET VEHICLE NUMBER
# -----------------------------
def get_vehicle_number(db: Session, vehicle_number: str):

    return db.query(Vehicle).filter(
        Vehicle.vehicle_number == vehicle_number
    ).first()


# -----------------------------
# GET ALL VEHICLES OF A PERSON
# -----------------------------
def get_person_vehicles(db: Session, person_id: int):

    return db.query(Vehicle).filter(
        Vehicle.person_id == person_id
    ).all()


# -----------------------------
# DELETE VEHICLE
# -----------------------------
def delete_vehicle(db: Session, vehicle_id: int):

    vehicle = get_vehicle_by_id(db, vehicle_id)

    if not vehicle:
        return False

    db.delete(vehicle)
    db.commit()

    return True
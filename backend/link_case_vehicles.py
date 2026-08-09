import json

from app.database import SessionLocal
from app.models import Case, Vehicle, CaseVehicle


DATASET_FILE = "demo_cases_CASE053_CASE102.json"


def link_case_vehicles():

    db = SessionLocal()

    try:

        with open(DATASET_FILE, "r", encoding="utf-8") as f:
            dataset = json.load(f)

        created = 0
        skipped = 0
        missing_cases = 0
        missing_vehicles = 0

        print("\n========================================")
        print("LINKING CASES TO VEHICLES")
        print("========================================\n")

        for item in dataset:

            case_number = item.get("case_id")
            vehicle_number = item.get("vehicle_number")

            if not case_number or not vehicle_number:
                continue

            # --------------------------------
            # FIND CASE
            # --------------------------------

            case = db.query(Case).filter(
                Case.case_number == case_number
            ).first()

            if not case:
                print(
                    f"CASE NOT FOUND: {case_number}"
                )
                missing_cases += 1
                continue

            # --------------------------------
            # FIND VEHICLE
            # --------------------------------

            vehicle = db.query(Vehicle).filter(
                Vehicle.vehicle_number == vehicle_number
            ).first()

            if not vehicle:
                print(
                    f"VEHICLE NOT FOUND: "
                    f"{vehicle_number} "
                    f"for {case_number}"
                )
                missing_vehicles += 1
                continue

            # --------------------------------
            # CHECK EXISTING LINK
            # --------------------------------

            existing = db.query(CaseVehicle).filter(
                CaseVehicle.case_id == case.id,
                CaseVehicle.vehicle_id == vehicle.id
            ).first()

            if existing:
                skipped += 1
                continue

            # --------------------------------
            # CREATE LINK
            # --------------------------------

            link = CaseVehicle(
                case_id=case.id,
                vehicle_id=vehicle.id
            )

            db.add(link)

            created += 1

            print(
                f"LINKED: {case_number} "
                f"<-> {vehicle_number}"
            )

        db.commit()

        print("\n========================================")
        print("COMPLETE")
        print("========================================")

        print(
            f"Links created       : {created}"
        )

        print(
            f"Already existed     : {skipped}"
        )

        print(
            f"Missing cases       : {missing_cases}"
        )

        print(
            f"Missing vehicles    : {missing_vehicles}"
        )

        print("========================================\n")

    except Exception as e:

        db.rollback()

        print("\nERROR:")
        print(e)

    finally:

        db.close()


if __name__ == "__main__":
    link_case_vehicles()
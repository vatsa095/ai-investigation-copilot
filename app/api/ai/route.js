from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.ml.db_adapter import get_ai_cases
from app.ml.model import InvestigationModel
from app.ml.ai_service import AIService

router = APIRouter(
    prefix="/ai",
    tags=["AI Investigation"]
)


@router.get("/investigate/{suspect_name}")
def investigate_suspect(
    suspect_name: str,
    db: Session = Depends(get_db)
):

    # Get investigation data from database
    cases = get_ai_cases(db)

    # Create investigation model
    model = InvestigationModel(cases)

    # Run investigation
    result = model.investigate(suspect_name)

    analysis = result["analysis"]
    assessment = result["assessment"]

    # No matching data
    if not analysis:
        return {
            "suspect_name": suspect_name,
            "message": "No investigation data found."
        }

    # -------------------------------------------------
    # FALLBACK RECOMMENDATIONS
    # -------------------------------------------------
    # If the model does not generate recommendations,
    # provide useful investigation actions based on
    # the available case information.

    if not assessment.get("observations"):
        assessment["observations"] = []

    if not assessment.get("recommendations"):
        recommendations = []

        total_cases = analysis.get("total_cases", 0)
        phone_numbers = analysis.get("phone_numbers", [])
        vehicle_numbers = analysis.get("vehicle_numbers", [])
        locations = analysis.get("locations", [])
        crime_types = analysis.get("crime_types", [])

        if total_cases == 1:
            recommendations.append({
                "priority": "MEDIUM",
                "action": "Review the complete case file and verify all available evidence.",
                "reason": "Only one linked case was identified for this subject."
            })

        if crime_types:
            recommendations.append({
                "priority": "MEDIUM",
                "action": f"Review the evidence and modus operandi associated with the {crime_types[0]} case.",
                "reason": "The subject is currently linked to this crime type."
            })

        if phone_numbers:
            recommendations.append({
                "priority": "MEDIUM",
                "action": f"Review authorized records associated with phone number {phone_numbers[0]}.",
                "reason": "A phone number is linked to the subject's case."
            })

        if vehicle_numbers:
            recommendations.append({
                "priority": "MEDIUM",
                "action": f"Review available CCTV and authorized records involving vehicle {vehicle_numbers[0]}.",
                "reason": "A vehicle is linked to the subject's case."
            })

        if locations:
            recommendations.append({
                "priority": "MEDIUM",
                "action": f"Review CCTV and other available records around {locations[0]}.",
                "reason": "The location is associated with the subject's case."
            })

        assessment["recommendations"] = recommendations

    # Generate AI report
    ai = AIService()

    report = ai.generate_report(
        analysis,
        assessment
    )

    return {
        "analysis": analysis,
        "assessment": assessment,
        "report": report
    }
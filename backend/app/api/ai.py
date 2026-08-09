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

    # Run complete investigation
    result = model.investigate(suspect_name)

    analysis = result["analysis"]
    assessment = result["assessment"]

    # No matching data
    if not analysis:
        return {
            "suspect_name": suspect_name,
            "message": "No investigation data found."
        }

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
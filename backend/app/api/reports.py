from fastapi import APIRouter, HTTPException

from app.ml.dataset import InvestigationDataset
from app.ml.model import InvestigationModel
from app.ml.ai_service import AIService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

dataset = InvestigationDataset("datasets/cases.json")
cases = dataset.load_dataset()

model = InvestigationModel(cases)
ai = AIService()


@router.get("/investigate/{suspect_name}")
def investigate(suspect_name: str):

    analysis = model.investigate(suspect_name)

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="Suspect not found"
        )

    evidence = model.evidence_analysis(suspect_name)

    if evidence is None:
        evidence = {}

    report = ai.generate_report(
        analysis,
        evidence
    )

    return {
        "analysis": analysis,
        "evidence": evidence,
        "report": report
    }
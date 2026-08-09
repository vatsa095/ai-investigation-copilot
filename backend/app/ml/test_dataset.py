from pathlib import Path
from app.ml.dataset import InvestigationDataset

BASE_DIR = Path(__file__).resolve().parents[2]
dataset_path = BASE_DIR / "datasets" / "cases.json"

dataset = InvestigationDataset(str(dataset_path))

dataset.load_dataset()

print("Total Cases:", dataset.total_cases())
print(dataset.get_case("CASE001"))
from app.ml.dataset import InvestigationDataset
from app.ml.model import InvestigationModel
from app.ml.ai_service import AIService

# Load dataset
dataset = InvestigationDataset("datasets/cases.json")
cases = dataset.load_dataset()

# Create the model object
model = InvestigationModel(cases)
print("\nLINK ANALYSIS\n")

analysis = model.link_analysis("Ramesh Patil")

if analysis:
    print(f"Suspect        : {analysis['suspect_name']}")
    print(f"Total Cases    : {analysis['total_cases']}")
    print(f"Case IDs       : {', '.join(analysis['case_ids'])}")
    print(f"Phone Numbers  : {', '.join(analysis['phone_numbers'])}")
    print(f"Vehicles       : {', '.join(analysis['vehicle_numbers'])}")
    print(f"Crime Types    : {', '.join(analysis['crime_types'])}")
    print(f"Locations      : {', '.join(analysis['locations'])}")
else:
    print("No links found.")

print("\nAI INVESTIGATION REPORT\n")

analysis = model.investigate("Ramesh Patil")

ai = AIService()

print(ai.generate_report(analysis))
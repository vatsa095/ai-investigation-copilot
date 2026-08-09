import json


class InvestigationDataset:

    def __init__(self, path):
        self.path = path
        self.data = []

    def load_dataset(self):

        with open(self.path, "r", encoding="utf-8") as file:
            self.data = json.load(file)

        return self.data

    def get_case(self, case_id):

        for case in self.data:

            if case["case_id"] == case_id:
                return case

        return None

    def total_cases(self):

        return len(self.data)

    def get_all_cases(self):

        return self.data
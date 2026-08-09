class AIService:

    def generate_report(self, analysis, assessment=None):

        if not analysis:
            return "No investigation data found."

        report = f"""
========== AI INVESTIGATION REPORT ==========

Suspect Name      : {analysis['suspect_name']}
Total Cases       : {analysis['total_cases']}

Phone Numbers     : {', '.join(analysis['phone_numbers'])}

Vehicles          : {', '.join(analysis['vehicle_numbers'])}

Crime Types      : {', '.join(analysis['crime_types'])}

Locations         : {', '.join(analysis['locations'])}


========== INVESTIGATION ASSESSMENT ==========

"""

        if assessment:

            observations = assessment.get(
                "observations",
                []
            )

            if observations:

                report += "Key Observations:\n\n"

                for observation in observations:
                    report += f"• {observation}\n"

        return report
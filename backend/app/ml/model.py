from difflib import SequenceMatcher
from collections import Counter


class InvestigationModel:

    def __init__(self, cases):
        self.cases = cases

    # =========================================================
    # HELPER
    # =========================================================

    def _get(self, case, key, default=None):
        if isinstance(case, dict):
            return case.get(key, default)

        return getattr(case, key, default)

    def similarity(self, text1, text2):
        return SequenceMatcher(
            None,
            str(text1).lower(),
            str(text2).lower()
        ).ratio()

    # =========================================================
    # SEARCH
    # =========================================================

    def search_by_name(self, name):
        results = []

        for case in self.cases:
            suspect = self._get(
                case,
                "suspect_name",
                ""
            )

            if suspect and self.similarity(
                name,
                suspect
            ) > 0.6:
                results.append(case)

        return results

    def search_by_phone(self, phone):
        return [
            case
            for case in self.cases
            if self._get(
                case,
                "phone_number"
            ) == phone
        ]

    def search_by_vehicle(self, vehicle):
        return [
            case
            for case in self.cases
            if self._get(
                case,
                "vehicle_number"
            ) == vehicle
        ]

    def search_by_crime(self, crime):
        return [
            case
            for case in self.cases
            if str(
                self._get(
                    case,
                    "crime_type",
                    ""
                )
            ).lower() == crime.lower()
        ]

    def search_by_location(self, location):
        return [
            case
            for case in self.cases
            if location.lower() in str(
                self._get(
                    case,
                    "location",
                    ""
                )
            ).lower()
        ]

    # =========================================================
    # DIRECT LINK ANALYSIS
    # =========================================================

    def link_analysis(self, suspect_name):
        related_cases = []

        for case in self.cases:
            suspect = str(
                self._get(
                    case,
                    "suspect_name",
                    ""
                )
            )

            if suspect.lower() == suspect_name.lower():
                related_cases.append(case)

        if not related_cases:
            return None

        return {
            "suspect_name": suspect_name,
            "total_cases": len(related_cases),

            "phone_numbers": list(set(
                self._get(
                    c,
                    "phone_number"
                )
                for c in related_cases
                if self._get(
                    c,
                    "phone_number"
                )
            )),

            "vehicle_numbers": list(set(
                self._get(
                    c,
                    "vehicle_number"
                )
                for c in related_cases
                if self._get(
                    c,
                    "vehicle_number"
                )
            )),

            "crime_types": list(set(
                self._get(
                    c,
                    "crime_type"
                )
                for c in related_cases
                if self._get(
                    c,
                    "crime_type"
                )
            )),

            "locations": list(set(
                self._get(
                    c,
                    "location"
                )
                for c in related_cases
                if self._get(
                    c,
                    "location"
                )
            )),

            "case_ids": [
                self._get(
                    c,
                    "case_id"
                )
                for c in related_cases
            ]
        }

    # =========================================================
    # CONNECTION SCORING
    # =========================================================

    def connection_score(
        self,
        base_case,
        other_case,
        suspect_name
    ):
        score = 0
        reasons = []

        base_suspect = str(
            self._get(
                base_case,
                "suspect_name",
                ""
            )
        ).lower()

        other_suspect = str(
            self._get(
                other_case,
                "suspect_name",
                ""
            )
        ).lower()

        base_phone = self._get(
            base_case,
            "phone_number"
        )

        other_phone = self._get(
            other_case,
            "phone_number"
        )

        base_vehicle = self._get(
            base_case,
            "vehicle_number"
        )

        other_vehicle = self._get(
            other_case,
            "vehicle_number"
        )

        base_location = str(
            self._get(
                base_case,
                "location",
                ""
            )
        ).lower()

        other_location = str(
            self._get(
                other_case,
                "location",
                ""
            )
        ).lower()

        base_crime = str(
            self._get(
                base_case,
                "crime_type",
                ""
            )
        ).lower()

        other_crime = str(
            self._get(
                other_case,
                "crime_type",
                ""
            )
        ).lower()

        # -----------------------------------------------------
        # SAME SUSPECT
        # -----------------------------------------------------

        if (
            base_suspect == suspect_name.lower()
            and
            other_suspect == suspect_name.lower()
        ):
            score += 5

            reasons.append(
                "Same suspect"
            )

        # -----------------------------------------------------
        # SAME PHONE
        # -----------------------------------------------------

        if (
            base_phone
            and other_phone
            and base_phone == other_phone
        ):
            score += 3

            reasons.append(
                "Same phone number"
            )

        # -----------------------------------------------------
        # SAME VEHICLE
        # -----------------------------------------------------

        if (
            base_vehicle
            and other_vehicle
            and base_vehicle == other_vehicle
        ):
            score += 3

            if (
                base_suspect != other_suspect
                and other_suspect
            ):
                reasons.append(
                    f"Same vehicle used by "
                    f"{other_suspect.title()}"
                )
            else:
                reasons.append(
                    "Same vehicle"
                )

        # -----------------------------------------------------
        # SAME LOCATION
        # -----------------------------------------------------

        if (
            base_location
            and other_location
            and base_location == other_location
        ):
            score += 1

            reasons.append(
                "Same location"
            )

        # -----------------------------------------------------
        # SAME CRIME TYPE
        # -----------------------------------------------------

        if (
            base_crime
            and other_crime
            and base_crime == other_crime
        ):
            score += 1

            reasons.append(
                "Same crime type"
            )

        # -----------------------------------------------------
        # CONNECTION STRENGTH
        # -----------------------------------------------------

        if score >= 8:
            strength = "HIGH"

        elif score >= 5:
            strength = "MEDIUM"

        else:
            strength = "LOW"

        return {
            "score": score,
            "strength": strength,
            "reasons": reasons
        }

    # =========================================================
    # NETWORK ANALYSIS
    # =========================================================

    def network_analysis(self, suspect_name):

        suspect_cases = [
            c
            for c in self.cases
            if str(
                self._get(
                    c,
                    "suspect_name",
                    ""
                )
            ).lower() == suspect_name.lower()
        ]

        if not suspect_cases:
            return None

        # -----------------------------------------------------
        # IDENTIFIERS BELONGING TO THE SUSPECT
        # -----------------------------------------------------

        phones = {
            self._get(
                c,
                "phone_number"
            )
            for c in suspect_cases
            if self._get(
                c,
                "phone_number"
            )
        }

        vehicles = {
            self._get(
                c,
                "vehicle_number"
            )
            for c in suspect_cases
            if self._get(
                c,
                "vehicle_number"
            )
        }

        linked_cases = []
        seen_case_ids = set()

        # -----------------------------------------------------
        # FIND CASES CONNECTED THROUGH PHONE OR VEHICLE
        # -----------------------------------------------------

        for case in self.cases:

            case_id = self._get(
                case,
                "case_id"
            )

            case_phone = self._get(
                case,
                "phone_number"
            )

            case_vehicle = self._get(
                case,
                "vehicle_number"
            )

            connected = (
                case_phone in phones
                or
                case_vehicle in vehicles
            )

            if connected and case_id not in seen_case_ids:

                linked_cases.append(case)

                seen_case_ids.add(case_id)

        return linked_cases

    # =========================================================
    # CONNECTION ANALYSIS
    # =========================================================

    def connection_analysis(self, suspect_name):

        suspect_cases = [
            c
            for c in self.cases
            if str(
                self._get(
                    c,
                    "suspect_name",
                    ""
                )
            ).lower() == suspect_name.lower()
        ]

        if not suspect_cases:
            return []

        # -----------------------------------------------------
        # IMPORTANT:
        #
        # Instead of only analysing the suspect's own cases,
        # analyse ALL cases connected through phone/vehicle.
        # -----------------------------------------------------

        linked_cases = self.network_analysis(
            suspect_name
        )

        if not linked_cases:
            return []

        connections = []

        base_case = suspect_cases[0]

        for case in linked_cases:

            result = self.connection_score(
                base_case,
                case,
                suspect_name
            )

            connections.append({

                "case_id": self._get(
                    case,
                    "case_id"
                ),

                "case_number": self._get(
                    case,
                    "case_number"
                ),

                "suspect_name": self._get(
                    case,
                    "suspect_name"
                ),

                "crime_type": self._get(
                    case,
                    "crime_type"
                ),

                "location": self._get(
                    case,
                    "location"
                ),

                "phone_number": self._get(
                    case,
                    "phone_number"
                ),

                "vehicle_number": self._get(
                    case,
                    "vehicle_number"
                ),

                "score": result["score"],

                "strength": result["strength"],

                "reasons": result["reasons"]
            })

        connections.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return connections
        # =========================================================
    # PATTERN ANALYSIS
    # =========================================================

    def pattern_analysis(self, suspect_name):

        linked_cases = self.network_analysis(
            suspect_name
        )

        # IMPORTANT:
        # Return an empty structure instead of None.
        # This prevents investigation_assessment()
        # from crashing when there are no linked cases.

        if not linked_cases:
            return {
                "total_linked_cases": 0,
                "crime_patterns": {},
                "location_patterns": {},
                "phone_patterns": {},
                "vehicle_patterns": {}
            }

        crimes = Counter()
        locations = Counter()
        phones = Counter()
        vehicles = Counter()

        for case in linked_cases:

            crime = self._get(
                case,
                "crime_type"
            )

            location = self._get(
                case,
                "location"
            )

            phone = self._get(
                case,
                "phone_number"
            )

            vehicle = self._get(
                case,
                "vehicle_number"
            )

            if crime:
                crimes[crime] += 1

            if location:
                locations[location] += 1

            if phone:
                phones[phone] += 1

            if vehicle:
                vehicles[vehicle] += 1

        return {
            "total_linked_cases": len(linked_cases),

            "crime_patterns":
                dict(crimes),

            "location_patterns":
                dict(locations),

            "phone_patterns":
                dict(phones),

            "vehicle_patterns":
                dict(vehicles)
        }

    # =========================================================
    # INVESTIGATION ASSESSMENT
    # =========================================================

    def investigation_assessment(
        self,
        suspect_name
    ):

        analysis = self.link_analysis(
            suspect_name
        )

        if not analysis:
            return None

        patterns = self.pattern_analysis(
            suspect_name
        )

        # Safety fallback
        if patterns is None:
            patterns = {
                "total_linked_cases": 0,
                "crime_patterns": {},
                "location_patterns": {},
                "phone_patterns": {},
                "vehicle_patterns": {}
            }

        connections = self.connection_analysis(
            suspect_name
        )

        observations = []
        recommendations = []

        # =====================================================
        # CASE COUNT
        # =====================================================

        if analysis["total_cases"] >= 3:

            observations.append(
                f"The subject is associated with "
                f"{analysis['total_cases']} cases."
            )

            recommendations.append({
                "priority": "HIGH",

                "action":
                    "Review the subject's previous cases "
                    "for recurring investigative patterns.",

                "reason":
                    "Multiple linked cases were identified."
            })

        elif analysis["total_cases"] == 2:

            observations.append(
                "The subject is associated with "
                "2 cases."
            )

            recommendations.append({
                "priority": "MEDIUM",

                "action":
                    "Compare the two case files for "
                    "common evidence, locations, vehicles "
                    "and modus operandi.",

                "reason":
                    "Two cases are associated with the subject."
            })

        elif analysis["total_cases"] == 1:

            observations.append(
                "Only one case is currently associated "
                "with the subject."
            )

            recommendations.append({
                "priority": "MEDIUM",

                "action":
                    "Review the complete case file and "
                    "verify all available evidence.",

                "reason":
                    "Only one direct case was identified."
            })

           # =====================================================
    # CRIME PATTERNS
    # =====================================================

        if patterns is None:
          patterns = {
            "total_linked_cases": 0,
            "crime_patterns": {},
            "location_patterns": {},
            "phone_patterns": {},
            "vehicle_patterns": {}
        }
          for crime, count in patterns[
              "crime_patterns"
              ].items():

            if count >= 2:

                observations.append(
                    f"{crime} appears in "
                    f"{count} linked cases."
                )

                recommendations.append({
                    "priority":
                        "HIGH"
                        if count >= 4
                        else "MEDIUM",

                    "action":
                        f"Compare evidence and modus operandi "
                        f"across the {crime} cases.",

                    "reason":
                        f"A repeated {crime} pattern was "
                        f"detected across {count} cases."
                })

        # =====================================================
        # LOCATION PATTERNS
        # =====================================================

        for location, count in patterns[
            "location_patterns"
        ].items():

            if count >= 2:

                observations.append(
                    f"{location} appears in "
                    f"{count} linked cases."
                )

                recommendations.append({
                    "priority": "MEDIUM",

                    "action":
                        f"Review CCTV and other available "
                        f"records around {location}.",

                    "reason":
                        f"The location appears in "
                        f"{count} linked cases."
                })

        # =====================================================
        # PHONE PATTERNS
        # =====================================================

        for phone, count in patterns[
            "phone_patterns"
        ].items():

            if count >= 2:

                observations.append(
                    f"Phone number {phone} is associated "
                    f"with {count} linked cases."
                )

                recommendations.append({
                    "priority": "HIGH",

                    "action":
                        f"Review authorized call records "
                        f"associated with {phone}.",

                    "reason":
                        f"The identifier appears across "
                        f"{count} linked cases."
                })

        # =====================================================
        # VEHICLE PATTERNS
        # =====================================================

        for vehicle, count in patterns[
            "vehicle_patterns"
        ].items():

            if count >= 2:

                observations.append(
                    f"Vehicle {vehicle} is associated "
                    f"with {count} linked cases."
                )

                recommendations.append({
                    "priority": "MEDIUM",

                    "action":
                        f"Compare available CCTV or "
                        f"vehicle sightings for {vehicle}.",

                    "reason":
                        f"The vehicle appears across "
                        f"{count} linked cases."
                })

        # =====================================================
        # SHARED VEHICLE DETECTION
        # =====================================================

        shared_vehicle_people = {}

        for case in connections:

            vehicle = case.get(
                "vehicle_number"
            )

            person = case.get(
                "suspect_name"
            )

            if not vehicle or not person:
                continue

            if person.lower() == suspect_name.lower():
                continue

            shared_vehicle_people.setdefault(
                vehicle,
                set()
            ).add(person)

        for vehicle, people in shared_vehicle_people.items():

            if people:

                people_text = ", ".join(
                    sorted(people)
                )

                observations.append(
                    f"Vehicle {vehicle} is also "
                    f"associated with other persons: "
                    f"{people_text}."
                )

                recommendations.append({
                    "priority": "HIGH",

                    "action":
                        f"Investigate the shared use of "
                        f"vehicle {vehicle} across the "
                        f"connected persons.",

                    "reason":
                        f"The vehicle links the subject "
                        f"to {people_text}."
                })

        # =====================================================
        # SHARED PHONE DETECTION
        # =====================================================

        shared_phone_people = {}

        for case in connections:

            phone = case.get(
                "phone_number"
            )

            person = case.get(
                "suspect_name"
            )

            if not phone or not person:
                continue

            if person.lower() == suspect_name.lower():
                continue

            shared_phone_people.setdefault(
                phone,
                set()
            ).add(person)

        for phone, people in shared_phone_people.items():

            if people:

                people_text = ", ".join(
                    sorted(people)
                )

                observations.append(
                    f"Phone number {phone} is also "
                    f"associated with other persons: "
                    f"{people_text}."
                )

                recommendations.append({
                    "priority": "HIGH",

                    "action":
                        f"Review the authorized records "
                        f"associated with phone {phone}.",

                    "reason":
                        f"The phone identifier links the "
                        f"subject to {people_text}."
                })

        # =====================================================
        # CONNECTION STRENGTH
        # =====================================================

        high_connections = [
            c
            for c in connections
            if c.get("strength") == "HIGH"
        ]

        if high_connections:

            observations.append(
                f"{len(high_connections)} high-strength "
                f"connection(s) were identified."
            )

            recommendations.append({
                "priority": "HIGH",

                "action":
                    "Prioritize review of the high-strength "
                    "case connections and supporting evidence.",

                "reason":
                    "Strong links were identified between "
                    "the subject and connected cases."
            })

        # =====================================================
        # NO CONNECTIONS
        # =====================================================

        if not connections:

            observations.append(
                "No additional connected cases were "
                "identified through the available "
                "phone or vehicle identifiers."
            )

        # =====================================================
        # REMOVE DUPLICATE RECOMMENDATIONS
        # =====================================================

        unique_recommendations = []

        seen_recommendations = set()

        for recommendation in recommendations:

            key = (
                recommendation.get("priority"),
                recommendation.get("action"),
                recommendation.get("reason")
            )

            if key not in seen_recommendations:

                seen_recommendations.add(key)

                unique_recommendations.append(
                    recommendation
                )

        recommendations = unique_recommendations

        # =====================================================
        # SORT RECOMMENDATIONS
        # =====================================================

        priority_order = {
            "HIGH": 1,
            "MEDIUM": 2,
            "LOW": 3
        }

        recommendations.sort(
            key=lambda x:
                priority_order.get(
                    x["priority"],
                    3
                )
        )

        # =====================================================
        # FINAL ASSESSMENT
        # =====================================================

        return {
            "suspect_name":
                suspect_name,

            "observations":
                observations,

            "recommendations":
                recommendations,

            "connections":
                connections,

            "patterns":
                patterns
        }

    # =========================================================
    # COMPLETE INVESTIGATION
    # =========================================================

    def investigate(
        self,
        suspect_name
    ):

        analysis = self.link_analysis(
            suspect_name
        )

        if not analysis:

            return {
                "analysis": None,
                "assessment": None
            }

        assessment = self.investigation_assessment(
            suspect_name
        )

        return {
            "analysis":
                analysis,

            "assessment":
                assessment
        }

    # =========================================================
    # EVIDENCE ANALYSIS
    # =========================================================

    def evidence_analysis(
        self,
        suspect_name
    ):

        linked_cases = self.network_analysis(
            suspect_name
        )

        if not linked_cases:
            return None

        evidence_counter = Counter()

        for case in linked_cases:

            evidence = self._get(
                case,
                "evidence"
            )

            if evidence:

                evidence_counter[
                    evidence
                ] += 1

        return dict(
            evidence_counter
        )

    # =========================================================
    # ADDITIONAL CASE SEARCH
    # =========================================================

    def find_related_cases(
        self,
        suspect_name
    ):

        return self.network_analysis(
            suspect_name
        )

    # =========================================================
    # FULL ANALYSIS
    # =========================================================

    def full_analysis(
        self,
        suspect_name
    ):

        analysis = self.link_analysis(
            suspect_name
        )

        if not analysis:

            return {
                "analysis": None,
                "assessment": None,
                "evidence": None
            }

        assessment = self.investigation_assessment(
            suspect_name
        )

        evidence = self.evidence_analysis(
            suspect_name
        )

        return {
            "analysis":
                analysis,

            "assessment":
                assessment,

            "evidence":
                evidence
        }
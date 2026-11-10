class FinancialValidator:
    def validate(self, fact: dict) -> bool:
        if fact["value"] is None:
            return False

        if not fact["unit"]:
            return False

        if not fact["period_end"]:
            return False

        if fact["period_type"] == "duration":
            if not fact["period_start"]:
                return False

        return True
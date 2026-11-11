class FinancialValidator:
    def validate(self, fact: dict) -> bool:
        if fact.get('form') != "10-K": 
            return False
            
        if fact.get("val") is None:
            return False

        if not fact.get("start"):
            return False

        if not fact.get("end"):
            return False

        return True
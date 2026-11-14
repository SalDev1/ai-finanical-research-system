"""Financial calculation utilities."""

class FinancialCalculator:

    @staticmethod
    def growth_rate(current : float, previous : float) -> float:
        if previous == 0:
            return 0.0
        return round(
            ((current - previous) / previous) * 100,
            2
        )

    @staticmethod
    def margin(numerator : float, denominator : float) -> float:
        if denominator == 0:
            return 0.0
        return round((numerator / denominator) * 100, 2) 

    @staticmethod
    def ratio(numerator : float, denominator : float) -> float:
        if denominator == 0:
            return None
        return numerator / denominator
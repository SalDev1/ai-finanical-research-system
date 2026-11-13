"""Financial analysis workflows."""
from .financial_calculator import FinancialCalculator
from .financial_metrics import FinancialMetric


class FinancialAnalysis:
    allowed_metrics = {
        "operating_cash_flow",
        "revenue",
        "assets",
        "liabilities",
        "net_income",
    }
    calculator = FinancialCalculator()

    def analyze(self, financial_facts):
        fy_results = {}
        revenue_growth_results = []

        # organize facts by year
        for fact in financial_facts:
            year = fact["fiscal_year"]
            fy_results.setdefault(year, {})
            if fact['metric'] in self.allowed_metrics:
                fy_results[year][fact['metric']] = fact['value']

        # calculate revenue growth
        years_results = sorted(fy_results, key=int)

        for year in years_results : 
            curr_year = year;
            prev_year = year - 1;

            if prev_year not in years_results:
                continue
            
            if "revenue" not in fy_results[curr_year] or "revenue" not in fy_results[prev_year]:
                continue

            curr_year_revenue = fy_results[curr_year]["revenue"]
            prev_year_revenue = fy_results[prev_year]['revenue']
            revenue_growth = self.calculator.growth_rate(curr_year_revenue, prev_year_revenue)
            print(f"Revenue Growth Calculated : {revenue_growth}")

            yoy_result_growth = {}
            yoy_result_growth['metric'] = FinancialMetric.REVENUE_GROWTH.value;
            yoy_result_growth['period'] = str(curr_year)
            yoy_result_growth['current_year'] = curr_year
            yoy_result_growth['previous_year'] = prev_year 
            yoy_result_growth['current_value'] = curr_year_revenue 
            yoy_result_growth['previous_value'] = prev_year_revenue     
            yoy_result_growth['value'] = revenue_growth
            yoy_result_growth['unit'] = 'percent'

            revenue_growth_results.append(yoy_result_growth)

        # calculate revenue growth

        # calculate net income growth

        # calculate margins

        # calculate asset/liability growth

        # calculate ratios
        print(f"Analysis results for : {fy_results}")
        print(f"YOY Revenue Results : {revenue_growth_results}")
        return fy_results
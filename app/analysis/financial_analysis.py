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
        net_income_growth_results = []
        net_margin_results = []
        operating_cash_flow_margin_results = []
        assest_growth_results = []
        liabilities_growth_results = []
        liabilities_to_assest_results = []

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

        # calculate net income growth
        for year in years_results : 
            curr_year = year;
            prev_year = year - 1;

            if prev_year not in years_results:
                continue
            
            if "net_income" not in fy_results[curr_year] or "net_income" not in fy_results[prev_year]:
                continue

            curr_year_revenue = fy_results[curr_year]["net_income"]
            prev_year_revenue = fy_results[prev_year]["net_income"]
            net_income_result = self.calculator.growth_rate(curr_year_revenue, prev_year_revenue)
            print(f"Net Income Growth Calculated : {net_income_result}")

            yoy_net_income_growth = {}
            yoy_net_income_growth['metric'] = FinancialMetric.NET_INCOME_GROWTH.value;
            yoy_net_income_growth['period'] = str(curr_year)
            yoy_net_income_growth['current_year'] = curr_year
            yoy_net_income_growth['previous_year'] = prev_year 
            yoy_net_income_growth['current_value'] = curr_year_revenue 
            yoy_net_income_growth['previous_value'] = prev_year_revenue     
            yoy_net_income_growth['value'] = net_income_result
            yoy_net_income_growth['unit'] = 'percent'

            net_income_growth_results.append(yoy_net_income_growth)
        

        # calculate net profit margins :  (net income / revenue) * 100
        for year in years_results : 
            curr_year = year;

            if "net_income" not in fy_results[curr_year] or "revenue" not in fy_results[curr_year]:
                continue

            net_income_curr_year = fy_results[curr_year]["net_income"]
            revenue_curr_year = fy_results[curr_year]["revenue"]

            margin_result = self.calculator.margin(net_income_curr_year, revenue_curr_year)
            print(f"Net Margin Calculated : {margin_result}")

            yoy_margin = {}
            yoy_margin['metric'] = FinancialMetric.NET_PROFIT_MARGIN.value;
            yoy_margin['period'] = str(curr_year)
            yoy_margin['net_income_curr_year'] = net_income_curr_year
            yoy_margin['revenue_curr_year'] = revenue_curr_year    
            yoy_margin['value'] = margin_result
            yoy_margin['unit'] = 'percent'

            net_margin_results.append(yoy_margin)

        # calculate operating cash flow margin : (operating cash flow / revenue) * 100;
        for year in years_results : 
            curr_year = year;

            if "operating_cash_flow" not in fy_results[curr_year] or "revenue" not in fy_results[curr_year]:
                continue

            operating_cash_flow_curr_year = fy_results[curr_year]["operating_cash_flow"]
            revenue_curr_year = fy_results[curr_year]["revenue"]

            operating_cash_flow_result = self.calculator.margin(operating_cash_flow_curr_year, revenue_curr_year)
            print(f"Net Opeating Cash Flow Calculated : {operating_cash_flow_result}")

            yoy_operating_cash_flow = {}
            yoy_operating_cash_flow['metric'] = FinancialMetric.OPERATING_CASH_FLOW_MARGIN.value;
            yoy_operating_cash_flow['period'] = str(curr_year)
            yoy_operating_cash_flow['operating_cash_flow_curr_year'] = operating_cash_flow_curr_year
            yoy_operating_cash_flow['revenue_curr_year'] = revenue_curr_year    
            yoy_operating_cash_flow['value'] = operating_cash_flow_result
            yoy_operating_cash_flow['unit'] = 'percent'

            operating_cash_flow_margin_results.append(yoy_margin)

        # calculate asset growth per year
        for year in years_results : 
            curr_year = year;
            prev_year = year - 1;

            if prev_year not in years_results:
                continue
            
            if "total_assets" not in fy_results[curr_year] or "total_assets" not in fy_results[prev_year]:
                continue

            curr_year_assest_revenue = fy_results[curr_year]["total_assets"]
            prev_year_assest_revenue = fy_results[prev_year]["total_assets"]
            assest_result = self.calculator.growth_rate(curr_year_assest_revenue, prev_year_assest_revenue)
            print(f"Net Assest Growth Calculated : {assest_result}")

            yoy_assest_growth = {}
            yoy_assest_growth['metric'] = FinancialMetric.ASSET_GROWTH.value;
            yoy_assest_growth['period'] = str(curr_year)
            yoy_assest_growth['current_year'] = curr_year
            yoy_assest_growth['previous_year'] = prev_year 
            yoy_assest_growth['curr_year_assest_revenue'] = curr_year_assest_revenue 
            yoy_assest_growth['prev_year_assest_revenue'] = prev_year_assest_revenue     
            yoy_assest_growth['value'] = assest_result
            yoy_assest_growth['unit'] = 'percent'
    
            assest_growth_results.append(yoy_assest_growth)
        
        # calculate liability growth per year.
        for year in years_results : 
            curr_year = year;
            prev_year = year - 1;

            if prev_year not in years_results:
                continue
            
            if "total_liabilities" not in fy_results[curr_year] or "total_liabilities" not in fy_results[prev_year]:
                continue

            curr_year_liability_value = fy_results[curr_year]["total_liabilities"]
            prev_year_liability_value = fy_results[prev_year]["total_liabilities"]
            liability_result = self.calculator.growth_rate(curr_year_liability_value, prev_year_liability_value)
            print(f"Net Liability Growth Calculated : {liability_result}")

            yoy_liability_growth = {}
            yoy_liability_growth['metric'] = FinancialMetric.LIABILITY_GROWTH.value;
            yoy_liability_growth['period'] = str(curr_year)
            yoy_liability_growth['current_year'] = curr_year
            yoy_liability_growth['previous_year'] = prev_year 
            yoy_liability_growth['curr_year_liability_value'] = curr_year_liability_value 
            yoy_liability_growth['prev_year_liability_value'] = prev_year_liability_value     
            yoy_liability_growth['value'] = liability_result
            yoy_liability_growth['unit'] = 'percent'
    
            liabilities_growth_results.append(yoy_assest_growth)

        # calculate liability to asset ratio ratios
        for year in years_results : 
            curr_year = year;

            if "total_liabilities" not in fy_results[curr_year] or "total_assets" not in fy_results[curr_year]:
                continue

            liabilities_curr_year = fy_results[curr_year]["total_liabilities"]
            assets_curr_year = fy_results[curr_year]["total_assets"]

            liability_to_asset_ratio = self.calculator.ratio(liabilities_curr_year, assets_curr_year)
            print(f"Net Opeating Cash Flow Calculated : {liability_to_asset_ratio}")

            yoy_liab_to_assest_ratio = {}
            yoy_liab_to_assest_ratio['metric'] = FinancialMetric.LIABILITY_TO_ASSET.value;
            yoy_liab_to_assest_ratio['period'] = str(curr_year)
            yoy_liab_to_assest_ratio['liabilities_curr_year'] = liabilities_curr_year
            yoy_liab_to_assest_ratio['assets_curr_year'] = assets_curr_year    
            yoy_liab_to_assest_ratio['value'] = liability_to_asset_ratio
            yoy_liab_to_assest_ratio['unit'] = 'percent'

            liabilities_to_assest_results.append(yoy_liab_to_assest_ratio)


        print(f"Analysis results for : {fy_results}")
        print(f"YOY Margin Results : {assest_growth_results}")
        return fy_results
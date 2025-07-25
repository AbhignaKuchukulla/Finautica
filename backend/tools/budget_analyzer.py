import pandas as pd

class BudgetAnalyzer:
    def analyze(self, transactions: pd.DataFrame, budget: dict):
        monthly = transactions.groupby(['month', 'category'])['amount'].sum().unstack()
        deviations = {}
        for month in monthly.index:
            deviations[month] = {
                cat: {
                    'spent': monthly.loc[month, cat],
                    'budgeted': budget.get(cat, 0),
                    'deviation': monthly.loc[month, cat] - budget.get(cat, 0)
                }
                for cat in budget.keys()
            }
        return deviations
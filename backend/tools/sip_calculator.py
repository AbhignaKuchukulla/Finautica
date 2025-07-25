import pandas as pd
import numpy as np

class SIPCalculator:
    def __init__(self):
        self.historical_returns = {
            'equity': 0.12, 
            'debt': 0.07,
            'hybrid': 0.09
        }
    
    def project(self, amount: float, years: int, asset_mix: dict):
        weighted_return = sum(
            self.historical_returns[asset] * weight 
            for asset, weight in asset_mix.items()
        )
        months = years * 12
        monthly_rate = weighted_return / 12
        future_value = amount * (((1 + monthly_rate)**months - 1) / monthly_rate)
        return {
            "total_invested": amount * months,
            "future_value": future_value,
            "xirr": ((future_value / (amount * months)) ** (1/years)) - 1
        }
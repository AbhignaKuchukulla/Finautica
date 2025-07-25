import numpy as np
from typing import Dict, List
from pydantic import BaseModel

class RiskProfile(BaseModel):
    volatility: float  # 0-1
    liquidity_needs: float  # 0-1
    concentration: float  # 0-1
    time_horizon: float  # 0-1
    loss_capacity: float  # 0-1

class RiskAssessor:
    def __init__(self):
        self.benchmarks = {
            'conservative': [30, 70, 20, 40, 80],
            'moderate': [50, 50, 50, 50, 50],
            'aggressive': [80, 30, 70, 80, 30]
        }
    
    def calculate_risk_score(self, profile: RiskProfile) -> Dict:
        weights = np.array([0.3, 0.2, 0.15, 0.2, 0.15])  # Weighted factors
        profile_array = np.array([
            profile.volatility,
            profile.liquidity_needs,
            profile.concentration,
            profile.time_horizon,
            profile.loss_capacity
        ])
        
        raw_score = np.dot(weights, profile_array) * 100
        
        # Classify risk level
        if raw_score < 30:
            risk_class = "Conservative"
        elif 30 <= raw_score < 60:
            risk_class = "Moderate"
        else:
            risk_class = "Aggressive"
        
        return {
            "score": round(raw_score, 1),
            "classification": risk_class,
            "components": {
                "volatility": profile.volatility * 100,
                "liquidity": profile.liquidity_needs * 100,
                "concentration": profile.concentration * 100,
                "time_horizon": profile.time_horizon * 100,
                "loss_capacity": profile.loss_capacity * 100
            },
            "benchmarks": self.benchmarks
        }
    
    def portfolio_risk_analysis(self, holdings: Dict[str, float]) -> Dict:
        """Analyze portfolio concentration risk"""
        holdings_values = np.array(list(holdings.values()))
        total = holdings_values.sum()
        percentages = holdings_values / total
        
        # Calculate Herfindahl-Hirschman Index (HHI)
        hhi = (percentages ** 2).sum() * 10000
        
        if hhi < 1500:
            concentration_risk = "Low"
        elif 1500 <= hhi < 2500:
            concentration_risk = "Moderate"
        else:
            concentration_risk = "High"
        
        return {
            "hhi_index": round(hhi, 2),
            "concentration_risk": concentration_risk,
            "top_holdings": dict(sorted(
                holdings.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3])
        }
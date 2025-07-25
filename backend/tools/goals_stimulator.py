import numpy as np

class GoalSimulator:
    def simulate(self, target: float, monthly: float, years: int, return_rate: float):
        simulations = []
        for _ in range(1000):  # Monte Carlo
            balance = 0
            for _ in range(years * 12):
                balance += monthly
                balance *= (1 + np.random.normal(return_rate/12, 0.02))
            simulations.append(balance)
        success_rate = sum(np.array(simulations) >= target) / 1000
        return {
            "success_rate": success_rate,
            "percentiles": np.percentile(simulations, [10, 50, 90]).tolist()
        }
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_sample_transactions(num: int = 200):
    categories = [
        "Groceries", "Dining", "Transport", 
        "Housing", "Utilities", "Entertainment"
    ]
    data = []
    for _ in range(num):
        date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        category = random.choice(categories)
        amount = round(random.uniform(100, 5000) / 50) * 50
        data.append({
            "date": date,
            "amount": amount,
            "category": category,
            "description": f"Payment for {category}"
        })
    return pd.DataFrame(data)
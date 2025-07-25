import sqlite3
from typing import Dict, List

class FinancialDatabase:
    def __init__(self, db_path: str = "finautica.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            date TEXT,
            amount REAL,
            category TEXT,
            description TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS investment_goals (
            id INTEGER PRIMARY KEY,
            goal_name TEXT,
            target_amount REAL,
            time_frame INTEGER,
            priority INTEGER
        )
        """)
        self.conn.commit()

    def add_transaction(self, transaction: Dict):
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO transactions (date, amount, category, description)
        VALUES (?, ?, ?, ?)
        """, (
            transaction["date"],
            transaction["amount"],
            transaction["category"],
            transaction["description"]
        ))
        self.conn.commit()

    def get_transactions(self, month: str = None) -> List[Dict]:
        cursor = self.conn.cursor()
        if month:
            cursor.execute("""
            SELECT * FROM transactions 
            WHERE strftime('%Y-%m', date) = ?
            """, (month,))
        else:
            cursor.execute("SELECT * FROM transactions")
        return [dict(row) for row in cursor.fetchall()]
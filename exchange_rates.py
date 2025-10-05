# FINE3300 – Assignment 1 (Part 2)
# Author: Abdallah Al Ghoul
# Loads the latest USD/CAD rate from the CSV and converts CAD ↔ USD.
# Date: 2025-10-05

import csv
from dataclasses import dataclass

@dataclass
class ExchangeRates:
    csv_path: str

    def __post_init__(self):
        self.latest_rate = None    # USD/CAD (CAD per 1 USD)
        self._load_latest_rate()

    def _load_latest_rate(self):
        # Read the CSV and use the last row (latest date)
        with open(self.csv_path, newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        last_row = rows[-1]
        # Expect a column named "USD/CAD"
        self.latest_rate = float(last_row["USD/CAD"])

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        # Convert using USD/CAD (CAD per 1 USD)
        if self.latest_rate is None:
            raise ValueError("Exchange rate not loaded.")

        frm = from_currency.upper()
        to = to_currency.upper()

        if frm == to:
            return round(amount, 2)
        if frm == "USD" and to == "CAD":
            return round(amount * self.latest_rate, 2)
        if frm == "CAD" and to == "USD":
            return round(amount / self.latest_rate, 2)

        raise ValueError("Currencies must be CAD or USD only.")

if __name__ == "__main__":
    csv_file = "BankOfCanadaExchangeRates.csv"
    ex = ExchangeRates(csv_file)

    amount = float(input("Enter amount: "))
    from_cur = input("From currency (CAD/USD): ").strip()
    to_cur = input("To currency (CAD/USD): ").strip()

    result = ex.convert(amount, from_cur, to_cur)
    print(f"{amount} {from_cur.upper()} = {result} {to_cur.upper()}")

import csv
from dataclasses import dataclass

@dataclass
class ExchangeRates:
    csv_path: str

    def __post_init__(self):
        # Load the latest USD/CAD exchange rate from the CSV
        self.latest_rate = None
        self._load_latest_rate()

    def _load_latest_rate(self):
        """
        Read the CSV file and set self.latest_rate
        to the last available USD/CAD exchange rate.
        The rate is CAD per 1 USD.
        """
        with open(self.csv_path, newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Get the last row (latest date)
        last_row = rows[-1]
        # Convert string from "USD/CAD" column to float
        self.latest_rate = float(last_row["USD/CAD"])

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert between CAD and USD using the latest USD/CAD rate (CAD per 1 USD).
        - USD → CAD: multiply by the rate
        - CAD → USD: divide by the rate
        """
        if self.latest_rate is None:
            raise ValueError("Exchange rate not loaded.")

        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency == "USD" and to_currency == "CAD":
            return round(amount * self.latest_rate, 2)
        elif from_currency == "CAD" and to_currency == "USD":
            return round(amount / self.latest_rate, 2)
        elif from_currency == to_currency:
            return round(amount, 2)
        else:
            raise ValueError("Currencies must be CAD or USD only.")

if __name__ == "__main__":
    csv_file = "BankOfCanadaExchangeRates.csv"
    ex = ExchangeRates(csv_file)

    amount = float(input("Enter amount: "))
    from_cur = input("From currency (CAD/USD): ").strip().upper()
    to_cur = input("To currency (CAD/USD): ").strip().upper()

    result = ex.convert(amount, from_cur, to_cur)
    print(f"{amount} {from_cur} = {result} {to_cur}")

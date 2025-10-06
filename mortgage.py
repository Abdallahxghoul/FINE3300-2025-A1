# FINE3300 – Assignment 1 (Part 1)
# Author: Abdallah Al Ghoul
# This program calculates mortgage payments for different schedules.
# Date: 2025-10-05

from dataclasses import dataclass

@dataclass
class MortgagePayment:
    quoted_rate_percent: float   # e.g., 5.5 means 5.5%
    amort_years: int             # e.g., 25 years

    def _ear_from_semi_annual_quote(self) -> float:
        # Convert quoted annual % (compounded semi-annually) to effective annual rate (EAR)
        j = self.quoted_rate_percent / 100.0
        return (1 + j / 2) ** 2 - 1

    def _pva(self, r: float, n: int) -> float:
        # Present value of an annuity-immediate factor
        return (1 - (1 + r) ** (-n)) / r

    def _payment_for_frequency(self, principal: float, m: int) -> float:
        # Calculate payment when there are m payments per year
        ear = self._ear_from_semi_annual_quote()
        r = (1 + ear) ** (1 / m) - 1
        n = self.amort_years * m
        return principal / self._pva(r, n)

    def payments(self, principal: float):
        # Return all six payment options (rounded to cents)
        monthly = self._payment_for_frequency(principal, 12)
        semi_monthly = self._payment_for_frequency(principal, 24)
        bi_weekly = self._payment_for_frequency(principal, 26)
        weekly = self._payment_for_frequency(principal, 52)

        # Accelerated schedules
        rapid_bi_weekly = monthly / 2
        rapid_weekly = monthly / 4

        # Round and return in order
        return tuple(round(x, 2) for x in [
            monthly, semi_monthly, bi_weekly, weekly, rapid_bi_weekly, rapid_weekly
        ])


if __name__ == "__main__":
    # Prompt user for inputs
    principal = float(input("Enter principal amount: "))
    quoted = float(input("Enter quoted annual rate %: "))
    years = int(input("Enter amortization (years): "))

    mp = MortgagePayment(quoted_rate_percent=quoted, amort_years=years)
    payments = mp.payments(principal)

    labels = [
        "Monthly Payment", "Semi-monthly Payment", "Bi-weekly Payment",
        "Weekly Payment", "Rapid Bi-weekly Payment", "Rapid Weekly Payment"
    ]

    for label, val in zip(labels, payments):
        print(f"{label}: ${val:.2f}")

from dataclasses import dataclass

@dataclass
class MortgagePayment:
    quoted_rate_percent: float   # e.g., 5.5 means 5.5%
    amort_years: int             # e.g., 25 years

    # 1) Quoted (semi-annual) -> Effective Annual Rate (EAR)
    def _ear_from_semi_annual_quote(self) -> float:
        j = self.quoted_rate_percent / 100.0
        return (1 + j/2) ** 2 - 1

    # 2) Present value of an annuity-immediate factor
    def _pva(self, r: float, n: int) -> float:
        return (1 - (1 + r) ** (-n)) / r

    # 3) Payment for a given frequency m (payments per year)
    def _payment_for_frequency(self, principal: float, m: int) -> float:
        ear = self._ear_from_semi_annual_quote()
        r = (1 + ear) ** (1 / m) - 1
        n = self.amort_years * m
        return principal / self._pva(r, n)

    # 4) Return the six payment options (rounded to cents)
    def payments(self, principal: float):
        """
        Returns (monthly, semi-monthly, bi-weekly, weekly, rapid bi-weekly, rapid weekly).
        """
        monthly      = self._payment_for_frequency(principal, 12)
        semi_monthly = self._payment_for_frequency(principal, 24)
        bi_weekly    = self._payment_for_frequency(principal, 26)
        weekly       = self._payment_for_frequency(principal, 52)

        # Accelerated schedules are fractions of the monthly payment (per assignment)
        rapid_bi_weekly = monthly / 2
        rapid_weekly    = monthly / 4

        rnd = lambda x: round(x + 1e-8, 2)
        return (
            rnd(monthly),
            rnd(semi_monthly),
            rnd(bi_weekly),
            rnd(weekly),
            rnd(rapid_bi_weekly),
            rnd(rapid_weekly),
        )


# ----- Simple CLI for Part 1 (matches the required output format) -----
def _print_outputs(vals):
    labels = [
        "Monthly Payment",
        "Semi-monthly Payment",
        "Bi-weekly Payment",
        "Weekly Payment",
        "Rapid Bi-weekly Payment",
        "Rapid Weekly Payment",
    ]
    for label, value in zip(labels, vals):
        print(f"{label}: ${value:.2f}")


if __name__ == "__main__":
    # We assume valid inputs (as per the assignment)
    principal = float(input("Enter principal amount (e.g., 500000): ").strip())
    quoted = float(input("Enter quoted annual rate % (e.g., 5.5): ").strip())
    years = int(input("Enter amortization (years) (e.g., 25): ").strip())

    mp = MortgagePayment(quoted_rate_percent=quoted, amort_years=years)
    results = mp.payments(principal)
    _print_outputs(results)

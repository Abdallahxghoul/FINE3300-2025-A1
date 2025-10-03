from dataclasses import dataclass

@dataclass
class MortgagePayment:
    quoted_rate_percent: float   # e.g. 5.5 means 5.5%
    amort_years: int             # e.g. 25 years

    def _ear_from_semi_annual_quote(self) -> float:
        # Convert quoted annual % (compounded semi-annually) to effective annual rate (EAR)
        j = self.quoted_rate_percent / 100.0
        return (1 + j/2) ** 2 - 1

    def payments(self, principal: float):
        # Will return six payment amounts later
        raise NotImplementedError("Implement this method next")

if __name__ == '__main__':
    print('MortgagePayment CLI will go here')

from dataclasses import dataclass

@dataclass
class MortgagePayment:
    quoted_rate_percent: float
    amort_years: int

    def payments(self, principal: float):
        # Will return six payment amounts later
        raise NotImplementedError("Implement this method next")

if __name__ == '__main__':
    print('MortgagePayment CLI will go here')


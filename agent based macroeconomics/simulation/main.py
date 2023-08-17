#   Considerations:
##      Without a government or central banks
##      Exclude growth
##      Fundamental time unit is day
##      Month is defined as coherent days


# Initial variables
num_households = 1000
num_firms = 50
days_of_month = 21              #days

# Define entities
class household:
    def __init__(self) -> None:
        self.employee = None

        # The reservation wage defines a minimal claim on labor income
        self.wage = None

        # the amount of monetary units the household currently possesses
        self.liquidity = None
        
    def consumption(self) -> int:
        pass

    def current_liquidity(self, m_t_1, income_1, spending_1) -> int:
        m_t_h = m_t_1 + income_1 - spending_1
    



class firm:
    def __init__(self) -> None:
        pass



households = []
firms = []

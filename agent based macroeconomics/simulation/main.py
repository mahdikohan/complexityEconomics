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
        self.employer = None

        # The reservation wage defines a minimal claim on labor income
        self.wage = None

        # the amount of monetary units the household currently possesses
        self.liquidity = None
        
    def consumption(self) -> int:
        pass

    def current_liquidity(self, m_t_1, income_t_1, spending_t_1) -> int:
        m_t_h = m_t_1 + income_t_1 - spending_t_1
        return m_t_h
    
    # If the household is unemployed, he visits a randomly 
    # chosen firm to check whether there is an open position.
    def get_new_position(self):
        pass
    

    # Households are picked in a random order to execute their goods demand.
    def execute_demand(self):
        pass


class firm:
    def __init__(self) -> None:
        self.liquidity = None
        self.wage = None
        self.inventory = None
        self.employees = None    # Labor
    

    # It means good prices
    def price(self):
        pass



    # firm has to decide on how to set its wage rate based on past
    # success or failure to find workers at the offered wage rate.
    def determine_wage_rate(self):
        # Wage adjustment
        pass

    
    def determine_number_employee(self):
        pass


    def determine_price(self):
        pass


    def execute_production(self):
        # we assume a production technology that is a linear function of labor input.
        pass


    def pay_wage(self):
        pass


    def build_buffer(self):
        pass

    def pay_profit(self):
        pass

    



households = []
firms = []



if __name__ == "__main__":
    # begining of the month first step of simulation

    # next step is starting the day

    # After all households and firms have performed their daily actions, the next day starts
    pass

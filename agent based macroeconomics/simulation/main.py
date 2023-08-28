import random
import matplotlib.pyplot as plt
from collections import Counter
import uuid

#   Considerations:
##      Without a government or central banks
##      Exclude growth
##      Fundamental time unit is day
##      Month is defined as coherent days


# Initial variables
num_households = 1000
num_firms = 100
_lambda = 3                     # positive technology parameter
theta = 0.25                    # price change probability
days_of_month = 21              # days
epoc = 500                      # years * 12
mu = 0.019                      # U(0, 0.019)
nu = 0.02                       # v(0, 0.02)
_ex = 0.1                         # rate of buffer


households = []
firms = []
unemployed = []


# Define entities
class household:
    def __init__(self) -> None:

        # Each household just work in one firm in a same time then -> l_h=1
        self.huid = uuid.uuid4()

        # The reservation wage defines a minimal claim on labor income
        self.wage = random.randrange(15080,89000,70)

        # The amount of monetary units the household currently possesses
        self.liquidity = random.randrange(0,15000,10)
    
    def get_huid(self):
        return self.huid

    # Households are picked in a random order to execute their goods demand.
    # Since households receive income on a monthly basis, the decision of
    #   dividing it on consumption and savings is also performed monthly.
    def consumption(self) -> int:
        return 0

    def get_liquidity(self):
        return self.liquidity

    def set_profit(self,profit):
        self.liquidity = self.liquidity + profit
    # def current_liquidity(self, m_t_1, income_t_1, spending_t_1) -> int:
    #     m_t_h = m_t_1 + income_t_1 - spending_t_1
    #     return m_t_h


    # If the household is unemployed, he visits a randomly 
    # chosen firm to check whether there is an open position.
    def get_new_position(self,firms,parent_firm=None):
        if parent_firm != None:
            for f in firms:
                # check wage rates
                if self.wage > f.get_wage():
                    pass
                elif self.wage < f.get_wage() and f.open_position_status()[0]:

                    # disconnect from parent
                    parent_firm.disconnect_employee(self.huid)

                    # connect to new firm
                    f.set_employee(f)

        elif parent_firm == None:
            for f in firms:
                # check wage rates
                if self.wage < f.get_wage() and f.open_position_status()[0]:

                    # connect to new firm
                    f.set_employee(f)

    # Daily action
    def exec_demand(self, firms):
        """Firms, picked in a random order to execute their goods demand
        each household visits one randomly determined firm of those
        he has a connection with.
        
        Demand c_h^r/21
        Satisfy 
            1. Household's liquidity
            2. Firm's inventory
            
        It decrease household's liquidity and increase firm's liquidity.

        Customer adjustments is based on their liquidity.

        If the firm's inventory where less than household demands
        households satisfy from several firms.   
        """

        for f in firms:
            demand = self.consumption / days_of_month

            # Check liquidity of households
            if demand > self.liquidity:
                    demand = self.liquidity

            finv = f.get_inventory()

            if finv >= demand:
                f.set_inventory(inventory= finv - demand)
                f.increase_liquidity(delta= demand)
                break
            elif finv < demand:
                f.set_inventory(inventory= demand - finv)
                f.increase_liquidity(delta= demand)
    

    # Daily action
    def exec_(self):
        pass

    def set_liquidity(self, liquidity):
        self.liquidity = liquidity



class firm:
    def __init__(self) -> None:

        self.fuid = uuid.uuid4()

        self.liquidity = 0

        self.buffer = 0

        self.wage = random.randrange(15080,89000,70)

        self.wage_t1 = random.randrange(15080,89000,70)

        # inventory critical bounds
        self.critical_inventory = [15080,(89000+15080)/2]

        # price critical bounds
        self.critical_price = [0,0]

        self.demand_t1 = 0

        self.inventory = random.randrange(15080,89000,70)

        self.employees_Cap = 0

        self.employees_Cap_t1 = 0

        self.price = 0

        self.price_t1 = 0

        self.employees = []

        self.next_month_fire = ''

    def get_fuid(self):
        return self.fuid
    
    def get_employees(self):
        return self.employees
    
    def get_inventory(self):
        return self.inventory
    
    def set_inventory(self, inventory) -> None:
        self.inventory = inventory

    def increase_liquidity(self,delta):
        self.liquidity = self.liquidity + delta
    
    def recruitment(self):

        # hire and fire employee
        if self.inventory < self.critical_inventory[0]:

            # hire immidiatly
            if self.employees_Cap >= 0:
                self.employees_Cap = self.employees_Cap + 1
            
            elif self.employees_Cap < 0:
                print('warning: Employment cap is negetive (Labor count is exceed)')

        elif self.inventory > self.critical_inventory[1]:

            # fire with one month delay
            self.next_month_fire = random.sample(self.employees,1)

    def set_employees_group(self,group:list) -> None:
        self.employees = group

    def set_employee(self,labor):
        self.employees.append(labor)

    def disconnect_employee(self,huid = None) -> None:
        if huid != None:
            for employee in self.employees:
                if employee.get_huid() == huid:
                    self.employees.remove(employee)

        elif huid == None:
            if self.next_month_fire != '':
                self.disconnect_employee(self.next_month_fire.get_huid())
                self.employees_Cap = self.employees_Cap - 1
        

    # It means good prices
    def set_price(self,theta):
        """In simple terms, a Calvo contract is a pricing 
        model where firms have a constant chance of being 
        able to change their prices, regardless of how long 
        it has been since they last changed them. This model 
        is commonly used in macroeconomic models to represent 
        how prices can be rigid and not change frequently."""

        # price adjusment
        #             
        if (self.inventory > self.critical_inventory[1]) \
            and (self.price > self.critical_price[1]):
            # Decrease price with prob \theta
            # handle prob
            if random.random() > theta:
                return
            # 
            # this is my change price code
            self.price = self.wage_t1 * (1-nu)
            #

        elif (self.inventory > self.critical_inventory[1]) \
            and (self.price < self.critical_price[0]):
            # Increase price with prob \theta
            # handle prob
            if random.random() > theta:
                return                   
            # 
            # this is my change price code
            self.price = self.wage_t1 * (1 + nu)
            # 


    # firm has to decide on how to set its wage rate based on past
    # success or failure to find workers at the offered wage rate.
    def set_wage(self):
        # Wage adjustment
        if self.employees_Cap_t1 <= 0:             # condition of increase wage
            self.wage = self.wage_t1*(1+mu)

        elif self.employees_Cap_t1 > 0:            # condition of decrease wage
            self.wage = self.wage_t1*(1-mu)

    def get_wage(self):
        return self.wage

    
    def get_num_labor(self):
        return len(self.employees)
    

    def open_position_status(self):
        """An empty position is significantly related to the 
        capacity of a company's employees, which can change over time. 
        It is important to note that this can sometimes appear negative 
        due to delays in firing people during the month and executing 
        it at the end of the month.
        """
        empty_position = self.employees_Cap-len(self.employees)

        if empty_position>0:
            return [True,empty_position]
        else:
            return [False,empty_position]


    def production(self):
        # we assume a production technology that is a linear function of labor input.
        return _lambda * self.get_num_labor()


    # First order
    def pay_wage(self):
        """ Add w_f to liquidity of households (Labors) and decrease liquidity of 
            households.

            * we assume that the firm's employees accept an immediate wage cut that 
                is sufficient to keep the firm operating.

            * If the labor income exceeds a household's reservation wage, is 
                raised to the level of the received labor income. If the labor
                income is lower than, the reservation wage is not changed.
                Instead, the household intensifies his search for a better-paid job.
            
            * If a household has been unemployed during the last month,
                his reservation wage for the next month is reduced by 10 percent.
        """

        
        if self.liquidity < (self.wage * len(self.employees)):
            print('warning: firm liquidity is not enough for paying labors\' wages')

        self.liquidity = self.liquidity - (self.wage * len(self.employees))

        for h in self.get_employees:
            h.set_liquidity(self.wage)
        


    # Second order
    def build_buffer(self):
        if self.liquidity < (_ex * (self.wage * len(self.employees))):
            print('warning: firm liquidity is not enough for *Buffer reservation*')

        self.buffer = _ex * (self.wage * len(self.employees))
        self.liquidity = self.liquidity - self.buffer


    # Third order
    def pay_profit(self):
        """all remaining liquidity of the firm is 
        distributed as profit among all households
        Rich households have higher claims on firms'
        profits than poor ones."""
        if self.liquidity < (_ex * (self.wage * len(self.employees))):
            print('warning: firm liquidity is not enough for *pay profit*')


        # because of simplicity uniform distribution of rofit
        for h in self.employees:
            h.set_profit(profit = self.liquidity/len(self.employees))



if __name__ == "__main__":
    """
    After all firms have formed decisions, it is 
    the households' turn to search for more beneficial 
    trading connections.
    Households are picked in a random order to seek for 
    new network connections that are more beneficial than 
    existing ones. 
    With a certain probability, each household picks one 
    randomly determined firm from the subset of all firms 
    he has a connection with and one randomly determined 
    firm from those he has no such connection with.
    """


    # we considered equality is init state then, also all parameter
    # generated by the equal shares
    for h in range(0,num_households):
        households.append(household())

    for f in range(0,num_firms):
        firms.append(firm())


    # Assign the same number of employees to each firm
    for n,f in enumerate(firms):
        print(n)
        f.set_employees_group(households[10*n:10*n+10])
        for h in households[10*n:10*n+10]:
            print(h.get_huid())
        print('++++++++++++++++++++++++')

    # -----------------------------------------------------------------------
    # Begining of the month first step of simulation

    # firms action
    for f in firms:
        f.set_price(theta= theta)
        f.set_wage()
        f.recruitment()
    
    # After all firms have formed decisions, it is the households’ 
    # turn to search for more beneficial trading connections.
    for f in firms:
        for h in households:
            sample_firms_group = random.sample(firms,random.randrange(1,10))
            h.get_new_position(parent_firm = f,
                                       firms = sample_firms_group)
            
    # unemployment households search
    for f in firms:
        for h in unemployed:
            h.get_new_position(parent_firm = f, firms = firms) 
    # -----------------------------------------------------------------------
    # Next step is starting the day

    # Loop of each days
    for _ in range(days_of_month):
        for h in households:
            sample_firms_group = random.sample(firms,random.randrange(1,10))
            h.exec_demand(firms=sample_firms_group)

    # -----------------------------------------------------------------------
    # End of the month

    # After all 21 working days are performed, the month ends.
    for f in firms:
        f.pay_wage()
        f.build_buffer()
        f.pay_profit()

    # After all households and firms have performed their daily
    # actions, the next day starts

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

    def current_liquidity(self, m_t_1, income_t_1, spending_t_1) -> int:
        m_t_h = m_t_1 + income_t_1 - spending_t_1
        return m_t_h
    

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




class firm:
    def __init__(self) -> None:

        self.fuid = uuid.uuid4()

        self.liquidity = None

        self.wage = random.randrange(15080,89000,70)

        # certain critical bounds
        self.critical_inventory = [15080,(89000+15080)/2]

        self.inventory = random.randrange(15080,89000,70)

        self.employees_Cap = 0

        self.employees_Cap_t1 = 0

        self.employees = []

    def get_fuid(self):
        return self.fuid()
    
    def recruitment(self):
        # hire and fire employee
        if self.inventory < self.critical_inventory[0]:
            # hire immidiatly
            if self.employees_Cap >= 0:
                self.employees_Cap = self.employees_Cap + 1
            elif self.employees_Cap < 0:
                print('warning: Emploment cap is negetive (Labor count is exceed)')

        elif self.inventory > self.critical_inventory[1]:
            # fire with one month delay
            pass

    def set_employees_group(self,group:list) -> None:
        self.employees = group

    def set_employee(self,labor):
        self.employees.append(labor)

    def disconnect_employee(self,huid) -> None:
        for employee in self.employees:
            if employee.get_huid() == huid:
                self.employees.remove(employee)
        
    # It means good prices
    def price(self,theta):
        """In simple terms, a Calvo contract is a pricing 
        model where firms have a constant chance of being 
        able to change their prices, regardless of how long 
        it has been since they last changed them. This model 
        is commonly used in macroeconomic models to represent 
        how prices can be rigid and not change frequently."""

        # price adjusment
        if self.inventory < self.critical_inventory[0]:
            # Increase price with prob \theta
            # handle prob
            if random.random() > theta:
                return

            # 
            # this is my change price code
            # 
            
        elif self.inventory > self.critical_inventory[1]:
            # Decrease price with prob \theta
            # handle prob
            if random.random() > theta:
                return
            
            # 
            # this is my change price code
            #

    # firm has to decide on how to set its wage rate based on past
    # success or failure to find workers at the offered wage rate.
    def wage(self):
        # Wage adjustment
        if True:
            self.wage = self.wage*(1+mu)
        elif False:
            self.wage = self.wage*(1-mu)

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

    # first order
    def pay_wage(self):
        pass

    # second order
    def build_buffer(self):
        pass
    
    # third order
    def pay_profit(self):
        """all remaining liquidity of the firm is 
        distributed as profit among all households
        Rich households have higher claims on firms'
        profits than poor ones."""
        pass





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
        print('++++++++++++++')
    

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


    # Begining of the month first step of simulation

    # Next step is starting the day

    # After all households and firms have performed their daily actions, the next day starts


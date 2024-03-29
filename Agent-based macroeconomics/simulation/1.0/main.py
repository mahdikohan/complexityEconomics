import random
import matplotlib.pyplot as plt
from collections import Counter
import uuid
import pandas as pd
import math

#   Considerations:
##      Without a government or central banks
##      Exclude growth
##      Fundamental time unit is day
##      Month is defined as coherent days


# Initial variables
num_households = 100
num_firms = 10
_lambda = 3                     # positive technology parameter
theta = 0.25                    # price change probability
days_of_month = 21              # days
num_month = 10
epoc = 500                      # years * 12
mu = 0.019                      # U(0, 0.019)
nu = 0.02                       # v(0, 0.02)
_ex = 0.1                       # rate of buffer
alpha = 0.9                     # alpha

households = []
firms = []
unemployed = []


# Define entities
class household:
    def __init__(self) -> None:

        # Each household just work in one firm in a same time then -> l_h=1
        self.huid = uuid.uuid4()

        # The reservation wage defines a minimal claim on labor income
        self.wage = random.randrange(2000,8000,70)

        # The amount of monetary units the household currently possesses
        self.liquidity = random.randrange(150000,300000,10)

        # Connected firms
        # Temporary considered connect firms to households
        # were random
        # self.firms = []
    
    def get_huid(self):
        return self.huid

    # Households are picked in a random order to execute their goods demand.
    # Since households receive income on a monthly basis, the decision of
    #   dividing it on consumption and savings is also performed monthly.
    def consumption(self, firms) -> int:
        """consumption is calculated by c_h^r = (m_h/P_h)^alpha"""
        pi = []
        for f in firms:
            pi.append(f.get_price())

        c = (self.liquidity/(sum(pi)/len(pi))) ** alpha
        if isinstance(c, complex):
            print(f"it's complex c:{c}, liq:{self.liquidity}, P_I:{sum(pi)/len(pi)}, pi:{pi}")
        return c

    def get_liquidity(self):
        return self.liquidity

    def set_profit(self,profit):
        self.set_liquidity(self.liquidity + profit)
    
    # def current_liquidity(self, m_t_1, income_t_1, spending_t_1) -> int:
    #     m_t_h = m_t_1 + income_t_1 - spending_t_1
    #     return m_t_h

    # If the household is unemployed, he visits a randomly 
    # chosen firm to check whether there is an open position.
    def get_new_position(self,firms,h,parent_firm=None):
        if parent_firm != None:
            for f in firms:
                # check wage rates
                if self.wage > f.get_wage():
                    pass
                elif self.wage <= f.get_wage() and f.open_position_status()[0]:

                    # disconnect from parent
                    parent_firm.disconnect_employee(self.huid)

                    # connect to new firm
                    f.set_employee(h)
                    if h in unemployed:
                        unemployed.remove(h)

        elif parent_firm == None:
            for f in firms:
                # check wage rates
                if self.wage < f.get_wage() and f.open_position_status()[0]:

                    # connect to new firm
                    f.set_employee(h)
                    if h in unemployed:
                        unemployed.remove(h)

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
            try:
                demand = self.consumption(firms= firms) / days_of_month

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
            except:
                print(f'Exception raised for values, demand: {demand}, liquidity: {self.liquidity}')


    # Daily action
    def exec_(self):
        pass

    def set_liquidity(self, liquidity):
        if liquidity > 0:
            self.liquidity = liquidity
        else:
            self.liquidity = 0



class firm:
    def __init__(self) -> None:

        self.fuid = uuid.uuid4()

        self.liquidity = random.randrange(15080,89000,70)

        self.buffer = 0

        self.wage = random.randrange(1508,8900,70)

        self.wage_t1 = random.randrange(1508,8900,70)

        # inventory critical bounds
        self.critical_inventory = [15080,(89000+15080)/2]

        # price critical bounds
        self.critical_price = [0,0]

        self.demand_t1 = 0

        self.inventory = random.randrange(15080,89000,70)

        self.employees_Cap = 0

        self.employees_Cap_t1 = 0

        self.price = 10

        self.price_t1 = 0

        self.employees = []

        self.next_month_fire = []

    def get_fuid(self):
        return self.fuid
    
    def get_price(self):
        return self.price

    def get_price_t1(self):
        return self.price_t1

    def get_employees(self):
        return self.employees
    
    def get_inventory(self):
        return self.inventory
    
    def set_inventory(self, inventory) -> None:
        self.inventory = inventory

    def get_employees_cap(self):
        return self.employees_Cap
    
    def set_employee_cap_t1(self):
        self.employees_Cap_t1 = self.employees_Cap

    def increase_liquidity(self,delta):
        self.set_liquidity(self.liquidity + delta)
    
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
            if len(self.employees)>0:
                self.next_month_fire.append(random.sample(self.employees,1))
            else:
                print('warning: Sample larger than population or is negative')

    def set_employees_group(self,group:list) -> None:
        self.employees = group

    def set_employee(self,labor):
        self.employees.append(labor)

    def set_liquidity(self, liquidity):
        if liquidity>0:
            self.liquidity = liquidity
        else:
            self.liquidity = 0

    def disconnect_employee(self,huid = None) -> None:
        if huid != None:
            for employee in self.employees:
                if employee.get_huid() == huid:
                    if employee in self.employees:
                        self.employees.remove(employee)
                    unemployed.append(employee)


        elif huid == None:
            if len(self.next_month_fire) > 0:
                print(f'**** fire an employee {len(self.next_month_fire)}')
                for l in self.next_month_fire:
                    self.disconnect_employee(huid= l[0].get_huid())
                    self.employees_Cap = self.employees_Cap - 1
                
        

    # ???? maybe has bug
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
            print(f'wage changed, It decreased {self.wage}')

        elif self.employees_Cap_t1 > 0:            # condition of decrease wage
            self.wage = self.wage_t1*(1-mu)
            print(f'wage changed, It increased {self.wage}')


    def get_wage(self):
        return self.wage

    
    def get_num_labor(self):
        return len(self.employees)
    
    def set_wage_t1(self):
        self.wage_t1 = self.wage

    def open_position_status(self):
        """An empty position is significantly related to the 
        capacity of a company's employees, which can change over time. 
        It is important to note that this can sometimes appear negative 
        due to delays in firing people during the month and executing 
        it at the end of the month.
        """
        empty_position = self.employees_Cap-len(self.employees)

        if empty_position > 0:
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
            # in this situation employees trying to find new job
            self.set_liquidity(self.liquidity)

        else:
            self.set_liquidity(self.liquidity - (self.wage * len(self.employees)))

        for h in self.employees:
            h.set_liquidity(self.wage)
        


    # Second order
    def build_buffer(self):
        if self.liquidity < (_ex * (self.wage * len(self.employees))):
            print('warning: firm liquidity is not enough for *Buffer reservation*')

        self.buffer = _ex * (self.wage * len(self.employees))
        self.set_liquidity(self.liquidity - self.buffer)


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
            h.set_profit(profit = self.liquidity / len(self.employees))



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

    result = []
    result_u = []
    result_i = []
    result_p = []
    ife = math.floor(num_households/num_firms)
    # we considered equality is init state then, also all parameter
    # generated by the equal shares
    for h in range(0, num_households):
        households.append(household())

    for f in range(0, num_firms):
        firms.append(firm())


    # Assign the same number of employees to each firm
    for n,f in enumerate(firms):
        
        # init firms employee
        

        print(n)
        f.set_employees_group(households[ife*n:ife*n+ife])
        for h in households[ife*n:ife*n+ife]:
            print(h.get_huid())
        print('++++++++++++++++++++++++')

    # -----------------------------------------------------------------------
    # Begining of the month first step of simulation

    for _ in range(num_month):
        # firms action
        for f in firms:
            f.set_price(theta= theta)
            f.set_wage()
            f.recruitment()
        
        # After all firms have formed decisions, it is the households’ 
        # turn to search for more beneficial trading connections.
        for f in firms:
            for h in households:
                sample_firms_group = random.sample(firms,random.randrange(1,math.floor(len(firms)/2)))
                h.get_new_position(parent_firm = f, h = h,
                                        firms = sample_firms_group)

        # unemployment households search
        for f in firms:
            for h in unemployed:
                h.get_new_position(parent_firm = f, h = h, firms = firms) 
        # -----------------------------------------------------------------------
        # Next step is starting the day
        # Loop of each days
        for _ in range(days_of_month):
            for h in households:
                sample_firms_group = random.sample(firms,random.randrange(1,math.floor(len(firms)/2)))
                h.exec_demand(firms = sample_firms_group)

        # -----------------------------------------------------------------------
        # End of the month
        # After all 21 working days are performed, the month ends.
        # result = []
        for f in firms:
            f.pay_wage()
            f.build_buffer()
            f.pay_profit()

            # before starting new month
            f.disconnect_employee()
            f.set_employee_cap_t1()
            f.set_wage_t1()

            # result.append([f.get_fuid(),len(f.get_employees()),f.get_wage(),f.get_price()])
            
        # result_i.append(f.get_wage())
        # result_p.append(f.get_price())
        # result_u.append(len(unemployed))
        

    # df = pd.DataFrame(result,columns=['uid','l_f','wage','price'])
    # print(df)
    # df.to_csv(r'')
    # plt.plot(result_p)
    # plt.show()

    print(f"count unemployed people {len(unemployed)}")

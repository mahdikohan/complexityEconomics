import matplotlib.pyplot
import random


## initial input variables for run simulaion

# this var show total number of our society
number_of_people = 100
# this var shows pleasable attendency in bar
attendency = 60
# this var determine distinct number strategy that each person can have 
number_of_strategy = 5
# this var gives number of execusion of model in simulation
ticks = 1000



# Defined each identities
class strategy:
    def __init__(self, strategyId, history) -> None:
        self.numberOfWeeks:int = strategyId
        self.history:list = history
    
    def result(self):
        return 0

class person:
    def __init__(self, history:list[int], strategyId, attendence) -> None:
        self.strategy:strategy = strategy(strategyId, history)
        self.decision:bool
        self.attendance:int = attendence

    def getStrategy(self)->int:
        n = 100
        return n

    def takeDecision(self):
        forecastAttendence = 50
        return forecastAttendence

class bar:
    def __init__(self) -> None:
        self.totalCap:int
        self.members:list[person]






if __name__ == '__main__':

    print("""Running simualtion with init parameters 
          number_of_people={number_of_people},
          attendency={attendency},
          number_of_strategy={number_of_strategy},
          ticks={ticks}
          """)
    
    # generate random numbers between [60,100)
    init_people = (random.random() * 40) + 60
    init_tick = ticks

    people = list[person]
    # start simulation
    if ticks > 0:
        if init_tick == ticks:

            i = 0
            while i<init_people:
                born = person(history=[]
                              ,strategyId = random.random() * number_of_strategy
                              ,attendence = attendency)
                
                people.append(born)
                i = i+1

        
        ticks = ticks - 1




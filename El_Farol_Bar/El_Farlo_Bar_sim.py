import matplotlib.pyplot
import random




## Initial input variables for run simulaion

# This var show total number of our society
number_of_people = 100
# This var shows pleasable attendency in bar
attendency = 60
# This var determine distinct number strategy that each person can have 
number_of_strategy = 5
# This var gives number of execusion of model in simulation
ticks = 1000





# Defined each identities
class strategy:
    def __init__(self, strategyId, history) -> None:
        self.numberOfWeeks:int = strategyId
        self.history:list = history
    
    def result(self):
        return 0





class person:
    def __init__(self) -> None:
        self.history:list
        self.strategy:strategy
        self.decision:bool
        self.attendance:int

    def __getStrategy(self)->int:
        if len(self.history) < self.strategy:
            return True
        else:
            last_strategy = history[-self.strategy:]
            predicted = sum(last_strategy) / len(last_strategy)
            return predicted < self.attendance
            
    
    def putHistory(self, history:list):
        self.history = history
    
    def appendHistory(self, attendanceCount:int):
        self.history.append(attendanceCount)
    
    def updateHistory(self, index:int, value:int):
        self.history[index] = value

    def takeDecision(self):
        forecastAttendence = self.__getStrategy()
        return forecastAttendence





class bar:
    def __init__(self) -> None:
        self.totalCap:int
        self.members:list[person]








if __name__ == '__main__':

    print(f"""Running simualtion with init parameters \nnumber_of_people\t={number_of_people}\nattendency\t\t={attendency}\nnumber_of_strategy\t={number_of_strategy}\nticks\t\t\t={ticks}""")

    people = []
    i = 0
    while i < number_of_people:
         borned = person(history=[],strategyId = random.random() * number_of_strategy,attendence = attendency)
         people.append(borned)
         i = i + 1
    
    # Start simulation
    init_tick = ticks

    while init_tick-ticks < init_tick:
        history = []

        if init_tick-ticks==0:
            # init first history
            history.append(100)

            for p in people:
                p.putHistory(history)
                p.takeDecision

            continue

        
        

        # # This part check that is first tick
        # if init_tick == ticks:
        #     history = [ticks*0]
        #     i = 0
        #     while i < init_people:
        #         history[0] = init_people
        #         i = i + 1

        # # This part check that is second tick
        # if init_tick - 1 == ticks:

        #     i = number_of_people - init_people
        #     while i < number_of_people:
        #         history[1] = number_of_people - init_people
        #         i = i + 1
            
        
        ticks = ticks - 1

import matplotlib.pyplot as plt
import random
import json
import pandas as pd 
from itertools import permutations



## Initial input variables for run simulaion

# This var show total number of our society
number_of_people = 5
# This var shows pleasable attendance in bar
attendance = 80
# This var determine distinct number strategy that each person can have 
number_of_strategy = 5
# This var gives number of execusion of model in simulation
ticks = 50
# This var shows length of long memory
length_of_long_memory = 5

    

# longMemory
class longMemory:
    def __init__(self) -> None:
        self.value:list
    
    def addExperience(self,experience:list) -> None:
        self.value.append(experience)
        self.value = self.value[-length_of_long_memory:]





class person:
    def __init__(self, decision, attendance) -> None:
        self.strategies:list
        self.decision:bool = decision
        self.attendance:int = attendance
        self.shortMemory:list = length_of_long_memory*[0]
        self.longMemory:list


    def __getStrategy(self)->list:
        allStates = length_of_long_memory*[0]+length_of_long_memory*[1]
        strategy = set()
        while True:
            strategy.add((tuple(random.sample(allStates,length_of_long_memory))))
            if len(strategy) == 2**length_of_long_memory:
                break
        lstrategy = list(strategy)
        history = random.sample(lstrategy,len(lstrategy))
        strategy_without_reward=[]
        for l in history:
            strategy_without_reward.append([l,random.choice([1,-1])])
        strategy_with_reward = [strategy_without_reward,0]
        return strategy_with_reward
    

    def __lookupStrategy(self, value):
        pass
    

    def __refreshShortMemory(self) -> None:
        self.shortMemory = [random.randrange(0,2,1) for i in range(0,length_of_long_memory)]


    def takeDecision(self):
        self.__refreshShortMemory()
        self.strategies = [self.__getStrategy() for i in range(0,number_of_strategy)]

        return 1
    

    def makeDFstrategy(self):
        self.dfStrategies = [pd.DataFrame(self.strategies[i][0]) for i in range(0,number_of_strategy)]
        print('df generated')
    

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)





class bar:
    def __init__(self) -> None:
        self.totalCap:int
        self.members:list[person]





if __name__ == '__main__':

    print(f"""Running simualtion with init parameters \nnumber_of_people\t={number_of_people}\nattendency\t\t={attendance}\nnumber_of_strategy\t={number_of_strategy}\nticks\t\t\t={ticks}""")
    people = []
    result_of_sim = []
    i = 0
    while i < number_of_people:
        # borned = person(history=[],
        #                 strategy= strategy(random.randrange(1,
        #                                                     number_of_strategy + 1,
        #                                                     1)),
        #                 attendance = attendance,
        #                 decision=True)
        borned = person(attendance = attendance,
                        decision=True)
        people.append(borned)
        i = i + 1
        
        borned.takeDecision()
        borned.makeDFstrategy()
        for p in borned.dfStrategies:
            print(p)
    
    # Start simulation
    # init_tick = ticks

    # while init_tick-ticks < init_tick:
    #     history = []

    #     attendanceCounter = 0
    #     tempAttendancePersonIndexes = []

    #     for j, p in enumerate(people):
    #         if p.takeDecision():
    #             attendanceCounter = attendanceCounter + 1
    #             tempAttendancePersonIndexes.append(j)
    #         # else:
    #         #     p.appendHistory(60)
        
    #     for k in tempAttendancePersonIndexes:
    #         people[k].appendHistory(attendanceCounter)
        
    #     result  = len(tempAttendancePersonIndexes)
    #     result_of_sim.append(result)
    #     # print(result)
    #     ticks = ticks - 1

    #     if ticks==1:
    #         for p in people:
    #             print(p.history)
    
    # plt.plot(result_of_sim)
    # plt.show()

    # for p in people:
    #     print(p.toJSON())

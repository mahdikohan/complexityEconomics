import matplotlib.pyplot as plt
import random
import json
import pandas as pd



### Initial input variables for run simulaion

# This var show total number of our society
number_of_people = 5
# This var shows pleasable attendance in bar
attendance = 80
# This var determine distinct number strategy that each person can have 
number_of_strategy = 5
# This var gives number of execusion of model in simulation
ticks = 2
# This var shows length of long memory
length_of_long_memory = 3

    

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
        self.shortMemory:list = [random.randrange(0,2,1) for i in range(0,length_of_long_memory)]
        self.longMemory:list


    def __getStrategy(self)->list:
        allStates = length_of_long_memory*[0]+length_of_long_memory*[1]
        strategy = set()
        while True:
            strategy.add((tuple(random.sample(allStates,length_of_long_memory))))
            if len(strategy) == 2**length_of_long_memory:
                break
        lstrategy = list(strategy)
        # history = random.sample(lstrategy,len(lstrategy))
        history = lstrategy
        strategy_without_reward=[]
        for l in history:
            strategy_without_reward.append([l,random.choice([1,-1])])
        strategy_with_reward = [strategy_without_reward,0]
        return strategy_with_reward


    def __lookupStrategy(self, value):
        address = []
        for id,strategy in enumerate(self.strategies):
            for row,hist in enumerate(strategy[0]):
                if hist[0] == tuple(value):
                    address.append([id,row,strategy[1]])
        return address



    def takeDecision(self):
        self.strategies = [self.__getStrategy() for i in range(0,number_of_strategy)]
        lookup_result = self.__lookupStrategy(self.shortMemory)
        df_lookup_result = pd.DataFrame(lookup_result,columns=['strg','rfound','score'])
        max_score = df_lookup_result.loc[df_lookup_result['score'].idxmax()]
        result = {
                        'strategyId':max_score['strg'],
                        'score': max_score['score'],
                        'rowIdFound': max_score['rfound']
                   }
        
        self.decision = result

        print(pd.DataFrame(lookup_result,columns=['strg','rfound','score']))
        print(self.decision)
        print("")

        return self.decision
    


    def getScore(self):
        pass
    


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

        # borned.makeDFstrategy()
        # for p in borned.dfStrategies:
        #     print(p)
        i = i + 1



    # Start simulation
    init_tick = ticks

    while init_tick-ticks < init_tick:
        for agent in people:
            agent.takeDecision()
            
        ticks = ticks - 1

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

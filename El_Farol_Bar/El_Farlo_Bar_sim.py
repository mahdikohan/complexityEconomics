import matplotlib.pyplot as plt
import random
import json



## Initial input variables for run simulaion

# This var show total number of our society
number_of_people = 50
# This var shows pleasable attendance in bar
attendance = 80
# This var determine distinct number strategy that each person can have 
number_of_strategy = 10
# This var gives number of execusion of model in simulation
ticks = 50




# if we consider decision is based on 
# p(x) = w1 x(t1) + w2 x(t2) + ... + wn x(tn)
def weight(h:int):
    return ((2*random.random())-1)*h
    


# Defined each identities
class strategy:
    def __init__(self, strategyId) -> None:
        self.strategyId:int = strategyId





class person:
    def __init__(self, history, strategy, decision, attendance) -> None:
        self.history:list = history
        self.strategy:strategy = strategy
        self.decision:bool = decision
        self.attendance:int = attendance

    def __getStrategy(self)->int:
        last_strategy = list(map(weight,self.history[-self.strategy.strategyId:]))
        predicted = sum(last_strategy)
        return predicted < self.attendance
            
    def putHistory(self, history:list):
        self.history = history
    
    def appendHistory(self, attendanceCount:int):
        self.history.append(attendanceCount)
    
    def updateHistory(self, index:int, value:int):
        self.history[index] = value

    def takeDecision(self):
        forecastAttendance = self.__getStrategy()
        return forecastAttendance
    
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
        borned = person(history=[],
                        strategy= strategy(number_of_strategy),
                        attendance = attendance,
                        decision=True)
        people.append(borned)
        i = i + 1
    
    # Start simulation
    init_tick = ticks

    while init_tick-ticks < init_tick:
        history = []

        attendanceCounter = 0
        tempAttendancePersonIndexes = []

        for j, p in enumerate(people):
            if p.takeDecision():
                attendanceCounter = attendanceCounter + 1
                tempAttendancePersonIndexes.append(j)
            # else:
            #     p.appendHistory(60)
        
        for k in tempAttendancePersonIndexes:
            people[k].appendHistory(attendanceCounter)
        
        result  = len(tempAttendancePersonIndexes)
        result_of_sim.append(result)
        # print(result)
        ticks = ticks - 1

        if ticks==1:
            for p in people:
                print(p.history)
    
    plt.plot(result_of_sim)
    plt.show()
    # for p in people:
    #     print(p.toJSON())

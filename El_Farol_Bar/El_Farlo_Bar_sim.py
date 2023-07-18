import matplotlib.pyplot


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
    
    def result():
        return 0

class person:
    def __init__(self, history:list[int], strategyId, attendence) -> None:
        self.strategy:strategy = strategy(strategyId, history)
        self.decision:bool
        self.attendance:int = attendence

    def getStrategy()->int:
        n = 100
        return n

    def takeDecision():

        return 0

class bar:
    def __init__(self) -> None:
        self.totalCap:int
        self.members:int





def selectRandom():
    return 0


if __name__ == '__main__':
    print('hi')

import random

random.seed(123456)

class oneBandit():
    
    def __init__(self, mu=None):
        # Hidden probability to win with the machine
        if mu is None:
            self._mu = random.random() 
        else:
            self._mu = mu
        
        # Stats
        self._plays = 0
        self._totalReward = 0
        self._totalLoss = 0

    def playIt(self, best):
              
        # Compute gain, reward and loss
        gain = random.random() 
        reward = 1 if gain > self._mu else 0
        loss = best[1] - self._mu
        
        # Uptade machine state
        self._totalReward += reward
        self._totalLoss += loss
        self._plays += 1
        
        return reward
    
    def hasPlayed(self):
        return self._plays != 0
            
class Casino():
    def __init__(self, nb=100):
        self._machines = []

        for _ in range(nb):
            self._machines.append(oneBandit())
    
    def playMachine(self, i):
        return self._machines[i].playIt(self.currentBest())
    
    def currentBest(self): 
        maxMean = 0
        maxA = -1
        for a in range(self.nbMachines()):
            machine = self._machines[a]
            if machine.hasPlayed():
                mean = machine._totalReward / machine._plays
            else:
                mean = 0
                
            if  mean > maxMean:
                maxMean = mean
                maxA = a
                
        return (maxA, maxMean)
    
    def nbMachines(self):
        return len(self._machines)
    
    def displayRecap(self):
        print(f"Obtained gain {sum(map(lambda m: m._totalReward, self._machines))} with {self.nbMachines()} machines")
        for a in range(self.nbMachines()):
            print(f"Machine {a} was played {self._machines[a]._plays} times, was rewarded {self._machines[a]._totalReward} and lost {self._machines[a]._totalLoss}")
    

def gainsEpsilonGreedy(casino, epsilon=0.05):
    
    gain = 0
    
    for i in range(initialCredits):
        
        # Take either best machine or random one
        if random.random() < epsilon:
            machine = random.randint(0, casino.nbMachines()-1)
        else:
            machine = casino.currentBest()[0] 
       
        r = casino.playMachine(machine)
        gain += r
        
    return gain
    
    
initialCredits = 10000 # Nombre d'essais maximums
casino = Casino()

gain = gainsEpsilonGreedy(casino)
casino.displayRecap()

    
        
        
    
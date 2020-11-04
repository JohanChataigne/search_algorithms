
import random
import numpy as np
import array

_CITIES = (("Bordeaux", (44.833333,-0.566667)), ("Paris",(48.8566969,2.3514616)),("Nice",(43.7009358,7.2683912)),
("Lyon",(45.7578137,4.8320114)),("Nantes",(47.2186371,-1.5541362)),("Brest",(48.4,-4.483333)),("Lille",(50.633333,3.066667)),
("Clermont-Ferrand",(45.783333,3.083333)),("Strasbourg",(48.583333,7.75)),("Poitiers",(46.583333,0.333333)),
("Angers",(47.466667,-0.55)),("Montpellier",(43.6,3.883333)),("Caen",(49.183333,-0.35)),("Rennes",(48.083333,-1.683333)),("Pau",(43.3,-0.366667)))

def distance(a,b):
    (x1,y1),(x2,y2) = (a,b)
    return np.sqrt((x1-x2)**2+(y1-y2)**2) 

class Configuration():
    RANDOMSEED = 12345
    POPULATIONSIZE = 50
    MUTATIONRATE = 5 # 5% de mutation rate
    NBCITIES = len(_CITIES)

    def __init__(self):
        random.seed(self.RANDOMSEED)

config = Configuration()

class Chromosome:
    _value = None

    def __init__(self, initialValue=None):
        if initialValue is not None:
            self._value = initialValue
        else:
            self._initRandomOne()

    def fitness(self):
        pass

    def reproduceWith(self, other):
        pass

    def mutation(self):
        pass

    def _initRandomOne(self):
        pass

    def __repr__(self):
        return str(self._value)
    
    
class ChromosomeTSP(Chromosome):
    _distance = None
    
    def __init__(self, initialValue=None):
        self._distance = 0
        
        super().__init__(initialValue)
        
    def fitness(self):
        global config
        
        return self._distance
    
    def reproduceWith(self, other):
        pass
    
    def mutation(self):
        pass

    def _initRandomOne(self):
        global config
        
        self._value = array.array('I', [0]*config.NBCITIES)
        
        permutation = [x for x in range(0, config.NBCITIES)]
        random.shuffle(permutation)
        
        for i in range(0,config.NBCITIES):
            self._value[i] = permutation[i]
            city = self._value[i]
            previous_city = self._value[i-1]
            start = self._value[0]
            
            if i == config.NBCITIES-1:
                
                assert i > 0
                
                self._distance += distance(_CITIES[city][1], _CITIES[previous_city][1])
                self._distance += distance(_CITIES[city][1], _CITIES[start][1])
                
            elif (i > 0) and (i < config.NBCITIES-1):
                
                self._distance += distance(_CITIES[city][1], _CITIES[previous_city][1])
      

    def __repr__(self):
        toret = ""
        
        for i in self._value:
            toret += _CITIES[i][0] + " --> "      
        toret += _CITIES[self._value[0]][0] + " (" + str(self._distance) + ")"
        
        return toret
    

class Population():
    _population = None
    _populationSize = None
    
    def __init__(self, populationsize = None):
        global config
        self._populationSize = populationsize if populationsize is not None else config.POPULATIONSIZE
        self.randomInit()
    
    def randomInit(self):
        self._population = []
        
        while len(self._population) < self._populationSize:
            self._population.append(ChromosomeTSP())
        self._sort()
        
    def oneGeneration(self):
        global config
        
        newpop = self._population[:4]
        while len(newpop) < len(self):
            i1 = self.randomSelect()
            i2 = self.randomSelect(i1)
            for newson in i1.reproduceWith(i2):
                if random.randint(0,100) < config.MUTATIONRATE:
                    newson.mutation()
                newpop.append(newson)
        self._population = newpop
        self._populationSize = len(newpop)
        self._sort()
        
    def randomSelect(self, taboo=None):       
        return self._population[random.randint(0,len(self._population)-1)]

    def _sort(self):
        self._population.sort(key=lambda x: x.fitness(), reverse=True)
    
    def __repr__(self):
        toret = ""
        for i in self._population:
            toret += i.__repr__() + " (f="+ str(int(i.fitness()))+")\n"
        return toret

    def __len__(self):
        return len(self._population)
        
        
test = ChromosomeTSP()
print(test)

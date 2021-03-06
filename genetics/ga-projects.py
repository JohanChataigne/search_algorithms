import random
import numpy as np
import array
import getopt, sys
import math

# Data class for a project
class Project():
    
    def __init__(self, name, duration, deadline):
        self._name = name
        self._duration = duration
        self._deadline = deadline
        
        
    def __repr__(self):
        return "Project " + self._name + " wil take about " + str(self._duration) + " day(s) of work and is due in " + str(self._deadline) + " day(s)."


_PROJECTS = []

_PROJECTS_TEST = [
    Project("Go", 10, 25),
    Project("Unity", 20, 50),
    Project("Computer Vision", 7, 30),
    Project("PFE", 30, 80),
    Project("Ingénierie logicielle IA", 5, 25), 
    Project("TP AlgosRecherche", 1, 20),
    Project("TP Repr Connaissances", 1, 20), 
    Project("TP SMAC", 1, 20), 
    Project("TP JV", 1, 20),
    Project("Reinforcement Learning", 5, 55)
]


# Simulation parameters class
class Configuration():
    RANDOMSEED = 12345
    POPULATIONSIZE = 50
    MUTATIONRATE = 5 # 5% de mutation rate
    PROJECTS = _PROJECTS
    NB_PROJECTS = len(_PROJECTS)
    POPULATIONS = 50
    GENERATIONS = 50

    def __init__(self, projects=None):
        random.seed(self.RANDOMSEED)
        if projects is not None:
            self.PROJECTS = projects
            self.NB_PROJECTS = len(projects)
            

add = True

# Handle test mode

argumentList = sys.argv[1:]
options = "t"
long_options = ["test"]

try:
    arguments, _ = getopt.getopt(argumentList, options, long_options)
    
    for argument, value in arguments:
        if argument in ("-t", "--test"):
            add = False
            
except getopt.error as err:
    print (str(err))

if not add:
    _PROJECTS = _PROJECTS_TEST

# Loop to retrieve user's projects list

while (add):
    project_name = input("What's your project's name ?: ")
    project_duration = int(input("How long will it take you to do the project ? (integer, number of days): "))
    project_deadline = int(input("In how many time the project is due ? (integer, number of days): "))
    print("\n")
    
    _PROJECTS.append(Project(project_name, project_duration, project_deadline))
    
    answer = ""
    while (answer not in ["YES", "NO"]):
        answer = input("Project " + project_name + " successfully added, add another one? (Yes or No): ").upper()
        print("\n")
        if answer == "NO": add = False
    
config = Configuration(_PROJECTS)


# Chromosome Interface
class Chromosome:
    _value = None

    def __init__(self, initialValue=None):
        if initialValue is not None:
            self._value = initialValue
        else:
            self._initRandomOne()

    # Compute fitness of this individual
    def fitness(self):
        pass

    # Reproduce this individual with another and return the resulting children
    def reproduceWith(self, other):
        pass

    # Mutate this individual
    def mutation(self):
        pass

    # Randomly initialize this individual
    def _initRandomOne(self):
        pass

    def __repr__(self):
        return str(self._value)

    
# Chromosome class specific to our problem
class ChromosomeProjects(Chromosome):
    
    # Used to remember fitness because computation can become costly
    _fitness = None
    
    def __init__(self, initialValue=None):      
        super().__init__(initialValue)
        self.fitness()

    def _initRandomOne(self):
        global config      
        self._value = config.PROJECTS.copy()
        random.shuffle(self._value)
        
    def fitness(self):
        global config
        
        f = 0
        tmp_projects = self._value.copy()
        
        # Simulate acting like the solution suggests:
        # Do the projects in the current order
        # Get +1 if the project is done in time
        # Get -d with d the delay days
        for i in range(config.NB_PROJECTS):
            p = tmp_projects[i]
            diff = (p._deadline - p._duration)
                
            if (diff >= 0):
                f += 1
            else: 
                f += diff

            # Substract the consumed time on the current project to the remaining ones
            tmp_projects = list(map(lambda x: Project(x._name, x._duration, x._deadline - p._duration), tmp_projects))
        
        # Store this computation for eventual later use
        self._fitness = f        
            
    def reproduceWith(self, other):
        global config 

        # Each child mainly inherits its value from 1 parent
        children = [ChromosomeProjects(self._value.copy()), ChromosomeProjects(other._value.copy())]
        
        # Then force one aspect of the parent it doesn't inherits
        
        # Random indexes to pick random projects for each parent
        index_p1 = random.randint(0, config.NB_PROJECTS-1)
        index_p2 = random.randint(0, config.NB_PROJECTS-1)
        
        # Random projects
        p1 = self._value[index_p1]
        p2 = other._value[index_p2]
        
        # Index of random project in the other parent
        index_p1_in_p2 = other._value.index(p1)
        index_p2_in_p1 = self._value.index(p2)
        
        # Invert targeted projects 
        children[0][index_p1] = children[0][index_p1_in_p2]
        children[0][index_p1_in_p2] = p1
        
        children[1][index_p2] = children[1][index_p2_in_p1]
        children[1][index_p2_in_p1] = p2
        
        # Update children fitness
        children[0].fitness()
        children[1].fitness()
        
        return children
    
    def mutation(self):
        
        # Mutation here consists in inverting two project in the solution order
        
        # Select 2 indexes to invert
        indexes = list(range(config.NB_PROJECTS))
        i1 = random.choice(indexes)
        indexes.remove(i1)
        i2 = random.choice(indexes)
  
        # Swap values
        tmp = self._value[i1]
        self._value[i1] = self._value[i2]
        self._value[i2] = tmp
        
        self.fitness()
          

    def __repr__(self):
        global config
        
        toret = "[" + self._value[0]._name
        
        for i in range(1, config.NB_PROJECTS):
            toret += ", " + self._value[i]._name 
        
        toret += " (" + str(self._fitness) + ")]"
        
        return toret
    
    def __getitem__(self, index):
        return self._value[index]
    
    def __setitem__(self, index, value):
        self._value[index] = value
    

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
            self._population.append(ChromosomeProjects())
        self._sort()
        
    def oneGeneration(self):
        global config
            
        # Select a sample of our population to create the new one
        newpop = self._population[:4]
        while len(newpop) < len(self):
            
            # Make random individuals reproduce with each other
            i1 = self.randomSelect()
            i2 = self.randomSelect(i1)
            for newson in i1.reproduceWith(i2):
                if random.randint(0,100) < config.MUTATIONRATE and config.NB_PROJECTS > 1:
                    newson.mutation()
                newpop.append(newson)
                
        # Update population
        self._population = newpop
        self._populationSize = len(newpop)
        self._sort()
        
    def randomSelect(self, taboo=None): 
        
        # Select random individual in the population, except taboo
        tmp = self._population.copy()
        
        if taboo is not None:   
            tmp.remove(taboo)
        
        return tmp[random.randint(0, len(tmp)-1)]

    # Sort individuals by fitness to have easy access to the best one
    def _sort(self):
        self._population.sort(key=lambda x: x._fitness, reverse=True)
    
    def __repr__(self):
        toret = ""
        for i in self._population:
            toret += i.__repr__() + " (f="+ str(int(i._fitness))+")\n"
        return toret

    def __len__(self):
        return len(self._population)
        
        

def recap(best):
    
    date = 0
    advance = 0
    late = 0

    print(f"\nAccording to what you said, you have {len(_PROJECTS)} projects to do.")
    print("We suggest you to do them in the following order:")
    
    for i, p in enumerate(best._value):
        date += p._duration
        print(f"\n{i+1}) Project {p._name}")
        print(f"          --> It will take approximately {p._duration} day(s)")
        print(f"          --> The work is due in {p._deadline} day(s)")
        if p._deadline - date >= 0:
            print(f"          ==> It will be finished on day {date}, {p._deadline - date} day(s) in advance")
            advance += 1
        else:
            print(f"          ==> It will be finished on day {date}, {abs(p._deadline - date)} day(s) late")
            late += 1

    print(f"\n==> With this schedule you would submit {advance} project(s) in advance and {late} project(s) late")
        
    
# Randomly change parameters to get better results
best = None
best_fitness = -math.inf

# Solve problem with multiple populations
for i in range(config.POPULATIONS):
    population = Population()
    
    # Loop over generations for given population
    for k in range(config.GENERATIONS):
        population.oneGeneration()
     
    # Best candidate in this population
    local_best = population._population[0]
    
    # Compare local best to global best and update
    if (local_best._fitness > best_fitness):
        best = local_best
        best_fitness = local_best._fitness
        
    

recap(best)


import numpy as np
import random


_CITIES = { "Bordeaux" : (44.833333,-0.566667), "Paris" : (48.8566969,2.3514616), "Nice" : (43.7009358,7.2683912), "Lyon" : (5.7578137,4.8320114), "Nantes" : (47.2186371,-1.5541362), "Brest" : (48.4,-4.483333), "Lille" : (50.633333,3.066667), "Clermont-Ferrand" : (45.783333,3.083333), "Strasbourg" : (48.583333,7.75), "Poitiers" : (46.583333,0.333333), "Angers" : (47.466667,-0.55), "Montpellier" : (43.6,3.883333), "Caen" : (49.183333,-0.35), "Rennes" : (48.083333,-1.683333), "Pau" : (43.3,-0.366667) }

TRIES = 10

def distance(a,b):
    (x1,y1),(x2,y2) = (a,b)
    return np.sqrt((x1-x2)**2+(y1-y2)**2) 


# SLS applied to TSP problem
# Solution are always working solutions of the problem i.e. cycles.
class SLS:
    
    _best_solutions = []
    _best_tries = []
    _best_scores = []
    
    def __init__(self, start_solution=None):
        
        if start_solution is not None:
            self._currentSolution = start_solution
        else:
            self._currentSolution = self.randomStart()
        
    # Pick random candidate to start searching
    def randomStart(self):
        
        start = list(_CITIES.keys())
        random.shuffle(start)
        start.append(start[0])
        
        return start
        
    
    # Get the neighbours of the current solution i.e solution with only 2 nodes inverted
    def getNeighbours(self):
        
        short_current = self._currentSolution[:-1]
        neighbours = []
        
        for i in range(len(short_current)-1):
            
            for j in range(i+1, len(short_current)):
                
                neighbour = short_current.copy()
                neighbour[i] = short_current[j]
                neighbour[j] = short_current[i]
                neighbour.append(neighbour[0])
                neighbours.append(neighbour)
        
        return neighbours
            
    
    # Compute whole length of a solution
    def computeScore(self, solution):
        score = 0
        l = len(solution)
        
        for i in range(l-1):
            score += distance(_CITIES[solution[i]], _CITIES[solution[i+1]])
            
        return score
    
    
    def run(self):
        
        # Stops when a solution was tried too many times
        while(not self._best_tries or max(self._best_tries) < TRIES):
            
            # Local search on nieghoburs of current solution
            neighbours = self.getNeighbours() 
            scores = [self.computeScore(n) for n in neighbours]

            # Get the best one
            best_index, best_score = min(enumerate(scores), key=lambda x: x[1])
            best = neighbours[best_index]

            # If it is better than the current replace current, else get another start
            if (best_score < self.computeScore(self._currentSolution)):
                self._currentSolution = best
            else:
                self._currentSolution = self.randomStart()
                
                if best not in self._best_solutions:
                    self._best_solutions.append(best)
                    self._best_tries.append(1)
                    self._best_scores.append(best_score)
                else:
                    self._best_tries[self._best_solutions.index(best)] += 1
        
        
        # Return the best solution we've found 
        best_index, best_score = min(enumerate(self._best_scores), key=lambda x: x[1])
        best = self._best_solutions[best_index]
        
        return best, best_score
    
    
    def recap(self):
        print(self._best_solutions)
        print(self._best_scores)
        print(self._best_tries)
            
sls = SLS()
best, best_score = sls.run()
print(f"Best solution found is : {best}")
print(f"Score is : {best_score}")
#sls.recap()

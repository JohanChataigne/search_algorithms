from random import randint, getrandbits, choice
import numpy
from heapq import *
from collections import namedtuple

__boardSize__ = 3

class Board:
    _data = None

    def __init__(self, copyFrom=None, randomize = False):
        if copyFrom is None:
            fromList = [x for x in range(0,__boardSize__**2)]
            if randomize:
                fromList = sorted(fromList, key = lambda x: getrandbits(1))
            self._data = numpy.reshape(fromList, (__boardSize__, __boardSize__))
        else:
            self._data = numpy.array(copyFrom, copy=True)

    def empty(self):
        p = numpy.where(self._data==0)
        return (p[0][0], p[1][0])

    def _inBound(self, x):
        return x >= 0 and x < __boardSize__

    def randomMove(self):
        p = self.empty()
        assert self._data[p[0], p[1]] == 0
        move = choice([(-1,0), (+1,0), (0,-1), (0,+1)])
        if self._inBound(move[0]+p[0]) and self._inBound(move[1]+p[1]): 
            self._data[p[0],p[1]] = self._data[p[0]+move[0], p[1]+move[1]]
            self._data[p[0]+move[0], p[1]+move[1]] = 0

    def next(self):
        toret= []
        e = self.empty()
        for x,y in ((-1,0), (+1,0), (0,-1), (0,+1)):
            if self._inBound(x+e[0]) and self._inBound(y+e[1]):
               n = Board(copyFrom=self._data)
               n._data[e[0],e[1]] = n._data[x+e[0], y+e[1]]
               n._data[x+e[0], y+e[1]] = 0
               toret.append(n)
        return toret

    def __eq__(self, other):
        return numpy.arra_equal(self._data, other._data)

    def __hash__(self):
        self._data.flags.writeable = False
        h = hash(self._data.data.tobytes())
        self._data.flags.writeable = True
        return h 

    #Number of misplaced elements
    def h1(self, toBoard):
        
        misplaced = 0
        
        for i in range(__boardSize__):
            for j in range(__boardSize__):
                if self._data[i][j] != toBoard._data[i][j]:
                    misplaced += 1
        
        return misplaced
    
    #Euclidian distance between two states
    def h2(self, toBoard):
        
        current_positions = 9 * [0]
        goal_positions = 9 * [0]
        
        for i in range(__boardSize__):
            for j in range(__boardSize__):
                current_positions[self._data[i][j]] = (i,j)
                goal_positions[toBoard._data[i][j]] = (i,j)
        
        norm = lambda x,y : numpy.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)
        norms = map(norm, current_positions, goal_positions)
        
        return sum(norms)
            

class Node:
    state = None
    father = None
    g = None
    f = None 

    def __init__(self, state, father = None, g = 0, f = 0):
        self.state = state
        self.father = father
        self.g = g
        self.f = f

    # Permet de savoir si deux noeuds sont identiques
    def sameAsState(self, state):
        return (state is self.state) or (numpy.array_equal(self.state._data, state._data))
    
    # < for Nodes = f comparison
    def __lt__(self, other):
        return self.f < other.f

class Frontiere:
    _nodes = None 

    def __init__(self):
       self._nodes = [] 

    # Vous devez implanter cette fonction aussi
    # C'est la fonction qui permet de récupérer le noeud suivant
    # dans la frontiere
    def getNext(self):
        return heappop(self._nodes)

    # Fonction qui récupère un noeud d'apres son etat. Vous devez la rendre plus efficace
    def getNodeByState(self, state):

        for n in self._nodes:
            if n.sameAsState(state):
                return n
        return None

    # Fonction permettant d'ajouter un noeud à la frontiere
    # Vous devez l'implanter également 
    def addNode(self, state, goal, father = None, g = 0, checkAlreadyThere = False):
        
        h = state.h1(goal)
        f = g + h
        s = Node(state, father, g, f)
        
        if checkAlreadyThere:
            for n in self._nodes:
                if n.sameAsState(s):
                    self._nodes.remove(n)
                    heeppush(self._nodes, s)
        else:
            heappush(self._nodes, s)

    def __len__(self):
        return len(self._nodes)

    def size(self):
        return len(self._nodes)


# Code qui prrend la liberté de Python d'écrire en dehors de toute fonction

frontiere = Frontiere()
closed = set() # Dictionary of seen boards 

boardGoal = Board(randomize = False) # Génération du taquin "but"
# Exemple d'un taquin bien mélangé
boardInit = Board(copyFrom=[[4, 5, 0],[6, 2, 3],[7, 1, 8]], randomize = False) # Exemple de construction d'un etat initial en mélangeant les pièces
#boardInit = Board(copyFrom=boardGoal._data)
#for i in range(0,10): # Plus vous mélangerez plus ce sera difficile
#    boardInit.randomMove()

print("Initial Node: ")
print(boardInit._data)
print("Goal Node: ")
print(boardGoal._data)
frontiere.addNode(boardInit, boardGoal)
found = False
iterations = 0

# Grandes lignes de l'itération principale de A*
while frontiere.size() > 0 and not found:
    n = frontiere.getNext()
    if n.sameAsState(boardGoal):
        found = True
        break

    for nn in n.state.next(): # Itération sur tous les successeurs de n
        if nn not in closed:
            previous = frontiere.getNodeByState(nn)
            if previous is None: # Le noeud n'a jamais été vu
                frontiere.addNode(nn, boardGoal, n, n.g + 1)
            elif previous.g > n.g: # Le nouveau noeud est mieux
                previous.valid = False
                frontiere.addNode(nn, boardGoal, n, n.g + 1)
    closed.add(n) # Ajout de n à l'ensemble "Fermé"
    iterations += 1

print("Solution of cost ", n.g, " found in ", iterations, " steps and ", len(closed) + len(frontiere), " created nodes:")
noeudCourant = n
solution = []
while noeudCourant is not None:
    solution.append(noeudCourant.state) 
    noeudCourant = noeudCourant.father

while len(solution) > 0:
    node = solution.pop()
    print(node._data)


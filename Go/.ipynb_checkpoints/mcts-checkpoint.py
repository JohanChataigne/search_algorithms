
class Node:
    
    def __init__(self, move, color, parent, wins=0, total=0):
        
        self._move = move
        
        # Black = 1, White = 2
        assert color in [1, 2]
        
        self._color = color
        self._wins = wins
        self._total = total
        
        self._children = []
        self._parent = parent
        
    
    def addChild(self, child):
        self._children.append(child)
        
    
    def addGame(self, result):
        
        assert result in [0, 1]
        
        self._wins += 1 if result else 0
        self._total += 1
        
    def getColorName(self):
        return 'Black' if self._color == 1 else 'White'
    
    def __repr__(self):
        
        toret = "Node(color=" + str(self.getColorName()) + ", wins=" + str(self._wins) + ", total=" + str(self._total) + ", nb_children=" + str(len(self._children)) + ")"   
        return toret

class Tree:
    
    def __init__(self, root):
        
        self._root = root
                
class MCTS:
    
    self._tree = None
    
    def __init__(self, root):
        
        self._tree = Tree(root)
        
    

if __name__ == "__main__":
    
    node = Node(1, None)
    node2 = Node(2, node)
    node.addChild(node2)

    print(node)
    print(node2)

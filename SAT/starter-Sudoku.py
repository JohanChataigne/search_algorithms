# First we need to print clauses
def printClause(clause):
    print(" ".join([str(v) for v in clause]) + " 0")

def equals1a(arrayOfVars):
    printClause(arrayOfVars) 
    for i,x in enumerate(arrayOfVars):
        for y in arrayOfVars[i+1:]:
            printClause([-x, -y])

tmp = [x for x in range(1,5)]
print("c Constraints forcing just on true variable in", tmp)
print("c we don't print any 'p cnf X Y' line, sorry")
equals1a(tmp)

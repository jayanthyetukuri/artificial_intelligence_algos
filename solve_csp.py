import numpy as np, random
from operator import itemgetter, sub


def solve_csp(nodes, arcs, max_steps):
    """
    This function solves the csp using the MinConflicts Search
    Algorithm.

    INPUTS:
    nodes:      a list of letters that indicates what type of node it is,
                the index of the node in the list indicates its id
                letters = {C, T, S, P, H}
    arcs:       a list of tuples that contains two numbers, indicating the
                IDS of the nodes the arc connects.
    max_steps:  max number of steps to make before giving up

    RETURNS: a list of values for the soltiion to the CSP where the
             index of the value correxponds the the value for that
             given node.

        Triangle - The leftmost digit of the product of all of its neightbors
        Square - The rightmost digit of of the product of all its neighbors
        Hexagon - The leftmost digit of the sum of all its neighbors
        Pentagon - The rightmost digit of the sum of all its neighbors
        Circle - No contraints

    """

    nodes = list(nodes)
    print 'nodes:', nodes

    node_values_dict = dict(zip(nodes, '2'*len(set(nodes))))
    print 'initial random assignment', node_values_dict
    indexes = np.arange(len(nodes))

    graph = {}
    for arc in arcs:
        if not arc[0] in graph:
            graph[arc[0]] = []
        if not arc[1] in graph:
            graph[arc[1]] = []
        graph[arc[0]].append(arc[1])
        graph[arc[1]].append(arc[0])
    for i in indexes:
        if i in graph:
            continue
        else:
            graph[i] = []
    graph = dict(sorted(graph.items()))
    print 'graph:', graph

    domain = [i for i in np.arange(1, 10, 1)]
    print 'initial domain for each node:', domain

    superAdjacency ={}
    for i in np.arange(len(nodes)):
        superAdjacency[i] = []
        superAdjacency[i].append(nodes[i])
        superAdjacency[i].append(node_values_dict[nodes[i]])
        superAdjacency[i].append(graph[i])
        superAdjacency[i].append(domain)

    print 'superAdjacency', superAdjacency

    def getNodeType(superAdjacency, index):
        return list(superAdjacency[index])[0]

    def getCurrentAssignment(superAdjacency, index):
        return list(superAdjacency[index])[1]

    def getCurrentAssignmentForList(superAdjacency, indexList):
        return [int(list(superAdjacency[index])[1]) for index in indexList]

    def getSolution(superAdjacency):
        return [int(list(superAdjacency[index])[1]) for index in superAdjacency]

    def getNeighbours(superAdjacency, index):
        return list(superAdjacency[index])[2]

    def getDomain(superAdjacency, index):
        return list(superAdjacency[index])[3]

    def updateSuperAdjacency(superAdjacency, nodeType, newValue):
        updateList =[]
        for i in superAdjacency:
            if str(getNodeType(superAdjacency, i)) == nodeType:
                updateList.append(i)
        for i in updateList:
            superAdjacency[i][1] = newValue

    def isSolution():
        return graphConstraints(superAdjacency)

    def graphConstraints(superAdjacency):
        graphEval = []

        for index in superAdjacency:
            neighbours = getNeighbours(superAdjacency, index)
            nodeType = getNodeType(superAdjacency, index)

            if nodeType == 'T':
                graphEval.append(int(str(eval(str(
                    getCurrentAssignmentForList(superAdjacency, neighbours)).replace(',', '*'))[0])[0]))
            elif nodeType == 'C':
                return 'NA'
            elif nodeType == 'S':
                graphEval.append(int(str(eval(str(
                    getCurrentAssignmentForList(superAdjacency, neighbours)).replace(',', '*'))[0])[::-1][0]))
            elif nodeType == 'H':
                graphEval.append(int(str(np.sum(
                    getCurrentAssignmentForList(superAdjacency, neighbours)))[0]))
            if nodeType == 'P':
                graphEval.append(int(str(np.sum(
                    getCurrentAssignmentForList(superAdjacency, neighbours)))[::-1][0]))

        currentAssignment = [item[1] for item in superAdjacency.values()]
        difference = map(sub, currentAssignment, graphEval)

        if sum(difference) == 0:
            return True
        else:
            return difference

    def findConflictVariable(superAdjacency, lastUpdateNode):
        node_conflict_count = {}
        for node in node_values_dict:
            node_conflict_count[node] = 0
        for index in superAdjacency:
            neighbours = getNeighbours(superAdjacency, index)
            nodeType = getNodeType(superAdjacency, index)
            if nodeType == 'T':
                try:
                    if getCurrentAssignment(superAdjacency, index) != \
                            int(str(eval(str(getCurrentAssignmentForList(superAdjacency, neighbours)).replace(',', '*'))[0])[0]):
                        node_conflict_count[nodeType] = node_conflict_count[nodeType] + 1
                except:
                    continue
            elif nodeType == 'S':
                try:
                    if getCurrentAssignment(superAdjacency, index) != int(str(eval(str(getCurrentAssignmentForList(superAdjacency, neighbours)).replace(',', '*'))[0])[::-1][0]):
                        node_conflict_count[nodeType] = node_conflict_count[nodeType] + 1
                except:
                    continue
            elif nodeType == 'H':
                try:
                    if getCurrentAssignment(superAdjacency, index) != int(str(np.sum(getCurrentAssignmentForList(superAdjacency, neighbours)))[0]):
                        node_conflict_count[nodeType] = node_conflict_count[nodeType] + 1
                except:
                    continue
            if nodeType == 'P':
                try:
                    if getCurrentAssignment(superAdjacency, index) != int(str(np.sum(getCurrentAssignmentForList(superAdjacency, neighbours)))[::-1][0]):
                        node_conflict_count[nodeType] = node_conflict_count[nodeType] + 1
                except:
                    continue
        choices = [k for k, v in node_conflict_count.items() if v > 0]
        if len(choices) > 0:
            updateNode = random.choice(choices)

            if updateNode == lastUpdateNode:
                choices.pop(choices.index(updateNode))
                try:
                    lastUpdateNode = random.choice(choices)
                    return lastUpdateNode, lastUpdateNode
                except:
                    return lastUpdateNode, lastUpdateNode
            else:
                lastUpdateNode = updateNode
                return updateNode, lastUpdateNode
        else:
            return 'NA', 'NA'



    def valueForConflictedVariable(superAdjacency, var):
        for index in superAdjacency:
            nodeType = getNodeType(superAdjacency, index)
            neighbours = getNeighbours(superAdjacency, index)
            if not neighbours:
                continue
            elif str(nodeType) == str(var):
                domain = getDomain(superAdjacency, index)

                choice = random.choice(domain)
                if nodeType == 'T':
                    choice = int(str(eval(str(getCurrentAssignmentForList(superAdjacency, neighbours)).replace(',', '*'))[0])[0])
                elif nodeType == 'S':
                    choice = int(str(eval(str(getCurrentAssignmentForList(superAdjacency, neighbours)).replace(',', '*'))[0])[::-1][0])
                elif nodeType == 'H':
                    choice = int(str(np.sum(getCurrentAssignmentForList(superAdjacency, neighbours)))[0])
                if nodeType == 'P':
                    choice = int(str(np.sum(getCurrentAssignmentForList(superAdjacency, neighbours)))[::-1][0])

                choice = int(choice)
                if choice % 2 == 0:
                    return choice
                else:
                    return choice

    def min_conflicts(nodes, arcs, max_steps):
        lastUpdateNode = ''
        for i in range(max_steps):
            if isSolution() == True:
                return
            var, lastUpdateNode = findConflictVariable(superAdjacency, lastUpdateNode)
            if var != 'NA':
                value = valueForConflictedVariable(superAdjacency, var)
                updateSuperAdjacency(superAdjacency, var, value)
                node_values_dict[var] = value
            else:
                pass

        return

    min_conflicts(nodes, arcs, max_steps)
    node_values = getSolution(superAdjacency)
    return node_values


nodes = 'CHTPS'
arcs = [(0,1), (0,2), (1,2), (1,3), (1,4), (2,3), (2,4)]
max_steps = 1000
node_values = solve_csp(nodes, arcs, max_steps)
print 'Solution:', node_values

'''
Sample output:

nodes: ['C', 'H', 'T', 'P', 'S']
initial random assignment {'S': '2', 'H': '2', 'C': '2', 'T': '2', 'P': '2'}
graph: {0: [1, 2], 1: [0, 2, 3, 4], 2: [0, 1, 3, 4], 3: [1, 2], 4: [1, 2]}
initial domain for each node: [0, 2, 4, 6, 8]
superAdjacency {0: ['C', '2', [1, 2], [0, 2, 4, 6, 8]], 1: ['H', '2', [0, 2, 3, 4], [0, 2, 4, 6, 8]], 2: ['T', '2', [0, 1, 3, 4], [0, 2, 4, 6, 8]], 3: ['P', '2', [1, 2], [0, 2, 4, 6, 8]], 4: ['S', '2', [1, 2], [0, 2, 4, 6, 8]]}
Solution: [2, 1, 4, 5, 4]


Outputs when the program is run for 60 times:

    OUTPUT           REPETITIONS
----------------------------------
[2, 1, 4, 5, 4]           36
[2, 7, 0, 7, 0]           2
[2, 1, 0, 9, 0]           3
[2, 1, 0, 1, 0]           3
[2, 5, 0, 5, 0]           3
[2, 3, 0, 1, 0]           3
[2, 9, 0, 9, 0]           2
[2, 5, 0, 3, 0]           2
[2, 7, 0, 5, 0]           2
[2, 3, 0, 3, 0]           2
[2, 9, 0, 7, 0]           2

'''

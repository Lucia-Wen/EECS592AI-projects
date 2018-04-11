"""General search code

This module implement basic BFS, DFS, iterative deeping, uniform cost, A* search for both route planning and TSP problems.

"""
class Node(object):
    """ Node class have state, parent, cost, depth, f, path arguments. Basic ndoe in search problem

    """
    def __init__(self, state, parent, cost, depth, f=0, path=None):
        self.state = state
        self.parent_node = parent
        self.cost = cost
        self.depth = depth
        self.f_hn = f
        self.path = path

class Solution(object):
    """return solutuion described in spec

    """
    def __init__(self, node, num_expanded):
        self._node = node
        self._expanded = num_expanded
    def expanded_num(self):
        """return number of expanded nodes

        """
        return self._expanded
    def path(self):
        """solution path

        """
        path = []
        path.append(self._node.state)
        parent = self._node.parent_node
        while True:
            if parent is None:
                return path
            path.insert(0, parent.state)
            parent = parent.parent_node
    def cost(self):
        """return true cost

        """
        return round(self._node.cost, 4)




def partition(li_st, l_o, h_i):
    """partition for quicksort

    """
    pivot = (li_st[h_i])
    i = l_o - 1
    for j in range(l_o, h_i):
        if (li_st[j]) < pivot:
            i = i+1
            li_st[j], li_st[i] = li_st[i], li_st[j]
    if (li_st[h_i]) < (li_st[i+1]):
        li_st[h_i], li_st[i+1] = li_st[i+1], li_st[h_i]

    return i+1

def quicksort(li_st, l_o, h_i):
    """quciksort for a list of str or num, increasing order

    """
    if l_o < h_i:
        p_artition = partition(li_st, l_o, h_i)
        quicksort(li_st, l_o, p_artition-1)
        quicksort(li_st, p_artition+1, h_i)


def partition_node(li_st, l_o, h_i):
    """partition for quciksort node

    """
    pivot = (li_st[h_i].f_hn)
    i = l_o - 1
    for j in range(l_o, h_i):
        if (li_st[j].f_hn) < pivot:
            i = i+1
            li_st[j], li_st[i] = li_st[i], li_st[j]
    if (li_st[h_i].f_hn) < (li_st[i+1].f_hn):
        li_st[h_i], li_st[i+1] = li_st[i+1], li_st[h_i]

    return i+1

def quicksort_node(li_st, l_o, h_i):
    """quciksort for a list of node ,increasing order

    """
    if l_o < h_i:
        p_artition = partition_node(li_st, l_o, h_i)
        quicksort_node(li_st, l_o, p_artition-1)
        quicksort_node(li_st, p_artition+1, h_i)




# B D I U A
def mysearch(graph, origin, destination, option, graph2=None, hashing=None, hashing2=None, i_limit=None, problem='route planning'):
    def checknode(key):
        """check whether node in closelist for route planning
        """
        status = True
        if key in explored:
            status = False
        for item in frontier:
            if key == item.state:
                status = False
        return status

    def checknodetsp(key):
        """check whether node in closelist for tsp
        """
        status = True
        if key in explored:
            status = False
        for item in frontier:
            if key == item.path:
                status = False
        return status

    def goalcheck(state):
        """goal check for tsp
        no 0 left in path
        """
        if 0 not in state:
            return True
        return False

    def heuristic_(currentpath):
        """caculate heuristic described in README
        """
        i = 0
        sum_ = 0
        for item in currentpath:
            if item == 0:
                min_ = 10000000
                for key in graph[hashing2[i]].keys():
                    if min_ > graph[hashing2[i]][key]:
                        min_ = graph[hashing2[i]][key]
                sum_ = sum_+min_
            i += 1
        return sum_

    problem = problem
    depth_limit = 30

    if problem == 'TSP':

        if option == 'I':
            limit = depth_limit
            for step_limit in range(1, limit+1):
                num_expanded = 0
                initial_path = len(hashing.keys())*[0]
                initial_path[hashing[origin]] = 2
                start = Node(origin, None, 0, 0, 0, initial_path)

                frontier = []
                explored = []

                frontier.append(start)

                while True:
                    if not frontier:
                        if step_limit == limit:
                            return False
                        else:
                            break
                    current_node = frontier[0]
                    frontier = frontier[1:]
                    if goalcheck(current_node.path):
                        return Solution(current_node, num_expanded)

                    if current_node.depth > depth_limit:
                        continue

                    if current_node.path in explored:
                        continue

                    num_expanded += 1

                    explored.append(current_node.path)
                    #check limit
                    if current_node.depth == step_limit:
                        pass
                    else:
                        keys = list(graph[current_node.state].keys())
                        quicksort(keys, 0, len(keys)-1)
                        for key in keys:
                            currentpath = list(current_node.path)
                            currentpath[hashing[current_node.state]] = 1
                            currentpath[hashing[key]] = 2
                            if currentpath not in explored:
                                child = Node(key, current_node, current_node.cost+graph[current_node.state][key], current_node.depth+1, current_node.f_hn+1, currentpath)
                                frontier.insert(0, child)
        elif option == 'U':
            num_expanded = 0
            initial_path = len(hashing.keys())*[0]
            initial_path[hashing[origin]] = 2
            start = Node(origin, None, 0, 0, 0, initial_path)
            frontier = []
            explored = []
            frontier.append(start)
            while True:
                if not frontier:
                    return False
                current_node = frontier[0]
                frontier = frontier[1:]
                if goalcheck(current_node.path):
                    return Solution(current_node, num_expanded)
                if current_node.path in explored:
                    continue
                num_expanded += 1
                explored.append(current_node.path)
                keys = list(graph[current_node.state].keys())
                for key in keys:

                    currentpath = list(current_node.path)
                    currentpath[hashing[current_node.state]] = 1
                    currentpath[hashing[key]] = 2
                    if currentpath not in explored:
                        child = Node(key, current_node, current_node.cost+graph[current_node.state][key], current_node.depth+1, current_node.cost+graph[current_node.state][key], currentpath)
                        count = 0
                        for i in range(0, len(frontier)):
                            if  currentpath == frontier[i].path:
                                count += 1

                                if child.f_hn < frontier[i].f_hn:
                                    frontier[i] = child
                        if count == 0:
                            frontier.append(child)
                    quicksort_node(frontier, 0, len(frontier)-1)
        elif option == 'A':
            num_expanded = 0
            initial_path = len(hashing.keys())*[0]
            initial_path[hashing[origin]] = 2
            start = Node(origin, None, 0, 0, heuristic_(initial_path), initial_path)
            frontier = []
            explored = []
            frontier.append(start)
            while True:
                if not frontier:
                    return False
                current_node = frontier[0]
                frontier = frontier[1:]
                if goalcheck(current_node.path):
                    return Solution(current_node, num_expanded)
                if current_node.path in explored:
                    continue
                num_expanded += 1
                explored.append(current_node.path)

                #
                keys = list(graph[current_node.state].keys())
                for key in keys:
                    currentpath = list(current_node.path)
                    currentpath[hashing[current_node.state]] = 1
                    currentpath[hashing[key]] = 2
                    if currentpath not in explored:
                        child = Node(key, current_node, current_node.cost+graph[current_node.state][key], current_node.depth+1, current_node.cost+graph[current_node.state][key]+heuristic_(currentpath), currentpath)
                        count = 0
                        for i in range(0, len(frontier)):
                            if  currentpath == frontier[i].path:
                                count += 1

                                if child.f_hn < frontier[i].f_hn:
                                    frontier[i] = child
                        if count == 0:
                            frontier.append(child)

                    quicksort_node(frontier, 0, len(frontier)-1)

        else:
            num_expanded = 0
            initial_path = len(hashing.keys())*[0]
            initial_path[hashing[origin]] = 2
            start = Node(origin, None, 0, 0, 0, initial_path)
            frontier = []
            explored = []
            frontier.append(start)
            while True:
                if not frontier:
                    return False
                current_node = frontier[0]
                frontier = frontier[1:]
                if goalcheck(current_node.path):
                    return Solution(current_node, num_expanded)
                if current_node.depth > depth_limit:
                    continue
                if current_node.path in explored:
                    continue
                num_expanded += 1
                explored.append(current_node.path)
                keys = list(graph[current_node.state].keys())
                if option == 'B':
                    quicksort(keys, 0, len(keys)-1)
                    for key in keys:
                        currentpath = list(current_node.path)
                        currentpath[hashing[current_node.state]] = 1
                        currentpath[hashing[key]] = 2
                        if checknodetsp(currentpath):
                            child = Node(key, current_node, current_node.cost+graph[current_node.state][key], current_node.depth+1, current_node.f_hn+1, currentpath)
                            frontier.append(child)

                if  option == 'D':
                    quicksort(keys, 0, len(keys)-1)
                    for key in keys:
                        currentpath = list(current_node.path)
                        currentpath[hashing[current_node.state]] = 1
                        currentpath[hashing[key]] = 2
                        if currentpath not in explored:
                            child = Node(key, current_node, current_node.cost+graph[current_node.state][key], current_node.depth+1, current_node.f_hn+1, currentpath)
                            frontier.insert(0, child)
    elif problem == 'route planning':
        if option == 'I':
            if i_limit is None:
                limit = len(graph.keys())
            else:
                limit = i_limit
            for step_limit in range(1, limit+1):
                num_expanded = 0
                start = Node(origin, None, 0, 0)
                if start.state == destination:
                    return Solution(start.state, num_expanded)
                frontier = []
                explored = []
                frontier.append(start)
                while True:
                    if not frontier:
                        if step_limit == limit:
                            return False
                        else:
                            break
                    current_node = frontier[0]
                    frontier = frontier[1:]
                    if current_node.state in explored:
                        continue
                    explored.append(current_node.state)
                    num_expanded += 1
                    if current_node.depth > depth_limit:
                        return False
                    #check limit
                    if current_node.depth == step_limit:
                        pass
                    else:
                        keys = list(graph[current_node.state].keys())


                        quicksort(keys, 0, len(keys)-1)
                        for key in keys:
                            if checknode(key):
                                child = Node(key, current_node, current_node.cost+graph[current_node.state][key], current_node.depth+1)

                                if key == destination:
                                    return Solution(child, num_expanded)
                                else:
                                    frontier.insert(0, child)
        elif option == 'U':
            num_expanded = 0
            start = Node(origin, None, 0, 0)

            frontier = []
            explored = []
            frontier.append(start)
            while True:
                if not frontier:
                    return False
                current_node = frontier[0]
                frontier = frontier[1:]
                if current_node.state == destination:
                    return Solution(current_node, num_expanded)
                if current_node.depth > depth_limit:
                    return False
                if current_node.state in explored:
                    continue
                num_expanded += 1
                explored.append(current_node.state)

                #
                keys = list(graph[current_node.state].keys())
                for key in keys:
                    if key not in explored:
                        child = Node(key, current_node, current_node.cost+graph[current_node.state][key], current_node.depth+1, current_node.f_hn +graph[current_node.state][key])
                        count = 0
                        for i in range(0, len(frontier)):
                            if key == frontier[i].state:
                                count += 1

                                if child.cost < frontier[i].cost:
                                    frontier[i] = child
                        if count == 0:
                            frontier.append(child)

                    quicksort_node(frontier, 0, len(frontier)-1)
        elif option == 'A':
            num_expanded = 0
            start = Node(origin, None, 0, 0)

            frontier = []
            explored = []
            frontier.append(start)
            while True:
                if not frontier:
                    return False
                current_node = frontier[0]
                frontier = frontier[1:]
                if current_node.state == destination:
                    return Solution(current_node, num_expanded)
                if current_node.depth > depth_limit:
                    return False
                if current_node.state in explored:
                    continue
                num_expanded += 1
                explored.append(current_node.state)

                #
                keys = list(graph[current_node.state].keys())
                for key in keys:
                    if key not in explored:
                        child = Node(key, current_node, current_node.cost+graph[current_node.state][key], current_node.depth+1, current_node.cost+graph[current_node.state][key]+graph2[destination][key])
                        count = 0
                        for i in range(0, len(frontier)):
                            if key == frontier[i].state:
                                count += 1

                                if child.f_hn < frontier[i].f_hn:
                                    frontier[i] = child
                        if count == 0:
                            frontier.append(child)

                    quicksort_node(frontier, 0, len(frontier)-1)



        else:
            num_expanded = 0
            start = Node(origin, None, 0, 0)
            if start.state == destination:
                return Solution(start, num_expanded)
            frontier = []
            explored = []
            #depth = -1
            frontier.append(start)
            while True:
                #depth += 1

                if not frontier:
                    return False
                current_node = frontier[0]
                frontier = frontier[1:]
                if current_node.state == destination:
                    return Solution(current_node, num_expanded)

                if current_node.depth > depth_limit:
                    return False

                if current_node.state in explored:
                    continue

                num_expanded += 1
                explored.append(current_node.state)


                #
                keys = list(graph[current_node.state].keys())


                if option == 'B':
                    quicksort(keys, 0, len(keys)-1)
                    for key in keys:
                        if checknode(key):
                            child = Node(key, current_node, current_node.cost+graph[current_node.state][key], current_node.depth+1, current_node.f_hn+1)
                            frontier.append(child)

                if  option == 'D':
                    quicksort(keys, 0, len(keys)-1)
                    #keys.reverse()
                    for key in keys:
                        if key not in explored:
                            child = Node(key, current_node, current_node.cost+graph[current_node.state][key], current_node.depth+1, current_node.f_hn+1)
                            frontier.insert(0, child)
                        

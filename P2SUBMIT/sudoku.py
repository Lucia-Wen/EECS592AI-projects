"""sudoku

This module implement AC3 and Backtracking algorithm to solve both easy and hard sudoku csp problem.
$ python sudoku.py
input: suinput.csv
output: suoutput.csv
"""
from copy import deepcopy

def convert(num):
    """convert 1d num to 2D axis

    """
    i_axis = num//9
    j_axis = num%9
    return i_axis, j_axis

def convert2(i_axis, j_axis):
    """convert 2D axis to 1d num

    """
    num = i_axis*9+j_axis
    return num

def arcs():
    """generating arcs dictionary 81*20, denotes all nodes and their neighbours.

    """
    unit = [[[], [], []], [[], [], []], [[], [], []]]
    for i_arcs in range(0, 9):
        for j_arcs in range(0, 9):
            x_arcs = i_arcs//3
            y_arcs = j_arcs//3
            unit[x_arcs][y_arcs].append(i_arcs*9+j_arcs)
    arcdic = {}
    for num in range(0, 81):
        arcdic[num] = set()
        i_axis, j_axis = convert(num)
        for a_axis in range(0, 9):
            arcdic[num].add(i_axis*9+a_axis)
            arcdic[num].add(a_axis*9+j_axis)
            x_arcs = i_axis//3
            y_arcs = j_axis//3
            for item in unit[x_arcs][y_arcs]:
                arcdic[num].add(item)
        arcdic[num].remove(num)
    return arcdic


def init_arc(nodes, arcdic):
    """generating arcs for list of nodes
       input: node, arc dictionary
       ouput: list of arcs
    """
    queue = []
    #print(nodes)
    for node in nodes:
        #print(arcdic)
        for neighbour in arcdic[node]:
            queue.append((node, neighbour))
    return queue

def revise(csp, x1_re, x2_re):
    """modify x2 domain according to x1 and constrains,check if x2 domain is been modified

    """
    revised = False
    if len(csp[x1_re]) == 1:
        if csp[x1_re][0] in csp[x2_re]:
            csp[x2_re].remove(csp[x1_re][0])
            revised = True
    return revised

def ac3(csp, arcdic, queue=None):
    """implement arc constrains for queue of arcs

    """
    while queue:
        c_arc = queue.pop(0)
        x1_ac3, x2_ac3 = c_arc[0], c_arc[1]
        if revise(csp, x1_ac3, x2_ac3):
            if not csp[x2_ac3]:
                return False
            queue.extend(init_arc([x2_ac3], arcdic))
    return True

def select_unassignedval(csp):
    """select the minimun domain length(>1) variable

    """
    lenlst = []
    for i_s in range(0, 81):
        if len(csp[i_s]) != 1:
            lenlst.append(len(csp[i_s]))
        else:
            lenlst.append(99)
    m_v, idx = min((lenlst[i_s], i_s) for i_s in range(len(lenlst)))
    return idx

def complete(csp):
    """check if csp problem is complete

    """
    for i_c in range(0, 81):
        if len(csp[i_c]) != 1:
            return False
    return True


def backtrack(csp, arcdic):
    """backtracking, always genetating new inference, if true return,if false discard

    """
    if complete(csp):
        return csp
        #complete check
    var = select_unassignedval(csp)
    for value in csp[var]:
        inference = deepcopy(csp)
        inference[var] = [value]
        queue = init_arc([var], arcdic)
        symbol = ac3(inference, arcdic, queue)
        if symbol:
            result = backtrack(inference, arcdic)
            if result:
                return result
    return None
def backtracksearch(csp, arcdic):
    """implement recursive backtracksearch algorithm

    """
    return backtrack(csp, arcdic)
if __name__ == '__main__':
    INITIAL_DOMAIN = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    INPUT_PATH = 'suinput.csv'
    CSP = {}
    IN_NODES = []
    ARCS = arcs()
    #print(ARCS)
    try:
        with open(INPUT_PATH, 'r') as f:
            i = 0
            for line in f:
                j = 0
                for dot in line.split(','):
                    dot = int(dot.strip())
                    if dot == 0:
                        CSP[convert2(i, j)] = deepcopy(INITIAL_DOMAIN)
                    else:
                        CSP[convert2(i, j)] = [dot]
                        IN_NODES.append(i*9+j)
                    j += 1
                i += 1
            QUEUE = init_arc(IN_NODES, ARCS)

            ac3(CSP, ARCS, QUEUE)
            FINALRESULT = backtracksearch(CSP, ARCS)
            with open('suoutput.csv', 'w') as f:
                LINE = []
                for i in range(1, 82):
                    LINE.append(str(FINALRESULT[i-1][0]))
                    if i % 9 == 0:
                        f.write(',' .join(LINE)+'\n')
                        LINE = []
    except:
        print('suinput.csv not found')

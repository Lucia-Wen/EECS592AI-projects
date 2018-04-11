"""Bayesnet
Implement simple bayesnet, enumeration_ask, enumerate_all algorithms to construct a simple bayesnet
input: bn.txt and input.txt
output: probability of node Q given edvidence e described in input.txt
"""

import copy
class Node(object):
    """ Node class keep infomation of nodename, nodeparents and cpt of current node
    """
    def __init__(self, node):
        self.__node = node
        self.__parents = []
        self.__cpt = None
    def name(self):
        """return nodename
        """
        return self.__node
    def parents(self):
        """return parents of this node
        """
        return self.__parents
    def add_parent(self, parent):
        """add parent of this node
        """
        self.__parents.append(parent)
    def cpt(self):
        """return cpt of this node
        """
        return self.__cpt
    def add_cpt(self, cpt):
        """add cpt of this node
        """
        self.__cpt = cpt
    def update_cpt(self, tup, value):
        """update cpt of this node
        """
        if self.__parents == []:
            self.__cpt = value
        else:
            self.__cpt[tup] = value

class BayesNet(object):
    """ BayesNet class constuct a simple bayes net with attribute vars and a graph
        contaning nodes
    """
    def __init__(self):
        self.__vars = []
        self.__nset = set()
        self.__graph = {}
    def nset(self):
        """set of parents
        """
        return self.__nset
    def add_nset(self, varv):
        """add variable parent
        """
        self.__nset.add(varv)
    def vars(self):
        """return vars of the net
        """
        return self.__vars
    def net(self):
        """return graph of nodes
        """
        return self.__graph
    def add_var(self, varv):
        """add variable
        """
        self.__vars.append(varv)
    def add_net(self, graph):
        """add graph
        """
        self.__graph = graph

    def enumerate_all(self, varv, e_v):
        """enumerate according to the order of variables
        """
        vari = copy.deepcopy(varv)
        if vari == []:
            return 1.0
        y_i = vari.pop(0)
        if y_i in e_v.keys():
            if self.net()[y_i].parents() == []:
                return tf_val(e_v[y_i], self.net()[y_i].cpt())*self.enumerate_all(vari, e_v)
            else:
                key = []
                for parent in self.net()[y_i].parents():
                    key += e_v[parent]
            return tf_val(e_v[y_i], self.net()[y_i].cpt()[tuple(key)])*self.enumerate_all(vari, e_v)
        else:
            if self.net()[y_i].parents() == []:
                return (self.net()[y_i].cpt()*self.enumerate_all(vari, extended(e_v, (y_i, 'T'))) +
                        (1 - self.net()[y_i].cpt())*self.enumerate_all(vari, extended(e_v, (y_i, 'F'))))
            else:
                key = []
                for parent in self.net()[y_i].parents():
                    key += e_v[parent]
            return (self.net()[y_i].cpt()[tuple(key)]*self.enumerate_all(vari, extended(e_v, (y_i, 'T'))) +
                    (1 - self.net()[y_i].cpt()[tuple(key)])*self.enumerate_all(vari, extended(e_v, (y_i, 'F'))))

    def enumeration_ask(self, x_v, e_vidence):
        """input a node = T and evidence return probability
        """
        q_uery = {}
        for xval in ['T', 'F']:
            q_uery[xval] = self.enumerate_all(self.vars(), extended(e_vidence, (x_v, xval)))
        return normalize(q_uery)

def normalize(dic):
    """normalize distribution with sum 1,return P(node = T)
    """
    s_um = 0
    for key in dic.keys():
        s_um += dic[key]
    for key in dic.keys():
        dic[key] = dic[key]/s_um
    return dic['T']

def extended(e_v, x_v):
    """extend evidence with node x = T of F
    """
    newe_v = copy.deepcopy(e_v)
    #tuple
    newe_v[x_v[0]] = x_v[1]
    return newe_v

def tf_val(symbol, val):
    """return probability  of T or F
    """
    if symbol == 'T':
        return val
    return 1 - val

def graphnode(graph, line_whole):
    """add node to the graph according bn.txt
    """
    line_s = line_whole.strip().split(',')
    for node in line_s:
        node = node.strip()
        graph[node] = Node(node)
def graphedge(graph, line_whole):
    """add edge to the graph according bn.txt
    """
    line_s = line_whole.strip().split(',')
    (v_1, v_2) = line_s
    v_1, v_2 = v_1.strip(), v_2.strip()
    graph[v_2].add_parent(v_1)

def updatecpt(b_n, graph, line_whole):
    """update cpt to the node in the graph according bn.txt
    """
    key = line_whole[2]
    if key not in b_n.nset():
        b_n.add_nset(key)
        b_n.add_var(key)
    tup = ['']*len(graph[key].parents())
    for i in range(5, len(line_whole)):
        if line_whole[i] == 'T' or line_whole[i] == 'F':
            idx = graph[key].parents().index(line_whole[i-2])
            tup[idx] = line_whole[i]
        if line_whole[i] == ')':
            variable = float(str(line_whole[i+2:]))
            break
    graph[key].update_cpt(tuple(tup), variable)

def tuples(val):
    """return conbination of T and F
    """
    def dfs(result, tup, val):
        """in a dfs style
        """
        if val == 0:
            result.append(tup)
        if val > 0:
            dfs(result, tup+['F'], val-1)
            dfs(result, tup+['T'], val-1)
        return result
    result = []
    tup = []
    r_e = {}
    dfs(result, tup, val)
    for seq in result:
        r_e[tuple(seq)] = 0
    return r_e

def cptinitialize(graph):
    """initailize cpt of each nodes
    """
    for key in graph.keys():
        if graph[key].parents() == []:
            graph[key].add_cpt(0)
        else:
            graph[key].add_cpt(tuples(len(graph[key].parents())))

if __name__ == '__main__':
    INPUT_PATH = 'bn.txt'
    BN = BayesNet()
    BN_GRAPH = {}
    with open(INPUT_PATH, 'r') as f:
        COUNT = 0
        for line in f:
            if line[0] == '%':
                COUNT += 1
                continue
            if  COUNT == 1:
                graphnode(BN_GRAPH, line)
            if  COUNT == 2:
                graphedge(BN_GRAPH, line)
            if  COUNT == 3:
                cptinitialize(BN_GRAPH)
                COUNT += 1
            if  COUNT == 4:
                updatecpt(BN, BN_GRAPH, line)

    BN.add_net(BN_GRAPH)
    INPUT_PATH = 'input.txt'
    with open(INPUT_PATH, 'r') as f:
        COUNT = 0
        for line in f:
            if line[0] == '%':
                COUNT += 1
                continue
            if  COUNT == 1:
                Q = line[0]
            if  COUNT == 2:
                line = line.strip()
                E = {}
                if line != '':
                    line_split = line.strip().split(',')
                    for item in line_split:
                        item = item.split()
                        #print(item)
                        E[item[0][0]] = item[0][2]

        print('Given evidence:')
        print(E)
        print('The probability of Node ' + str(Q) + ' is:')
        print(BN.enumeration_ask(Q, E))

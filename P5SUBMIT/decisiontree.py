"""Bayesnet
Implement decision tree generation algorithm,
branch is detemined by best informaiton gain
input:examples.txt
output:dtree.txt
"""
import math
class TreeNode(object):
    """ TreeNode class
    """
    def __init__(self, attribute=None):
        """initialze a decision tree node
        """
        self.__attribute = attribute[0]
        self.__values = attribute[1::]
        self.__branch = {}

    def add_branch(self, label, subtree):
        """add branch with label and subtree
        """
        self.__branch[label] = subtree

    def attribute(self):
        """return attribute name
        """
        return self.__attribute
    def branch(self):
        """return branch
        """
        return self.__branch


def pluralityvalue(examples):
    """return the plurality outcome
    """
    dic = {}
    for item in examples:
        if item['outcome'] in dic.keys():
            dic[item['outcome']] += 1
        else:
            dic[item['outcome']] = 1
    re_turn = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    return re_turn[0][0]

def examples_check(examples):
    """check whether examples have mutiple outcomes
    """
    lst = []
    re_turn = True
    for item in examples:
        if item['outcome'] not in lst and len(lst) == 1:
            re_turn = False
            break
        else:
            lst.append(item['outcome'])
    return re_turn

def importance(attributes, examples, decisionval):
    """return the most important attribute according to information gain
    """
    def infomation(val):
        """compute according to formula
        """
        return -val*(math.log(val, 2))
    def dicinitialize(dictt):
        """initialize dictionary
        """
        for de_val in decisionval:
            dictt[de_val] = float(0)
    dic = {}
    dicinitialize(dic)
    total_all = float(len(examples))
    for item in examples:
        dic[item['outcome']] += 1

    info = 0
    for dickey in dic:
        val = dic[dickey]/total_all
        if val != 0:
            info += infomation(val)
    info_g = {}
    for i in range(len(attributes)):
        name = attributes[i][0]
        reminder = float(0)
        attr_dic = {}
        info_g[name] = float(0)
        for val in attributes[i][1::]:
            attr_dic[val] = {}
            total = float(0)
            dicinitialize(attr_dic[val])
            for item in examples:
                if item[name] == val:
                    attr_dic[val][item['outcome']] += 1
                    total += 1
            for keydic in attr_dic[val].keys():
                if attr_dic[val][keydic] != 0:
                    reminder += (total/total_all)*infomation(attr_dic[val][keydic]/total)
        info_g[name] = info - reminder

    sortedval = sorted(info_g.values(), reverse=True)
    maxval = sortedval[0]
    for attribute in attributes:
        if info_g[attribute[0]] == maxval:
            return attribute

def dtree_learning(examples, attributes, parent_examples, decisionval):
    """ examples: list of examples
        attributes: list of tuple
        parent_examples: list of dictinaries including all examples
        output:decision tree instance
    """
    if not examples:
        return pluralityvalue(parent_examples)
    elif examples_check(examples):
        return examples[0]['outcome']
    elif not attributes:
        return pluralityvalue(examples)
    else:
        attr = importance(attributes, examples, decisionval)
    tree = TreeNode(attr)
    attributes.remove(attr)
    for value in attr[1::]:
        exs = []
        for example in examples:
            if example[attr[0]] == value:
                exs.append(example)
        subtree = dtree_learning(exs, attributes, examples, decisionval)
        tree.add_branch(value, subtree)
    return tree


def attribute_initialize(attributes, line_w):
    """initialize attributes list
    """
    line_s = line_w.strip().split(':')
    attribute = (line_s[0], )
    line_val = line_s[1].strip().split(',')
    for val in line_val:
        attribute += (val.strip(), )
    attributes.append(attribute)

def decisionval_initialize(decisionval, line_w):
    """initialize decisionval list
    """
    line_s = line_w.strip().split(',')
    for val in line_s:
        decisionval.append(val.strip())

def examples_initialize(attr, examples, line_w):
    """initialize examples dictionary
    """
    line_s = line_w.strip().split(',')
    example = {}
    for i in range(len(attr)):
        example[attr[i][0]] = line_s[i].strip()
    example['outcome'] = line_s[-1].strip()
    examples.append(example)


if __name__ == '__main__':
    INPUT_PATH = 'examples.txt'
    ATTRS = []
    DECISIONVAL = []
    EXAMPLES = []
    with open(INPUT_PATH, 'r') as f:
        COUNT = 0
        for line in f:
            if line[0] == '%':
                COUNT += 1
                continue
            elif COUNT == 1:
                attribute_initialize(ATTRS, line)
            elif COUNT == 2:
                decisionval_initialize(DECISIONVAL, line)
            elif COUNT == 4:
                examples_initialize(ATTRS, EXAMPLES, line)
    ROOT = dtree_learning(EXAMPLES, ATTRS, EXAMPLES, DECISIONVAL)



    OUTPUT_PATH = 'dtree.txt'
    with open(OUTPUT_PATH, 'w+') as f:
        f.write("%"+" Format: decision? value, next node (leaf value or next decision?)"+'\n')
        f.write("%"+" Use question mark and comma markers as indicated below."+'\n')

        FRONTIER = [ROOT]
        while FRONTIER:
            CURRENT = FRONTIER.pop(0)
            for key in CURRENT.branch().keys():
                if type(CURRENT.branch()[key]) is TreeNode:
                    f.write(str(CURRENT.attribute())+'? '+str(key)+', '+ \
                        CURRENT.branch()[key].attribute()+'\n')
                    FRONTIER.append(CURRENT.branch()[key])
                else:
                    f.write(str(CURRENT.attribute())+'? '+str(key)+', '+CURRENT.branch()[key]+'\n')

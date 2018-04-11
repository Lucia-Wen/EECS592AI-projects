"""tsp

This module read tsp.txt file to print solution desecibed in spec.

"""
import math
import mysearch as m
if __name__ == '__main__':
    INPUT_PATH = 'tsp.txt'
    try:
        with open(INPUT_PATH, 'r') as f:
            INPUT_ = []
            for line in f:
                line = line.strip()
                INPUT_.append(line)
            print('problem:  '+str(INPUT_))
            ORIGIN = INPUT_[0]
            DESTI = None
            OPTION = INPUT_[1]
        MYGRAPH = {}
        INFO = [["Ann Arbor", "Brighton", 19.2],
                ["Ann Arbor", "Plymouth", 17.2],
                ["Ann Arbor", "Romulus", 23.1],
                ["Brighton", "Farmington Hills", 21.4],
                ["Brighton", "Pontiac", 34.1],
                ["Plymouth", "Romulus", 23.1],
                ["Plymouth", "Farmington Hills", 14.0],
                ["Plymouth", "Detroit", 27.9],
                ["Romulus", "Detroit", 31.0],
                ["Farmington Hills", "Royal Oak", 16.9],
                ["Farmington Hills", "Detroit", 28.3],
                ["Farmington Hills", "Pontiac", 15.5],
                ["Pontiac", "Sterling Heights", 17.2],
                ["Pontiac", "Royal Oak", 13.3],
                ["Romeo", "Pontiac", 27.8],
                ["Romeo", "Sterling Heights", 16.5]]
        for item in INFO:
            v1, v2, distance = item[0], item[1], item[2]
            if v1 not in MYGRAPH:
                MYGRAPH[v1] = {}
                MYGRAPH[v1][v2] = distance
            else:
                MYGRAPH[v1][v2] = distance
            if v2 not in MYGRAPH:
                MYGRAPH[v2] = {}
                MYGRAPH[v2][v1] = distance
            else:
                MYGRAPH[v2][v1] = distance
        INFO2 = [["Ann Arbor", 42.280826, -83.743038],
                 ["Brighton", 42.529477, -83.780221],
                 ["Detroit", 42.331427, -83.045754],
                 ["Farmington Hills", 42.482822, -83.418382],
                 ["Plymouth", 42.37309, -83.50202],
                 ["Pontiac", 42.638922, -83.291047],
                 ["Romeo", 42.802808, -83.012987],
                 ["Romulus", 42.24115, -83.612994],
                 ["Royal Oak", 42.48948, -83.144648],
                 ["Sterling Heights", 42.580312, -83.030203]]
        GRAPH2 = {}
        R = 3959
        FACTOR = math.pi/180
        for item in INFO2:
            for item2 in INFO2:
                v1, v2 = item[0], item2[0]
                phi, theta = item[1]*FACTOR, item[2]*FACTOR
                phi2, theta2 = item2[1]*FACTOR, item2[2]*FACTOR
                x = math.cos(phi) * math.cos(theta) * R
                y = math.cos(phi) * math.sin(theta) * R
                z = math.sin(phi) * R # z is 'up'
                x2 = math.cos(phi2) * math.cos(theta2) * R
                y2 = math.cos(phi2) * math.sin(theta2) * R
                z2 = math.sin(phi2) * R # z is 'up'
                delta_x, delta_y, delta_z = x2-x, y2-y, z2-z
                distance = round(math.sqrt(delta_x**2+delta_y**2+delta_z**2), 1)
                if v1 not in GRAPH2:
                    GRAPH2[v1] = {}
                    GRAPH2[v1][v2] = distance
                else:
                    GRAPH2[v1][v2] = distance
                if v2 not in GRAPH2:
                    GRAPH2[v2] = {}
                    GRAPH2[v2][v1] = distance
                else:
                    GRAPH2[v2][v1] = distance
        i = 0
        HASHING = {}
        HASHING2 = {}
        for key in GRAPH2.keys():
            HASHING[key] = i
            HASHING2[i] = key
            i += 1
        PROBLEM = 'TSP'
        SOLUTION = m.mysearch(MYGRAPH, ORIGIN, DESTI, OPTION, GRAPH2, HASHING, HASHING2, None, PROBLEM)
        if not SOLUTION is False:
            print('Total Nodes Expanded:  ' + str(SOLUTION.expanded_num()))
            print('Solution Path:  '+str(SOLUTION.path()))
            print('Total Solution Cost:  '+str(SOLUTION.cost()))
        else:
            print('fail')
    except:
        print('tsp.txt not found')

1.General Search Code:

To use general search, you should import mysearch.py and pass parameters for mysearch function.

mysearch(graph, origin, destination, option, graph2=None, hashing=None, hashing2=None, i_limit=None, problem=None)

Parameters:

graph is route information, for example, route planning graph from Southern Michigan.

origin is both origins for route planning problem and tsp.

destination only works in route planning. For tsp, simply pass None.

option decides search strategies including DFS, BFS, iterative deepening, Uniform and A* corresponding to D, B, I, U and A.

graph2 only used for A* for both problems.For Southern Michigan problem, graph2 contains straight-line distance of cities.

hashing and hashing2 are used in tsp problem to encode cities' names to formulate path, which will be explained in 3.TSP.

i_limit is customized depth limit for iterative deepening, the default setting is same with depth_limit = 30.

problem specifies problem domain including 'route planning' and 'TSP'.The default setting is 'route planning'


For route planning, requires to specify: mysearch(MYGRAPH, ORIGIN, DESTI, OPTION, GRAPH2)

For TSP,requires to specify:mysearch(MYGRAPH, ORIGIN, None, OPTION, GRAPH2, HASHING, HASHING2, None, 'TSP')

2.route planning

command:
python routeplanning.py
Requires route.txt
After this command,number of nodes expanded, path and total cost will be printed.


3.TSP

command:
python tsp.py
Requires tsp.txt
After this command,number of nodes expanded, path and total cost will be printed.

In this problem, I define state as searched path and current city stored in Node.path and Node.state.
Path is a list of number including 0, 1 and 2. 0 represents cites unvisted, 1 represnets cities visited and 2 represents current city.
HASHING is used to encode these cities to ensure position in path. For exmaple,HASHING = 
{'Pontiac': 0, 'Plymouth': 9, 'Detroit': 7, 'Romeo': 1, 'Farmington Hills': 3, 'Romulus': 5, 'Sterling Heights': 4, 'Royal Oak': 6, 'Ann Arbor': 8, 'Brighton': 2}

while HASHING2 = 
{0: 'Pontiac', 1: 'Romeo', 2: 'Brighton', 3: 'Farmington Hills', 4: 'Sterling Heights', 5: 'Romulus', 6: 'Royal Oak', 7: 'Detroit', 8: 'Ann Arbor', 9: 'Plymouth'}

Goal checking is to check no 0 in this list,which means no unvisited cities left.

HEURISTIC FUNTION: Sum of distance from unvisted cities to their nearest cities. This heuristic is admissable because distance to nearest city is always the best senario to reach left cities, and leads to visiting new cities.
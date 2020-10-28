"""
The Kevin Bacon Game.

Replace "pass" with your code.
"""

import simpleplot
import comp140_module4 as movies
from collections import defaultdict

class Queue:
    """
    A simple implementation of a FIFO queue.
    """

    def __init__(self):
        """
        Initialize the queue.
        """
        # I will use a list as a base DS to represent queue
        # initially the queue will be empty, so que will be empty 
        self._items = []
        
    def __len__(self):
        """
        Returns: an integer representing the number of items in the queue.
        """
        # The length of queue is equal to that of list
        return len(self._items)

    def __str__(self):
        """
        Returns: a string representation of the queue.
        """
        ### print the elements of list from Left to Right: 
        ### from earliest to lastest
        strep = ""
        for ele in self._items:
            strep += str(ele)+" "
        return strep

    def push(self, item):
        """
        Add item to the queue.

        input:
            - item: any data type that's valid in a list
        """
        # add the item to the end of list
        self._items.append(item)

    def pop(self):
        """
        Remove the least recently added item.

        Assumes that there is at least one element in the queue.  It
        is an error if there is not.  You do not need to check for
        this condition.

        Returns: the least recently added item.
        """
        # pop the first element in the list
        return self._items.pop(0)

    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items.clear()


def bfs(graph, start_node):
    """
    Performs a breadth-first search on graph starting at the
    start_node.

    inputs:
        - graph: a graph object
        - start_node: a node in graph representing the start node

    Returns: a two-element tuple containing a dictionary
    associating each visited node with the order in which it
    was visited and a dictionary associating each visited node
    with its parent node.
    """
    ### initialize two empty dictionaries to for later return
    dis = defaultdict(int)
    parent = defaultdict(str)
    
    ### preperation 
    # obtain a list of nodes
    nodes = graph.nodes()
    # set dis of nodes to infinity, set all of the parents to none
    for node in nodes:
        dis[node] = float("inf")
        parent[node] = None

    ### start implementing the BFS
    # initialize an empty queue
    queue = Queue()
    queue.push(start_node)
    print(queue)
    dis[start_node] = 0
    
    while len(queue) != 0:
        node = queue.pop()
        neighbors = graph.get_neighbors(node)
        for neighbor in neighbors:
            if dis[neighbor] == float("inf"):
                dis[neighbor] = dis[node] + 1
                queue.push(neighbor)
                parent[neighbor] = node
        
    return dis, parent 


def distance_histogram(graph, node):
    """
    Computes the distance between the given node and all other
    nodes in that graph and creates a histogram of those distances.

    inputs:
        - graph: a graph object
        - node: a node in graph

    returns: a dictionary mapping each distance with the number of
    nodes that are that distance from node.
    """
    # obtain the distance mapping from the start_node to every node
    dis = bfs(graph, node)[0]
    # create a defaultdict to store the frequency of distances
    res = defaultdict(int)
    # parse the distance dictionary
    for value in dis.values():
        res[value] += 1

    return res

def find_path(graph, start_person, end_person, parents):
    """
    Computes the path from start_person to end_person in the graph.

    inputs:
        - graph: a graph oject with edges representing the connections between people
        - start_person: a node in graph representing the starting node
        - end_person: a node in graph representing the ending node
        - parents: a dictionary representing the parents in the graph

    returns a list of tuples of the path in the form:
        [(actor1, {movie1a, ...}), (actor2, {movie2a, ...}), ...]
    """
    # initilize an empty list to contain results for later return
    res = []
    
    if start_person == end_person:
        res.append((start_person, set()))
        return res
    # obtain the parent mapping from start_node to every other nodes
    # parents = bfs(graph, start_person)[1] already in parameter
    
    if parents[a] != None:
        res.append((end_person, set()))
        child = end_person
        paren = parents[child]
    else:
        return []

    # while the parent is not start_node continue the loop
    while paren != start_person and child != None:
        res.insert(0, (paren, graph.get_attrs(paren, child)))
        child = paren
        if parents[child] == None:
            return []
        paren = parents[child]
    
    res.insert(0, (start_person, graph.get_attrs(paren, child)))
    return res


def play_kevin_bacon_game(graph, start_person, end_people):
    """
    Play the "Kevin Bacon Game" on the actors in the given
    graph.

    inputs:
        - graph: a a graph oject with edges representing the connections between people
        - start_person: a node in graph representing the node from which the search will start
        - end_people: a list of nodes in graph to which the search will be performed

    Prints the results out.
    """
    # obtain the parent mapping from start_node to every other nodes
    parents = bfs(graph, start_person)[1]
    # loop over the end_people
    for des in end_people:
        print(movies.print_path(graph, start_person, des, parents))

def run():
    """
    Load a graph and play the Kevin Bacon Game.
    """
    graph5000 = movies.load_graph('subgraph5000')

    if len(graph5000.nodes()) > 0:
        # You can/should use smaller graphs and other actors while
        # developing and testing your code.
        play_kevin_bacon_game(graph5000, 'Kevin Bacon', ['Amy Adams', 
                                                         'Andrew Garfield', 
                                                         'Anne Hathaway', 
                                                         'Barack Obama', 
                                                         'Benedict Cumberbatch', 
                                                         'Chris Pine', 
                                                         'Daniel Radcliffe', 
                                                         'Jennifer Aniston', 
                                                         'Joseph Gordon-Levitt', 
                                                         'Morgan Freeman', 
                                                         'Sandra Bullock', 'Tina Fey'])

        # Plot distance histograms
        for person in ['Kevin Bacon', 'Stephanie Fratus']:
            hist = distance_histogram(graph5000, person)
            simpleplot.plot_bars(person, 400, 300, 'Distance', \
                'Frequency', [hist], ["distance frequency"])

# Uncomment the call to run below when you have completed your code.

run()
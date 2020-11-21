"""
Map Search
"""

import comp140_module7 as maps
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


class Stack:
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
        return self._items.pop()

    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items.clear()


def bfs_dfs(graph, rac_class, start_node, end_node):
    """
    Performs a breadth-first search or a depth-first search on graph
    starting at the start_node.  The rac_class should either be a
    Queue class or a Stack class to select BFS or DFS.

    Completes when end_node is found or entire graph has been
    searched.

    inputs:
        - graph: a directed Graph object representing a street map
        - rac_class: a restricted access container (Queue or Stack) class to
          use for the search
        - start_node: a node in graph representing the start
        - end_node: a node in graph representing the end

    Returns: a dictionary associating each visited node with its parent
    node.
    """
    ### initialize two empty dictionaries to for later return
    dis = defaultdict(int)
    parent = {}
    
    ### preperation 
    # obtain a list of nodes
    nodes = graph.nodes()
    # set dis of nodes to infinity, set all of the parents to none
    for node in nodes:
        dis[node] = float("inf")
        parent[node] = None

    ### start implementing the DFS
    # initialize an empty stack
    stack = rac_class()
    stack.push(start_node)
    #print(stack)
    dis[start_node] = 0
    
    while len(stack) != 0:
        node = stack.pop()
        neighbors = graph.get_neighbors(node)
        for neighbor in neighbors:
            if dis[neighbor] == float("inf"):
                dis[neighbor] = dis[node] + 1
                stack.push(neighbor)
                parent[neighbor] = node
            if neighbor == end_node:
                return parent
        
    return parent 


def dfs(graph, start_node, end_node, parent):
    """
    Performs a recursive depth-first search on graph starting at the
    start_node.

    Completes when end_node is found or entire graph has been
    searched.

    inputs:
        - graph: a directed Graph object representing a street map
        - start_node: a node in graph representing the start
        - end_node: a node in graph representing the end
        - parent: a dictionary that initially has one entry associating
                  the original start_node with None

    Returns: the modified parent dictionary which maps each visited node
    to its parent node
    """
    if start_node == end_node:
        return parent
    else:
        for neighbor in graph.get_neighbors(start_node):
            if neighbor not in parent:
                parent[neighbor] = start_node
                dfs(graph, neighbor, end_node, parent)
    
    return parent

def astar(graph, start_node, end_node,
          edge_distance, straight_line_distance):
    """
    Performs an A* search on graph starting at start_node.

    Completes when end_node is found or entire graph has been
    searched.

    inputs:
        - graph: a directed Graph object representing a street map
        - start_node: a node in graph representing the start
        - end_node: a node in graph representing the end
        - edge_distance: a function which takes two nodes and a graph
                         and returns the actual distance between two
                         neighboring nodes
        - straight_line_distance: a function which takes two nodes and
                         a graph and returns the straight line distance 
                         between two neighboring nodes

    Returns: a dictionary associating each visited node with its parent
    node.
    """

    # the result that will be returned eventually
    parent = {}
    parent[start_node] = None

    # initialize the open set and closed set both of which contains node #
    ope_set = []
    clo_set = []
    # append the starting node to the open set
    ope_set.append(start_node)

    # g value
    gv_re = {}
    # the g value of the starting node is zero
    gv_re[start_node] = 0

    # if the open set is empty, terminate the searching
    while len(ope_set) != 0:
        # choose current node to explore
        node = -1

        # the initilal case where there is only start_node
        if len(ope_set) == 1 and ope_set[0] == start_node:
            node = ope_set[0]

        # find the node with smallest f value within the open_set
        else:
            # sentenal f cost
            sen_fv = float("inf")
            # sentinal node
            sen_no = float("inf")

            for node in ope_set:  
                # the g value
                g_val = gv_re[node]
                # the h value
                h_val = straight_line_distance(node, end_node, graph)
                # the f value
                f_val = g_val + h_val
                # compare them to the sentinal value
                if f_val < sen_fv:
                    sen_fv = f_val
                    sen_no = node

            node = sen_no

        # if we will visit the target node, then return parent
        if node == end_node:
            return parent

        # we now know the node with least amount of f value in the openset
        ope_set.remove(node)
        clo_set.append(node)

        # explore its neighbors
        for neighbor in graph.get_neighbors(node):
            if neighbor not in clo_set:
                if neighbor not in ope_set:
                    ope_set.append(neighbor)
                    gv_re[neighbor] = gv_re[node] + edge_distance(node, neighbor, graph)
                    parent[neighbor] = node
                else:
                    # if the cost is lower then update
                    if gv_re[neighbor] > gv_re[node] + edge_distance(node, neighbor, graph):
                        gv_re[neighbor] = gv_re[node] + edge_distance(node, neighbor, graph)
                        parent[neighbor] = node

    return parent

# You can replace functions/classes you have not yet implemented with
# None in the call to "maps.start" below and the other elements will
# work.

maps.start(bfs_dfs, Queue, Stack, dfs, astar)
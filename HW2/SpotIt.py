"""
Code to implement the game of Spot it!

http://www.blueorangegames.com/spotit/

For each function, replace the return statement with your code.  Add
whatever helper functions you deem necessary.
"""

import comp140_module2 as spotit

def equivalent(point1, point2, mod):
    """
    Determines if the two given points are equivalent in the projective
    geometric space in the finite field with the given modulus.

    Each input point, point1 and point2, must be valid within the
    finite field with the given modulus.

    inputs:
        - point1: a tuple of 3 integers representing the first point
        - point2: a tuple of 3 integers representing the second point
        - mod: an integer representing the modulus

    returns: a boolean indicating whether or not the points are equivalent
    """
    
    ### find the x y z coordinate of first point with mod operation
    point1_x = point1[0] % mod
    point1_y = point1[1] % mod
    point1_z = point1[2] % mod
    
    ### find the x y z coordinate of second point with mod operation
    point2_x = point2[0] % mod
    point2_y = point2[1] % mod
    point2_z = point2[2] % mod
    
    ### find the cross product of two points with mod operation
    kone = (point1_y * point2_z - point1_z * point2_y) % mod
    ktwo = (point1_z * point2_x - point1_x * point2_z) % mod
    kthr = (point1_x * point2_y - point1_y * point2_x) % mod
    
    ### check whether two points are equivalent using [k1,k2,k3]=[0,0,0]
    return kone == 0 and kone == ktwo and ktwo == kthr

def incident(point, line, mod):
    """
    Determines if a point lies on a line in the projective
    geometric space in the finite field with the given modulus.

    The inputs point and line must be valid within the finite field
    with the given modulus.

    inputs:
        - point: a tuple of 3 integers representing a point
        - line: a tuple of 3 integers representing a line
        - mod: an integer representing the modulus

    returns: a boolean indicating whether or not the point lies on the line
    """
    
    ### find the x y z coordinates of the point
    point_x = point[0] % mod
    point_y = point[1] % mod
    point_z = point[2] % mod
    
    ### find the x y z coordinate of the line
    line_x = line[0] % mod
    line_y = line[1] % mod
    line_z = line[2] % mod
    
    ### find whether the point is on line or not using the fomulat with mod operation
    res = (point_x * line_x + point_y * line_y + point_z * line_z) % mod
    
    return res == 0

### This is a helper function to subdivide the task and find all the possible 
### coordinate of the point using combination and permutation and recursive backtracking
def hlp(res, mod):
    """
    Generate all the possible points to be checked
    
    inputs:
        - res: an empty list to put points into
        - mod: an integer representing the modulus
        
        Returns: recursively defined to generate all points
    """
    ### I will need another list cur to contain all the current state point
    def permutate(res, cur, mod):
        ### if the list cur already has three elements, push it into res
        if len(cur) == 3:
            res.append(cur)
        else:
            ### using for loop to parse through all possible choices
            for i_r in range(mod):
                ### since python list is passed by reference I need to make a copy
                ### instead of pop the original list
                b_n = cur[:]
                ### choose one currently available choice
                b_n.append(i_r)
                ### explore possible choices
                permutate(res, b_n, mod)
                c_n = b_n[:]
                ### backtracking: pop the last element to contain a new choice
                c_n.pop()
    ### call the inner function at the end
    return permutate(res, [], mod)


def generate_all_points(mod):
    """
    Generate all unique points in the projective geometric space in
    the finite field with the given modulus.

    inputs:
        - mod: an integer representing the modulus

    Returns: a list of unique points, each is a tuple of 3 elements
    """    
    ### use an empty list to contain all possible points
    res = []
    ### use helper function find all possible points
    hlp(res, mod)
    ### pop off the first [0,0,0] because it is not valid to be a point
    res.pop(0)
    ### use points to contain the result unique points
    points = []
    ### parse to find if the point is unqie then add it
    for lst in res:
        ### find the coordinates of the point
        cor_x = lst[0]
        cor_y = lst[1]
        cor_z = lst[2]
        ### make point as a tuple and assume that point doesn't exist
        point = (cor_x, cor_y, cor_z)
        already_exist = False
        ### parse all previous points if it already exist an equivalent one
        ### don't add otherwise add it
        for ele in points:
            if equivalent(point, ele, mod):
                print(ele, point, mod)
                already_exist = True
                break
        if not already_exist:
            points.append(point)

    return points

def create_cards(points, lines, mod):
    """
    Create a list of unique cards.

    Each point and line within the inputs, points and lines, must be
    valid within the finite field with the given modulus.

    inputs:
        - points: a list of unique points, each represented as a tuple of 3 integers
        - lines: a list of unique lines, each represented as a tuple of 3 integers
        - mod: an integer representing the modulus

    returns: a list of lists of integers, where each nested list represents a card.
    """
    ### use an empty res to contain all the cards
    res = []
    ### parse through the lines and points to find whether a point is on 
    ### the current line. If so, then add to the cur list, otherwise don't
    for line in lines:
        cur = []
        for point_index in range(len(points)):
            if incident(points[point_index], line, mod):
                cur.append(point_index)
        res.append(cur)
    return res

def run():
    """
    Create the deck and play the game.
    """
    # Prime modulus
    # Set to 2 or 3 during development
    # Set to 7 for the actual game
 
    modulus = 2

    # Generate all unique points for the given modulus
    points = generate_all_points(modulus)
    
    # Lines are the same as points, so make a copy
    lines = points[:]
    
    # Generate a deck of cards given the points and lines
    deck = create_cards(points, lines, modulus)

    # Run GUI - uncomment the line below after you have implemented
    #           everything and you can play your game.  The GUI does
    #           not work if the modulus is larger than 7.

    spotit.start(deck)

# Uncomment the following line to run your game (once you have
# implemented the run function.)

run()

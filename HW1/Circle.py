"""
Code to calculate the circle that passes through three given points.

Fill in each function with your code (including fixing the return
statement).
"""

import math
import comp140_module1 as circles

def distance(point0x, point0y, point1x, point1y):
    """
    Computes the distance between two points.

    inputs:
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point

    returns: a float that is the distance between the two points
    """
    x_distance = math.fabs(point0x-point1x)
    y_distance = math.fabs(point0y-point1y)
    
    return math.sqrt(x_distance**2+y_distance**2)

def midpoint(point0x, point0y, point1x, point1y):
    """
    Computes the midpoint between two points.

    inputs:
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point

    returns: two floats that are the x- and y-coordinates of the midpoint
    """
    x_coordinate = (point0x+point1x)/2
    y_coordinate = (point0y+point1y)/2
    return x_coordinate, y_coordinate

def slope(point0x, point0y, point1x, point1y):
    """
    Computes the slope of the line that connects two given points.

    The x-values of the two points, point0x and poin1x, must be different.

    inputs:
        -point0x: a float representing the x-coordinate of the first point.
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point.
        -point1y: a float representing the y-coordinate of the second point

    returns: a float that is the slope between the points
    """
    rise = point1y - point0y
    run = point1x - point0x
    slo = rise/run
    return slo

def perp(lineslope):
    """
    Computes the slope of a line perpendicular to a given slope.

    input:
        -lineslope: a float representing the slope of a line.
                    Must be non-zero

    returns: a float that is the perpendicular slope
    """
    per_slope = -1 * (1/lineslope)
    return per_slope

def intersect(slope0, point0x, point0y, slope1, point1x, point1y):
    """
    Computes the intersection point of two lines.

    The two slopes, slope0 and slope1, must be different.

    inputs:
        -slope0: a float representing the slope of the first line.
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -slope1: a float representing the slope of the second line.
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point

    returns: two floats that are the x- and y-coordinates of the intersection
    point
    """
    x_coordinate = (point1y-point0y+slope0*point0x-slope1*point1x)/(slope0-slope1)
    y_coordinate = slope0*x_coordinate+point0y-slope0*point0x
    return x_coordinate, y_coordinate

def make_circle(point0x, point0y, point1x, point1y, point2x, point2y):
    """
    Computes the center and radius of a circle that passes through
    thre given points.

    The points must not be co-linear and no two points can have the
    same x or y values.

    inputs:
        -point0x: a float representing the x-coordinate of the first point
        -point0y: a float representing the y-coordinate of the first point
        -point1x: a float representing the x-coordinate of the second point
        -point1y: a float representing the y-coordinate of the second point
        -point2x: a float representing the x-coordinate of the third point
        -point2y: a float representing the y-coordinate of the third point

    returns: three floats that are the x- and y-coordinates of the center
    and the radius
    """
    a_ab_slope = slope(point0x, point0y, point1x, point1y)
    a_ac_slope = slope(point0x, point0y, point2x, point2y)
    a_bc_slope = slope(point1x, point1y, point2x, point2y)
    
    aax, aay = intersect(a_ab_slope, point0x, point0y, a_ac_slope, point2x, point2y)
    abx, aby = intersect(a_ab_slope, point0x, point0y, a_bc_slope, point1x, point1y)
    acx, acy = intersect(a_ac_slope, point0x, point0y, a_bc_slope, point2x, point2y)

    axx, axy = midpoint(aax, aay, abx, aby)
    ayx, ayy = midpoint(acx, acy, abx, aby)
    
    axs = perp(a_ab_slope)
    ays = perp(a_bc_slope)
    
    center_x, center_y = intersect(axs, axx, axy, ays, ayx, ayy)
    
    radius = distance(center_x, center_y, aax, aay)
    
    return center_x, center_y, radius

# Run GUI - uncomment the line below after you have
#           implemented make_circle
#circles.start(make_circle)

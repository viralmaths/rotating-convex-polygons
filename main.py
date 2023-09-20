import pygame as py
import numpy as np
from matplotlib import pyplot as plt
import warnings


# Points need to be presented or otherwise it won't work
class PolygonClipper:

    def __init__(self, warn_if_empty=True):
        self.warn_if_empty = warn_if_empty

    def is_inside(self, p1, p2, q):
        R = (p2[0] - p1[0]) * (q[1] - p1[1]) - (p2[1] - p1[1]) * (q[0] - p1[0])
        if R <= 0:
            return True
        else:
            return False

    def compute_intersection(self, p1, p2, p3, p4):

        """
        given points p1 and p2 on line L1, compute the equation of L1 in the
        format of y = m1 * x + b1. Also, given points p3 and p4 on line L2,
        compute the equation of L2 in the format of y = m2 * x + b2.

        To compute the point of intersection of the two lines, equate
        the two line equations together

        m1 * x + b1 = m2 * x + b2

        and solve for x. Once x is obtained, substitute it into one of the
        equations to obtain the value of y.

        if one of the lines is vertical, then the x-coordinate of the point of
        intersection will be the x-coordinate of the vertical line. Note that
        there is no need to check if both lines are vertical (parallel), since
        this function is only called if we know that the lines intersect.
        """

        # if first line is vertical
        if p2[0] - p1[0] == 0:
            x = p1[0]

            # slope and intercept of second line
            m2 = (p4[1] - p3[1]) / (p4[0] - p3[0])
            b2 = p3[1] - m2 * p3[0]

            # y-coordinate of intersection
            y = m2 * x + b2

        # if second line is vertical
        elif p4[0] - p3[0] == 0:
            x = p3[0]

            # slope and intercept of first line
            m1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
            b1 = p1[1] - m1 * p1[0]

            # y-coordinate of intersection
            y = m1 * x + b1

        # if neither line is vertical
        else:
            m1 = (p2[1] - p1[1]) / (p2[0] - p1[0])
            b1 = p1[1] - m1 * p1[0]

            # slope and intercept of second line
            m2 = (p4[1] - p3[1]) / (p4[0] - p3[0])
            b2 = p3[1] - m2 * p3[0]

            # x-coordinate of intersection
            x = (b2 - b1) / (m1 - m2)

            # y-coordinate of intersection
            y = m1 * x + b1

        intersection = (x, y)

        return intersection

    def clip(self, subject_polygon, clipping_polygon):

        final_polygon = subject_polygon.copy()

        for i in range(len(clipping_polygon)):

            # stores the vertices of the next iteration of the clipping procedure
            next_polygon = final_polygon.copy()

            # stores the vertices of the final clipped polygon
            final_polygon = []

            # these two vertices define a line segment (edge) in the clipping
            # polygon. It is assumed that indices wrap around, such that if
            # i = 1, then i - 1 = K.
            c_edge_start = clipping_polygon[i - 1]
            c_edge_end = clipping_polygon[i]

            for j in range(len(next_polygon)):
                # these two vertices define a line segment (edge) in the subject
                # polygon
                s_edge_start = next_polygon[j - 1]
                s_edge_end = next_polygon[j]

                if self.is_inside(c_edge_start, c_edge_end, s_edge_end):
                    if not self.is_inside(c_edge_start, c_edge_end, s_edge_start):
                        intersection = self.compute_intersection(s_edge_start, s_edge_end, c_edge_start, c_edge_end)
                        final_polygon.append(intersection)
                    final_polygon.append(tuple(s_edge_end))
                elif self.is_inside(c_edge_start, c_edge_end, s_edge_start):
                    intersection = self.compute_intersection(s_edge_start, s_edge_end, c_edge_start, c_edge_end)
                    final_polygon.append(intersection)

        return np.asarray(final_polygon)

    def __call__(self, A, B):
        clipped_polygon = self.clip(A, B)
        if len(clipped_polygon) == 0 and self.warn_if_empty:
            warnings.warn("No intersections found. Are you sure your \
                          polygon coordinates are in clockwise order?")

        return clipped_polygon

# GitHub link for this function: https://github.com/mhdadk/sutherland-hodgman/blob/main/SH.py

def cross_product(point1, point2, ref):
    """
    Calculates cross product of two points in order w.r.t. to a reference point
    """
    x1, x2 = point1[0] - ref[0], point2[0] - ref[0]
    y1, y2 = point1[1] - ref[1], point2[1] - ref[1]

    return x1*y2 - x2*y1


def find_centre(polygon):
    """
    finds centroid of given convex polygon
    """
    centre = [0,0]
    for i in range(len(polygon)):
        centre += polygon[i]

    centre[0], centre[1] = centre[0]/len(polygon), centre[1]/len(polygon)

    return centre


def polyarea(polygon):
    """
    finds area of given convex polygon
    """
    area = 0
    centre = polygon[0]
    for i in range(len(polygon)-1):
        area += cross_product(polygon[i], polygon[i+1], centre)

    return abs(area)


def rot_coords(rot_centre, point, theta):
    """
    returns rotated copy of a polygon wrt to a given point and with a given angle
    """
    x = point[0] - rot_centre[0]
    y = point[1] - rot_centre[1]
    new_x = x*np.cos(theta) - y*np.sin(theta) + rot_centre[0]
    new_y = x*np.sin(theta) + y*np.cos(theta) + rot_centre[1]

    return (new_x, new_y)


if __name__ == '__main__':
    py.init()  # initialising screen
    width, height = 800, 600
    screen = py.display.set_mode((width, height))


    # Initialising variables - MAKE CHANGES HERE
    angle_inc = 0.001  # angle increment
    draw_stage = True  # toggles between allowing user to enter polygons through lists or by clicking

    # DON'T CHANGE THESE
    clip = PolygonClipper()  # setting up clip function
    taking_input = False  # tracks when the program is expecting more points from the user
    running = True # for the pygame loop
    polygon1, polygon2, poly_intersect, poly_copy, og_intersect, cur_intersect, vertex_clips, rot_centre, area_array = [], [], [], [], [], [], [], [], []
    # initialising the polygon and polygon intersection vertex lists
    angle = [0]  # stores the different angles increments


    # Can input hard-coded polygons if we want reproducibility of data
    if not draw_stage:
        polygon1, polygon2 = [(178, 123), (174, 383), (408, 446), (651, 376)], [(315, 136), (177, 238), (152, 350), (319, 438), (592, 450), (641, 319), (672, 154), (582, 86)]
        rot_centre = find_centre(clip(polygon1, polygon2))
        poly_copy = polygon2.copy()


    while running:  # pygame loop
        for event in py.event.get():
            if event.type == py.QUIT:  # needed for proper exit
                running = False

            if draw_stage:  # stage where key presses and mouse clicks are checked
                if event.type == py.KEYDOWN:
                    if event.key == py.K_BACKSPACE:  # stops taking input for points
                        draw_stage = False

                        find_rot_coord = True  # takes input for rotation centre of the second polygon
                        while find_rot_coord:
                            evt_list = py.event.get()
                            for evt in evt_list:
                                if evt.type == py.MOUSEBUTTONDOWN:
                                    rot_centre = (int(evt.pos[0]), int(evt.pos[1]))  # rotation center set
                                    find_rot_coord = False
                                    break

                    elif event.key == py.K_ESCAPE: # removes last point entered in polygon
                        if len(polygon1) > 0:
                            polygon1.pop()
                    elif event.key == py.K_BACKSLASH:  # switching from taking inputs for first to second polygon
                        polygon2 = polygon1.copy()
                        poly_copy = polygon1.copy()
                        polygon1 = []
                        taking_input = False

                elif event.type == py.MOUSEBUTTONDOWN:
                    polygon1.append((int(event.pos[0]), int(event.pos[1])))
                    taking_input = True
                    if len(polygon1) > 2:  # ensuring a convex polygon is entered in clockwise order
                        if cross_product(polygon1[-1], polygon1[-3], polygon1[-2]) >= 0:
                            polygon1.pop()
                        elif cross_product(polygon1[1], polygon1[-1], polygon1[0]) >= 0:
                            polygon1.pop()
                        elif cross_product(polygon1[0], polygon1[-2], polygon1[-1]) >= 0:
                            polygon1.pop()

                elif event.type == py.MOUSEBUTTONUP:  # stops taking input after mouse is released
                    taking_input = False

                elif event.type == py.MOUSEMOTION and taking_input:  # makes end of line follow the mouse cursor
                    polygon1[-1] = (int(event.pos[0]), int(event.pos[1]))

        screen.fill("black")
        if len(polygon1) > 1:
            py.draw.lines(screen, "red", True, polygon1, 3)
        if len(polygon2) > 1:
            py.draw.lines(screen, "green", True, polygon2, 3)

        if not draw_stage:  # Only runs when inputting has finished
            for i in range(len(polygon2)):  # rotating the polygon by angle increment
                polygon2[i] = rot_coords(rot_centre, poly_copy[i], angle[-1] + angle_inc)

            cmp_length = len(cur_intersect) # stores number of sides of old intersection polygon
            cur_intersect = clip(polygon1, polygon2) # Finding new intersection polygon
            py.draw.polygon(screen, "yellow", cur_intersect)  # Drawing Intersection Polygon
            py.draw.circle(screen, "blue", rot_centre, 3)  # Drawing rotation centre

            # calculating intersection area for one full rotation and storing it in a list
            if angle[-1] <= 2*np.pi:
                if cmp_length != len(cur_intersect):  # If the number of sides of the intersection polygon changes
                    vertex_clips.append(angle[-1])

                ar = polyarea(cur_intersect)
                area_array.append(ar)  # stores area of each intersection in an array
                angle.append(angle[-1] + angle_inc)

        py.display.flip()

    py.quit()


    # plotting the intersection curve for different angles
    angle.pop()
    plt.xlabel("Angle (in radians)")
    plt.ylabel("Intersection Area")
    plt.plot(angle, area_array)

    # plots vertical lines on angles where a point of one polygon intersects an edge or a point of another polygon
    # between two vertical lines, the function will be continuous and differentiable
    min_area, max_area = min(area_array), max(area_array)
    plt.vlines(x=vertex_clips, ymin=min_area, ymax=max_area, color="red", linestyles=":")
    plt.show()

    #prints out the coordinates of the polygons entered in case we want to save them for later use
    print(polygon1, poly_copy, rot_centre)

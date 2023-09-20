# rotating-convex-polygons
This program is part of a project in computational geometry to attempt to solve the problem of maximising overlaps of two planar convex polygons under rotations about a fixed point done under Professor Minati De of IIT-Delhi.

Instructions:
- The program is written in pygame. It requires entering two convex polygons in counter-clockwise order. 
- The points are taken as input by mouse clicks, and if the clicks are not in the correct order they will not register as a point. 
- To remove a point added by mistake, press the ESC key. 
- After one polygon has been entered, to switch to entering the second polygon, press the backslash (\) key. The first polygon should change colour to green.
- Enter the second polygon as before. MAKE SURE THEY INTERSECT.
- After the second polygon has been entered, press the BACKSPACE key. Then, press anywhere on the screen to choose a centre of rotation for the second polygon.
- It is recommended that the centre of rotation be chosen within the overlap of the two polygons to prevent them losing overlap during rotation.
- After the rotation centre has been entered, an animation of the rotation plays and stops after one rotation.
- Closing this window shows a graph of angle vs intersection area, with vertical red lines marking the angles where the number of sides of the intersection polygon changes.
- The program prints the coordinates of both polygons in order and their rotation centre in case you want to save an interesting example.

To calculate the overlapping polygon, the program uses the computationally simple Sutherland-Hodgman algorithm for finding the intersection of the two convex polygons (code for this portion taken from https://github.com/mhdadk/sutherland-hodgman/blob/main/SH.py). This was created as a tool for helping me visualise the problem in an attempt to solve it. Have fun with it!

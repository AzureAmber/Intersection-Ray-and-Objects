import math
import os
from vector import matrix, vector, intersection, ray, test_intersection
from perspective import camera

# screen dimensions
scr_width = 160
scr_height = 90

# camera
cam_x = 0.0
cam_y = 0.0
cam_z = 0.0
x = camera(cam_x, cam_y, cam_z, 120 * math.pi / 180, scr_width, scr_height, 0.01, 1000.0)

# raytrace
# for i in range(scr_width):
#     for j in range(scr_height):
#         print(i+1, j+1, x.screen_coord(x.get_ray(i+1, j+1).dir))
        






























import math
import os
from vector import matrix, vector, intersection, ray, test_intersection

class camera:
    def __init__(self, x: float, y: float, z: float, fov: float, width: float, height: float, z_n: float, z_f: float):
        self.position = vector(x,y,z)
        self.aspect_ratio = width / height
        self.mat = matrix([1.0 / (self.aspect_ratio * math.tan(fov / 2)), 0.0, 0.0, -1.0 * x / (self.aspect_ratio * math.tan(fov / 2))],
                          [0.0, 1.0 / math.tan(fov / 2), 0.0, 0.0, -1.0 * y / math.tan(fov / 2)],
                          [0.0, 0.0, (z_n + z_f) / (z_n - z_f), (2.0 * z_n * z_f - (z_n + z_f) * z) / (z_n - z_f)],
                          [0.0, 0.0, -1.0, z])
    def perspective(self, v: vector):
        temp = v.matmult(self.mat)
        result = [temp.getx() / temp.getw(), temp.gety() / temp.getw(), temp.getz() / temp.getw()]
        print(result)

# check cases
# x = camera(0.0, 0.0, 0.0, 60 * math.pi / 180, 1920, 1080, 0.01, 100.0)
# x.perspective(vector(25, 14, -25))










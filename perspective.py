import math
import os
from vector import matrix, vector, intersection, ray, test_intersection

class camera:
    def __init__(self, x: float, y: float, z: float, fov: float, width: float, height: float, z_n: float, z_f: float, roth = 0.0, rotv = 0.0, tilt = 0.0):
        self.position = vector(x,y,z)
        self.width = width
        self.height = height
        self.aspect_ratio = width / height
        self.persp = matrix([1.0 / (self.aspect_ratio * math.tan(fov / 2)), 0.0, 0.0, 0.0],
                            [0.0, 1.0 / math.tan(fov / 2), 0.0, 0.0],
                            [0.0, 0.0, (z_n + z_f) / (z_n - z_f), (2.0 * z_n * z_f) / (z_n - z_f)],
                            [0.0, 0.0, -1.0, 0.0])
        self.roth = roth
        self.rotv = rotv
        self.tilt = tilt
    def update_x(self, v: float):
        new_x = self.position.getx() + v
        self.position.setx(new_x)
    def update_y(self, v: float):
        new_y = self.position.gety() + v
        self.position.sety(new_y)
    def update_z(self, v: float):
        new_z = self.position.getz() + v
        self.position.setz(new_z)
    def update_roth(self, v: float):
        self.roth = self.roth + v
    def update_rotv(self, v: float):
        self.rotv = self.rotv + v
    def update_tilt(self, v: float):
        self.tilt = self.tilt + v
    # apply the perspective projection matrix
    def perspective(self, v: vector):
        m_tran = matrix([1.0, 0.0, 0.0, -1.0 * self.position.getx()],
                        [0.0, 1.0, 0.0, -1.0 * self.position.gety()],
                        [0.0, 0.0, 1.0, -1.0 * self.position.getz()],
                        [0.0, 0.0, 0.0, 1.0])
        m_roth = matrix([math.cos(self.roth), 0.0, math.sin(self.roth), 0.0],
                        [0.0, 1.0, 0.0, 0.0],
                        [-1.0 * math.sin(self.roth), 0.0, math.cos(self.roth), 0.0],
                        [0.0, 0.0, 0.0, 1.0])
        m_rotv = matrix([1.0, 0.0, 0.0, 0.0],
                        [0.0, math.cos(self.rotv), math.sin(self.rotv), 0.0],
                        [0.0, -1.0 * math.sin(self.rotv), math.cos(self.rotv), 0.0],
                        [0.0, 0.0, 0.0, 1.0])
        m_tilt = matrix([math.cos(self.tilt), -1.0 * math.sin(self.tilt), 0.0, 0.0],
                        [math.sin(self.tilt), math.cos(self.tilt), 0.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0])
        m = self.persp * m_tilt * m_rotv * m_roth * m_tran
        temp = v.matmult(m)
        return temp
    # returns the screen coordinates of vector v after perspective projection
    def screen_coord(self, v: vector):
        temp = self.perspective(v)
        temp_clip = temp / temp.getw()
        # clip if vector is outside camera view
        if ((temp_clip.getx() >= -1.0 and temp_clip.getx() <= 1.0)
            and (temp_clip.gety() >= -1.0 and temp_clip.gety() <= 1.0)
            and (temp_clip.getz() >= -1.0 and temp_clip.getz() <= 1.0)):
            return( vector((1 + temp_clip.getx()) * self.width / 2.0, (1 - temp_clip.gety()) * self.height / 2.0, temp_clip.getz()) )
        else:
            return None

# check cases
# x = camera(0.0, 0.0, 0.0, 120 * math.pi / 180, 1920, 1080, 0.01, 100.0)
# print(x.perspective(vector(-1, 0, -100)))
# print(x.screen_coord(vector(-1, 0, -100)))










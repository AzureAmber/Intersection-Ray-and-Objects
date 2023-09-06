import math
import os
from vector import matrix, vector, intersection, ray, test_intersection

err_tol = 1e-7

class camera:
    def __init__(self, x: float, y: float, z: float, fov: float, width: float, height: float, z_n: float, z_f: float, roth = 0.0, rotv = 0.0, tilt = 0.0):
        self.position = vector(x,y,z)
        self.fov = fov
        self.width = width
        self.height = height
        self.aspect_ratio = width / height
        self.z_n = z_n
        self.z_f = z_f
        self.persp = matrix([1.0 / (self.aspect_ratio * math.tan(fov / 2)), 0.0, 0.0, 0.0],
                            [0.0, 1.0 / math.tan(fov / 2), 0.0, 0.0],
                            [0.0, 0.0, (z_n + z_f) / (z_n - z_f), (2.0 * z_n * z_f) / (z_n - z_f)],
                            [0.0, 0.0, -1.0, 0.0])
        self.roth = roth
        self.rotv = rotv
        self.tilt = tilt
    def update_x(self, v: float):
        m_roth = matrix([math.cos(self.roth), 0.0, -1.0 * math.sin(self.roth), 0.0],
                        [0.0, 1.0, 0.0, 0.0],
                        [math.sin(self.roth), 0.0, math.cos(self.roth), 0.0],
                        [0.0, 0.0, 0.0, 1.0])
        m_rotv = matrix([1.0, 0.0, 0.0, 0.0],
                        [0.0, math.cos(self.rotv), -1.0 * math.sin(self.rotv), 0.0],
                        [0.0, math.sin(self.rotv), math.cos(self.rotv), 0.0],
                        [0.0, 0.0, 0.0, 1.0])
        m_tilt = matrix([math.cos(self.tilt), math.sin(self.tilt), 0.0, 0.0],
                        [-1.0 * math.sin(self.tilt), math.cos(self.tilt), 0.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0])
        x_dir = vector(1.0, 0.0, 0.0).matmult(m_tilt * m_rotv * m_roth) * v
        self.position = self.position + x_dir
    def update_y(self, v: float):
        m_roth = matrix([math.cos(self.roth), 0.0, -1.0 * math.sin(self.roth), 0.0],
                        [0.0, 1.0, 0.0, 0.0],
                        [math.sin(self.roth), 0.0, math.cos(self.roth), 0.0],
                        [0.0, 0.0, 0.0, 1.0])
        m_rotv = matrix([1.0, 0.0, 0.0, 0.0],
                        [0.0, math.cos(self.rotv), -1.0 * math.sin(self.rotv), 0.0],
                        [0.0, math.sin(self.rotv), math.cos(self.rotv), 0.0],
                        [0.0, 0.0, 0.0, 1.0])
        m_tilt = matrix([math.cos(self.tilt), math.sin(self.tilt), 0.0, 0.0],
                        [-1.0 * math.sin(self.tilt), math.cos(self.tilt), 0.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0])
        y_dir = vector(0.0, 1.0, 0.0).matmult(m_tilt * m_rotv * m_roth) * v
        self.position = self.position + y_dir
    def update_z(self, v: float):
        m_roth = matrix([math.cos(self.roth), 0.0, -1.0 * math.sin(self.roth), 0.0],
                        [0.0, 1.0, 0.0, 0.0],
                        [math.sin(self.roth), 0.0, math.cos(self.roth), 0.0],
                        [0.0, 0.0, 0.0, 1.0])
        m_rotv = matrix([1.0, 0.0, 0.0, 0.0],
                        [0.0, math.cos(self.rotv), -1.0 * math.sin(self.rotv), 0.0],
                        [0.0, math.sin(self.rotv), math.cos(self.rotv), 0.0],
                        [0.0, 0.0, 0.0, 1.0])
        m_tilt = matrix([math.cos(self.tilt), math.sin(self.tilt), 0.0, 0.0],
                        [-1.0 * math.sin(self.tilt), math.cos(self.tilt), 0.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0])
        z_dir = vector(0.0, 0.0, -1.0).matmult(m_tilt * m_rotv * m_roth) * v
        self.position = self.position + z_dir
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
        if (temp.getw() > 0):
            temp_clip = temp / temp.getw()
            # clip if vector is outside camera view
            if (((temp_clip.getx() > -1.0 and temp_clip.getx() < 1.0) or math.isclose(abs(temp_clip.getx()), 1.0, rel_tol = 0, abs_tol = err_tol))
                and ((temp_clip.gety() > -1.0 and temp_clip.gety() < 1.0) or math.isclose(abs(temp_clip.gety()), 1.0, rel_tol = 0, abs_tol = err_tol))
                and ((temp_clip.getz() > -1.0 and temp_clip.getz() < 1.0) or math.isclose(abs(temp_clip.getz()), 1.0, rel_tol = 0, abs_tol = err_tol))):
                result = vector((1 + temp_clip.getx()) * self.width / 2.0, (1 - temp_clip.gety()) * self.height / 2.0, temp_clip.getz())
                result.setw(temp.getw())
                return(result)
            else:
                return None
        else:
            return None
    # return world coordinates (for ray) based on pixel coordinates (i=[1,width], j=[1,height])
    def get_ray(self, pixel_x: int, pixel_y: int):
        world_vec = vector(self.aspect_ratio * math.tan(self.fov / 2) * self.z_n * (2.0 * pixel_x - self.width - 1.0) / self.width,
                           math.tan(self.fov / 2) * self.z_n * (self.height + 1.0 - 2.0 * pixel_y) / self.height,
                           -1.0 * self.z_n)
        m_roth = matrix([math.cos(self.roth), 0.0, -1.0 * math.sin(self.roth), 0.0],
                        [0.0, 1.0, 0.0, 0.0],
                        [math.sin(self.roth), 0.0, math.cos(self.roth), 0.0],
                        [0.0, 0.0, 0.0, 1.0])
        m_rotv = matrix([1.0, 0.0, 0.0, 0.0],
                        [0.0, math.cos(self.rotv), -1.0 * math.sin(self.rotv), 0.0],
                        [0.0, math.sin(self.rotv), math.cos(self.rotv), 0.0],
                        [0.0, 0.0, 0.0, 1.0])
        m_tilt = matrix([math.cos(self.tilt), math.sin(self.tilt), 0.0, 0.0],
                        [-1.0 * math.sin(self.tilt), math.cos(self.tilt), 0.0, 0.0],
                        [0.0, 0.0, 1.0, 0.0],
                        [0.0, 0.0, 0.0, 1.0])
        m = m_tilt * m_rotv * m_roth
        new_world_vec = world_vec.matmult(m)
        return(ray(self.position, new_world_vec, math.inf))


# check cases
# x = camera(5.0, 10.0, -3.0, 120 * math.pi / 180, 1920, 1080, 0.01, 100.0)
# print(x.perspective(vector(-1, 0, -100)))
# print(x.screen_coord(vector(-1, 0, -100)))








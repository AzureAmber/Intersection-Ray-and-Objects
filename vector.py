import math
import os

err_tol = 1e-7

# definition of matrix
class matrix:
    # row vectors
    def __init__(self, a, b, c, d):
        self.data = [a, b, c, d]

# definition and properties of vectors
class vector:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
        self.w = 1
    def getx(self):
        return self.x
    def gety(self):
        return self.y
    def getz(self):
        return self.z
    def getw(self):
        return self.w
    def setw(self, value: float):
        self.w = value
    def dot(self, v: 'vector'):
        return (self.x * v.x + self.y * v.y + self.z * v.z)
    def cross(self, v: 'vector'):
        return vector(self.y * v.z - v.y * self.z,
                      v.x * self.z - self.x * v.z,
                      self.x * v.y - v.x * self.y)
    def length(self):
        return (math.sqrt(self.x**2 + self.y**2 + self.z**2))
    def __eq__(self, v: 'vector'):
        return (math.isclose(self.x, v.x, rel_tol = 0, abs_tol = err_tol)
                and math.isclose(self.y, v.y, rel_tol = 0, abs_tol = err_tol)
                and math.isclose(self.z, v.z, rel_tol = 0, abs_tol = err_tol))
    def iszero(self):
        return self == vector(0.0, 0.0, 0.0)
    def isorthogonal(self, v: 'vector'):
        return math.isclose(self.dot(v), 0.0, rel_tol = 0, abs_tol = err_tol)
    def isparallel(self, v: 'vector'):
        return (self.cross(v)).iszero()
    def getangle(self, v: 'vector'):
        return math.acos(self.dot(v) / (self.length() * v.length()))
    def __add__(self, v):
        if isinstance(v, float):
            return vector(self.x + v, self.y + v, self.z + v)
        elif isinstance(v, vector):
            return vector(self.x + v.x, self.y + v.y, self.z + v.z)
        else:
            raise TypeError('add: Not float or vector')
    def __radd__(self, v):
        if isinstance(v, float):
            return vector(self.x + v, self.y + v, self.z + v)
        elif isinstance(v, vector):
            return vector(self.x + v.x, self.y + v.y, self.z + v.z)
        else:
            raise TypeError('add: Not float or vector')
    def __sub__(self, v):
        if isinstance(v, float):
            return vector(self.x - v, self.y - v, self.z - v)
        elif isinstance(v, vector):
            return vector(self.x - v.x, self.y - v.y, self.z - v.z)
        else:
            raise TypeError('subtract: Not float or vector')
    def __mul__(self, v: float):
        return vector(v * self.x, v * self.y, v * self.z)
    def __rmul__(self, v: float):
        return vector(v * self.x, v * self.y, v * self.z)
    def __truediv__(self, v: float):
        if (math.isclose(v, 0, rel_tol = 0, abs_tol = err_tol)):
            raise ValueError('division: Division by 0')
        else:
            return vector(self.x / v, self.y / v, self.z/ v)
    def __str__(self):
        return "({0}, {1}, {2}, {3})".format(self.x, self.y, self.z, self.w)
    def matmult(self, M: matrix):
        mat = M.data
        v = [self.x, self.y, self.z, self.w]
        result = [0, 0, 0, 0]
        for i in range(4):
            temp = 0
            for j in range(4):
                temp = temp + mat[i][j] * v[j]
            result[i] = temp
        w = vector(result[0], result[1], result[2])
        w.setw(result[3])
        return w

# definition of intersection
class intersection:
    def __init__(self, point: vector, len: float):
        self.point = point
        self.length = len
    def getpoint(self):
        return self.point
    def getlength(self):
        return self.length
    def __str__(self):
        return "point: {0}, t: {1}".format(self.point, self.length)

# definition of ray
class ray:
    def __init__(self, origin: vector, dir: vector, len: float):
        self.origin = origin
        self.dir = dir
        self.length = len
        self.end = origin + (dir / dir.length()) * len
    # If intersection is within [0, ray.length], return intersection else return None
    def reachable(self, x):
        if (x is not None):
            t = x.getlength()
            if (math.isclose(t, 0, rel_tol = 0, abs_tol = err_tol)
                or math.isclose(t, self.length / self.dir.length(), rel_tol = 0, abs_tol = err_tol)
                or (t > 0 and t < self.length / self.dir.length())):
                return x
            else:
                return None
        else:
            return None
    def __str__(self):
        return "origin: {0}, dir: {1} of length {2}".format(self.origin, self.dir, self.length)
    
# definition of ray and object intersection test case
class test_intersection:
    def __init__(self, name: float, r: ray, geo_object):
        self.name = name
        self.r = r
        self.geo_object = geo_object
        self.point_inf = geo_object.intersect(r)
        self.point_fin = r.reachable(self.point_inf)
    def __str__(self):
        return "Test case: {0}\n\tIntersection: {1}\n\tReachable: {2}".format(self.name, self.point_inf, self.point_fin)














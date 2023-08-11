import math
import os
from vector import vector, intersection, ray, test_intersection

err_tol = 1e-7

# definition of plane
class plane:
    def __init__(self, point: vector, normal: vector):
        self.point = point
        self.normal = normal
    def getnormal(self):
        return self.normal
    def __str__(self):
        return "{0}x + {1}y + {2}z = {3}".format(self.normal.getx(), self.normal.gety(), self.normal.getz(), self.normal.dot(self.point))
    # Return True if point p is in plane else return False
    def inplane(self, p: vector):
        return math.isclose(self.normal.dot(p), self.normal.dot(self.point), rel_tol = 0, abs_tol = err_tol)
    # If ray and plane intersect, return intersection else return None
    def intersect(self, r: ray):
        # check if plane and ray are parallel
        if (self.normal.isorthogonal(r.dir)):
            # check if plane and ray are overlapping
            if (self.inplane(r.origin)):
                return intersection(r.origin, 0.0)
            else:
                return None
        else:
            t = self.normal.dot(self.point - r.origin) / self.normal.dot(r.dir)
            # check if intersection is in front of ray
            if (math.isclose(t, 0, rel_tol = 0, abs_tol = err_tol) or t > 0):    
                return intersection(r.origin + r.dir * t, t)
            else:
                return None
    # Similar to intersect, but return None if intersection is less than ray's length
    def bounded_intersect(self, r: ray):
        return r.reachable(self.intersect(r))

# Check cases

# r = ray(vector(0,0,0), vector(0,1,1), 5)
# x = plane(vector(0,0,3), vector(0,0,1))
# tc = test_intersection(1, r, x)
# print(tc)
















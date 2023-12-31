import math
import os
from vector import vector, intersection, ray, test_intersection
from segment import segment
from plane import plane

err_tol = 1e-7

# definition of triangle
class triangle:
    def __init__(self, pointA: vector, pointB: vector, pointC: vector):
        self.pointA = pointA
        self.pointB = pointB
        self.pointC = pointC
    def __str__(self):
        return "A: {0}, B: {1}, C: {2}".format(self.pointA, self.pointB, self.pointC)
    # Return True if point p is in triangle else return False
    def intriangle(self, p: vector):
        tri_normal = (self.pointB - self.pointA).cross(self.pointC - self.pointA)
        Area_ab = ((self.pointA - p).cross(self.pointB - p)).length() / 2
        Area_ac = ((self.pointA - p).cross(self.pointC - p)).length() / 2
        Area_bc = ((self.pointB - p).cross(self.pointC - p)).length() / 2
        return math.isclose(tri_normal.length() / 2, Area_ab + Area_ac + Area_bc, rel_tol = 0, abs_tol = err_tol)
    # If ray and triangle intersect, return intersection else return None
    def intersect(self, r: ray):
        tri_normal = (self.pointB - self.pointA).cross(self.pointC - self.pointA)
        tri_plane = plane(self.pointA, tri_normal)
        # check if plane containing triangle and ray are parallel
        if (tri_normal.isorthogonal(r.dir)):
            # check if plane containing triangle and ray are overlapping
            if (tri_plane.inplane(r.origin)):
                # check if ray's origin is inside triangle
                if (self.intriangle(r.origin)):
                    return intersection(r.origin, 0.0)
                else:
                    # ray is not in triangle so find closest intersection at triangle's sides if exist
                    final_point = segment(self.pointA, self.pointB).intersect(r)
                    
                    second_point = segment(self.pointA, self.pointC).intersect(r)
                    if (second_point is not None):
                        if ((final_point is None) or second_point.getlength() < final_point.getlength()):
                            final_point = second_point
                    third_point = segment(self.pointB, self.pointC).intersect(r)
                    if (third_point is not None):
                        if ((final_point is None) or third_point.getlength() < final_point.getlength()):
                            final_point = third_point
                    return final_point
            else:
                # None: plane containing triangle and ray are parallel
                return None
        else:
            # ray and plane containing triangle intersect
            tri_plane_intersect = tri_plane.intersect(r)
            # check if ray reaches intersection
            if (tri_plane_intersect is not None):
                # check if intersection is inside triangle
                if (self.intriangle(tri_plane_intersect.getpoint())):
                    return tri_plane_intersect
                else:
                    return None
            else:
                return None
    # Similar to intersect, but return None if intersection is less than ray's length
    def bounded_intersect(self, r: ray):
        return r.reachable(self.intersect(r))

# Check Cases

# r = ray(vector(0,0,0), vector(1,1,0), math.inf)
# x = triangle(vector(5,1,0), vector(-2,6,0), vector(2,10,0))
# tc = test_intersection(1, r, x)
# print(tc)










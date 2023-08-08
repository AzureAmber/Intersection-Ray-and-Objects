import math
import os
from vector import vector, ray, intersection
from segment import segment

err_tol = 1e-7

# definition of triangle
class triangle:
    def __init__(self, pointA: vector, pointB: vector, pointC: vector):
        self.pointA = pointA
        self.pointB = pointB
        self.pointC = pointC
    def __str__(self):
        return "A: {0}, B: {1}, C: {2}".format(self.pointA, self.pointB, self.pointC)
    def intersect(self, r: ray):
        tri_normal = (self.pointB - self.pointA).cross(self.pointC - self.pointA)
        # check if plane containing triangle and ray are parallel
        if (math.isclose(tri_normal.dot(r.dir), 0.0, rel_tol = 0, abs_tol = err_tol)):
            # check if plane containing triangle and ray are overlapping
            if (math.isclose(tri_normal.dot(r.origin), tri_normal.dot(self.pointA), rel_tol = 0, abs_tol = err_tol)):
                # check if ray's origin is inside triangle
                Area_ab = ((self.pointA - r.origin).cross(self.pointB - r.origin)).length() / 2
                Area_ac = ((self.pointA - r.origin).cross(self.pointC - r.origin)).length() / 2
                Area_bc = ((self.pointB - r.origin).cross(self.pointC - r.origin)).length() / 2
                if (math.isclose(tri_normal.length() / 2, Area_ab + Area_ac + Area_bc, rel_tol = 0, abs_tol = err_tol)):
                    return intersection(r.origin, 0.0)
                else:
                    # ray is not in triangle so find closest intersection at triangle's sides if exist
                    final_point = segment(self.pointA, self.pointB).intersect(r)
                    
                    second_point = segment(self.pointA, self.pointC).intersect(r)
                    if (isinstance(second_point, intersection)):
                        if ((final_point is None) or second_point.getlength() < final_point.getlength()):
                            final_point = second_point
                    third_point = segment(self.pointB, self.pointC).intersect(r)
                    if (isinstance(third_point, intersection)):
                        if ((final_point is None) or third_point.getlength() < final_point.getlength()):
                            final_point = third_point
                    return final_point
            else:
                # None: plane containing triangle and ray are parallel
                return None
        else:
            # ray and plane containing triangle are skew so find intersection
            t = (tri_normal.dot(self.pointA - r.origin)) / (tri_normal.dot(r.dir))
            final_point = r.origin + r.dir * t
            # check if ray reaches intersection
            if (math.isclose(t, 0, rel_tol = 0, abs_tol = err_tol)
                or math.isclose(t, r.length, rel_tol = 0, abs_tol = err_tol)
                or (t > 0 and t < r.length)):
                # check if intersection is inside triangle
                Area_ab = ((self.pointA - final_point).cross(self.pointB - final_point)).length() / 2
                Area_ac = ((self.pointA - final_point).cross(self.pointC - final_point)).length() / 2
                Area_bc = ((self.pointB - final_point).cross(self.pointC - final_point)).length() / 2
                if (math.isclose(tri_normal.length() / 2, Area_ab + Area_ac + Area_bc, rel_tol = 0, abs_tol = err_tol)):
                    return intersection(final_point, t)
                else:
                    # intersection is outside triangle
                    return None
            else:
                # intersection too far away
                return None

# Check Cases
r = ray(vector(0,0,0), vector(1,4,2), math.inf)
x = triangle(vector(10,-5,4), vector(6,7,8), vector(-2,1,-1))
print(x.intersect(r))










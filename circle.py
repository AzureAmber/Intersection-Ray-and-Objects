import math
import os
from vector import vector, ray, intersection
from plane import plane
from sphere import sphere

err_tol = 1e-7

# definition of cirle
class circle:
    def __init__(self, center: vector, normal: vector, radius: float):
        self.center = center
        self.normal = normal
        self.radius = radius
    def getcenter(self):
        return self.center
    def getnormal(self):
        return self.normal
    def getradius(self):
        return self.radius
    def incircle(self, p: vector):
        return (math.isclose(self.normal.dot(p), self.normal.dot(self.center), rel_tol = 0, abs_tol = err_tol)
                and (math.isclose((p - self.center).length(), self.radius, rel_tol = 0, abs_tol = err_tol) or (p - self.center).length() < self.radius))
    def intersect(self, r: ray):
        # check if plane containing circle and ray are parallel
        if (self.normal.isorthogonal(r.dir)):
            # find intersection between sphere and ray if exist
            circ_sphere_intersect = sphere(self.center, self.radius).intersect(r)
            if (circ_sphere_intersect is not None):
                # check if intersection is inside circle
                if (self.incircle(circ_sphere_intersect.getpoint())):
                    return circ_sphere_intersect
                else:
                    return None
            else:
                return None
        else:
            # plane containing circle and ray intersect so find intersection
            circ_plane = plane(self.center, self.normal)
            circ_plane_intersect = circ_plane.intersect(r)
            # check if intersection is inside circle
            if (self.incircle(circ_plane_intersect.getpoint())):
                return circ_plane_intersect
            else:
                return None

# Check cases

# parallel intersection
# r = ray(vector(0,0,0), vector(1,0,0), math.inf)
# x = circle(vector(5,0,0), vector(0,0,1), 2)
# print(x.intersect(r))

# not parallel intersection
# r = ray(vector(0,0,0), vector(1,1,2), math.inf)
# x = circle(vector(5,5,1), vector(0,0,1), 10)
# print(x.intersect(r))











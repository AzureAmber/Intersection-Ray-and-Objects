import math
import os
from vector import vector, intersection, ray, test_intersection
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
    def __str__(self):
        return "center: {0}, radius: {1}, on plane: {2}x + {3}y + {4}z = {5}".format(self.center, self.radius,
                                                                                     self.normal.getx(), self.normal.gety(), self.normal.getz(),
                                                                                     self.normal.dot(self.center))
    # Return True if point p is inside circle else return False
    def incircle(self, p: vector):
        return (math.isclose(self.normal.dot(p), self.normal.dot(self.center), rel_tol = 0, abs_tol = err_tol)
                and (math.isclose((p - self.center).length(), self.radius, rel_tol = 0, abs_tol = err_tol) or (p - self.center).length() < self.radius))
    # If ray and circle intersect, return intersection else return None
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
            # plane containing circle and ray intersect so find intersection if exist
            circ_plane = plane(self.center, self.normal)
            circ_plane_intersect = circ_plane.intersect(r)
            # check if intersection is inside circle
            if (circ_plane_intersect is not None):
                if (self.incircle(circ_plane_intersect.getpoint())):
                    return circ_plane_intersect
                else:
                    return None
            else:
                return None
    # Similar to intersect, but return None if intersection is less than ray's length
    def bounded_intersect(self, r: ray):
        return r.reachable(self.intersect(r))

# Check cases

# parallel intersection
# r = ray(vector(0,0,0), vector(1,0,0), math.inf)
# x = circle(vector(5,0,0), vector(0,0,1), 2)
# tc = test_intersection(1, r, x)
# print(tc)

# not parallel intersection
# r = ray(vector(0,0,0), vector(1,1,2), 1.23)
# x = circle(vector(5,5,1), vector(0,0,1), 10)
# tc = test_intersection(2, r, x)
# print(tc)

# parallel no intersection
# r = ray(vector(0,0,0), vector(1,0,0), math.inf)
# x = circle(vector(1,0,1), vector(0,0,1), 2)
# tc = test_intersection(3, r, x)
# print(tc)

# skew
# r = ray(vector(0,0,0), vector(1,0,0), math.inf)
# x = circle(vector(1,0,1), vector(1,0,1), 1.42)
# tc = test_intersection(4, r, x)
# print(tc)









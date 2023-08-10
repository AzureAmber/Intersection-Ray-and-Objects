import math
import os
from vector import vector, ray, intersection

err_tol = 1e-7

# definition of sphere (filled)
class sphere:
    def __init__(self, center: vector, radius: float):
        self.center = center
        self.radius = radius
    def getcenter(self):
        return self.center
    def getradius(self):
        return self.radius
    def __str__(self):
        return "center: {0}, radius: {1}".format(self.center, self.radius)
    def intersect(self, r: ray):
        circ_A = r.dir.length()**2
        circ_B = 2.0 * r.dir.dot(r.origin - self.center)
        circ_C = (r.origin - self.center).length()**2 - self.radius**2
        det = circ_B**2 - 4.0 * circ_A * circ_C
        # check if sphere and ray intersect
        if ((not math.isclose(det, 0, rel_tol = 0, abs_tol = err_tol)) and det > 0):
            first_t = (-1.0 * circ_B - math.sqrt(det)) / (2.0 * circ_A)
            second_t = (-1.0 * circ_B + math.sqrt(det)) / (2.0 * circ_A)
            if (math.isclose(first_t, 0, rel_tol = 0, abs_tol = err_tol)
                or math.isclose(second_t, 0, rel_tol = 0, abs_tol = err_tol)):
                # ray is on the sphere
                return intersection(r.origin, 0.0)
            elif (first_t < 0 and second_t < 0):
                # sphere is behind ray
                return None
            elif (first_t > 0 and second_t > 0):
                final_t = min(first_t, second_t)
                if (math.isclose(final_t, r.length / r.dir.length(), rel_tol = 0, abs_tol = err_tol)
                    or final_t < r.length / r.dir.length()):
                    # sphere is reachable by ray
                    return intersection(r.origin + r.dir * final_t, final_t)
                else:
                    return None
            else:
                # ray is inside sphere
                return intersection(r.origin, 0.0)
        else:
            return None

# check cases

# r = ray(vector(0,0,0), vector(1,-1,2), math.inf)
# x = sphere(vector(2,-3,2), 2)
# print(x.intersect(r))













import math
import os
from vector import vector, intersection, ray, test_intersection
from line import line
from circle import circle

err_tol = 1e-7

# definition of cylinder
class cylinder:
    def __init__(self, center: vector, normal: vector, radius: float, height: float):
        self.center = center
        self.normal = normal
        self.radius = radius
        self.height = height
    def __str__(self):
        return "center: {0}+{1}t, radius: {2}, height: {3}".format(self.center, self.normal, self.radius, self.height)
    def incylinder(self, p: vector):
        # check if point is less than radius away from cylinder's center axis
        center_axis = line(self.center, self.normal)
        point_dist = center_axis.distance(p)
        check_dist = math.isclose(point_dist, self.radius, rel_tol = 0, abs_tol = err_tol) or point_dist < self.radius
        # check if point lies between cylinder's two circle bases
        first_bound = self.normal.dot(self.center)
        second_bound = first_bound + self.height * self.normal.length()
        point_bound = self.normal.dot(p)
        check_bound = (math.isclose(point_bound, first_bound, rel_tol = 0, abs_tol = err_tol)
                       or math.isclose(point_bound, second_bound, rel_tol = 0, abs_tol = err_tol)
                       or (point_bound > first_bound and point_bound < second_bound))
        return check_dist and check_bound
    def intersect(self, r: ray):
        # check if ray is inside cylinder
        if (self.incylinder(r.origin)):
            return intersection(r.origin, 0.0)
        else:
            # ray is outside cylinder so find closest intersection between the 2 circle bases and lateral surface
            # find closest intersection between ray and cylinder's 2 circle bases if exist
            final_point = circle(self.center, self.normal, self.radius).intersect(r)
            second_circ_point = circle(self.center + self.normal * (self.height / self.normal.length()), self.normal, self.radius).intersect(r)
            if (second_circ_point is not None):
                if ((final_point is None) or second_circ_point.getlength() < final_point.getlength()):
                    final_point = second_circ_point
            # check if ray is parallel to cylinder
            if (self.normal.isparallel(r.dir)):
                # ray and cylinder are parallel so closest intersection is only on the circle bases
                return final_point
            else:
                # find intersection between ray and cylinder's lateral surface (infinite version) if exist
                v = self.normal.dot(self.normal) * (r.origin - self.center) - (self.normal.dot(r.dir) + self.normal.dot(self.center)) * self.normal
                cyl_A = self.normal.dot(self.normal) * (self.normal.dot(self.normal) * r.dir.dot(r.dir) - (self.normal.dot(r.dir))**2)
                cyl_B = 2.0 * self.normal.dot(self.normal) * v.dot(r.dir) - 2.0 * self.normal.dot(r.dir) * self.normal.dot(v)
                cyl_C = v.dot(v) - (self.radius * self.normal.dot(self.normal))**2
                det = cyl_B**2 - 4.0 * cyl_A * cyl_C
                # check if cylinder's lateral surface (infinite version) and ray intersect
                if ((not math.isclose(det, 0, rel_tol = 0, abs_tol = err_tol)) and det > 0):
                    first_t = (-1.0 * cyl_B - math.sqrt(det)) / (2.0 * cyl_A)
                    second_t = (-1.0 * cyl_B + math.sqrt(det)) / (2.0 * cyl_A)
                    # find closest intersection between ray and cylinder's lateral surface
                    lateral_final_point = None
                    if (math.isclose(first_t, 0, rel_tol = 0, abs_tol = err_tol) or first_t > 0):
                        # check if intersection is on cylinder's lateral and reachable
                        if (self.incylinder(r.origin + r.dir * first_t)
                            and (math.isclose(first_t, r.length / r.dir.length(), rel_tol = 0, abs_tol = err_tol) or first_t < r.length / r.dir.length())):
                            lateral_final_point = intersection(r.origin + r.dir * first_t, first_t)
                    lateral_second_point = None
                    if (math.isclose(second_t, 0, rel_tol = 0, abs_tol = err_tol) or second_t > 0):
                        # check if intersection is on cylinder's lateral and reachable
                        if (self.incylinder(r.origin + r.dir * second_t)
                            and (math.isclose(second_t, r.length / r.dir.length(), rel_tol = 0, abs_tol = err_tol) or second_t < r.length / r.dir.length())):
                            lateral_second_point = intersection(r.origin + r.dir * second_t, second_t)
                    if (lateral_second_point is not None):
                        if ((lateral_final_point is None) or lateral_second_point.getlength() < lateral_final_point.getlength()):
                            lateral_final_point = lateral_second_point
                    # find closest intersection between intersections of ray and 2 circle bases, lateral surface
                    if (lateral_final_point is not None):
                        if ((final_point is None) or lateral_final_point.getlength() < final_point.getlength()):
                            final_point = lateral_final_point
                    return final_point
                else:
                    return final_point
            

# check cases

# ray in cylinder
r = ray(vector(1,0,2.5), vector(0,0,1), 0.2)
x = cylinder(vector(0,0,3), vector(0,0,2), 2, 5)
print(x.intersect(r))

# ray intersects circle bases only
# r = ray(vector(0,0,0), vector(0,0,1), math.inf)
# x = cylinder(vector(0,0,3), vector(0,0,2), 2, 5)
# print(x.intersect(r))

# ray intersect lateral only


# ray intersects both circle bases and lateral


# no intersection













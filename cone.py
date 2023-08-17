import math
import os
from vector import vector, intersection, ray, test_intersection
from line import line
from circle import circle

err_tol = 1e-7

# definition of cone (filled)
class cone:
    def __init__(self, vertex: vector, axis: vector, radius: float, height: float):
        self.vertex = vertex
        self.axis = axis
        self.radius = radius
        self.height = height
        self.circ_center = vertex + (axis / axis.length()) * height
        self.angle = math.atan(radius / height)
    def getvertex(self):
        return self.vertex
    def getaxis(self):
        return self.axis
    def getradius(self):
        return self.radius
    def getheight(self):
        return self.height
    def __str__(self):
        return "vertex: {0}, axis of symmetry: {1}, radius: {2}, height: {3}".format(self.vertex, self.axis, self.radius, self.height)
    # Return True if point p is inside cone else return False
    def incone(self, p: vector):
        # check if the point is the cone's vertex
        if (p == self.vertex):
            return True
        else:
            # check if point is within bounary of lateral surface
            point_angle = math.acos((p-self.vertex).dot(self.axis) / ((p-self.vertex).length() * self.axis.length()))
            angle_check = math.isclose(point_angle, self.angle, rel_tol = 0, abs_tol = err_tol) or (point_angle < self.angle)
            # check if point is within boundary of circle base
            point_height = (p-self.vertex).length() * math.cos(point_angle)
            point_height_check = math.isclose(point_height, self.height, rel_tol = 0, abs_tol = err_tol) or (point_height < self.height)
            return angle_check and point_height_check
    # If ray and cone intersect, return intersection else return None
    def intersect(self, r: ray):
        # check if ray is inside cone
        if (self.incone(r.origin)):
            return intersection(r.origin, 0.0)
        else:
            # intersection between ray and cone's circle base
            final_point = circle(self.circ_center, -1.0 * self.axis, self.radius).intersect(r)
            # intersection between ray and cone's vertex
            ray_line = line(r.origin, r.dir)
            ray_vertex_t = ray_line.inline(r.origin, self.vertex)
            # find closest intersection between ray and cone's circle base, vertex
            if (ray_vertex_t is not None and (math.isclose(ray_vertex_t, 0, rel_tol = 0, abs_tol = err_tol) or ray_vertex_t > 0)):
                if ((final_point is None) or (ray_vertex_t < final_point.getlength())):
                    final_point = intersection(self.vertex, ray_vertex_t)        
            # check if ray is parallel to cone's lateral surface and goes through vertex
            if ((math.isclose(self.axis.getangle(r.dir), self.angle, rel_tol = 0, abs_tol = err_tol)
                or math.isclose(self.axis.getangle(r.dir), math.pi - self.angle, rel_tol = 0, abs_tol = err_tol))
                and ray_vertex_t is not None):
                # ray has infinite intersection with cone's lateral surface so the closest is either cone's vertex or with circle base
                return final_point
            else:
                # find closest intersection between ray and cone's lateral surface (infinite version)
                con_A = math.cos(self.angle)**2 * self.axis.dot(self.axis) * r.dir.dot(r.dir) - (self.axis.dot(r.dir))**2
                con_B = 2.0 * math.cos(self.angle)**2 * self.axis.dot(self.axis) * r.dir.dot(r.origin - self.vertex) - 2.0 * self.axis.dot(r.dir) * self.axis.dot(r.origin - self.vertex)
                con_C = math.cos(self.angle)**2 * self.axis.dot(self.axis) * (r.origin - self.vertex).dot(r.origin - self.vertex) - (self.axis.dot(r.origin - self.vertex))**2
                det = con_B**2 - 4.0 * con_A * con_C
                if ((not math.isclose(det, 0, rel_tol = 0, abs_tol = err_tol)) and det > 0):
                    first_t = (-1.0 * con_B - math.sqrt(det)) / (2.0 * con_A)
                    second_t = (-1.0 * con_B + math.sqrt(det)) / (2.0 * con_A)
                    lateral_final_point = None
                    # check if intersection is reachable and on cone
                    if (math.isclose(first_t, 0, rel_tol = 0, abs_tol = err_tol) or first_t > 0):
                        if (self.incone(r.origin + r.dir * first_t)):
                            lateral_final_point = intersection(r.origin + r.dir * first_t, first_t)
                    lateral_second_point = None
                    # check if intersection is reachable and on cone
                    if (math.isclose(second_t, 0, rel_tol = 0, abs_tol = err_tol) or second_t > 0):
                        if (self.incone(r.origin + r.dir * second_t)):
                            lateral_second_point = intersection(r.origin + r.dir * second_t, second_t)
                    if (lateral_second_point is not None):
                        if ((lateral_final_point is None) or lateral_second_point.getlength() < lateral_final_point.getlength()):
                            lateral_final_point = lateral_second_point
                    # find closest intersection between ray and cone's circle base, vertex, and lateral surface
                    if (lateral_final_point is not None):
                        if ((final_point is None) or lateral_final_point.getlength() < final_point.getlength()):
                            final_point = lateral_final_point
                    return final_point
                else:
                    return final_point
    # Similar to intersect, but return None if intersection is less than ray's length
    def bounded_intersect(self, r: ray):
        return r.reachable(self.intersect(r))

# test cases


# ray intersect only base
# r = ray(vector(0,-10,4), vector(0,1,0), 5)
# x = cone(vector(0,0,7), vector(0,0,-1), 2, 3)
# tc = test_intersection(1, r, x)
# print(tc)

# ray hits only vertex
# r = ray(vector(0,5,7), vector(0,-1,0), 10)
# x = cone(vector(0,0,7), vector(0,0,-1), 2, 3)
# tc = test_intersection(2, r, x)
# print(tc)

# ray hits vertex and base
# r = ray(vector(0,0,0), vector(0,0,1), math.inf)
# x = cone(vector(0,0,7), vector(0,0,-1), 2, 3)
# tc = test_intersection(3, r, x)
# print(tc)

# ray only hits lateral surface
# r = ray(vector(-5,0,6), vector(1,0,0), 2)
# x = cone(vector(0,0,7), vector(0,0,-1), 2, 3)
# tc = test_intersection(4, r, x)
# print(tc)

# ray intersect base and lateral surface
# r = ray(vector(0,-1,2), vector(0,1,1), math.inf)
# x = cone(vector(0,0,7), vector(0,0,-1), 2, 3)
# tc = test_intersection(5, r, x)
# print(tc)

# ray don't intersect
# r = ray(vector(0,0,0), vector(0,1,1), math.inf)
# x = cone(vector(0,0,7), vector(0,0,-1), 2, 3)
# tc = test_intersection(6, r, x)
# print(tc)

r = ray(vector(0,-2,-1), vector(0,1,4), math.inf)
x = cone(vector(0,0,7), vector(0,0,-1), 2, 3)
tc = test_intersection(3, r, x)
print(tc)








import math
import os
from vector import vector, intersection, ray, test_intersection
from quadrilateral import quad

err_tol = 1e-7

# definition of a parallelogram (filled)
class prism:
    def __init__(self, point: vector, base_vec1: vector, base_length1: float, base_vec2: vector, base_length2: float, height_vec: vector, height: float):
        self.point = point
        self.b_vec1 = (base_vec1 / base_vec1.length()) * base_length1
        self.b_vec2 = (base_vec2 / base_vec2.length()) * base_length2
        self.h_vec = (height_vec / height_vec.length()) * height
    def __str__(self):
        return "vertex {0} with base {1} by {2} and height {3}".format(self.point, self.b_vec1, self.b_vec2, self.h_vec)
    # Return True if point p is in prism else return False
    def inprism(self, p: vector):
        det = (self.b_vec1.getx() * self.b_vec2.gety() * self.h_vec.getz()
               + self.b_vec2.getx() * self.h_vec.gety() * self.b_vec1.getz()
               + self.h_vec.getx() * self.b_vec1.gety() * self.b_vec2.getz()
               - self.b_vec1.getz() * self.b_vec2.gety() * self.h_vec.getx()
               - self.b_vec2.getz() * self.h_vec.gety() * self.b_vec1.getx()
               - self.h_vec.getz() * self.b_vec1.gety() * self.b_vec2.getx())
        sol = p - self.point
        detx = (sol.getx() * self.b_vec2.gety() * self.h_vec.getz()
                + self.b_vec2.getx() * self.h_vec.gety() * sol.getz()
                + self.h_vec.getx() * sol.gety() * self.b_vec2.getz()
                - sol.getz() * self.b_vec2.gety() * self.h_vec.getx()
                - self.b_vec2.getz() * self.h_vec.gety() * sol.getx()
                - self.h_vec.getz() * sol.gety() * self.b_vec2.getx())
        dety = (self.b_vec1.getx() * sol.gety() * self.h_vec.getz()
                + sol.getx() * self.h_vec.gety() * self.b_vec1.getz()
                + self.h_vec.getx() * self.b_vec1.gety() * sol.getz()
                - self.b_vec1.getz() * sol.gety() * self.h_vec.getx()
                - sol.getz() * self.h_vec.gety() * self.b_vec1.getx()
                - self.h_vec.getz() * self.b_vec1.gety() * sol.getx())
        detz = (self.b_vec1.getx() * self.b_vec2.gety() * sol.getz()
                + self.b_vec2.getx() * sol.gety() * self.b_vec1.getz()
                + sol.getx() * self.b_vec1.gety() * self.b_vec2.getz()
                - self.b_vec1.getz() * self.b_vec2.gety() * sol.getx()
                - self.b_vec2.getz() * sol.gety() * self.b_vec1.getx()
                - sol.getz() * self.b_vec1.gety() * self.b_vec2.getx())
        solx = detx / det
        check_x = (math.isclose(solx, 0, rel_tol = 0, abs_tol = err_tol) or math.isclose(solx, 1, rel_tol = 0, abs_tol = err_tol) or (solx > 0 and solx < 1))
        soly = dety / det
        check_y = (math.isclose(soly, 0, rel_tol = 0, abs_tol = err_tol) or math.isclose(soly, 1, rel_tol = 0, abs_tol = err_tol) or (soly > 0 and soly < 1))
        solz = detz / det
        check_z = (math.isclose(solz, 0, rel_tol = 0, abs_tol = err_tol) or math.isclose(solz, 1, rel_tol = 0, abs_tol = err_tol) or (solz > 0 and solz < 1))
        print(solx, soly, solz)
        return check_x and check_y and check_z
    # If ray and prism intersect, return intersection else return None
    def intersect(self, r: ray):
        # defined each prism's eight vertex
        vertex1 = self.point
        vertex2 = self.point + self.b_vec1
        vertex3 = self.point + self.b_vec1 + self.b_vec2
        vertex4 = self.point + self.b_vec2
        vertex5 = self.point + self.h_vec
        vertex6 = self.point + self.h_vec + self.b_vec1
        vertex7 = self.point + self.h_vec + self.b_vec1 + self.b_vec2
        vertex8 = self.point + self.h_vec + self.b_vec2
        # intersection between ray and each prism's six face
        pri_face1 = quad(vertex1, vertex2, vertex3, vertex4).intersect(r)
        pri_face2 = quad(vertex5, vertex6, vertex7, vertex8).intersect(r)
        pri_face3 = quad(vertex1, vertex2, vertex6, vertex5).intersect(r)
        pri_face4 = quad(vertex4, vertex3, vertex7, vertex8).intersect(r)
        pri_face5 = quad(vertex1, vertex4, vertex8, vertex5).intersect(r)
        pri_face6 = quad(vertex2, vertex3, vertex7, vertex6).intersect(r)
        # find closest intersection
        final_point = None
        if (pri_face1 is not None):
            if ((final_point is None) or pri_face1.getlength() < final_point.getlength()):
                final_point = pri_face1
        if (pri_face2 is not None):
            if ((final_point is None) or pri_face2.getlength() < final_point.getlength()):
                final_point = pri_face2
        if (pri_face3 is not None):
            if ((final_point is None) or pri_face3.getlength() < final_point.getlength()):
                final_point = pri_face3
        if (pri_face4 is not None):
            if ((final_point is None) or pri_face4.getlength() < final_point.getlength()):
                final_point = pri_face4
        if (pri_face5 is not None):
            if ((final_point is None) or pri_face5.getlength() < final_point.getlength()):
                final_point = pri_face5
        if (pri_face6 is not None):
            if ((final_point is None) or pri_face6.getlength() < final_point.getlength()):
                final_point = pri_face6
        return final_point
    # Similar to intersect, but return None if intersection is less than ray's length
    def bounded_intersect(self, r: ray):
        return r.reachable(self.intersect(r))



# test cases

# r = ray(vector(2,4,1), vector(-1,-1,1), 3.5)
# x = prism(vector(0,0,0), vector(0,1,0), 5.0, vector(-1,0,0), 4.0, vector(0,0,1), 6.0)
# tc = test_intersection(1, r, x)
# print(tc)













import math
import os
from vector import vector, ray, intersection
from segment import segment
from triangle import triangle

err_tol = 1e-7

# definition of quadrilateral
class quad:
    def __init__(self, pointA: vector, pointB: vector, pointC: vector, pointD: vector):
        self.pointA = pointA
        self.pointB = pointB
        self.pointC = pointC
        self.pointD = pointD
    def __str__(self):
        return "A: {0}, B: {1}, C: {2}, D: {3}".format(self.pointA, self.pointB, self.pointC, self.pointD)
    def intersect(self, r: ray):
        # split quadrilateral at the >180 angle if exist
        Angle_a = math.acos((self.pointD - self.pointA).dot(self.pointB - self.pointA) /
                            ((self.pointD - self.pointA).length() * (self.pointB - self.pointA).length()))
        Angle_b = math.acos((self.pointA - self.pointB).dot(self.pointC - self.pointB) /
                            ((self.pointA - self.pointB).length() * (self.pointC - self.pointB).length()))
        Angle_c = math.acos((self.pointB - self.pointC).dot(self.pointD - self.pointC) /
                            ((self.pointB - self.pointC).length() * (self.pointD - self.pointC).length()))
        Angle_d = math.acos((self.pointC - self.pointD).dot(self.pointA - self.pointD) /
                            ((self.pointC - self.pointD).length() * (self.pointA - self.pointD).length()))
        if (math.isclose(-1.0 * Angle_a + Angle_b + Angle_c + Angle_d, 0, rel_tol = 0, abs_tol = err_tol)):
            first_tri = triangle(self.pointA, self.pointC, self.pointB)
            second_tri = triangle(self.pointA, self.pointC, self.pointD)
        elif (math.isclose(Angle_a - Angle_b + Angle_c + Angle_d, 0, rel_tol = 0, abs_tol = err_tol)):
            first_tri = triangle(self.pointB, self.pointD, self.pointA)
            second_tri = triangle(self.pointB, self.pointD, self.pointC)
        elif (math.isclose(Angle_a + Angle_b - Angle_c + Angle_d, 0, rel_tol = 0, abs_tol = err_tol)):
            first_tri = triangle(self.pointC, self.pointA, self.pointB)
            second_tri = triangle(self.pointC, self.pointA, self.pointD)
        else:
            first_tri = triangle(self.pointD, self.pointB, self.pointA)
            second_tri = triangle(self.pointD, self.pointB, self.pointC)
        # find closest intersection if exist
        final_point = first_tri.intersect(r)                    
        second_point = second_tri.intersect(r)
        if (isinstance(second_point, intersection)):
            if ((final_point is None) or second_point.getlength() < final_point.getlength()):
                final_point = second_point
        return final_point

# Check Cases
# r = ray(vector(0,0,0), vector(1,1,0), math.inf)
# x = quad(vector(5,1,0), vector(-2,4,0), vector(3,8,0), vector(4,7,0))
# print(x.intersect(r))




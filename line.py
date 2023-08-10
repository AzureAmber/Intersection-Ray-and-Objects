import math
import os
from vector import vector, ray, intersection

err_tol = 1e-7

# definition of line
class line:
    def __init__(self, point: vector, dir: vector):
        self.point = point
        self.dir = dir
    def getdirection(self):
        return self.dir
    def __str__(self):
        return "{0} + {1}t".format(self.point, self.dir)
    # If point is in line, returns a float t where point.line + dir.line * t = point else return None
    def inline(self, line_p: vector, p: vector):
        t = 0
        if (not math.isclose(self.dir.getx(), 0, rel_tol = 0, abs_tol = err_tol)):
            t = (p - line_p).getx() / self.dir.getx()
        elif (not math.isclose(self.dir.gety(), 0, rel_tol = 0, abs_tol = err_tol)):
            t = (p - line_p).gety() / self.dir.gety()
        elif (not math.isclose(self.dir.getz(), 0, rel_tol = 0, abs_tol = err_tol)):
            t = (p - line_p).getz() / self.dir.getz()
        else:
            # None: line has no direction
            return None
        if (line_p + self.dir * t == p):
            return t
        else:
            return None
    def intersect(self, r: ray):
        # check if ray and line are parallel
        if (self.dir.isparallel(r.dir)):
            # check if line and ray are separate
            if (self.inline(self.point, r.origin) is not None):
                return intersection(r.origin, 0.0)
            else:
                return None
        else:
            # line and ray intersect or skew
            result = r.origin - self.point
            
            detDa = -1.0 * self.dir.getx() * r.dir.gety() + self.dir.gety() * r.dir.getx()
            detSa = -1.0 * result.getx() * r.dir.gety() + result.gety() * r.dir.getx()
            detTa = self.dir.getx() * result.gety() - self.dir.gety() * result.getx()
            
            detDb = -1.0 * self.dir.getx() * r.dir.getz() + self.dir.getz() * r.dir.getx()
            detSb = -1.0 * result.getx() * r.dir.getz() + result.getz() * r.dir.getx()
            detTb = self.dir.getx() * result.getz() - self.dir.getz() * result.getx()
            
            detDc = -1.0 * self.dir.gety() * r.dir.getz() + self.dir.getz() * r.dir.gety()
            detSc = -1.0 * result.gety() * r.dir.getz() + result.getz() * r.dir.gety()
            detTc = self.dir.gety() * result.getz() - self.dir.getz() * result.gety()
            # check if line and ray are skew = no intersection
            s = 0
            t = 0
            if (not math.isclose(detDa, 0, rel_tol = 0, abs_tol = err_tol)):
                s = detSa / detDa
                t = detTa / detDa
                # None: line is skew (3D)
                if (not math.isclose(result.getz(), self.dir.getz() * s - r.dir.getz() * t, rel_tol = 0, abs_tol = err_tol)):
                    return None
            elif (not math.isclose(detDb, 0, rel_tol = 0, abs_tol = err_tol)):
                s = detSb / detDb
                t = detTb / detDb
                # None: line is skew (3D)
                if (not math.isclose(result.gety(), self.dir.gety() * s - r.dir.gety() * t, rel_tol = 0, abs_tol = err_tol)):
                    return None
            elif (not math.isclose(detDc, 0, rel_tol = 0, abs_tol = err_tol)):
                s = detSc / detDc
                t = detTc / detDc
                # None: line is skew (3D)
                if (not math.isclose(result.getx(), self.dir.getx() * s - r.dir.getx() * t, rel_tol = 0, abs_tol = err_tol)):
                    return None
            else:
                # None: segment is line (2D projection)
                return None
            # check if line is reachable by ray
            if (math.isclose(t, 0, rel_tol = 0, abs_tol = err_tol)
                or math.isclose(t, r.length / r.dir.length(), rel_tol = 0, abs_tol = err_tol)
                or (t > 0 and t < r.length / r.dir.length())):
                return intersection(r.origin + r.dir * t, t)
            else:
                return None        
    
# check cases

# not parallel intersect
# r = ray(vector(0,0,0), vector(0,0,1), math.inf)
# x = line(vector(0,-2,5), vector(0,1,1))
# print(x.intersect(r))

# parallel overlap
# r = ray(vector(0,0,0), vector(0,1,1), math.inf)
# x = line(vector(0,2,2), vector(0,3,3))
# print(x.intersect(r))

# parallel separate
# r = ray(vector(0,0,0), vector(0,1,1), math.inf)
# x = line(vector(0,2,3), vector(0,3,3))
# print(x.intersect(r))
















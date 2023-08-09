import math
import os
from vector import vector, ray, intersection

err_tol = 1e-7

# definition of segment
class segment:
    def __init__(self, start: vector, end: vector):
        self.start = start
        self.end = end
    def __str__(self):
        return "start: {0}, end: {1}".format(self.start, self.end)
    # intersection between ray and segment
    def intersect(self, r: ray):
        # check if ray and segment are parallel
        line_dir = self.end - self.start
        if (line_dir.isparallel(r.dir)):
            # check if segment and ray are separate
            toa = 0
            tob = 0
            tea = 0
            teb = 0
            if (not math.isclose(r.dir.getx(), 0, rel_tol = 0, abs_tol = err_tol)):
                toa = (self.start - r.origin).getx() / r.dir.getx()
                tob = (self.end - r.origin).getx() / r.dir.getx()
                tea = (self.start - r.end).getx() / r.dir.getx()
                teb = (self.end - r.end).getx() / r.dir.getx()
            elif (not math.isclose(r.dir.gety(), 0, rel_tol = 0, abs_tol = err_tol)):
                toa = (self.start - r.origin).gety() / r.dir.gety()
                tob = (self.end - r.origin).gety() / r.dir.gety()
                tea = (self.start - r.end).gety() / r.dir.gety()
                teb = (self.end - r.end).gety() / r.dir.gety()
            elif (not math.isclose(r.dir.getz(), 0, rel_tol = 0, abs_tol = err_tol)):
                toa = (self.start - r.origin).getz() / r.dir.getz()
                tob = (self.end - r.origin).getz() / r.dir.getz()
                tea = (self.start - r.end).getz() / r.dir.getz()
                teb = (self.end - r.end).getz() / r.dir.getz()
            else:
                # None: ray has no direction
                return None
            if (not (r.origin + r.dir * toa == self.start)):
                # None: segment and ray are parallel separate
                return None
            # segment and ray overlap so find closest intersection if exist
            if (math.isclose(toa, 0, rel_tol = 0, abs_tol = err_tol)
                or math.isclose(tob, 0, rel_tol = 0, abs_tol = err_tol)):
                return intersection(r.origin, 0.0)
            elif (toa < 0 and tob < 0):
                # None: segment is behind ray
                return None
            elif (toa < 0 or tob < 0):
                return intersection(r.origin, 0.0)
            elif ((not math.isclose(tea, 0, rel_tol = 0, abs_tol = err_tol))
                  and (not math.isclose(teb, 0, rel_tol = 0, abs_tol = err_tol))
                  and tea < 0 and teb < 0):
                if (toa < tob):
                    return intersection(self.start, toa)
                else:
                    return intersection(self.end, tob)
            elif tea < 0:
                return intersection(self.start, toa)
            elif teb < 0:
                return intersection(self.end, tob)
            elif (math.isclose(tea, 0, rel_tol = 0, abs_tol = err_tol)
                  or math.isclose(teb, 0, rel_tol = 0, abs_tol = err_tol)):
                return intersection(r.end, r.length / r.dir.length())
            else:
                # None: segment is far in front of ray
                return None
        else:
            result = r.origin - self.start
            
            detDa = -1.0 * line_dir.getx() * r.dir.gety() + line_dir.gety() * r.dir.getx()
            detSa = -1.0 * result.getx() * r.dir.gety() + result.gety() * r.dir.getx()
            detTa = line_dir.getx() * result.gety() - line_dir.gety() * result.getx()
            
            detDb = -1.0 * line_dir.getx() * r.dir.getz() + line_dir.getz() * r.dir.getx()
            detSb = -1.0 * result.getx() * r.dir.getz() + result.getz() * r.dir.getx()
            detTb = line_dir.getx() * result.getz() - line_dir.getz() * result.getx()
            
            detDc = -1.0 * line_dir.gety() * r.dir.getz() + line_dir.getz() * r.dir.gety()
            detSc = -1.0 * result.gety() * r.dir.getz() + result.getz() * r.dir.gety()
            detTc = line_dir.gety() * result.getz() - line_dir.getz() * result.gety()
            # check if segment and ray are skew = no intersection
            s = 0
            t = 0
            if (not math.isclose(detDa, 0, rel_tol = 0, abs_tol = err_tol)):
                s = detSa / detDa
                t = detTa / detDa
                # None: segment is skew (3D)
                if (not math.isclose(result.getz(), line_dir.getz() * s - r.dir.getz() * t, rel_tol = 0, abs_tol = err_tol)):
                    return None
            elif (not math.isclose(detDb, 0, rel_tol = 0, abs_tol = err_tol)):
                s = detSb / detDb
                t = detTb / detDb
                # None: segment is skew (3D)
                if (not math.isclose(result.gety(), line_dir.gety() * s - r.dir.gety() * t, rel_tol = 0, abs_tol = err_tol)):
                    return None
            elif (not math.isclose(detDc, 0, rel_tol = 0, abs_tol = err_tol)):
                s = detSc / detDc
                t = detTc / detDc
                # None: segment is skew (3D)
                if (not math.isclose(result.getx(), line_dir.getx() * s - r.dir.getx() * t, rel_tol = 0, abs_tol = err_tol)):
                    return None
            else:
                # None: segment is skew (2D projection)
                return None
            # segment and ray intersect so check if intersection lies in segment
            if ((math.isclose(s, 0, rel_tol = 0, abs_tol = err_tol)
                    or math.isclose(s, 1, rel_tol = 0, abs_tol = err_tol)
                    or (s > 0 and s < 1))
                and (math.isclose(t, 0, rel_tol = 0, abs_tol = err_tol)
                        or math.isclose(t, r.length, rel_tol = 0, abs_tol = err_tol)
                        or (t > 0 and t < r.length))):
                return intersection(r.origin + r.dir * t, t)
            else:
                # None: intersection not in segment
                return None



# Check Cases

# parallel separate
# r = ray(vector(0,0,0), vector(1,1,2), math.inf)
# s = segment(vector(2, 3, 4), vector(0, 1, 0))
# print(s.intersect(r))

# parallel overlap hit
# r = ray(vector(0,0,0), vector(3,4,12), 39)
# s = segment(vector(6, 8, 24), vector(15, 20, 60))
# print(s.intersect(r))

# parallel overlap inside
# r = ray(vector(12,16,48), vector(3,4,12), 13)
# s = segment(vector(6, 8, 24), vector(30, 40, 120))
# print(s.intersect(r))

# parallel overlap outside behind
# r = ray(vector(0,0,0), vector(3,4,12), 13)
# s = segment(vector(-6, -8, -24), vector(-30, -40, -120))
# print(s.intersect(r))

# parallel overlap outside front far
# r = ray(vector(0,0,0), vector(3,4,12), 13)
# s = segment(vector(3.003, 4.004, 12.012), vector(9, 12, 36))
# print(s.intersect(r))

# skew
# r = ray(vector(0,0,0), vector(1,1,1), math.inf)
# s = segment(vector(1, -1, 1), vector(-1, 1, 2))
# print(s.intersect(r))

# hit segment above
# r = ray(vector(0,0,0), vector(0,0,1), 5)
# s = segment(vector(0, -1, 3.5), vector(0, 4, 3.5))
# print(s.intersect(r))

# hit segment below
# r = ray(vector(0,0,0), vector(0,0,-1), 5)
# s = segment(vector(0, -1, -5), vector(0, 4, -5))
# print(s.intersect(r))

# hit segment right
# r = ray(vector(0,0,0), vector(0,1,0), 5)
# s = segment(vector(0, 4, -5), vector(0, 4, 10))
# print(s.intersect(r))

# hit segment left
# r = ray(vector(0,0,0), vector(0,-1,0), 5)
# s = segment(vector(0, -1.5, -2), vector(0, -1.5, 3))
# print(s.intersect(r))

# hit segment front
# r = ray(vector(0,0,0), vector(1,0,0), 5)
# s = segment(vector(3.5, -1, 0), vector(3.5, 1, 0))
# print(s.intersect(r))

# hit segment back
# r = ray(vector(0,0,0), vector(-1,0,0), 5)
# s = segment(vector(-0.5, -3, 0), vector(-0.5, 1, 0))
# print(s.intersect(r))

# hit diagonal
# (1,2,3) - (2.1, 4.2, 2.1) + (2,4,6)
# r = ray(vector(0,0,0), vector(1,2,1), 5)
# s = segment(vector(1.1, 2.2, -0.9), vector(4.1, 8.2, 8.1))
# print(s.intersect(r))

# not hit diagonal (segment not on sight)
# (2.1, 4.2, 2.1) + (2,4,6) + (5,10,15)
# r = ray(vector(0,0,0), vector(1,2,1), 5)
# s = segment(vector(4.1, 8.2, 8.2), vector(7.1, 14.2, 17.1))
# print(s.intersect(r))

# not hit diagonal (segment too far away)
# (1,2,3) - (6.5, 13, 6.5) + (2,4,6)
# r = ray(vector(0,0,0), vector(1,2,1), 5)
# s = segment(vector(5.5, 11, 3.5), vector(8.5, 17, 12.5))
# print(s.intersect(r))












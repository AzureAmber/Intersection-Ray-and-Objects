import math
import os
from vector import vector, ray, intersection
from line import line

err_tol = 1e-7

# definition of segment
class segment:
    def __init__(self, start: vector, end: vector):
        self.start = start
        self.end = end
    def __str__(self):
        return "start: {0}, end: {1}".format(self.start, self.end)
    def insegment(self, p: vector):
        # check if point is in line and between segment's endpoints
        seg_line = line(self.start, self.end - self.start)
        s = seg_line.inline(self.start, p)
        return s is not None and (math.isclose(s, 0, rel_tol = 0, abs_tol = err_tol)
                                  or math.isclose(s, 1, rel_tol = 0, abs_tol = err_tol)
                                  or (s > 0 and s < 1))
    def intersect(self, r: ray):
        # check if ray and segment are parallel
        line_dir = self.end - self.start
        if (line_dir.isparallel(r.dir)):
            # check if segment and ray are separate
            r_line = line(r.origin, r.dir)
            toa = r_line.inline(r.origin, self.start)
            tob = r_line.inline(r.origin, self.end)
            tea = r_line.inline(r.end, self.start)
            teb = r_line.inline(r.end, self.end)
            if (toa is None):
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
            # ray and segment are skew or intersect
            seg_line = line(self.start, line_dir)
            seg_line_intersect = seg_line.intersect(r)
            # check if ray and line containing segment intersect
            if (seg_line_intersect is not None):
                # intersection exist in line containing segment so check if intersection lies in segment
                if (self.insegment(seg_line_intersect.getpoint())):
                    return seg_line_intersect
                else:
                    return None
            else:
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
# r = ray(vector(0,0,0), vector(1,2,1), 10)
# s = segment(vector(1.1, 2.2, -0.9), vector(4.1, 8.2, 8.1))
# print(s.intersect(r))

# not hit diagonal (segment not on sight)
# (2.1, 4.2, 2.1) + (2,4,6) + (5,10,15)
# r = ray(vector(0,0,0), vector(1,2,1), math.inf)
# s = segment(vector(4.1, 8.2, 8.2), vector(7.1, 14.2, 17.1))
# print(s.intersect(r))

# not hit diagonal (segment too far away)
# (1,2,3) - (6.5, 13, 6.5) + (2,4,6)
# r = ray(vector(0,0,0), vector(1,2,1), 5)
# s = segment(vector(5.5, 11, 3.5), vector(8.5, 17, 12.5))
# print(s.intersect(r))












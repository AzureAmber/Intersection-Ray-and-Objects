import math
import os
from vector import vector, intersection, ray, test_intersection
from line import line

err_tol = 1e-7

# definition of segment
class segment:
    def __init__(self, start: vector, end: vector):
        self.start = start
        self.end = end
    def __str__(self):
        return "start: {0}, end: {1}".format(self.start, self.end)
    # Return True if point p inside segment else return False
    def insegment(self, p: vector):
        # check if point is in line and between segment's endpoints
        seg_line = line(self.start, self.end - self.start)
        s = seg_line.inline(self.start, p)
        return s is not None and (math.isclose(s, 0, rel_tol = 0, abs_tol = err_tol)
                                  or math.isclose(s, 1, rel_tol = 0, abs_tol = err_tol)
                                  or (s > 0 and s < 1))
    # If ray intersect segment, then return intersection else return None
    def intersect(self, r: ray):
        # check if ray and segment are parallel
        line_dir = self.end - self.start
        if (line_dir.isparallel(r.dir)):
            # check if segment and ray are separate
            r_line = line(r.origin, r.dir)
            toa = r_line.inline(r.origin, self.start)
            tob = r_line.inline(r.origin, self.end)
            if (toa is None):
                # None: segment and ray are parallel separate
                return None
            else:
                # segment and ray overlap so find closest intersection if exist
                if (math.isclose(toa, 0, rel_tol = 0, abs_tol = err_tol)
                    or math.isclose(tob, 0, rel_tol = 0, abs_tol = err_tol)):
                    # ray is on segment
                    return intersection(r.origin, 0.0)
                elif (toa > 0 and tob > 0):
                    # segment in front of ray
                    final_t = min(toa, tob)
                    return intersection(r.origin + r.dir * final_t, final_t)
                elif (toa < 0 and tob < 0):
                    # segment behind ray
                    return None
                else:
                    # ray inside segment
                    return intersection(r.origin, 0.0)
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
    # Similar to intersect, but return None if intersection is less than ray's length
    def bounded_intersect(self, r: ray):
        return r.reachable(self.intersect(r))

# Check Cases

# parallel separate
# r = ray(vector(0,0,0), vector(1,1,2), math.inf)
# x = segment(vector(2, 3, 4), vector(0, 1, 0))
# tc = test_intersection(1, r, x)
# print(tc)

# parallel overlap hit
# r = ray(vector(0,0,0), vector(3,4,12), 39)
# x = segment(vector(6, 8, 24), vector(15, 20, 60))
# tc = test_intersection(2, r, x)
# print(tc)

# parallel overlap inside
# r = ray(vector(12,16,48), vector(3,4,12), 13)
# x = segment(vector(6, 8, 24), vector(30, 40, 120))
# tc = test_intersection(3, r, x)
# print(tc)

# parallel overlap outside behind
# r = ray(vector(0,0,0), vector(3,4,12), 13)
# x = segment(vector(-6, -8, -24), vector(-30, -40, -120))
# tc = test_intersection(4, r, x)
# print(tc)

# parallel overlap outside front far
# r = ray(vector(0,0,0), vector(3,4,12), 13)
# x = segment(vector(3.003, 4.004, 12.012), vector(9, 12, 36))
# tc = test_intersection(5, r, x)
# print(tc)

# skew
# r = ray(vector(0,0,0), vector(1,1,1), math.inf)
# x = segment(vector(1, -1, 1), vector(-1, 1, 2))
# tc = test_intersection(6, r, x)
# print(tc)

# hit segment above
# r = ray(vector(0,0,0), vector(0,0,1), 5)
# x = segment(vector(0, -1, 3.5), vector(0, 4, 3.5))
# tc = test_intersection(7, r, x)
# print(tc)

# hit segment below
# r = ray(vector(0,0,0), vector(0,0,-1), 5)
# x = segment(vector(0, -1, -5), vector(0, 4, -5))
# tc = test_intersection(8, r, x)
# print(tc)

# hit segment right
# r = ray(vector(0,0,0), vector(0,1,0), 5)
# x = segment(vector(0, 4, -5), vector(0, 4, 10))
# tc = test_intersection(9, r, x)
# print(tc)

# hit segment left
# r = ray(vector(0,0,0), vector(0,-1,0), 5)
# x = segment(vector(0, -1.5, -2), vector(0, -1.5, 3))
# tc = test_intersection(10, r, x)
# print(tc)

# hit segment front
# r = ray(vector(0,0,0), vector(1,0,0), 5)
# x = segment(vector(3.5, -1, 0), vector(3.5, 1, 0))
# tc = test_intersection(11, r, x)
# print(tc)

# hit segment back
# r = ray(vector(0,0,0), vector(-1,0,0), 5)
# x = segment(vector(-0.5, -3, 0), vector(-0.5, 1, 0))
# tc = test_intersection(12, r, x)
# print(tc)

# hit diagonal
# (1,2,3) - (2.1, 4.2, 2.1) + (2,4,6)
# r = ray(vector(0,0,0), vector(1,2,1), 10)
# x = segment(vector(1.1, 2.2, -0.9), vector(4.1, 8.2, 8.1))
# tc = test_intersection(13, r, x)
# print(tc)

# not hit diagonal (segment not on sight)
# (2.1, 4.2, 2.1) + (2,4,6) + (5,10,15)
# r = ray(vector(0,0,0), vector(1,2,1), math.inf)
# x = segment(vector(4.1, 8.2, 8.2), vector(7.1, 14.2, 17.1))
# tc = test_intersection(14, r, x)
# print(tc)

# not hit diagonal (segment too far away)
# (1,2,3) - (6.5, 13, 6.5) + (2,4,6)
# r = ray(vector(0,0,0), vector(1,2,1), 5)
# x = segment(vector(5.5, 11, 3.5), vector(8.5, 17, 12.5))
# tc = test_intersection(15, r, x)
# print(tc)












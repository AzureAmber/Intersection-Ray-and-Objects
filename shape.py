import math
import os
from vector import matrix, vector, intersection, ray, test_intersection
from triangle import triangle
from sphere import sphere

# generates a list of triangles that create a sphere 
def generate_points(c: vector, r: float, num_h: int, num_r: int):
    result = []
    p = vector(0, -1.0 * r, 0)
    result.append([p+c])
    for i in range(num_h):
        temp = []
        mid = p + vector(0, 1, 0) * (2.0 * r / (num_h + 1)) * (i+1)
        for j in range(num_r):
            m = matrix([math.cos(2.0 * math.pi / num_r * j), 0, -1.0 * math.sin(2.0 * math.pi / num_r * j), 0],
                       [0, 1, 0, 0],
                       [math.sin(2.0 * math.pi / num_r * j), 0, math.cos(2.0 * math.pi / num_r * j), 0],
                       [0, 0, 0, 1])
            new_d = vector(1, 0, 0).matmult(m)
            t = -1.0 * mid.dot(new_d) + math.sqrt(mid.dot(new_d)**2 - mid.dot(mid) + r**2)
            cur_p = mid + new_d * t
            temp.append(cur_p+c)
        result.append(temp)
    p = vector(0, r, 0)
    result.append([p+c])
    return(result)

def create_triangles(x: list):
    result = []
    for i in range(len(x) - 2):
        psize = len(x[i])
        csize = len(x[i+1])
        fsize = len(x[i+2])
        for j in range(csize):
            result.append(triangle(x[i+1][j % csize],
                                   x[i+1][(j+1) % csize],
                                   x[i][j % psize]))
            result.append(triangle(x[i+1][j % csize],
                                   x[i+1][(j+1) % csize],
                                   x[i+2][(j+1) % fsize]))
    return(result)
            
x = generate_points(vector(0,10,-50), 5, 17, 36)
y = create_triangles(x)




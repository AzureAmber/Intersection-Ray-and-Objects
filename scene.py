import math
import os
from vector import matrix, vector, intersection, ray, test_intersection
from perspective import camera
from tkinter import *

# screen dimensions
scr_width = 1280
scr_height = 720

# canvas
root = Tk()
root.geometry("1280x720")
scr = Canvas(root, width = scr_width, height = scr_height, bg = 'white')
scr.pack()

# camera
cam_x = 0.0
cam_y = 0.0
cam_z = 0.0
x = camera(cam_x, cam_y, cam_z, 120 * math.pi / 180, scr_width, scr_height, 0.01, 1000.0)

# create shape
pointa = vector(-20, 20, -200)
pointb = vector(0, 40, -200)
pointc = vector(20, 30, -200)

pointa_scr = x.screen_coord(pointa)
pointb_scr = x.screen_coord(pointb)
pointc_scr = x.screen_coord(pointc)
points = [pointa_scr.getx(), pointa_scr.gety(), pointb_scr.getx(), pointb_scr.gety(), pointc_scr.getx(), pointc_scr.gety()]
geoobj = scr.create_polygon(points, outline = 'red', fill = 'black', width = 2)

def update():
    pointa_scr = x.screen_coord(pointa)
    pointb_scr = x.screen_coord(pointb)
    pointc_scr = x.screen_coord(pointc)
    # print(pointa_scr, pointb_scr, pointc_scr)
    if (pointa_scr is not None and pointb_scr is not None and pointc_scr is not None):
        points = [pointa_scr.getx(), pointa_scr.gety(), pointb_scr.getx(), pointb_scr.gety(), pointc_scr.getx(), pointc_scr.gety()]
        scr.coords(geoobj, points)

# user controls
def left(event):
    x.update_x(-5.0)
    update()
def right(event):
    x.update_x(5.0)
    update()
def up(event):
    x.update_z(-5.0)
    update()
def down(event):
    x.update_z(5.0)
    update()
def key_press(event):
    if (event.keysym == 'a'):
        x.update_roth(-1.0 * 10 * math.pi / 180)
    elif (event.keysym == 'd'):
        x.update_roth(10 * math.pi / 180)
    elif (event.keysym == 'w'):
        x.update_rotv(10 * math.pi / 180)
    elif (event.keysym == 's'):
        x.update_rotv(-1.0 * 10 * math.pi / 180)
    update()

root.bind("<Left>", left)
root.bind("<Right>", right)
root.bind("<Up>", up)
root.bind("<Down>", down)
root.bind("<Key>", key_press)

update()

# execute
root.mainloop()





















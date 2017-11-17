#!/usr/bin/python3
from itertools import chain
from math import sin,cos,pi
import apple410

axiom = list("LFL+F+LFL")

rules = { 'L' : list("-RF+LFL+FR-"),
          'R' : list("+LF-RFR-FL+") }

def L_repl(c):
    global rules
    r = rules.get(c)
    if r:
        return r
    return [c]

def L_iter(system):
    a = map(L_repl,system)
    return list(chain.from_iterable(a))

def L_sys(system,depth):
    l = axiom
    for i in range(depth):
        l = L_iter(l)
    return l

seq=L_sys(axiom,5)

direction = 0.0
theta = (pi/2)
distance = 16
location = (452.0,451.0)

def move(pos,angle,distance):
    nx = pos[0] + sin(angle)*distance
    ny = pos[1] + cos(angle)*distance
    return (nx,ny)

a = apple410.Apple410('/dev/ttyUSB0')
a.pen_select(2)
a.move_to(location)

for e in seq:
    if e == 'F':
        nl = move(location, direction, distance)
        a.draw_to(nl)
        print("DA {}".format(nl))
        location = nl
    elif e == '+':
        direction = direction + theta
    elif e == '-':
        direction = direction - theta


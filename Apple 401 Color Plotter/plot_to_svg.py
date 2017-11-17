#!/usr/bin/python3
import sys
import svgwrite
import math

d = svgwrite.Drawing(profile='tiny')


def getnum(line):
    pass

def coordlist(line,expected=-1):
    l = list(map(float,line.split(',')))
    if expected > -1:
        assert len(l) == expected
    return l

pens = [
    svgwrite.rgb(0, 0, 0, '%'),
    svgwrite.rgb(100, 0, 0, '%'),
    svgwrite.rgb(0, 100, 0, '%'),
    svgwrite.rgb(0, 0, 100, '%') ]

pennum = 0
pos = (0.0,0.0)
text_rotation = 0.0
text_size = 1
# "viewport"? part of the page to plot on
vp = (0.0,0.0,2394,1759)
# virtual size for viewport
wd = (0.0,0.0,2394,1759)

def tcoord(x, vpl, vph, wdl, wdh):
    vpw = vph-vpl
    wdw = wdh-wdl
    nx = vpw*(x/wdw)
    return nx + vpl

def transform1(x):
    vpw = vp[2]-vp[0]
    wdw = wd[2]-wd[0]
    nx = vpw*(x/wdw)
    return nx

def transform(x,y):
    nx = tcoord(x,vp[0],vp[2],wd[0],wd[2])
    ny = tcoord(y,vp[1],vp[3],wd[1],wd[3])
    return nx, ny

for line in sys.stdin.readlines():
    line = line.strip()
    cmd = line[0:2]
    line = line[2:].strip()
    if cmd == 'MA':
        l=coordlist(line,2)
        pos=transform(l[0],l[1])
    elif cmd == 'VP': #viewport?
        l=coordlist(line,4)
        vp=(l[0],l[1],l[2],l[3])
    elif cmd == 'WD': 
        l=coordlist(line,4)
        wd=(l[0],l[1],l[2],l[3])
    elif cmd == 'DA':
        l=coordlist(line)
        while len(l) > 0:
            nextp = transform(l[0],l[1])
            l = l[2:]
            d.add(d.line(pos,nextp,stroke=pens[pennum]))
            pos = nextp
    elif cmd == 'CA': #circle
        l=coordlist(line)
        r=transform1(l[0])
        p=transform(l[1],l[2])
        c=d.circle(center=p,r=r)
        c.fill(opacity=0)
        c.stroke(color=pens[pennum],opacity=100,width=2)
        d.add(c)
    elif cmd == 'AC': #arc
        l=coordlist(line)
        r=transform1(l[0])
        p=transform(l[3],l[4])
        t2, t1 = math.radians(l[1]),math.radians(l[2])
        x1, y1 = p[0] + (r*math.cos(t1)), p[1] + (r*math.sin(t1))
        x2, y2 = p[0] + (r*math.cos(t2)), p[1] + (r*math.sin(t2))
        ds="M {} {} A {} {} 0 0 0 {} {}".format(x1,y1,r,r,x2,y2)
        path=d.path(
            d=ds,
            stroke=pens[pennum])
        path.fill(opacity=0)
        d.add(path)
    elif cmd == 'LR':
        text_rotation = float(line)
    elif cmd == 'LS':
        text_size = float(line)
    elif cmd == 'PS':
        pennum = int(line) - 1
        #print("Switching to pen {}".format(pennum))
    elif cmd == 'PL':
        t = d.text(line,insert=pos)
        t.rotate(text_rotation,center=pos)
        d.add(t)
        pass
    else:
        #print("Command {}".format(cmd))
        pass

d.write(sys.stdout)

    
    
    
    

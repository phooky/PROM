#!/usr/bin/python

# Convert BDF file to tinyfont representation as used in
# fbpad.

import sys
import os.path
import struct

def readc(f):
    t = ['']
    while t[0] != 'STARTCHAR':
        t = inf.readline().split()
    id = int(t[1][2:],16)
    while t[0] != 'BBX':
        t = inf.readline().split()
    width = int(t[1])
    height = int(t[2])
    while t[0] != 'BITMAP':
        t = inf.readline().split()
    data = []
    t = inf.readline().split()
    while t[0] != 'ENDCHAR':
        data.append(int(t[0],16))
        t = inf.readline().split()
    return (id, data, width,height)

if __name__ == '__main__':
    path = sys.argv[1]
    if not os.path.isfile(path):
        sys.exit(1)
    outpath = os.path.split(path)[1].split('.')[0] + '.tf'
    inf = open(path,"r")
    maxw = 0
    maxh = 0
    chars = []
    count = 0
    while True:
        t = inf.readline().split()
        if t[0] == 'CHARS':
            count = int(t[1])
            break
    
    # Read chars
    for _ in range(count):
        (id, data, width, height) = readc(inf)
        maxw = max(maxw, width)
        maxh = max(maxh, height)
        chars.append((id,data))
        
    print("W:{} H:{} COUNT:{}".format(maxw, maxh, count))

    outf = open(outpath,"wb")

    outf.write('tinyfont')
    outf.write(struct.pack('<IIII',0,count,maxh,maxw))
    for (id,_) in chars:
        outf.write(struct.pack('<I',id))
    for (_,data) in chars:
        d = ''
        for row in data:
            for i in range(maxw):
                if ( (1<< ((maxw-1)-i) ) & row ):
                    d = d + '\xff'
                else:
                    d = d + '\x00'
        outf.write(d)
    outf.close()
    
        
        

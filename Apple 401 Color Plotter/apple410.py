#!/usr/bin/python3
import serial
import time
import sys

class Apple410:
    """A simple class for queing up commands for the Apple 410"""
    def __init__(self, portname, baud=1200):
        self.serial = serial.Serial(portname, baud, rtscts=True, dsrdtr=True, timeout=0.1)
        self.pos = (0,0)
        self.wd = self.vp = (0,0,2394,1759)

    def sendchar(self, c):
        self.serial.flush()
        while not self.serial.cts:
            time.sleep(0.1)
        while not self.serial.dsr:
            time.sleep(0.1)
        self.serial.write(c.encode('ascii'))
        
    def send(self, command):
        for c in command:
            self.sendchar(c)
        self.sendchar('\x03')

    def move_to(self, coords):
        self.send('MA{},{}'.format(coords[0],coords[1]))
        self.pos = coords

    def draw_to(self, coords):
        self.send('DA{:.2f},{:.2f}'.format(coords[0],coords[1]))
        self.pos = coords
            
    def pen_select(self, index):
        self.send('PS{}'.format(index))
    
if __name__ == '__main__':
    scr = 'test_script.cmds'
    if len(sys.argv) > 1:
        scr = sys.argv[1]
    print("Running file {}".format(scr))
    a = Apple410('/dev/ttyUSB0')
    if scr == "-":
        f = sys.stdin
    else:
        f = open(scr)
    for line in f.readlines():
        print("SENDING: {}".format(line.strip()))
        a.send(line.strip())
    

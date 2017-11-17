#!/usr/bin/python3
import sys

st_start = 0x94b

assert len(sys.stdin.buffer.read(st_start)) == st_start

while 1:
    cmdlen = ord(sys.stdin.buffer.read(1))
    if cmdlen == 0:
        break
    cmd = sys.stdin.buffer.read(cmdlen)
    if cmd[-1] != 3:
        print("Invalid entry")
        break
    else:
        print(cmd[0:-1].decode('ascii'))
        



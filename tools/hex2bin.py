#!/usr/bin/python
import sys

lines = sys.stdin.readlines()

for line in lines:
    bytes = map(lambda x:int(x,16), line.split())
    for b in bytes:
        sys.stdout.write(chr(b))



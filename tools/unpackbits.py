#!/usr/bin/python
import sys

skip = int(sys.argv[1])
count = int(sys.argv[2])
sys.stdin.read(skip)

while True:
    r = sys.stdin.read(1)
    if not r:
        break
    n = ord(r[0])
    if n < 128:
        sys.stderr.write("COPY "+str(n+1)+"\n")
        sys.stdout.write(sys.stdin.read(n+1))
    elif n == 128:
        sys.stderr.write("SKIP\n")
        pass
    elif n < 256:
        count = (256-n) + 1
        sys.stderr.write("RPT "+str(count)+"\n")
        r = sys.stdin.read(1)
        for i in range(count):
            sys.stdout.write(r)
    else:
        sys.stderr.write("ERROR- VAL OUT OF RANGE\n")

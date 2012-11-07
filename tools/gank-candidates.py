#!/usr/bin/python

import sys

bytes=eval(sys.argv[1])

print "looking for ",bytes

idx = 0

prefix="candidate"

candidateTab=[]

allbytes = sys.stdin.read()

found=allbytes.find(bytes)
while found != -1:
    candidateTab.append(found)
    path=prefix+str(idx)
    out = open(path,'wb')
    out.write(allbytes[found:])
    print found, path
    out.close()
    idx = idx + 1
    found=allbytes.find(bytes,found+1)


    

#!/usr/bin/python
import sys
import Image

buf = sys.stdin.read()

# rearrange buf into parallel columns
cols=128
w=8*cols
h=128*256/cols
img = Image.new("1",(w,h))

for c in range(cols):
    colimg = Image.fromstring("1",(8,h),buf[c*h:(c+1)*h])
    img.paste(colimg,(8*c,0))

img.save(sys.argv[1])



#!/usr/bin/python
import sys
import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cwidth",help="character width in pixels",type=int,default=8)
parser.add_argument("--cheight",help="character height in pixels",type=int,default=8)
parser.add_argument("--count",help="character count",type=int,default=128)
parser.add_argument("--skip",help="skip bytes",type=int,default=0)
parser.add_argument("--rotated",help="mark as rotated",action="store_true",default=False)

parser.add_argument("outfile")

args=parser.parse_args()

buf = sys.stdin.read()[args.skip:]

cw = args.cwidth
ch = args.cheight
r = args.rotated

w=args.cwidth * args.count
h=args.cheight

print args.cheight
img = Image.new("1",(w,h))

x = 0
y = 0
for b in buf:
    idx = y+(x*ch)
    colimg = Image.fromstring("1",(cw,1),buf[idx:idx+1])
    img.paste(colimg,(x*cw,y))
    y = y+1
    if y >= ch:
        y = 0
        x = x + 1

img.save(args.outfile)



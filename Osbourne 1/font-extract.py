#!/usr/bin/python
import sys
import Image


buf = sys.stdin.read()

# rearrange buf into parallel columns
cols = 1
bitw = 1024
imgw = cols * bitw
imgh = len(buf)/(cols*bitw/8)

print imgw, imgh, len(buf)

img = Image.new("1",(imgw,imgh))

for c in range(cols):
    colimg = Image.fromstring("1",(bitw,imgh),buf[c*imgh*(bitw/8):(c+1)*imgh*(bitw/8)])
    img.paste(colimg,(bitw*c,0))

img.save("eprom-font.png")


# Create BDF file
f = open("eprom-font.bdf","w")
f.write("""STARTFONT 2.1
FONT -osbourne-charrom-medium-r-normal--16-160-75-75-c-80-iso10646-1
SIZE 16 75 75
FONTBOUNDINGBOX 8 10 0 -2
STARTPROPERTIES 2
FONT_ASCENT 7
FONT_DESCENT 2
ENDPROPERTIES
CHARS 128""")

for i in range(128):
    f.write("""
STARTCHAR U+{0:04X}
ENCODING {0:d}
SWIDTH 500 0
DWIDTH 8 0
BBX 8 10 0 -2
BITMAP
""".format(i))
    for j in range(10):
        offset = 128*j + i
        f.write("{0:02X}\n".format(ord(buf[offset])))
    f.write("ENDCHAR")

f.write("\nENDFONT\n")
f.close()

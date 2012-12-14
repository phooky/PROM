#!/usr/bin/python
import sys
import Image


buf = sys.stdin.read()

# Start of first byte of table
start = 0x7711
startchar = 0x20 # starts with space
charw = 5
charh = 8
endchar = 0x7e
charcnt = (endchar - startchar) + 1
imgw = charw * charcnt
imgh = charh

print imgw, imgh, len(buf)

baseImg = Image.fromstring("1",(charh,imgw),buf[start:start+imgw])
img = baseImg.transpose(Image.ROTATE_90)
img.save("eprom-font.png")


# Create BDF file
f = open("eprom-font.bdf","w")
f.write("""STARTFONT 2.1
FONT -osbourne-charrom-medium-r-normal--16-160-75-75-c-80-iso10646-1
SIZE 16 75 75
FONTBOUNDINGBOX 8 8 0 0
STARTPROPERTIES 2
FONT_ASCENT 7
FONT_DESCENT 1
ENDPROPERTIES
CHARS {0}""".format(charcnt))

for i in range(charcnt):
    left = i * charw
    charImg = img.crop((left,0,left+charw,charh))
    f.write("""
STARTCHAR U+{0:04X}
ENCODING {0:d}
SWIDTH 500 0
DWIDTH 8 0
BBX 8 8 0 0
BITMAP
""".format(i+startchar))
                       
    d = list(charImg.getdata())
    for j in range(charh):
        line = reduce(lambda x,y: (x<<1)+(y&0x01), d[j*charw:(j+1)*charw],0)
        f.write("{0:02X}\n".format(line))
    f.write("ENDCHAR")

f.write("\nENDFONT\n")
f.close()

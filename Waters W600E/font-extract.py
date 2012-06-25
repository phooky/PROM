#!/usr/bin/python
import sys
import Image

off = ((1896/8) * 256) - 6
chars = (16*6) + 9

f = open(sys.argv[1])
f.seek(off)

# height in bytes
height = 16

buf = f.read(chars * height)

print "chars", chars, "buflen ", len(buf)
ob = open("eprom-font.bin","wb")
ob.write(buf)
ob.close()

oc = open("eprom-font.c","w")
oc.write("#include <stdint.h>\n\n")
oc.write("const unsigned uint8_t eprom_font[{0}] = {{\n".format(len(buf)))
for i in range(0,len(buf),16):
    oc.write(",".join(map(lambda x:hex(ord(x)),buf[i:i+16])))
    oc.write("\n")
oc.write("};\n\n")

charstr = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~\xB1\xB2\xDB\xCD\xBA\xC9\xBB\xC8\xBC\x9C"
charmap = [0] * 256
coff = 0
for c in charstr:
    charmap[ord(c)] = coff
    coff = coff + 16

oc.write("const unsigned uint16_t eprom_map[256] = {\n")
for i in range(0,len(charmap),16):
    oc.write(",".join(map(hex,charmap[i:i+16])))
    oc.write(",\n")
oc.write("};\n")


# rearrange buf into parallel columns
imgh = 16 * 16
cols = ((chars -1) / 16) +1
imgw = cols * 8

img = Image.new("1",(imgw,imgh))

buf = buf + 'a' * ((imgw*imgh) - len(buf))
for c in range(cols):
    colimg = Image.fromstring("1",(8,imgh),buf[c*imgh:(c+1)*imgh])
    img.paste(colimg,(8*c,0))

img.save("eprom-font.png")


# Create BDF file
f = open("eprom-font.bdf","w")
f.write("""STARTFONT 2.1
FONT -osbourne-charrom-medium-r-normal--16-160-75-75-c-80-iso10646-1
SIZE 16 75 75
FONTBOUNDINGBOX 8 16 0 -4
STARTPROPERTIES 2
FONT_ASCENT 9
FONT_DESCENT 2
ENDPROPERTIES
CHARS {0}""".format(len(charstr)))

coff = 0
for c in charstr:
    f.write("""
STARTCHAR U+{0:04X}
ENCODING {0:d}
SWIDTH 500 0
DWIDTH 8 0
BBX 8 16 0 -4
BITMAP
""".format(ord(c)))
    for j in range(16):
        offset = coff + j
        f.write("{0:02X}\n".format(ord(buf[offset])))
    f.write("ENDCHAR")
    coff = coff + 16
f.write("\nENDFONT\n")
f.close()

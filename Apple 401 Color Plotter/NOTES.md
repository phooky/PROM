Self test starts at 94b. Strings are formatted:
1B length N
NB data terminated with 0x03

Pull with: 
/test_extractor.py <ROM.bin | ./plot_to_svg.py >test.svg


Branch table for commands appears to start around 0x1eec
14ce is routine that begins with 1eec in hl

Each entry 5B long:
0-1 command code
2-4 ???

List terminated by 0xffff

Command list:

DA - draw absolute
DR - draw relative?
MA - move absolute
MR - move relative?
LT - letter ???
CA - circle absolute
XT - ? xticks ?
YT - ? yticks ?
CH - ???
LS - letter size
LR - ???
PL - Print letters
PM - ???
PS - ???
PV - ???
WD - ???
AC - arc
LI - ???
IM - ???
PK - ???
RS - ???
VP - ???
UL - ???
SP - ???
LF - ???
SL - ???


import sys

f1 = open(sys.argv[1])
f2 = open(sys.argv[2])

lines1 = f1.readlines()
lines2 = f2.readlines()

bs1=[]
bs2=[]

for a in range(len(lines1)):
    bs1 = bs1 + map(lambda x:int(x,16), lines1[a].split())
    bs2 = bs2 + map(lambda x:int(x,16), lines2[a].split())

for a in range(len(bs1)):
    if bs1[a] != bs2[a]:
        print bin(a)[::-1]


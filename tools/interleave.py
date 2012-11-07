#!/usr/bin/python

import os.path
import sys
import argparse

def validateSizes(inpaths):
    size = -1
    for path in inpaths:
        if not os.path.isfile(path):
            raise Exception("Path "+path+" is not a file, aborting")
        fsize = os.path.getsize(path)
        if size == -1:
            size = fsize
        elif size != fsize:
            raise Exception("Filesize of "+path+" did not match size of other files, aborting")


def interleave(inpaths,outpath,blocksize=1):
    if outpath:
        out = open(outpath,"w")
    else:
        out = sys.stdout
    validateSizes(inpaths)
    files = [open(path) for path in inpaths]
    moreData = True
    while moreData:
        for f in files:
            d = f.read(blocksize)
            if not d:
                moreData = False
                break
            else:
                out.write(d)
    map(lambda x:x.close(),files)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Output of interleave operation (defaults to stdout)")
    parser.add_argument("files",metavar="FILES",nargs='+',help="the files to interleave")
    arguments = parser.parse_args()
    interleave(arguments.files,arguments.output)
    

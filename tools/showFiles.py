#!/usr/bin/env python
'''
Show files in tar incremental file lists (tar -g file)
'''

import sys, os, re

def main(tarfilelist, dironly = False, deep=999):
    print(tarfilelist, deep)
    f = open(tarfilelist, 'rb')
    l=0
    null = float(0)
    files = []
    p = re.compile('/')
    for x in f:
        items = x.split(chr(0))
        for i in items:
            if i.find('/') == 0:
                if len(p.findall(i)) <= int(deep):
                    l+=1
                    files.append(i + '/')
                    cdir = i
            if not dironly and i.find('Y') == 0:
                files.append(os.path.join(cdir, i[1:]))

    f.close()
    files.sort()
    for f in files:
        print f
    print("%d items found" % l)
    

if __name__ == '__main__':
    if len(sys.argv) == 2: 
        main(sys.argv[1])
    elif len(sys.argv) == 3:
        if sys.argv[2] == "-d":
            main(sys.argv[1], True)
        elif sys.argv[2].find("-c") == 0:
            main(sys.argv[1], True, sys.argv[2][2:])            
    else:
        print("Usage: %s <tar incremental file> [-d|-c<x>]" % sys.argv[0])
        print("\t -d   ... dirs only")
        print("\t -c<x> .. show only x dirs deep")

    


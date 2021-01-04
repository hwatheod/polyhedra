import os
import netlib_solid
import json
import sys

all_solids = []
for path, dirs, files in os.walk(sys.argv[1]):
    for file in files:
        f = open(os.path.join(path, file))
        try:
            solid = netlib_solid.read_netlib_solid(f)
            all_solids.append(solid)
        except IOError:
            print('File ' + os.path.join(path, file) + ' skipped')

f = open(sys.argv[2], 'w')
je = json.JSONEncoder()
for chunk in je.iterencode(all_solids):
    f.write(chunk)
f.close()
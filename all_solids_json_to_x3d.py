import shutil
import os
import json
import solid_to_x3d

x3d_path = 'build/x3d'

shutil.rmtree(x3d_path, ignore_errors=True)
os.mkdir(x3d_path)
f = open('build/all_solids.json')
solids = json.loads(f.read())
f.close()

for solid in solids:
    x3d = solid_to_x3d.generate_x3d(solid)
    number = solid['number']
    filename = os.path.join(x3d_path, 'p' + str(number) + '.x3d')
    x3d.write(filename)
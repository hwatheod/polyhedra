import json

def rle(l):
    if l == []:
        return []
    result = []
    prev = l[0]
    count = 0
    for value in l:
        if value == prev:
            count += 1
        else:
            result.append([prev, count])
            count = 1
            prev = value
    result.append([prev, count])
    return result

f = open('build/all_solids.json')
all_solids = json.loads(f.read())
f.close()

catalog = {int(x['number']): {'name': x['name'], 'vertexCount': len(x['vertices']), 'faceCount': len(x['faces']), 'faceTypes': rle(sorted(map(len, x['faces'])))} for x in all_solids}
g = open('build/solid_catalog.js', 'w')
g.write('solid_catalog =\n')
je = json.JSONEncoder()
for chunk in je.iterencode(catalog):
    g.write(chunk)
g.write('\n;\n')
g.close()
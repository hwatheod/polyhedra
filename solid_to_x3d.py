import xml.etree.ElementTree as ET
import json
import sys


def generate_x3d(solid):
    faces = solid['faces']
    vertices = solid['vertices']
    name = solid['name']
    number = solid['number']

    ##### Convert to X3D specific format strings
    edge_count = sum(map(len, faces)) // 2
    indexedLineSet_colorIndex = ' '.join(['0']*edge_count)
    indexedLineSet_coordIndex = ''
    indexedFaceSet_colorIndex = ' '.join(map(str, list(map(len, faces))))
    indexedFaceSet_coordIndex = ''
    edge_set = set()
    for face in faces:
        indexedFaceSet_coordIndex += ' '.join(map(str, face))
        indexedFaceSet_coordIndex += ' -1 '

        prev = face[-1]
        for v in face:
            if (prev, v) in edge_set or (v, prev) in edge_set:
                prev = v
                continue
            edge_set.add((prev, v))
            indexedLineSet_coordIndex += str(prev)
            indexedLineSet_coordIndex += ' '
            indexedLineSet_coordIndex += str(v)
            indexedLineSet_coordIndex += ' -1 '
            prev = v

    coordinate_point = ''
    for vertex in vertices:
        coordinate_point += ' '.join(map(str, vertex))
        coordinate_point += ' '

    colorList = """0 0 0 1 1 0 1 1 0 0 0 1 1 0.5 0 0 1 0 0 0.6 1 0.8 0.8 0.8 1 0 1 0.8 0.8 0.8 1 0 0 0.8 0.8 0.8 0.8 0.8 0.8 0 0 0 0 0 0 0 0.6 0 0 0 0 0.8 0.8 0.8 0.5 0 0.5 0.8 0.8 0.8 0.7 0.2 0 0.8 0.8 0.8 0.8 0.8 0.8"""

    x3d = ET.Element('X3D')
    scene = ET.SubElement(x3d, 'scene')
    worldInfo = ET.SubElement(scene, 'worldInfo', attrib={'info': 'Autogenerated from netlib polyhedra data http://www.netlib.org/polyhedra', 'title': name})
    background = ET.SubElement(scene, 'background')
    transform = ET.SubElement(scene, 'transform')
    shape = ET.SubElement(transform, 'shape')
    appearance = ET.SubElement(shape, 'appearance')
    material = ET.SubElement(appearance, 'material', attrib = {'shininess': '1', 'specularColor': '1 1 1'})
    indexedFaceSet = ET.SubElement(shape, 'indexedFaceSet', attrib = {'colorPerVertex': 'false', 'solid': 'false', 'convex': 'false', 'colorIndex': indexedFaceSet_colorIndex, 'coordIndex': indexedFaceSet_coordIndex})
    coordinate = ET.SubElement(indexedFaceSet, 'coordinate', attrib = {'DEF': 'COORDINATES', 'point': coordinate_point})
    color = ET.SubElement(indexedFaceSet, 'color', attrib = {'DEF': 'COLORS', 'color': colorList})

    inner_transform = ET.SubElement(transform, 'transform')
    inner_shape = ET.SubElement(inner_transform, 'shape')
    indexedLineSet = ET.SubElement(inner_shape, 'indexedLineSet', attrib = {'colorPerVertex': 'false', 'colorIndex': indexedLineSet_colorIndex, 'coordIndex': indexedLineSet_coordIndex})
    inner_coordinate = ET.SubElement(indexedLineSet, 'coordinate', attrib = {'USE': 'COORDINATES'})
    inner_color = ET.SubElement(indexedLineSet, 'color', attrib = {'color': '0 0 0'})

    for elt in x3d.iter():
        if elt.getchildren() == [] and not elt.text:
            elt.text = ' '

    return ET.ElementTree(x3d)

if __name__ == "__main__":
    solid = json.loads(sys.stdin.read())
    x3d = generate_x3d(solid)
    x3d.write(sys.stdout)
    sys.stdout.write('\n')
import sys
import json


def section(file, section_name):
    section_found = False
    last_line = ''
    for line in file:
        line = line.strip()
        if not section_found:
            if line == ':' + section_name:
                section_found = True
        else:
            if line[0] == ':':
                return
            yield line
    if not section_found:
        raise IOError, "Section " + section_name + " not found"


def read_netlib_solid(netlib_file):
    name = section(netlib_file, 'name').next()
    number = section(netlib_file, 'number').next()

    solid_section = section(netlib_file, 'solid')
    face_count, largest_face = map(int, solid_section.next().split(' '))
    faces = [0]*face_count
    for i, line in enumerate(solid_section):
        faces[i] = map(int, line.split(' ')[1:])

    vertices_section = section(netlib_file, 'vertices')
    total_vertices, net_vertices = map(int, vertices_section.next().split(' '))
    solid_vertices = total_vertices - net_vertices
    vertices = [0] * solid_vertices
    for i, line in enumerate(vertices_section):
        if i < net_vertices:
            continue
        vertices[i - net_vertices] = map(float, line.split(' '))

    for face in faces:
        for i, val in enumerate(face):
            face[i] -= net_vertices

    return {'name': name, 'number': number, 'faces': faces, 'vertices': vertices}


def write_netlib_solid(solid, filename):
    name = solid['name']
    number = solid['number']
    f = open(filename, 'w')
    f.write(':name\n')
    f.write(name + '\n')
    f.write(':number\n')
    f.write(str(number) + '\n')
    f.write(':solid\n')
    num_faces = len(solid['faces'])
    max_face = max(map(len, solid['faces']))
    f.write(str(num_faces) + ' ' + str(max_face) + '\n')
    for face in solid['faces']:
        f.write(str(len(face)) + ' ')
        f.write(' '.join(map(str, face)))
        f.write('\n')
    f.write(':dummy\n')
    f.write(':vertices\n')
    f.write(str(len(solid['vertices'])) + ' 0\n')
    for vertex in solid['vertices']:
        f.write(' '.join(map(str, vertex)))
        f.write('\n')
    f.write(':EOF\n')
    f.close()


if __name__ == "__main__":
    solid = read_netlib_solid(sys.stdin)
    je = json.JSONEncoder()
    for chunk in je.iterencode(solid):
        sys.stdout.write(chunk)
    sys.stdout.write('\n')
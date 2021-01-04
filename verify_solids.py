import json
import sys


def verify(solid):
    vertex_count = len(solid['vertices'])
    vertex_figures = [0]*vertex_count
    faces = solid['faces']
    errors = []
    for face in faces:
        face_size = len(face)
        if face_size < 3:
            errors.append('Face ' + str(face) + ' has less than 3 sides')
        for vertex in face:
            if vertex_figures[vertex] == 0:
                vertex_figures[vertex] = []
            vertex_figures[vertex].append(face_size)

    missing_vertex = False
    for i, vf in enumerate(vertex_figures):
        if vf == 0:
            errors.append('Vertex ' + str(i) + ' was never used')
            missing_vertex = True
        elif len(vf) < 3:
            errors.append('Vertex ' + str(i) + ' has vertex figure ' + str(vf))
    if missing_vertex:
        return errors
    angle_sums = [sum([1 - 2.0 / face_size for face_size in vf]) for vf in vertex_figures]
    total_defect = sum([2 - angle_sum for angle_sum in angle_sums])

    if abs(total_defect - 4) > 0.000001:
        errors.append('Total defect = ' + str(total_defect))

    return errors
if __name__ == "__main__":
    f = open('build/all_solids.json')
    solids = json.loads(f.read())
    f.close()
    if type(solids) == dict:
        solids = [solids]
    for solid in solids:
        result = verify(solid)
        if result == []:
            pass
        else:
            print(str(solid['number']) + ' ' + solid['name'] + ' may be broken. ')
            for error in result:
                print(error)
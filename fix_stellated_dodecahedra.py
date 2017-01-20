"""
  Because of rendering issues with pentagrams in the great and small stellated dodecahedra, the
  faces of these 2 polyhedra have been artificially decomposed into triangles in the netlib polyhedra files.
  Therefore, their metadata (vertex and face count, etc.) as calculated directly from the netlib polyhedra files
  are incorrect.  Here we correct them.

  For a discussion of the pentagram rendering issues, see:
    http://www.georgehart.com/virtual-polyhedra/pentagram.html
"""

small_stellated_dodecahedron_index = '5'
great_stellated_dodecahedron_index = '7'

f = open('build/solid_catalog.js')
js_file = f.readlines()
solids = eval(js_file[1])
f.close()

solids[small_stellated_dodecahedron_index]['faceCount'] = 12
solids[small_stellated_dodecahedron_index]['vertexCount'] = 12
solids[small_stellated_dodecahedron_index]['faceTypes'] = [[5, 12]]
solids[great_stellated_dodecahedron_index]['faceCount'] = 12
solids[great_stellated_dodecahedron_index]['vertexCount'] = 20
solids[great_stellated_dodecahedron_index]['faceTypes'] = [[5, 12]]

js_file[1] = str(solids) + '\n'

f = open('build/solid_catalog.js', 'w')
for line in js_file:
    f.write(line)
f.close()
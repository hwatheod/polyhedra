#!/usr/bin/env bash
rm -rf build
mkdir build
echo "--- Generating all_solids.json ---"
python all_solids_to_json.py ./netlib_polyhedra build/all_solids.json

echo "--- Running verification routines ---"
python verify_solids.py

echo "--- Generating x3d files ---"
python all_solids_json_to_x3d.py

echo "--- Generating js solid catalog ---"
python generate_solid_catalog.py

echo "--- Fixing stellated dodecahedra ---"
python fix_stellated_dodecahedra.py

echo "--- Copying HTML and CSS files ---"
cp polyhedra.html build
cp solid.css build
import os
import sys
import trimesh
import mesh2sdf
import numpy as np
import time
from os.path import join, exists
# filename = sys.argv[1] if len(sys.argv) > 1 else  \
#     os.path.join(os.path.dirname(__file__), 'data', 'plane.obj')

def mesh2sdf_core(filename, mesh_scale=0.8, size=128, save_dir=None):
    level = 2 / size

    mesh = trimesh.load(filename, force='mesh')
    mesh_name = filename.split("/")[-1].split(".")[0]
    
    mesh_processed_pth = join(save_dir, f'{mesh_name}.fixed.obj')
    
    if exists(mesh_processed_pth):
        print("skip")
        exit(0)
    else:
        print(f"Processing {filename}")

    # normalize mesh
    vertices = mesh.vertices
    bbmin = vertices.min(0)
    bbmax = vertices.max(0)
    center = (bbmin + bbmax) * 0.5
    scale = 2.0 * mesh_scale / (bbmax - bbmin).max()
    vertices = (vertices - center) * scale

    # fix mesh
    t0 = time.time()
    sdf, mesh = mesh2sdf.compute(
        vertices, mesh.faces, size, fix=True, level=level, return_mesh=True)
    t1 = time.time()

    # output
    mesh.vertices = mesh.vertices / scale + center
    mesh.export(mesh_processed_pth)
    np.save(join(save_dir, f'{mesh_name}.npy'), sdf)
    print('It takes %.4f seconds to process %s' % (t1-t0, filename))

if __name__ == "__main__":
    file_name = "OBJ_MODELS/RESIDENTIALhouse_mesh3855.obj"
    dir_path = "sdf/bnet_sdf_128"
    if not exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    mesh2sdf_core(file_name, save_dir=dir_path)


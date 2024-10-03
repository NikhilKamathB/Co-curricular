import re
import os
import bpy
import math
import bmesh
from collections import defaultdict

os.chdir("/Users/tyche/nikhil/Co-curricular/OA/Kaedim")


def parse_obj_file_and_get_groups(file_path):
    groups = []
    current_group = None
    vertices = []
    faces = []
    group_data = {}

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('g ') or line.startswith('o '):
                if current_group:
                    group_data[current_group] = {
                        'vertices': vertices, 'faces': faces}
                current_group = line[2:].strip()
                groups.append(current_group)
                vertices = []
                faces = []
            elif line.startswith('v '):
                vertices.append([float(x) for x in line.split()[1:]])
            elif line.startswith('f '):
                face = [int(x.split('/')[0]) for x in line.split()[1:]]
                faces.append(face)

    if current_group:
        group_data[current_group] = {'vertices': vertices, 'faces': faces}

    return groups, group_data


def create_mesh(name, verts, faces):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()
    for v in verts:
        bm.verts.new(v)
    bm.verts.ensure_lookup_table()

    for f in faces:
        try:
            # Subtract 1 from each index to convert from 1-based to 0-based indexing
            bm.faces.new([bm.verts[i-1] for i in f])
        except ValueError as e:
            print(f"Skipping invalid face: {f}. Error: {e}")
        except IndexError as e:
            print(f"Skipping face with out-of-range index: {f}. Error: {e}")
        continue

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    return obj


def create_mesh_from_obj_file(obj_file_path):
    # Extract the name from the file path
    name = os.path.splitext(os.path.basename(obj_file_path))[0]

    # Read OBJ file
    with open(obj_file_path, 'r') as file:
        obj_content = file.read()

    # Parse OBJ content
    verts = []
    faces = []
    for line in obj_content.split('\n'):
        if line.startswith('v '):
            v = line.split()[1:]
            verts.append([float(x) for x in v])
        elif line.startswith('f '):
            f = line.split()[1:]
            face = []
            for vert in f:
                # OBJ files can have vertex/texture/normal indices
                # We only care about vertex indices here
                face.append(int(vert.split('/')[0]))
            faces.append(face)

    # Create mesh
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()
    for v in verts:
        bm.verts.new(v)
    bm.verts.ensure_lookup_table()

    for f in faces:
        try:
            # OBJ files use 1-based indexing, so we subtract 1
            bm.faces.new([bm.verts[i-1] for i in f])
        except ValueError as e:
            print(f"Skipping invalid face: {f}. Error: {e}")
        except IndexError as e:
            print(f"Skipping face with out-of-range index: {f}. Error: {e}")

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    return obj


def setup_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    bpy.ops.object.camera_add(
        location=(0, 0, 10), rotation=(math.pi/2, 0, math.pi/2))
    camera = bpy.context.active_object

    bpy.ops.object.light_add(type='SUN', location=(
        5, 5, 5), rotation=(math.pi/4, -math.pi/4, 0))
    bpy.ops.object.light_add(
        type='SUN', location=(-5, -5, 5), rotation=(-math.pi/4, math.pi/4, 0))
    bpy.ops.object.light_add(
        type='SUN', location=(0, 0, 10), rotation=(0, 0, 0))

    light = bpy.context.active_object

    bpy.context.scene.camera = camera

    return camera, light


def render_group(output_path):
    bpy.context.scene.render.filepath = output_path
    bpy.context.scene.render.image_settings.file_format = 'JPEG'
    bpy.ops.render.render(write_still=True)


file_path = './Cocktail.obj'
groups, group_data = parse_obj_file_and_get_groups(file_path)


print("Groups found:")
for idx in range(len(groups)+1):

    # Setup new scene
    camera, light = setup_scene()

    # Create mesh for this group
    if idx == len(groups):
        obj = create_mesh_from_obj_file(file_path)
        name = "Cocktail"
    else:
        vertices = group_data[groups[idx]]['vertices']
        faces = group_data[groups[idx]]['faces']
        obj = create_mesh(groups[idx], vertices, faces)
        name = groups[idx]

    # Center and scale object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    obj.location = (0, 0, 0)
    bpy.ops.object.select_all(action='DESELECT')

    # Set camera to look at object
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = obj

    # Render
    output_path = os.path.join(os.path.dirname(file_path), f"{name}.jpg")
    render_group(output_path)
    print(f"  Rendered image saved as {output_path}")

    # Clean up
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

print("Rendering complete.")

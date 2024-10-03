import os
import bpy
import math

os.chdir("/Users/tyche/nikhil/Co-curricular/OA/Kaedim")


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()


def import_obj(file_path):
    bpy.ops.wm.obj_import(filepath=file_path)


def get_groups():
    return [obj for obj in bpy.data.objects if obj.type == 'MESH']


def setup_scene():
    bpy.ops.object.camera_add(
        location=(0, 0, 25), rotation=(math.pi/2, 0, math.pi/2))
    camera = bpy.context.active_object
    bpy.ops.object.light_add(type='SUN', location=(
        5, 5, 5), rotation=(math.pi/4, -math.pi/4, 0))
    bpy.ops.object.light_add(
        type='SUN', location=(-5, -5, 5), rotation=(-math.pi/4, math.pi/4, 0))
    bpy.ops.object.light_add(
        type='SUN', location=(0, 0, 10), rotation=(0, 0, 0))
    bpy.context.scene.camera = camera


def render_group(group, output_path):
    # Hide all objects
    for obj in bpy.data.objects:
        obj.hide_render = True
        obj.hide_viewport = True

    # Show only the current group
    group.hide_render = False
    group.hide_viewport = False

    # Center the view on the object
    bpy.ops.object.select_all(action='DESELECT')
    group.select_set(True)
    bpy.context.view_layer.objects.active = group
    bpy.ops.view3d.camera_to_view_selected()

    # Render and save
    bpy.context.scene.render.filepath = output_path
    bpy.context.scene.render.image_settings.file_format = 'JPEG'
    bpy.ops.render.render(write_still=True)


def main():
    obj_file_path = "./Cocktail.obj"
    output_folder = "."

    clear_scene()
    import_obj(obj_file_path)
    setup_scene()

    groups = get_groups()

    for i, group in enumerate(groups):
        output_path = os.path.join(output_folder, f"{group.name}.png")
        render_group(group, output_path)

    print(f"Rendered {len(groups)} groups.")


main()

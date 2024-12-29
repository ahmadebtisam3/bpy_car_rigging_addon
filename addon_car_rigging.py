bl_info = {
    "name": "Car Rigging",
    "author": "Ibtisam Ahmad",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Rigged a Car",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector


def add_object(self, context):
    scale_x = self.scale.x
    scale_y = self.scale.y

    verts = [
        Vector((-1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, 1 * scale_y, 0)),
        Vector((1 * scale_x, -1 * scale_y, 0)),
        Vector((-1 * scale_x, -1 * scale_y, 0)),
    ]

    edges = []
    faces = [[0, 1, 2, 3]]

    mesh = bpy.data.meshes.new(name="New Object Mesh")
    mesh.from_pydata(verts, edges, faces)
    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    object_data_add(context, mesh, operator=self)


class OBJECT_OT_animate_car(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "object.animate_car"
    bl_label = "Animate car object"
    bl_options = {'REGISTER', 'UNDO'}

def change_main_body_position(context):
    main_car_obj = context.object
    main_car_obj.keyframe_insert(data_path='location', frame=1, index=1)
    main_car_obj.location.y += 3
    for child_obj in main_car_obj.children:
        child_obj.keyframe_insert(data_path='rotation_euler', frame=1, index=1)
        child_obj.rotation_euler.y += 360
        child_obj.keyframe_insert(data_path='rotation_euler', frame=100, index=1)
    main_car_obj.keyframe_insert(data_path='location', frame=100, index=1)

    def execute(self, context):
        self.change_main_body_position(context)
        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_animate_car.bl_idname,
        text="Animate Car",
        icon='PLUGIN')


# This allows you to right click on a button and link to documentation
#def add_object_manual_map():
#    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
#    url_manual_mapping = (
#        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
#    )
#    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_animate_car)
#    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_object_animation.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_animate_car)
#    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()

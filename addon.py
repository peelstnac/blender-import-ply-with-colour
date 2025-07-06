bl_info = {
    "name": "Colour PLY",
    "blender": (4, 4, 0),
    "category": "Import-Export",
}

import bpy
from bpy_extras.io_utils import ImportHelper

class IMPORT_OT_colour_ply(bpy.types.Operator, ImportHelper):
    bl_idname = "import_scene.colour_ply"
    bl_label = "Import PLY with colour (.ply)"

    filename_ext = ".ply"

    filter_glob: bpy.props.StringProperty(
        default="*.ply", options={'HIDDEN'}
    )

    geo_group: bpy.props.StringProperty(
        name="Geometry Node Group",
        default="ProcessPointCloud"
    )

    def execute(self, context):
        before = set(bpy.data.objects)
        # NOTE: Ensure that https://github.com/TombstoneTumbleweedArt/import-ply-as-verts is installed first!
        bpy.ops.import_mesh.ply(filepath=self.filepath)
        after = set(bpy.data.objects)
        new_objs = [obj for obj in after - before if obj.type == "MESH"]
        for obj in new_objs:
            mod = obj.modifiers.new("AutoProcess", type='NODES')
            mod.node_group = bpy.data.node_groups[self.geo_group]
        return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(IMPORT_OT_colour_ply.bl_idname, text="PLY with colour (.ply)")

def register():
    bpy.utils.register_class(IMPORT_OT_colour_ply)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(IMPORT_OT_colour_ply)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()

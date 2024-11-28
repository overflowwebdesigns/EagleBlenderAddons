bl_info = {
    "name": "Vertex Color Swap Tool",
    "author": "Eage11",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Vertex Color Swap",
    "description": "Allows swapping two vertex colors on the active object",
    "category": "Mesh",
}

import bpy
from bpy.props import EnumProperty, PointerProperty
from bpy.types import Operator, Panel, PropertyGroup


# Property Group for settings
class colorSwapSettings(PropertyGroup):
    vertex_paint_type_from: EnumProperty(
        items=[
            ('red', 'Red', 'Swap red color'),
            ('green', 'Green', 'Swap green color'),
            ('blue', 'Blue', 'Swap blue color'),
            ('black', 'Black', 'Swap black color'),
        ],
        name="From",
        description="Select the vertex color to swap from",
        default='red',
    )

    vertex_paint_type_to: EnumProperty(
        items=[
            ('red', 'Red', 'Swap red color'),
            ('green', 'Green', 'Swap green color'),
            ('blue', 'Blue', 'Swap blue color'),
            ('black', 'Black', 'Swap black color'),
        ],
        name="To",
        description="Select the vertex color to swap to",
        default='black',
    )

class WM_OT_swap_vertex_colors(Operator):
    """Swap two vertex colors"""
    bl_label = "Swap Vertex Colors"
    bl_idname = "wm.swap_vertex_colors"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or not obj.data.vertex_colors:
            self.report({'WARNING'}, "No active object with vertex colors")
            return {'CANCELLED'}

        vcol_from = context.scene.vertex_color_swap_settings.vertex_paint_type_from
        vcol_to = context.scene.vertex_color_swap_settings.vertex_paint_type_to

        vcols = obj.data.vertex_colors.active.data
        color_map = {
            'red': (1, 0, 0, 1),
            'green': (0, 1, 0, 1),
            'blue': (0, 0, 1, 1),
            'black': (0, 0, 0, 1)
        }

        color_from = color_map.get(vcol_from)
        color_to = color_map.get(vcol_to)

        for loop in vcols:
            if tuple(loop.color)[:3] == color_from[:3]:
                loop.color = color_to
            elif tuple(loop.color)[:3] == color_to[:3]:
                loop.color = color_from

        self.report({'INFO'}, f"Swapped {vcol_from} and {vcol_to}")
        return {'Done'}


# Panel in the 3D View Sidebar
class VIEW3D_PT_vertex_color_swap(Panel):
    bl_label = "Vertex Color Swap"
    bl_idname = "VIEW3D_PT_vertex_color_swap"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Vertex Color Swap'

    def draw(self, context):
        layout = self.layout
        settings = context.scene.vertex_color_swap_settings

        layout.prop(settings, "vertex_paint_type_from", text="From")
        layout.prop(settings, "vertex_paint_type_to", text="To")
        layout.operator("wm.swap_vertex_colors", text="Swap Vertex Colors")


# Registration
classes = (
    colorSwapSettings,
    WM_OT_swap_vertex_colors,
    VIEW3D_PT_vertex_color_swap,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.vertex_color_swap_settings = PointerProperty(type=colorSwapSettings)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.vertex_color_swap_settings


if __name__ == "__main__":
    register()

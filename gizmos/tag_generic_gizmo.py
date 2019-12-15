# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# Hell is other people's code.

import bpy
import bmesh
import mathutils
from bl_ui.space_toolsystem_toolbar import (
    VIEW3D_PT_tools_active as view3d_tools
)
from bpy.types import (
    # Operator,
    GizmoGroup,
)


def get_active_tool():
    return view3d_tools.tool_active_from_context(bpy.context)


def set_pivot():
    if bpy.context.mode == 'EDIT_MESH':
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        active = bm.select_history.active

        loc = mathutils.Vector((0.0, 0.0, 0.0))
        normal = mathutils.Vector((0.0, 0.0, 0.0))

        sel_coords = [v.co for v in bm.verts if v.select]
        sel_normals = [v.normal for v in bm.verts if v.select]

        face_normals = [f.normal for f in bm.faces if f.select]

        if len(face_normals) > 1:
            # normal = mathutils.geometry.normal(face_normals)
            for no in face_normals:
                normal += no

            normal = normal / len(face_normals)
        elif len(face_normals) > 0:
            normal = face_normals[0]
        else:
            for no in sel_normals:
                normal += no
            normal = normal / len(sel_normals)

        for co in sel_coords:
            loc += co

        active = loc / len(sel_coords)

        # Normal Rotation
        norm = normal.to_track_quat('Z', 'X')
        n_mat = norm.to_matrix()

        # Object Matrix
        w_mat = obj.matrix_world.copy()
        w_mat = w_mat.to_3x3()

        matrix_new = w_mat.to_3x3().inverted().transposed()
        foik = matrix_new @ n_mat
        foik = foik.to_4x4()

        # Translation Component
        sel_loc = active.copy()
        sel_loc_mat = mathutils.Matrix.Translation(sel_loc)
        sel_loc_mat = w_mat.to_4x4() @ sel_loc_mat

        a_mat = mathutils.Matrix.Translation(sel_loc_mat.to_translation())

        final = a_mat @ foik

        return final

    elif bpy.context.mode == 'OBJECT':
        obj = bpy.context.active_object
        pivot = obj.matrix_world
        return pivot


class TAGGenericGizmo(GizmoGroup):
    bl_idname = "OBJECT_GGT_TAG_generic_gizmo"
    bl_label = "Dick Gizmo"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_options = {'3D', 'PERSISTENT', 'SHOW_MODAL_ALL'}

    @classmethod
    def poll(cls, context):
        if bpy.context.mode == 'EDIT_MESH':
            obj = bpy.context.edit_object
            me = obj.data
            bm = bmesh.from_edit_mesh(me)

            sel = [v for v in bm.verts if v.select]
            if len(sel) > 0:
                active_tool = get_active_tool()

                tool_list = [
                    "builtin.bevel",
                    "builtin.inset_faces",
                    "builtin.rip_region"
                ]

                if active_tool.idname in tool_list:
                    return True

    def set_op_from_tool(self, giz):
        active_tool = get_active_tool()

        tool_list = [
            "builtin.bevel",
            "builtin.inset_faces",
            "builtin.rip_region"
        ]

        if active_tool.idname in tool_list:
            if giz.select:
                op = giz.target_set_operator("wm.context_pie_enum")
                op.data_path = "window_manager.sel_fb_props.active_operator"
            else:
                if active_tool.idname == 'builtin.bevel':
                    giz.target_set_operator("mesh.bevel")
                elif active_tool.idname == 'builtin.inset_faces':
                    giz.target_set_operator("mesh.inset")
                elif active_tool.idname == 'builtin.rip_region':
                    giz.target_set_operator("mesh.rip_move")

    @classmethod
    def setup_keymap(self, keys):
        # Key Map - box, not present
        if not keys.keymaps.find(name="TAG Generic Gizmo", space_type="VIEW_3D"):
            print("No Keymap - Making a New One")
            km = keys.keymaps.new(name='TAG Generic Gizmo', space_type="VIEW_3D")

            # Key Map Item - present, not box
            km.keymap_items.new("gizmogroup.gizmo_tweak", "LEFTMOUSE", "CLICK_DRAG", any=True)

            kmi = km.keymap_items.new("gizmogroup.gizmo_select", "LEFT_CTRL", "PRESS", any=True)
            kmi.properties.toggle = True
        else:
            km = keys.keymaps.find(name="TAG Generic Gizmo", space_type="VIEW_3D")
            km.restore_to_default()
            # print("TAG Generic Gizmo Keymap Found: " + str(len(km.keymap_items)) + " Entries")
            if (len(km.keymap_items)) < 2:
                km.restore_to_default()
                km.keymap_items.new("gizmogroup.gizmo_tweak", "LEFTMOUSE", "CLICK_DRAG", any=True)

                kmi = km.keymap_items.new("gizmogroup.gizmo_select", "LEFT_CTRL", "PRESS", any=True)
                kmi.properties.toggle = True
        return km

    def setup(self, context):
        pivot = set_pivot()

        giz = self.gizmos.new('GIZMO_GT_arrow_3d')
        # giz.draw_options = {'OUTLINE', 'BACKDROP'}
        # giz.icon = 'NONE'

        giz.use_draw_modal = True
        giz.use_draw_value = True
        giz.use_draw_offset_scale = True
        giz.use_draw_scale = True
        # giz.use_snap = True

        giz.scale_basis = 1.25

        giz.color = 0.5, 0.5, 1.0
        giz.color_highlight = 0.9, 0.9, 0.9

        giz.alpha = 1.0
        giz.alpha_highlight = 1.0

        giz.line_width = 1

        self.set_op_from_tool(giz)

        giz.use_operator_tool_properties = True

        giz.matrix_basis = pivot

        self.giz = giz

    def draw_prepare(self, context):
        pivot = set_pivot()

        giz = self.giz
        giz.matrix_basis = pivot
        self.set_op_from_tool(giz)

        if giz.select:
            giz.color = 1.0, 0.5, 0.5
            giz.color_highlight = 1.0, 1.0, 0.5
        else:
            giz.color = 0.5, 0.5, 1.0
            giz.color_highlight = 0.9, 0.9, 0.9

        if not giz.is_highlight:
            giz.select = False

    def refresh(self, context):
        pivot = set_pivot()

        giz = self.giz
        giz.matrix_basis = pivot
        self.set_op_from_tool(giz)

        if not giz.is_highlight:
            giz.select = False

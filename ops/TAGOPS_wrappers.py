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
from bpy.props import (
    EnumProperty,
    BoolProperty
)


# A general-purpose wrapper for fallback operators
class TAGSelectFallback(bpy.types.Operator):
    """A wrapper for selection operators"""
    bl_idname = "tag.select_fallback"
    bl_label = "ThatAsherGuy's Selection Fallback Operator"
    bl_description = """A wrapper selection operators"""
    bl_options = {'REGISTER'}

    active_operator_items = [
                    ('SEL', "Select", "Select", 'NONE', 1),
                    ('BOX_SEL', "Box Select", "Box Select", 'NONE', 2),
                    ('CIRCLE_SEL', "Circle Select", "Circle Select", 'NONE', 3)
                 ]

    active_operator: EnumProperty(
        name="Active Operator",
        description="The operator to call",
        items=active_operator_items,
        default='SEL'
    )

    use_globals: BoolProperty(
        name="Use Global Settings",
        default=True
    )

    def invoke(self, context, event):
        wm = bpy.context.window_manager
        g_props = wm.sel_fb_props

        op = self.active_operator
        use_globals = self.use_globals

        if use_globals:
            if g_props.active_operator == 'SEL':
                if g_props.dir_sel_mode == 'SMART':
                    if bpy.context.mode == 'EDIT_MESH':
                        if bpy.context.tool_settings.mesh_select_mode[0]:

                            bpy.ops.view3d.select('INVOKE_DEFAULT', True, extend=True)
                            bpy.ops.mesh.select_more('INVOKE_DEFAULT', True)

                        elif bpy.context.tool_settings.mesh_select_mode[1]:

                            bpy.ops.mesh.loop_select('INVOKE_DEFAULT', True, toggle=True)

                        elif bpy.context.tool_settings.mesh_select_mode[2]:

                            bpy.ops.view3d.select('INVOKE_DEFAULT', True, extend=True)
                            bpy.ops.mesh.faces_select_linked_flat('INVOKE_DEFAULT', True)

                    elif bpy.context.mode == 'OBJECT':

                        bpy.ops.view3d.select('INVOKE_DEFAULT', True, extend=True)
                        bpy.ops.object.select_grouped(
                            'INVOKE_DEFAULT',
                            True,
                            extend=True,
                            type='CHILDREN_RECURSIVE'
                            )
                        bpy.ops.object.select_grouped(
                            'INVOKE_DEFAULT',
                            True,
                            extend=True,
                            type='PARENT'
                            )
                elif g_props.dir_sel_mode == 'TWEAK':
                    bpy.ops.view3d.select('INVOKE_DEFAULT', True, toggle=True)
                    bpy.ops.transform.translate('INVOKE_DEFAULT', True)
            elif g_props.active_operator == 'BOX_SEL':
                bpy.ops.view3d.select_box(
                    'INVOKE_DEFAULT',
                    True,
                    mode=g_props.box_sel_mode,
                    wait_for_input=False
                    )
            elif g_props.active_operator == 'CIRCLE_SEL':
                bpy.ops.view3d.select_circle(
                    'INVOKE_DEFAULT',
                    True,
                    mode=g_props.circle_sel_mode,
                    wait_for_input=False
                    )
            elif g_props.active_operator == 'LASSO_SEL':
                bpy.ops.view3d.select_lasso(
                    'INVOKE_DEFAULT',
                    True,
                    mode=g_props.lasso_sel_mode,
                    )
        else:
            if op == 'SEL':
                bpy.ops.view3d.select('INVOKE_DEFAULT', True)
            elif op == 'BOX_SEL':
                bpy.ops.view3d.select_box('INVOKE_DEFAULT', True, wait_for_input=False)
            elif op == 'CIRCLE_SEL':
                bpy.ops.view3d.select_circle('INVOKE_DEFAULT', True, wait_for_input=False)

        return {'FINISHED'}

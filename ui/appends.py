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


def TAGToolbarButton(self, context):
    wm = bpy.context.window_manager
    sel_fb_globals = wm.sel_fb_props

    layout = self.layout
    row = layout.row(align=True)
    row.ui_units_x = 10
    act_op_icon = 'NONE'
    mode = 'dir_sel_mode'

    if sel_fb_globals.active_operator == 'SEL':
        act_op_icon = 'RESTRICT_SELECT_OFF'
        mode = 'dir_sel_mode'
    elif sel_fb_globals.active_operator == 'BOX_SEL':
        act_op_icon = 'STICKY_UVS_LOC'
        mode = 'box_sel_mode'
    elif sel_fb_globals.active_operator == 'CIRCLE_SEL':
        act_op_icon = 'ONIONSKIN_ON'
        mode = 'circle_sel_mode'
    elif sel_fb_globals.active_operator == 'LASSO_SEL':
        act_op_icon = 'PHYSICS'
        mode = 'lasso_sel_mode'

    row.prop(sel_fb_globals, "active_operator", text="", icon=act_op_icon)
    row.prop(sel_fb_globals, mode, text="", expand=True, icon_only=True)

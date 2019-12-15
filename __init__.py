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
from bpy.types import (
    WindowManager,
    )

from bpy.props import (
    PointerProperty
)

# Addon Properties
from .props.op_globals import OmniSelectProps

# Addon Operators
from .ops.TAGOPS_wrappers import TAGSelectFallback

# Addon UI
from .ui.appends import TAGToolbarButton

# Addon Gizmos
from .gizmos.tag_generic_gizmo import TAGGenericGizmo


bl_info = {
    "name": "ThatAsherGuy's Contextual Operators",
    "author": "Asher",
    "description": "A set of wrappers that lets users access"
    " multiple operators through a shared keymap entry.",
    "blender": (2, 82, 0),
    "version": (0, 0, 1),
    "location": "View3D | Ctrl + Alt + Right Mouse",
    "warning": "We're in 'Proof of Concept' territory here.",
    "category": "3D View"
}

classes = (
    OmniSelectProps,
    TAGSelectFallback,
    TAGGenericGizmo
)

tag_keymaps = []


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    WindowManager.sel_fb_props = PointerProperty(type=OmniSelectProps)

    bpy.types.VIEW3D_HT_tool_header.append(TAGToolbarButton)

    wm = bpy.context.window_manager

    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            "tag.select_fallback",
            'RIGHTMOUSE',
            'CLICK_DRAG',
            ctrl=True,
            alt=True)
        tag_keymaps.append((km, kmi))


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_HT_tool_header.remove(TAGToolbarButton)

    del bpy.types.WindowManager.sel_fb_props

    for km, kmi in tag_keymaps:
        km.keymap_items.remove(kmi)
    tag_keymaps.clear()

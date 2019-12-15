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

from bpy.types import PropertyGroup
from bpy.props import (
    EnumProperty,
)


class OmniSelectProps(PropertyGroup):

    active_operator_items = [
                    (
                        'SEL',
                        "Smart Select",
                        "Fancy Stuff",
                        'RESTRICT_SELECT_OFF',
                        1
                    ),
                    (
                        'BOX_SEL',
                        "Box Select",
                        "A fast selection tool with a variety of modes",
                        'STICKY_UVS_LOC',
                        2
                    ),
                    (
                        'CIRCLE_SEL',
                        "Circle Select",
                        "A brush-like selection tool",
                        'ONIONSKIN_ON',
                        3
                    ),
                    (
                        'LASSO_SEL',
                        "Lasso Select",
                        "A flexible selection tool with a variety of modes",
                        'PHYSICS',
                        4
                    )
                 ]

    active_operator: EnumProperty(
        name="Active Operator",
        description="Fallback Operator",
        items=active_operator_items,
        default='SEL'
    )

    dir_sel_items = [
                (
                    'SMART',
                    "Smart Extend",
                    "Grows the selection by distance, loops, or corner angles"
                    " depending on the selection mode",
                    'FULLSCREEN_ENTER',
                    1
                ),
                (
                    'TWEAK',
                    "Tweak Element",
                    "Selects and moves in one operation",
                    'CON_LOCLIKE',
                    2
                ),
                    ]

    dir_sel_mode: EnumProperty(
        name="Select",
        description="Mode",
        items=dir_sel_items,
        default='SMART'
    )

    box_sel_items = [
                (
                    'SET',
                    "Select",
                    "Selects elements inside the box. \n"
                    "Deselects elements outside the box.",
                    'SELECT_SET',
                    1
                ),
                (
                    'ADD',
                    "Extend",
                    "Selects elements inside the box.\n"
                    "Does not deleselct elements outside the box.",
                    'SELECT_EXTEND',
                    2
                ),
                (
                    'SUB',
                    "Deselect Inner",
                    "Deselects elements inside the box.",
                    'SELECT_SUBTRACT',
                    3
                ),
                (
                    'XOR',
                    "Invert",
                    "Inverts selections inside the box. \n"
                    "Does not affect elements outside the box.",
                    'SELECT_DIFFERENCE',
                    4
                ),
                (
                    'AND',
                    "Deselect Outer",
                    "Deselects elements outside the box.",
                    'SELECT_INTERSECT',
                    5
                    ),
                    ]

    box_sel_mode: EnumProperty(
        name="Box Select",
        description="Mode",
        items=box_sel_items,
        default='ADD'
    )

    circle_sel_items = [
                    ('SET', "Select", "Creates a new selection.", 'SELECT_SET', 1),
                    ('ADD', "Extend", "Extends the current selection.", 'SELECT_EXTEND', 2),
                    (
                        'SUB',
                        "Subtract",
                        "Subtracts from the current selection.",
                        'SELECT_SUBTRACT',
                        3
                    )
                 ]

    circle_sel_mode: EnumProperty(
        name="Circle Select",
        description="Mode",
        items=circle_sel_items,
        default='ADD'
    )

    lasso_sel_items = [
                (
                    'SET',
                    "Select",
                    "Selects elements inside the lasso. \n"
                    "Deselects elements outside the lasso.",
                    'SELECT_SET',
                    1
                ),
                (
                    'ADD',
                    "Extend",
                    "Selects elements inside the lasso.\n"
                    "Does not deleselct elements outside the lasso.",
                    'SELECT_EXTEND',
                    2
                ),
                (
                    'SUB',
                    "Deselect Inner",
                    "Deselects elements inside the lasso.",
                    'SELECT_SUBTRACT',
                    3
                ),
                (
                    'XOR',
                    "Invert",
                    "Inverts selections inside the lasso. \n"
                    "Does not affect elements outside the lasso.",
                    'SELECT_DIFFERENCE',
                    4
                ),
                (
                    'AND',
                    "Deselect Outer",
                    "Deselects elements outside the lasso.",
                    'SELECT_INTERSECT',
                    5
                    ),
                    ]

    lasso_sel_mode: EnumProperty(
        name="Lasso Select",
        description="Mode",
        items=lasso_sel_items,
        default='ADD',
    )

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from django import template

register = template.Library()

@register.filter
def get_first(value):
    try:
        return value[0]
    except (TypeError, IndexError):
        return None
    
@register.filter
def cut_suffix(value, suffix):
    """Remove a specified suffix from a string."""
    if value.endswith(suffix):
        return value[:-len(suffix)]
    return value

@register.filter
def slice_list(value, slice):
    """Slices the list."""
    slice_parts = slice.split(':')
    start = int(slice_parts[0]) if slice_parts[0] else None
    end = int(slice_parts[1]) if slice_parts[1] else None
    return value[start:end]

@register.filter
def get_attr_with_count(value, attr_name):
    """Gets an attribute of an object dynamically and appends '_count' to the attribute name."""
    full_attr_name = f"{attr_name}_count"
    return getattr(value, full_attr_name, "")

@register.filter
def divide(value, arg):
    try:
        return round((float(value) / float(arg)) * 100, 2)
    except (ValueError, ZeroDivisionError):
        return None
    
@register.filter
def to_query_params(combo_tuple):
    return '&'.join([f"{part[0]}_id={part[1:]}" for part in combo_tuple])

@register.filter
def get_attr(value, arg):
    """Gets an attribute of an object dynamically from a string name
    Useful to get specific row values from a df column"""
    return getattr(value, arg, "")

@register.filter
def format_bbs_combo(value, index):
    return value[index]

@register.filter(name='color_for_property')
def color_for_property(value, property_name):
    color_map = {
        'EC50_main': [(10, '#d4f4c9'), (30, '#ffe099'), '#ffad99'],
        'OX1_IP1_EC50': [(10, '#d4f4c9'), (30, '#ffe099'), '#ffad99'],
        'IC50': [(10, '#d4f4c9'), (30, '#ffe099'), '#ffad99'],
        'HLM': [(100, '#d4f4c9'), (300, '#ffe099'), '#ffad99'],
        'MDR1_efflux': [(5, '#d4f4c9'), (10, '#ffe099'), '#ffad99'],
        'MDR1_PappAB': [(4, '#ffad99'), (10, '#ffe099'), '#d4f4c9'],
        'sol_FaSSIF': [(25, '#ffad99'), (100, '#ffe099'), '#d4f4c9'],
        'logD': [(3, '#d4f4c9'), (4, '#ffe099'), '#ffad99'],
        'GSH': [(100, '#d4f4c9'), (200, '#ffe099'), '#ffad99'],
        'PXR_EC50': [(1, '#ffad99'), (4, '#ffe099'), '#d4f4c9'],
        'CYP_testo': [(1, '#ffad99'), (4, '#ffe099'), '#d4f4c9'],
        'BPI_calc': [(1, '#ffad99'), (1.5, '#ffe099'), '#d4f4c9'],
        'fu': [(0.2, '#d4f4c9'), (0.5, 'transparent'), 'transparent'],
        'IP1_effect': [(80, '#ffad99'), (90, '#ffe099'), '#d4f4c9'],
        'bb_count': [(0, '#ffad99'), (2, '#ffe099'), '#transparent'],
        'improvement_ratio': [(40, '#ffad99'), (60, '#ffe099'), '#d4f4c9'],
        'ratio_hOX1R_hOX2R': [(5, '#ffad99'), (20, '#ffe099'), '#d4f4c9'],
    }
    thresholds_colors = color_map.get(property_name, [])
    default_color = thresholds_colors[-1] if thresholds_colors else 'defaultColor'
    try:
        for threshold, color in thresholds_colors[:-1]:  # Exclude the last item (default color)
            if value <= threshold:
                return color

        return default_color
    except: 
        return 'transparent'
        
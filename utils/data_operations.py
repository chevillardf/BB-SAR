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

import re

def custom_sort(id):
    # used in boxPlot sort bb_ids in ascending order
    numeric_part = re.search(r'\d+', id).group()
    return int(numeric_part)

def prepend_char(value, char):
        if value.isnumeric():
            return char + value
        return value

def process_field(input_id, char):
    # used in molecules_home view
    if ',' in input_id:
        id_list = input_id.split(',')
        id_list = [prepend_char(id.strip(), char) for id in id_list]
        return id_list
    else:
        return [prepend_char(input_id, char)]
    

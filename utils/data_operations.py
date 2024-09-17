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
    

import json
from os.path import exists

coord_file = 'coordinates.txt'


def get_saved_coordinates(image_path, selection_title):
    if not exists(coord_file):
        return None
    with open(coord_file, 'r') as f:
        try:
            content = json.load(f)
            coordinates = content[image_path][selection_title]
            return coordinates
        except:
            return None



def save_coordinates(image_path, selection_title, coordinates):
    content = {}
    if exists(coord_file):
        with open(coord_file, 'r') as f:
            try:
                content = json.load(f)
            except:
                pass

    if image_path not in content:
        content[image_path] = {selection_title: coordinates}
    else:
        content[image_path][selection_title] = coordinates

    with open(coord_file, 'w') as f:
        json_content = json.dumps(content, indent=4)
        f.write(json_content)

# save_coordinates('2.JPG', 'sfdsf', (123.1232, 44.2342, 11.2, 1232))
# save_coordinates('3.JPG', 'sss', (123.1232, 44.2342, 11.2, 1232))
# save_coordinates('2.JPG', 'sss', (55.23, 44.2342, 11.2, 1232))
# save_coordinates('2.JPG', 'sfdsf', (22, 44.2342, 11.2, 1232))
# print(get_saved_coordinates('2.JPG', 'sfdsf'))
# print(get_saved_coordinates('3.JPG', 'sss'))
# print(get_saved_coordinates('3.JPG', 'ssss'))
# print(get_saved_coordinates('2.JPG', 'sss fafd'))
# save_coordinates('2.JPG', 'sss fafd', (54545354.22, 44.2342, 11.2, 1232))
# print(get_saved_coordinates('2.JPG', 'sss fafd'))
# print(get_saved_coordinates('2.JPG', 'sfdsf'))



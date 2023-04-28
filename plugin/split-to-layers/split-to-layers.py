from gimpfu import *
import os
import json
import pkg_resources
import pip
import sys
import subprocess

print("Python version %s:" % sys.version)

current_dir = os.getcwd()
plugin_path = os.path.dirname(os.path.realpath(__file__))

with open("%s\config.json" % plugin_path) as f:
    config = json.load(f)

script_file = config['script']
python_location = config["python"]

import tempfile
import os

def get_selection_bounds(image):
    if pdb.gimp_selection_is_empty(image):
        gimp.message("There is no selection")
        return (-1,-1,-1,-1)
    else:
        bounds = pdb.gimp_selection_bounds(image)
        print(bounds)
        return (bounds[1], bounds[2], bounds[3], bounds[4])

def split_to_layers_no_face(image, layer):
    return split_to_layers(image, layer, False)

def split_to_layers_face(image, layer):
    return split_to_layers(image, layer, True)

def split_to_layers(image, layer, face):

    layer = pdb.gimp_image_get_active_layer(image)
    temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    pdb.gimp_file_save(
        image,
        layer,
        temp_file.name,
        temp_file.name
    )
    temp_file.close()

    gimp.message("Layer saved as temporary file: {}".format(temp_file.name))

    gimp.message("Subprocessing out: %s %s " % (script_file,temp_file.name))

    [x1, y1, x2, y2] = get_selection_bounds(image)

    #result = subprocess.check_output([python_location, script_file, temp_file.name, str(x1), str(y1), str(x2), str(y2)])
    result = None
    try:
        result = subprocess.check_output([python_location, script_file, temp_file.name, str(x1), str(y1), str(x2), str(y2), str(face)])
    except WindowsError as e:
        if e.errno == 5:
            gimp.message("Error: Access is denied to file: %s" % e.filename)
        else:
            gimp.message("Error:%s" % e.strerror)

    if not result:
        return

    try:
        os.remove(temp_file.name)
        gimp.message("File %s deleted successfully." % temp_file.name)
    except OSError as e:
        gimp.message("Error: %s - %s." % (e.filename, e.strerror))

    gimp.message("getting results")
    data = json.loads(result)
    masks = data["data"]
    i = 0
    cut_layer = None

    mask_len = len(masks)
    gimp.message("results 0 of %d" % mask_len)

    mask_index = 0
    for mask_points in masks:
        mask_index = mask_index+1
        gimp.message("results %d of %d" % (mask_index, mask_len))

        pdb.gimp_image_select_polygon(
            image, #GimpImage*
            CHANNEL_OP_REPLACE,#operation
            len(mask_points), #should be number segments but doesn't seem to be the case, it should be the number of the array WTH?
            mask_points # segments
            )
        selection = pdb.gimp_selection_bounds(image)
        if selection[0] == -1:
            # no selection exists
            pass
        elif selection[0] == selection[2] or selection[1] == selection[3]:
            # selection has a width or height of zero
            pass
        else:
            pdb.gimp_edit_copy(layer)
            mask_layer = pdb.gimp_layer_new(image, image.width, image.height, RGBA_IMAGE, "Segment_ %s" % i, 100, NORMAL_MODE)
            pdb.gimp_image_insert_layer(image, mask_layer, None, 0)
            cut_layer = pdb.gimp_edit_paste(mask_layer, False)
            mask_layer.flush()
            pdb.gimp_selection_none(image)
            gimp.displays_flush()
            i+=1

    if i>0:
       pdb.gimp_floating_sel_anchor(cut_layer)

    gimp.displays_flush()

register(
    "python_fu_segments_to_layers_no_face",
    "Split To Layers",
    "Split an image into layers from segments",
    "Carl Burks wrapping github.com/facebookresearch/segment-anything",
    "Carl Burks wrapping github.com/facebookresearch/segment-anything",
    "2023",
    "<Image>/Image/Split To Layers",#"<Image>/Filters/Selection/Split To Layers",
    "*",
    [],
    [],
    split_to_layers_no_face)

register(
    "python_fu_segments_to_layers_face",
    "Split To Layers Faces",
    "Split an image into layers from segments",
    "Carl Burks wrapping github.com/facebookresearch/segment-anything",
    "Carl Burks wrapping github.com/facebookresearch/segment-anything",
    "2023",
    "<Image>/Image/Split To Layers Faces",#"<Image>/Filters/Selection/Split To Layers",
    "*",
    [],
    [],
    split_to_layers_face)

main()
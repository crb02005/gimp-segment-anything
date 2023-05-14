#import time
import os
import json
import cv2
import sys
import json
import numpy as np
import torch
#import matplotlib.pyplot as plt

current_path = os.path.dirname(os.path.realpath(__file__))

with open("%s/config.json" % current_path) as f:
    config = json.load(f)

checkpoint_location = config["checkpoint_location"]
#"C:\\MLModels\\SegmentAnything\\sam_vit_h_4b8939.pth"
face_cascade_location = config["face_cascade_location"]
#'C:\\MLModels\\Open_CV\\haarcascade_frontalface_default.xml'


filename = sys.argv[1]
x1 = int(sys.argv[2])
y1 = int(sys.argv[3])
x2 = int(sys.argv[4])
y2 = int(sys.argv[5])
find_faces = bool(sys.argv[6])


# results = [
#         [30,50,10,10,130,10,180,80,100,170,50,80],
#         [230,250,210,210,330,210,380,280,300,370,250,280],
#         [330,350,310,310,530,510,480,580,500,570,650,880]
#     ]

def get_mid_point_of_largest_face(faces):
    faces_data = []
    for (x, y, w, h) in faces:
        center_x = x + w // 2
        center_y = y + h // 2
        faces_data.append([center_x,center_y,(x,y,w,h,w*h)])
    faces_data = sorted(faces_data, key=lambda x: x[2][4])[-1]
    return np.array([[faces_data[0],faces_data[1]]])

def get_bound_size(item):
    x_coords = item[::2]
    y_coords = item[1::2]
    return (max(x_coords) - min(x_coords), max(y_coords) - min(y_coords))


def filter_small_items(items, smallest_x_delta, smallest_y_delta):
    for item in items:
        sizeX, sizeY = get_bound_size(item)
        if(sizeX > smallest_x_delta and sizeY > smallest_y_delta):
            yield item


def get_masks_box(anns):
    if len(anns) == 0:
        return
    masks = []
    for m in anns:

        m = np.array(m).astype(np.uint8)  # Convert mask to numpy array of type uint8
        contours, _ = cv2.findContours(m, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            contour = contour.flatten().tolist()
            masks.append(contour)
            
    return filter_small_items(masks,30,30)

def get_masks_auto(anns):
    if len(anns) == 0:
        return
    
    sorted_anns = sorted(anns, key=(lambda x: x['area']), reverse=True)
    masks = []
    
    for ann in sorted_anns:
        m = ann['segmentation']
        m = np.array(m).astype(np.uint8)  # Convert mask to numpy array of type uint8
        contours, _ = cv2.findContours(m, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            contour = contour.flatten().tolist()
            masks.append(contour)
            
    return filter_small_items(masks,30,30)

# this could move the file off to a SAN and then process on a powerful machine and fire back

image = cv2.imread(filename)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


from segment_anything import SamAutomaticMaskGenerator, sam_model_registry, SamPredictor
sam = sam_model_registry["default"](checkpoint=checkpoint_location)
face_cascade = cv2.CascadeClassifier(face_cascade_location)



if(x1>-1):
    predictor = SamPredictor(sam)
    predictor.set_image(image)
    items = [x1, y1, x2, y2]
    input_box = np.array(items)
    if(find_faces):
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        point = get_mid_point_of_largest_face(faces)
        masks, _, _ = predictor.predict(
            point_labels=np.array([1]),
            point_coords=point,
            box=input_box)
    else:   
        masks, _, _ = predictor.predict(box=input_box)
    results = get_masks_box(masks)

else:
    mask_generator = SamAutomaticMaskGenerator(sam)
    masks = mask_generator.generate(image)
    results = get_masks_auto(masks)


response = {
    "file": filename,
    "data": [_ for _ in results]
}


print(json.dumps(response, indent = 4))
#import time
import cv2
import sys
import json
import numpy as np
import torch
import matplotlib.pyplot as plt

filename = sys.argv[1]
x1 = int(sys.argv[2])
y1 = int(sys.argv[3])
x2 = int(sys.argv[4])
y2 = int(sys.argv[5])

# results = [
#         [30,50,10,10,130,10,180,80,100,170,50,80],
#         [230,250,210,210,330,210,380,280,300,370,250,280],
#         [330,350,310,310,530,510,480,580,500,570,650,880]
#     ]

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
            
    return masks

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
            
    return masks

# this could move the file off to a SAN and then process on a powerful machine and fire back

image = cv2.imread(filename)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

from segment_anything import SamAutomaticMaskGenerator, sam_model_registry, SamPredictor
sam = sam_model_registry["default"](checkpoint="C:\\MLModels\\SegmentAnything\\sam_vit_h_4b8939.pth")

if(x1>-1):
    predictor = SamPredictor(sam)
    predictor.set_image(image)
    items = [x1, y1, x2, y2]
    input_box = np.array(items)
    masks, _, _ = predictor.predict(box=input_box)
    results = get_masks_box(masks)

else:
    mask_generator = SamAutomaticMaskGenerator(sam)
    masks = mask_generator.generate(image)
    results = get_masks_auto(masks)

response = {
    "file": filename,
    "data": results
}


print(json.dumps(response, indent = 4))
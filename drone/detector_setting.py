import numpy as np

LABELS = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train',
          'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter',
          'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
          'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
          'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
          'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon',
          'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
          'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop',
          'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator',
          'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

IMAGE_H, IMAGE_W = 416, 416
GRID_H, GRID_W = 13, 13

CLASS = len(LABELS)
CLASS_WEIGHTS = np.ones(CLASS, dtype='float32')  #
OBJ_THRESHOLD = 0.3  # 0.5
NMS_THRESHOLD = 0.3  # 0.45

# training setting
BATCH_SIZE = 16
WARM_UP_BATCHES = 0

OBJ_THRESHOLD = 0.3  # 0.5
NMS_THRESHOLD = 0.3  # 0.45

BOX              = 5 # bounding_box_machine 개수
ANCHORS          = [0.57273, 0.677385, 1.87446, 2.06253, 3.33843, 5.47434, 7.88282, 3.52778, 9.77052, 9.16828] #xy*2
TRUE_BOX_BUFFER  = 50 # 이미지 안에 최대 사물 개수
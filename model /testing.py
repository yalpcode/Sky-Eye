import glob
import json

import cv2

from tqdm import tqdm
from ultralytics import YOLO

model = YOLO('best-3.pt')

ans = []
for path in tqdm(glob.glob('data/*'), total=len(glob.glob('data/*'))):
    frame = cv2.imread(path)
    frame_info = model(frame)[0]
    objects = []
    for box in frame_info.boxes:
        x, y, w, h = box.xywhn[0]
        cls = int(box.cls)
        obj = {
            "obj_class": str(cls),
            "x": str(x.item()),
            "y": str(y.item()),
            "width": str(w.item()),
            "height": str(h.item())
        }
        objects.append(obj)

    ans.append({
        'filename': path.split('/')[-1],
        'objects': objects
    })

with open('submit.json', 'w') as f:
    json.dump(ans, f)
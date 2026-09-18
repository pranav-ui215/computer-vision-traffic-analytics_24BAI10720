from dataclasses import dataclass
from app.config import DEFAULT_MODEL,VEHICLE_CLASSES

@dataclass
class YOLODetection:
    bbox: tuple
    confidence: float
    class_id: int
    label: str

class YOLODetector:
    def __init__(self,model_name=DEFAULT_MODEL,confidence=.35):
        from ultralytics import YOLO
        self.model=YOLO(model_name); self.confidence=confidence
    def detect(self,frame,vehicle_only=True):
        results=self.model.predict(frame,conf=self.confidence,verbose=False)
        out=[]
        for r in results:
            if r.boxes is None: continue
            for b in r.boxes:
                cid=int(b.cls[0].item()); conf=float(b.conf[0].item())
                if vehicle_only and cid not in VEHICLE_CLASSES: continue
                x1,y1,x2,y2=map(int,b.xyxy[0].tolist())
                label=r.names.get(cid,VEHICLE_CLASSES.get(cid,str(cid)))
                out.append(YOLODetection((x1,y1,x2,y2),conf,cid,label))
        return out

from collections import Counter

def classify_density(vehicle_count,frame_area):
    if frame_area<=0:return "UNKNOWN"
    r=vehicle_count/max(frame_area/100000,1)
    return "LOW" if r<2 else "MEDIUM" if r<5 else "HIGH"

def summarize(detections):
    labels=[getattr(d,"label","object") for d in detections]
    return {"total":len(labels),"by_type":dict(Counter(labels))}

def trajectory_direction(history):
    if len(history)<2:return "STATIONARY"
    x0,y0=history[0];x1,y1=history[-1];dx,dy=x1-x0,y1-y0
    if abs(dx)+abs(dy)<8:return "STATIONARY"
    return ("RIGHT" if dx>0 else "LEFT") if abs(dx)>abs(dy) else ("DOWN" if dy>0 else "UP")

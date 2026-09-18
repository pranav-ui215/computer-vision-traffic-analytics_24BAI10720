import cv2

def draw_detections(frame,detections):
    out=frame.copy()
    for d in detections:
        x1,y1,x2,y2=d.bbox
        cv2.rectangle(out,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.putText(out,f"{getattr(d,'label','object')} {getattr(d,'confidence',0):.2f}",
                    (x1,max(20,y1-7)),cv2.FONT_HERSHEY_SIMPLEX,.55,(0,255,0),2)
    return out

def draw_tracks(frame,tracks):
    out=frame.copy()
    for t in tracks:
        x1,y1,x2,y2=t.bbox
        cv2.rectangle(out,(x1,y1),(x2,y2),(255,180,0),2)
        cv2.putText(out,f"ID {t.track_id} {t.label}",(x1,max(20,y1-8)),
                    cv2.FONT_HERSHEY_SIMPLEX,.55,(255,180,0),2)
        for a,b in zip(t.history,t.history[1:]):cv2.line(out,a,b,(255,180,0),2)
    return out

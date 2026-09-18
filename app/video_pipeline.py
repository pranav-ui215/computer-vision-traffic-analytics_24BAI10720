import cv2,numpy as np
from app.detection.classical_detector import ContourDetector
from app.detection.tracker import CentroidTracker
from app.motion.background import BackgroundMotionAnalyzer
from app.motion.optical_flow import dense_optical_flow,flow_visualization,motion_statistics
from app.visualization.drawing import draw_detections,draw_tracks

def process_video(source,detector_mode="Classical Motion",confidence=.35,min_area=500,max_frames=300,enable_optical_flow=True):
    cap=cv2.VideoCapture(source)
    if not cap.isOpened():raise ValueError(f"Could not open video: {source}")
    yolo=None
    if detector_mode=="YOLO":
        from app.detection.yolo_detector import YOLODetector
        yolo=YOLODetector(confidence=confidence)
    bg=BackgroundMotionAnalyzer(); classical=ContourDetector(min_area); tracker=CentroidTracker()
    prev=None; latest=None; flow_img=None; motions=[]; counts=[]; i=0
    while i<max_frames:
        ok,frame=cap.read()
        if not ok:break
        if frame.shape[1]>960:
            scale=960/frame.shape[1];frame=cv2.resize(frame,(960,int(frame.shape[0]*scale)))
        mask=bg.apply(frame)
        detections=classical.detect(mask) if detector_mode=="Classical Motion" else yolo.detect(frame)
        tracks=tracker.update(detections)
        latest=draw_tracks(draw_detections(frame,detections),tracks)
        g=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if enable_optical_flow and prev is not None:
            f=dense_optical_flow(prev,g);flow_img,mag=flow_visualization(f);motions.append(motion_statistics(mag))
        prev=g;counts.append(len(detections));i+=1
    cap.release()
    return {"frame":latest,"flow":flow_img,"frames_processed":i,"max_objects":max(counts) if counts else 0,
            "average_objects":float(np.mean(counts)) if counts else 0,
            "average_motion":float(np.mean([m["mean"] for m in motions])) if motions else 0,
            "active_tracks":len(tracker.tracks)}

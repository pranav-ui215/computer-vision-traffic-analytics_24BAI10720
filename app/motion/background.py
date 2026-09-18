import cv2, numpy as np
class BackgroundMotionAnalyzer:
    def __init__(self):
        self.subtractor=cv2.createBackgroundSubtractorMOG2(history=300,varThreshold=32,detectShadows=True)
    def apply(self,frame):
        m=self.subtractor.apply(frame); k=np.ones((5,5),np.uint8)
        return cv2.morphologyEx(cv2.morphologyEx(m,cv2.MORPH_OPEN,k),cv2.MORPH_CLOSE,k)

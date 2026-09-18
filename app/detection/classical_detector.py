import cv2
from dataclasses import dataclass

@dataclass
class Detection:
    bbox: tuple
    confidence: float
    label: str = "moving-object"

class ContourDetector:
    def __init__(self, min_area=500):
        self.min_area = min_area

    def detect(self, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        out = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area < self.min_area:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            out.append(Detection((x, y, x + w, y + h),
                                 min(0.99, area / (area + self.min_area))))
        return out

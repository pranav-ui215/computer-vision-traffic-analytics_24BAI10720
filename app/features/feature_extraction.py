import cv2
import numpy as np

def harris_corners(image):
    g = np.float32(image if image.ndim == 2 else cv2.cvtColor(image,cv2.COLOR_BGR2GRAY))
    r = cv2.cornerHarris(g,2,3,0.04)
    return cv2.normalize(r,None,0,255,cv2.NORM_MINMAX).astype(np.uint8)

def hog_descriptor(image):
    hog = cv2.HOGDescriptor()
    return hog.compute(cv2.resize(image,(64,128)))

def sift_keypoints(image):
    g = image if image.ndim == 2 else cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    return cv2.SIFT_create().detectAndCompute(g,None)

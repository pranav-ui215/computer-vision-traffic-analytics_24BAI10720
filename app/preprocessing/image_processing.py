import cv2
import numpy as np

def gray(image):
    if image is None: raise ValueError("Input image is None")
    return image if image.ndim == 2 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def gaussian_blur(image, kernel=5):
    if kernel < 3 or kernel % 2 == 0: raise ValueError("Kernel must be odd and >= 3")
    return cv2.GaussianBlur(image, (kernel,kernel), 0)

def histogram_equalization(image):
    return cv2.equalizeHist(gray(image))

def canny(image, low=50, high=150):
    return cv2.Canny(gaussian_blur(gray(image),5), low, high)

def threshold(image, value=120):
    return cv2.threshold(gray(image), value, 255, cv2.THRESH_BINARY)[1]

def clean_mask(mask, kernel=5):
    k = np.ones((kernel,kernel), np.uint8)
    return cv2.morphologyEx(cv2.morphologyEx(mask, cv2.MORPH_OPEN,k), cv2.MORPH_CLOSE,k)

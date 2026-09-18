import numpy as np,cv2
from types import SimpleNamespace
from app.preprocessing.image_processing import gaussian_blur,canny,histogram_equalization
from app.analytics.traffic import classify_density,trajectory_direction
from app.detection.tracker import CentroidTracker

def img():
    x=np.zeros((100,100,3),np.uint8);cv2.rectangle(x,(20,20),(80,80),(255,255,255),-1);return x

def test_blur_shape(): assert gaussian_blur(img()).shape==img().shape
def test_canny(): assert canny(img()).shape==(100,100)
def test_histogram(): assert histogram_equalization(img()).shape==(100,100)
def test_density(): assert classify_density(1,960*540)=="LOW"
def test_direction(): assert trajectory_direction([(0,0),(20,0)])=="RIGHT"
def test_tracker(): 
    t=CentroidTracker(); tracks=t.update([SimpleNamespace(bbox=(10,10,30,30),label="car")])
    assert tracks[0].track_id==1

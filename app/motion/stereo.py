import cv2,numpy as np

def compute_disparity(left,right,num_disparities=128,block_size=5):
    if num_disparities%16: raise ValueError("num_disparities must be divisible by 16")
    if block_size<3 or block_size%2==0: raise ValueError("block_size must be odd and >= 3")
    l=cv2.cvtColor(left,cv2.COLOR_BGR2GRAY);r=cv2.cvtColor(right,cv2.COLOR_BGR2GRAY)
    s=cv2.StereoSGBM_create(minDisparity=0,numDisparities=num_disparities,blockSize=block_size,
        P1=8*block_size**2,P2=32*block_size**2,uniquenessRatio=10,
        speckleWindowSize=100,speckleRange=2,disp12MaxDiff=1)
    d=s.compute(l,r).astype(np.float32)/16
    valid=d>0; n=np.zeros_like(d,dtype=np.uint8)
    if valid.any(): n[valid]=cv2.normalize(d[valid],None,0,255,cv2.NORM_MINMAX).astype(np.uint8)
    return d,n

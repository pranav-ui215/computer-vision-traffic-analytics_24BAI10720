import cv2,numpy as np

def dense_optical_flow(prev,cur):
    return cv2.calcOpticalFlowFarneback(prev,cur,None,.5,3,15,3,5,1.2,0)

def flow_visualization(flow):
    mag,ang=cv2.cartToPolar(flow[...,0],flow[...,1])
    hsv=np.zeros((flow.shape[0],flow.shape[1],3),np.uint8)
    hsv[...,0]=(ang*180/np.pi/2).astype(np.uint8);hsv[...,1]=255
    hsv[...,2]=cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX).astype(np.uint8)
    return cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR),mag

def motion_statistics(mag):
    return {"mean":float(np.mean(mag)),"median":float(np.median(mag)),"max":float(np.max(mag))}

import cv2

def contours(mask, min_area=500):
    cs,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    return [c for c in cs if cv2.contourArea(c)>=min_area]

def draw(image, cs):
    out=image.copy()
    cv2.drawContours(out,cs,-1,(0,255,0),2)
    return out

from pathlib import Path
import cv2,numpy as np
from app.config import SAMPLE_VIDEO_DIR

def generate_video(output_path=None,frames=180,fps=24,width=960,height=540):
    SAMPLE_VIDEO_DIR.mkdir(parents=True,exist_ok=True)
    out=Path(output_path) if output_path else SAMPLE_VIDEO_DIR/"synthetic_traffic.mp4"
    w=cv2.VideoWriter(str(out),cv2.VideoWriter_fourcc(*"mp4v"),fps,(width,height))
    for i in range(frames):
        f=np.full((height,width,3),35,np.uint8)
        cv2.rectangle(f,(0,110),(width,height),(70,70,70),-1)
        cv2.line(f,(width//2,110),(width//2,height),(220,220,220),2)
        x=int(80+(i*4)%780);y=260
        cv2.rectangle(f,(x,y),(x+90,y+50),(180,180,180),-1)
        cv2.rectangle(f,(x+12,y+8),(x+35,y+28),(40,40,40),-1);cv2.rectangle(f,(x+55,y+8),(x+78,y+28),(40,40,40),-1)
        x2=int(700-(i*3)%600);y2=380
        cv2.rectangle(f,(x2,y2),(x2+120,y2+60),(150,150,150),-1)
        cv2.circle(f,(x2+25,y2+62),12,(20,20,20),-1);cv2.circle(f,(x2+95,y2+62),12,(20,20,20),-1)
        cv2.putText(f,"Synthetic Traffic Demo",(25,45),cv2.FONT_HERSHEY_SIMPLEX,1,(240,240,240),2)
        w.write(f)
    w.release();return out

if __name__=="__main__":print(generate_video())

import sys
import tempfile
from pathlib import Path

# Make the repository root importable when Streamlit executes app/main.py directly.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import cv2
import numpy as np
import streamlit as st
from PIL import Image
from app.config import DEFAULT_CONFIDENCE,DEFAULT_MIN_CONTOUR_AREA,SAMPLE_VIDEO_DIR
from app.preprocessing.image_processing import gray,gaussian_blur,histogram_equalization,canny,threshold,clean_mask
from app.motion.stereo import compute_disparity
from app.video_pipeline import process_video
from app.analytics.traffic import classify_density

st.set_page_config(page_title="CV Traffic Analytics",page_icon="🚦",layout="wide")
st.title("🚦 Vision-Based Traffic & Road Scene Analytics")
st.caption("CSE3010 Computer Vision — modular image and video analysis")

mode=st.sidebar.radio("Choose module",["Image Processing","Video Analytics","Stereo / Depth"])

if mode=="Image Processing":
    st.subheader("Image Processing")
    up=st.file_uploader("Upload an image",type=["jpg","jpeg","png"])
    if up:
        bgr=cv2.cvtColor(np.array(Image.open(up).convert("RGB")),cv2.COLOR_RGB2BGR)
        op=st.selectbox("Operation",["Grayscale","Gaussian Blur","Histogram Equalization","Canny Edge Detection","Threshold Segmentation","Clean Segmentation Mask"])
        if op=="Grayscale":res=gray(bgr)
        elif op=="Gaussian Blur":res=gaussian_blur(bgr,st.slider("Kernel",3,15,5,2))
        elif op=="Histogram Equalization":res=histogram_equalization(bgr)
        elif op=="Canny Edge Detection":res=canny(bgr,st.slider("Low",0,200,50),st.slider("High",50,300,150))
        elif op=="Threshold Segmentation":res=threshold(bgr,st.slider("Threshold",0,255,120))
        else:res=clean_mask(threshold(bgr,st.slider("Threshold",0,255,120)))
        c1,c2=st.columns(2);c1.image(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB),caption="Input",use_container_width=True)
        c2.image(res if res.ndim==2 else cv2.cvtColor(res,cv2.COLOR_BGR2RGB),caption="Output",use_container_width=True,clamp=True)

elif mode=="Video Analytics":
    st.subheader("Video Analytics")
    up=st.file_uploader("Upload road/traffic video",type=["mp4","avi","mov","mkv"])
    demo=st.checkbox("Use included synthetic demo")
    det=st.selectbox("Detection mode",["Classical Motion","YOLO"])
    conf=st.slider("YOLO confidence",.10,.90,DEFAULT_CONFIDENCE,.05)
    area=st.slider("Minimum contour area",100,5000,DEFAULT_MIN_CONTOUR_AREA,100)
    frames=st.slider("Frames to process",30,1000,300,30)
    optical=st.checkbox("Enable optical flow",True)
    if st.button("Run Video Analysis",type="primary"):
        temp=None
        if demo:
            p=SAMPLE_VIDEO_DIR/"synthetic_traffic.mp4"
            if not p.exists():
                from app.generate_demo import generate_video
                generate_video(p)
            source=str(p)
        elif up:
            f=tempfile.NamedTemporaryFile(delete=False,suffix=Path(up.name).suffix or ".mp4");f.write(up.read());f.close();temp=f.name;source=temp
        else:st.error("Upload a video or enable the demo.");st.stop()
        try:
            with st.spinner("Processing video..."):r=process_video(source,det,conf,area,frames,optical)
            a,b,c,d=st.columns(4);a.metric("Frames",r["frames_processed"]);b.metric("Peak Objects",r["max_objects"]);c.metric("Avg Objects",f'{r["average_objects"]:.1f}');d.metric("Avg Motion",f'{r["average_motion"]:.3f}')
            if r["frame"] is not None:st.image(cv2.cvtColor(r["frame"],cv2.COLOR_BGR2RGB),caption="Latest analyzed frame",use_container_width=True)
            if r["flow"] is not None:st.image(cv2.cvtColor(r["flow"],cv2.COLOR_BGR2RGB),caption="Optical flow",use_container_width=True)
            st.info(f"Estimated traffic density category: **{classify_density(round(r['average_objects']),960*540)}**")
        except Exception as e:st.exception(e)
        finally:
            if temp:Path(temp).unlink(missing_ok=True)

else:
    st.subheader("Stereo / Depth")
    left=st.file_uploader("Left image",type=["jpg","jpeg","png"],key="left")
    right=st.file_uploader("Right image",type=["jpg","jpeg","png"],key="right")
    if left and right and st.button("Compute Disparity",type="primary"):
        l=cv2.cvtColor(np.array(Image.open(left).convert("RGB")),cv2.COLOR_RGB2BGR)
        r=cv2.cvtColor(np.array(Image.open(right).convert("RGB")),cv2.COLOR_RGB2BGR)
        if l.shape[:2]!=r.shape[:2]:st.error("Images must have equal dimensions.");st.stop()
        try:
            _,disp=compute_disparity(l,r)
            c1,c2=st.columns(2);c1.image(cv2.cvtColor(l,cv2.COLOR_BGR2RGB),caption="Left image",use_container_width=True);c2.image(disp,caption="Normalized disparity/depth proxy",use_container_width=True)
            st.caption("Metric depth requires calibrated camera parameters and stereo baseline.")
        except Exception as e:st.exception(e)

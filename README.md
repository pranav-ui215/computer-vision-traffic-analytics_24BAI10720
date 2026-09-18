# Vision-Based Traffic & Road Scene Analytics

A modular **Computer Vision** project for image processing, traffic-video analysis, object detection/tracking, optical-flow visualization, and stereo disparity estimation. The project is implemented in Python with OpenCV and exposed through a Streamlit web interface.

## Features

### 1. Image Processing
- Grayscale conversion
- Gaussian smoothing
- Histogram equalization
- Canny edge detection
- Binary threshold segmentation
- Morphological mask cleanup

### 2. Video Analytics
- Classical motion detection using MOG2 background subtraction
- Contour-based moving-object detection
- Centroid-based multi-object tracking with track IDs and trajectories
- Optional YOLO vehicle detection
- Dense Farneback optical flow
- Motion statistics
- Basic traffic-density categorization
- Included synthetic traffic video for reproducible testing

### 3. Stereo / Depth
- StereoSGBM disparity estimation from a left/right image pair
- Normalized disparity visualization
- Clear distinction between disparity/depth proxy and calibrated metric depth

## Project Structure

```text
computer-vision-traffic-analytics/
├── app/
│   ├── main.py
│   ├── video_pipeline.py
│   ├── generate_demo.py
│   ├── config.py
│   ├── preprocessing/
│   ├── features/
│   ├── detection/
│   ├── motion/
│   ├── analytics/
│   └── visualization/
├── data/
│   └── sample_videos/
├── docs/
├── notebooks/
├── tests/
├── assets/
├── .gitignore
├── LICENSE
├── pytest.ini
├── requirements.txt
└── requirements-dev.txt
```

## Setup on Windows

Open the project folder in VS Code and run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

If PowerShell blocks activation, use the appropriate execution-policy setting for your machine, then activate `.venv` again.

## Run the tests

```powershell
pytest -q
```

The test suite covers core preprocessing, analytics, and tracking behavior.

## Generate the reproducible demo video

```powershell
python -m app.generate_demo
```

The video is written to:

```text
data/sample_videos/synthetic_traffic.mp4
```

## Run the application

```powershell
streamlit run app/main.py
```

Then open the local Streamlit address shown in the terminal, normally `http://localhost:8501`.

### Recommended first demo

1. Select **Image Processing** and upload a JPG/PNG image.
2. Select **Video Analytics**.
3. Enable **Use included synthetic demo**.
4. Keep **Classical Motion** selected.
5. Enable optical flow.
6. Click **Run Video Analysis**.
7. After the classical pipeline is verified, try **YOLO** with a suitable traffic video.
8. Use **Stereo / Depth** with a genuine stereo image pair.

## YOLO note

YOLO is loaded only when the YOLO detection mode is selected. The project does not require model weights to be committed to GitHub. Ultralytics may download the configured model weights the first time YOLO is used.

## Stereo note

The stereo module produces a disparity visualization. **Metric depth requires camera calibration and a known stereo baseline**; this project intentionally labels the uncalibrated output as a disparity/depth proxy rather than claiming metric distance.

## Testing

Run:

```powershell
pytest -q
```

`pytest.ini` is included so the project root is automatically available for imports when tests are run from the repository root.

## Academic scope

The repository is organized to demonstrate core Computer Vision concepts through a single practical traffic/road-scene application. See `docs/syllabus_mapping.md` for the mapping between implemented components and the course topics.

## License

See [LICENSE](LICENSE).

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
SAMPLE_VIDEO_DIR = DATA_DIR / "sample_videos"
DEFAULT_MODEL = "yolo11n.pt"
DEFAULT_CONFIDENCE = 0.35
DEFAULT_MIN_CONTOUR_AREA = 500
VEHICLE_CLASSES = {2:"car", 3:"motorcycle", 5:"bus", 7:"truck"}

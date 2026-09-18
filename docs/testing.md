# Testing

Run `pytest -q`.

Automated tests cover filtering, edge output, histogram processing, density classification, trajectory direction and tracker ID assignment.

Manual validation should cover:
- image operations with normal and high-resolution images;
- synthetic video with classical detection and optical flow;
- real traffic video with YOLO;
- equal-sized stereo image pairs;
- invalid/missing inputs and unavailable video sources.

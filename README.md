# AI-Powered Retail Video Analytics System

An intelligent retail video analytics application built using Python, YOLOv8 and computer vision to analyse customer movement and behaviour inside retail environments.

## Features

- **Person Detection:** Detect people in video streams using YOLOv8.
- **Object Tracking:** Track detected individuals across video frames.
- **Zone Analytics:** Monitor customer activity within predefined retail zones.
- **Entry and Exit Counting:** Analyse customer movement across designated zones.
- **Dwell-Time Analysis:** Measure how long customers spend in specific areas.
- **Heatmap Generation:** Visualise customer movement and activity patterns.

## Technologies Used

- Python
- YOLOv8
- OpenCV
- ByteTrack
- Computer Vision

## Installation

```bash
git clone https://github.com/asokanharish810-commits/retai_cv.git
cd retai_cv
pip install -r requirements.txt
```

## Usage

Run using your webcam:

```bash
python main.py --source 0
```

Run using a video file:

```bash
python main.py --source store_video.mp4
```

## Author

Asokan Harish

GitHub: https://github.com/asokanharish810-commits
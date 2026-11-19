import argparse
from ultralytics import YOLO
from video_processor import VideoProcessor, ProcessorConfig
from zones import get_zone, update_journey, journey
from analytics import show_summary
import cv2
import zones

CONFIDENCE = 0.4


def parse_args():
    p = argparse.ArgumentParser("Retail Analytics System")
    p.add_argument("--source", default=0, help="Webcam index or video file")
    p.add_argument("--output", default=None, help="Save output video path")
    p.add_argument("--width", type=int, default=None)
    p.add_argument("--height", type=int, default=None)
    p.add_argument("--no-preview", action="store_true")
    return p.parse_args()


def annotate(frame, box, track_id, zone):
    x1, y1, x2, y2 = map(int, box.xyxy[0])

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.putText(
        frame,
        f"ID:{track_id} {zone}",
        (x1, max(20, y1 - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )


def draw_zones(frame):
    colors = {
        "CASHIER":  (255, 0,   0),    # blue
        "SHOPPING": (0,   255, 0),    # green
        "EMPTY":    (0,   0,   255),  # red
        "ENTRY":    (0,   255, 255),  # yellow
    }
    for name, (x1, y1, x2, y2) in zones.ZONES.items():
        color = colors.get(name, (255, 255, 255))
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, name, (x1 + 10, y1 + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)


def main():
    args = parse_args()

    source = int(args.source) if str(args.source).isdigit() else args.source

    config = ProcessorConfig(
        resize_width=args.width,
        resize_height=args.height,
        show_preview=not args.no_preview,
    )

    model = YOLO("yolov8n.pt")

    with VideoProcessor(source=source, output_path=args.output, config=config) as vp:

        # ✅ Detect resolution first
        actual_w = args.width or vp.w
        actual_h = args.height or vp.h
        print(f"📐 Resolution: {actual_w} x {actual_h}")

        # ✅ Set ZONES directly on the module so get_zone() sees them
        zones.ZONES = {
            "CASHIER":  (0,           0,           actual_w//2, actual_h//2),
            "SHOPPING": (actual_w//2, 0,           actual_w,    actual_h//2),
            "EMPTY":    (0,           actual_h//2, actual_w//2, actual_h),
            "ENTRY":    (actual_w//2, actual_h//2, actual_w,    actual_h),
        }
        print(f"📦 ZONES: {zones.ZONES}")

        for frame_idx, frame in vp.frames():

            results = model.track(
                frame,
                persist=True,
                tracker="bytetrack.yaml",
                classes=[0],
                conf=CONFIDENCE
            )

            boxes = results[0].boxes

            if boxes is not None and boxes.id is not None:

                for i, box in enumerate(boxes):

                    track_id = boxes.id[i]

                    if track_id is None:
                        continue

                    track_id = int(track_id)

                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    zone = get_zone(cx, cy)
                    update_journey(track_id, zone)

                    annotate(frame, box, track_id, zone)

            draw_zones(frame)

            vp.show(frame)
            vp.write(frame)

    show_summary(journey)


if __name__ == "__main__":
    main()
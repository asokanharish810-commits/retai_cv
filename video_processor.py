print("🔥 VIDEO PROCESSOR LOADED")

import cv2
import os
import time
from dataclasses import dataclass
from typing import Optional, Generator


# ───────────────── CONFIG ─────────────────
@dataclass
class ProcessorConfig:
    resize_width: Optional[int] = None
    resize_height: Optional[int] = None
    target_fps: Optional[float] = None
    show_preview: bool = True
    window_title: str = "Retail Analytics"


# ───────────────── CORE ─────────────────
class VideoProcessor:

    def __init__(self, source=0, output_path=None, config=None):
        self.source = source
        self.output_path = output_path
        self.config = config or ProcessorConfig()

        self.cap = None
        self.writer = None
        self.stop = False

        self.w = 0
        self.h = 0
        self.fps = 30.0

    def __enter__(self):
        self._open()
        if self.output_path:
            self._open_writer()
        return self

    def __exit__(self, *args):
        self.release()

    # ───────── OPEN VIDEO ─────────
    def _open(self):

        source = self.source

        if isinstance(source, str) and source.isdigit():
            source = int(source)

        if isinstance(source, str):
            source = source.strip().strip('"').strip("'")
            if not os.path.exists(source):
                raise FileNotFoundError(f"Video not found: {source}")

        self.cap = cv2.VideoCapture(source)

        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open source: {source}")

        self.w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.fps = fps if fps and fps > 1 else 30

        print(f"📹 OPENED: {source}")

    # ───────── FRAME LOOP ─────────
    def frames(self) -> Generator:

        idx = 0
        cfg = self.config

        delay = (1 / cfg.target_fps) if cfg.target_fps else 0

        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("📌 Video finished OR cannot read frame")
                break

            if delay:
                time.sleep(delay)

            if cfg.resize_width or cfg.resize_height:
                w = cfg.resize_width or self.w
                h = cfg.resize_height or self.h
                frame = cv2.resize(frame, (w, h))

            yield idx, frame
            idx += 1

            if self.stop:
                break

    # ───────── SHOW ─────────
    def show(self, frame):
        if self.config.show_preview:
            cv2.imshow(self.config.window_title, frame)
            if cv2.waitKey(1) & 0xFF == 27:
                self.stop = True

    # ───────── WRITE ─────────
    def write(self, frame):
        if self.writer:
            self.writer.write(frame)

    # ───────── OUTPUT ─────────
    def _open_writer(self):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        w = self.config.resize_width or self.w
        h = self.config.resize_height or self.h
        fps = self.config.target_fps or self.fps

        self.writer = cv2.VideoWriter(
            self.output_path,
            fourcc,
            fps,
            (w, h)
        )

        print(f"💾 Saving to: {self.output_path}")

    # ───────── CLEAN ─────────
    def release(self):
        if self.cap:
            self.cap.release()

        if self.writer:
            self.writer.release()
            print("✅ Video saved")

        cv2.destroyAllWindows()
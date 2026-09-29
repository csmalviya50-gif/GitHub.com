#!/usr/bin/env python3
"""
Turn a single photo into a short video with a smooth zoom/pan (Ken Burns)
effect and fade in/out. All settings live in config.py.

Usage:
    python3 make_video.py
"""
import os
import sys
import numpy as np
from PIL import Image
import imageio.v2 as imageio

import config as C


def ease(t: float) -> float:
    """Ease-in-out so the motion starts and ends gently."""
    return t * t * (3 - 2 * t)


def build_frame(img: Image.Image, progress: float) -> np.ndarray:
    """Crop + zoom + pan the source image for one moment in time."""
    iw, ih = img.size
    target_ratio = C.WIDTH / C.HEIGHT

    # Largest region of the source that matches the output aspect ratio.
    if iw / ih > target_ratio:
        base_h = ih
        base_w = int(ih * target_ratio)
    else:
        base_w = iw
        base_h = int(iw / target_ratio)

    zoom = C.ZOOM_START + (C.ZOOM_END - C.ZOOM_START) * progress
    crop_w = base_w / zoom
    crop_h = base_h / zoom

    # Center, then apply pan drift over the available slack.
    max_dx = (iw - crop_w) / 2
    max_dy = (ih - crop_h) / 2
    cx = iw / 2 + C.PAN_X * max_dx * progress
    cy = ih / 2 + C.PAN_Y * max_dy * progress

    left = max(0, min(iw - crop_w, cx - crop_w / 2))
    top = max(0, min(ih - crop_h, cy - crop_h / 2))

    frame = img.crop((int(left), int(top),
                      int(left + crop_w), int(top + crop_h)))
    frame = frame.resize((C.WIDTH, C.HEIGHT), Image.LANCZOS)
    return np.asarray(frame)


def apply_fade(frame: np.ndarray, t: float, total: float) -> np.ndarray:
    k = 1.0
    if C.FADE_IN_SEC > 0 and t < C.FADE_IN_SEC:
        k = min(k, t / C.FADE_IN_SEC)
    if C.FADE_OUT_SEC > 0 and t > total - C.FADE_OUT_SEC:
        k = min(k, (total - t) / C.FADE_OUT_SEC)
    if k >= 1.0:
        return frame
    return (frame.astype(np.float32) * max(0.0, k)).astype(np.uint8)


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    in_path = os.path.join(here, C.INPUT_IMAGE)
    out_path = os.path.join(here, C.OUTPUT_VIDEO)

    if not os.path.exists(in_path):
        print(f"ERROR: input image not found: {in_path}", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    img = Image.open(in_path).convert("RGB")
    total_frames = int(C.FPS * C.DURATION_SEC)
    total_sec = C.DURATION_SEC

    print(f"Input : {in_path} ({img.size[0]}x{img.size[1]})")
    print(f"Output: {out_path}")
    print(f"Video : {C.WIDTH}x{C.HEIGHT}, {C.FPS}fps, "
          f"{C.DURATION_SEC}s ({total_frames} frames)")

    writer = imageio.get_writer(
        out_path, fps=C.FPS, codec=C.CODEC,
        bitrate=C.BITRATE, macro_block_size=None,
        ffmpeg_params=["-pix_fmt", "yuv420p"],  # broad player compatibility
    )
    try:
        for i in range(total_frames):
            t = i / C.FPS
            progress = ease(i / max(1, total_frames - 1))
            frame = build_frame(img, progress)
            frame = apply_fade(frame, t, total_sec)
            writer.append_data(frame)
    finally:
        writer.close()

    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"Done. Wrote {out_path} ({size_mb:.2f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""
Project = version 1 Caption for videos
"""

import cv2
import numpy as np
import pysrt
from PIL import Image, ImageDraw, ImageFont
import subprocess
import tempfile
import os
from functools import lru_cache

# Config

INPUT_VIDEO = "input.mp4"
INPUT_SRT = "subtitles.srt"
OUTPUT_VIDEO = "output.mp4"
FONT_PATH = "Anton-Regular.ttf"

FONT_SIZE = 80
FONT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 0, 0)
STROKE_COLOR = (0, 0, 0)
STROKE_WIDTH = 8

CAPTION_Y_POSITION = 0.6
HIGHLIGHT_SCALE = 1.15
WORD_SPACING = 10
LINE_SPACING = 12

# Text Renderer

class TextRenderer:
    def __init__(self, font_path, font_size, stroke_width):
        self.stroke_width = stroke_width

        try:
            self.font = ImageFont.truetype(font_path, font_size)
            self.font_hl = ImageFont.truetype(
                font_path, int(font_size * HIGHLIGHT_SCALE)
            )
        except:
            self.font = ImageFont.load_default()
            self.font_hl = self.font

        self.cache = {}

    @lru_cache(maxsize=3000)
    def get_text_size(self, text, highlight=False):
        font = self.font_hl if highlight else self.font
        img = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), text, font=font)

        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]

        # SAFETY EXPANSION
        expand = self.stroke_width * 4
        return width + expand, height + expand

    def render_text(self, text, color, highlight=False):
        key = (text, color, highlight)
        if key in self.cache:
            return self.cache[key]

        font = self.font_hl if highlight else self.font
        width, height = self.get_text_size(text, highlight)

        # OVER-ALLOCATED padding
        pad = int(self.stroke_width * 2.5) + 10

        img = Image.new(
            "RGBA",
            (width + pad * 2, height + pad * 2),
            (0, 0, 0, 0),
        )
        draw = ImageDraw.Draw(img)

        x, y = pad, pad

        # Stroke
        for dx in range(-self.stroke_width, self.stroke_width + 1, 2):
            for dy in range(-self.stroke_width, self.stroke_width + 1, 2):
                draw.text(
                    (x + dx, y + dy),
                    text,
                    font=font,
                    fill=STROKE_COLOR + (255,),
                )

        # Main text
        draw.text(
            (x, y),
            text,
            font=font,
            fill=color + (255,),
        )

        arr = np.array(img)
        self.cache[key] = arr
        return arr



# OVERLAY


def overlay_rgba(bg, overlay, x, y):
    h, w = overlay.shape[:2]
    bg_h, bg_w = bg.shape[:2]

    sx0 = max(0, -x)
    sy0 = max(0, -y)
    sx1 = min(w, bg_w - x)
    sy1 = min(h, bg_h - y)

    if sx1 <= sx0 or sy1 <= sy0:
        return bg

    dx0 = max(x, 0)
    dy0 = max(y, 0)

    ov = overlay[sy0:sy1, sx0:sx1]
    alpha = ov[:, :, 3:4] / 255.0
    ov_rgb = cv2.cvtColor(ov[:, :, :3], cv2.COLOR_RGB2BGR)

    roi = bg[dy0:dy0 + ov.shape[0], dx0:dx0 + ov.shape[1]]
    bg[dy0:dy0 + ov.shape[0], dx0:dx0 + ov.shape[1]] = (
        ov_rgb * alpha + roi * (1 - alpha)
    ).astype(np.uint8)

    return bg


# SUBTITLE HELPERS


def split_words(text, start, end):
    words = text.split()
    if not words:
        return []
    dur = end - start
    step = dur / len(words)
    return [
        (w, start + i * step, start + (i + 1) * step)
        for i, w in enumerate(words)
    ]


def build_index(subs):
    index = {}
    for s in subs:
        start = s.start.ordinal / 1000
        end = s.end.ordinal / 1000
        text = s.text.replace("\n", " ").upper()
        words = split_words(text, start, end)

        for sec in range(int(start), int(end) + 1):
            index.setdefault(sec, []).append(
                {
                    "text": text,
                    "start": start,
                    "end": end,
                    "words": words,
                }
            )
    return index


# =========================
# FAST LINE WRAPPING
# =========================

def wrap_words(words, renderer, max_width, active_idx):
    lines = []
    current = []
    current_width = 0

    for i, word in enumerate(words):
        is_active = (i == active_idx)
        w, _ = renderer.get_text_size(word, is_active)
        w += WORD_SPACING

        if current_width + w <= max_width:
            current.append((word, i))
            current_width += w
        else:
            lines.append(current)
            current = [(word, i)]
            current_width = w

    if current:
        lines.append(current)

    return lines


# =========================
# FRAME PROCESSING
# =========================

def add_captions(frame, t, index, renderer, vw, vh):
    sec = int(t)
    if sec not in index:
        return frame

    sub = next(
        (s for s in index[sec] if s["start"] <= t < s["end"]), None
    )
    if not sub:
        return frame

    active_idx = -1
    for i, (_, a, b) in enumerate(sub["words"]):
        if a <= t < b:
            active_idx = i
            break

    words = sub["text"].split()
    max_line_width = int(vw * 0.92)

    lines = wrap_words(words, renderer, max_line_width, active_idx)

    y = int(vh * CAPTION_Y_POSITION)

    for line in lines:
        sizes = []
        total_width = 0

        for word, idx in line:
            is_active = idx == active_idx
            w, h = renderer.get_text_size(word, is_active)
            sizes.append((word, idx, w, h, is_active))
            total_width += w + WORD_SPACING

        x = max((vw - total_width) // 2, 10)

        max_h = max(s[3] for s in sizes)
        if y + max_h > vh - 20:
            y = vh - max_h - 20

        for word, idx, w, h, is_active in sizes:
            color = HIGHLIGHT_COLOR if is_active else FONT_COLOR
            img = renderer.render_text(word, color, is_active)
            frame = overlay_rgba(frame, img, x, y)
            x += w + WORD_SPACING

        y += max_h + LINE_SPACING

    return frame


# =========================
# MAIN
# =========================

def main():
    cap = cv2.VideoCapture(INPUT_VIDEO)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    vw = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    vh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    THUMBNAIL_SECONDS = 0.5
    skip_last_frames = int(fps * THUMBNAIL_SECONDS)

    subs = pysrt.open(INPUT_SRT)
    index = build_index(subs)

    renderer = TextRenderer(FONT_PATH, FONT_SIZE, STROKE_WIDTH)

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    out = cv2.VideoWriter(
        temp, cv2.VideoWriter_fourcc(*"mp4v"), fps, (vw, vh)
    )

    frame_no = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        t = frame_no / fps

        if frame_no < total - skip_last_frames:
            frame = add_captions(frame, t, index, renderer, vw, vh)

        out.write(frame)
        frame_no += 1

        # ✅ PROGRESS
        if frame_no % fps == 0:
            print(f"Processing: {frame_no}/{total} frames", end="\r")

    cap.release()
    out.release()

    print("\nMerging audio...")

    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", temp,
            "-i", INPUT_VIDEO,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest", OUTPUT_VIDEO,
        ]
    )

    os.remove(temp)
    print("DONE:", OUTPUT_VIDEO)


if __name__ == "__main__":
    main()

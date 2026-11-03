"""
Polaroid Camera Application
----------------------------
A fun desktop webcam app that captures photos, applies filters/stickers/text,
composites them onto polaroid-style frames, and saves/prints them.

Dependencies:
    pip install opencv-python pillow numpy
"""

import cv2
import os
import random
import math
import threading
import time
from datetime import datetime

from PIL import (Image, ImageDraw, ImageFont, ImageEnhance,
                  ImageFilter, ImageTk, ImageOps)
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# ======================================================================
# CONSTANTS
# ======================================================================

POLAROID_W = 1050
POLAROID_H = 1260
BORDER = 60
BOTTOM_BORDER = 200
SEP = 60  # 0.2 inch at 300 DPI

FONT_PATH = r"C:\Windows\Fonts\Comicbd.ttf"

PICTURES_FOLDER = os.path.join(os.path.expanduser("~"), "Pictures")

TEXT_COLORS = {
    "black": (0, 0, 0), "white": (255, 255, 255), "pink": (255, 105, 180),
    "red": (220, 20, 60), "blue": (30, 100, 220), "gray": (120, 120, 120),
    "yellow": (240, 200, 0), "purple": (150, 60, 200), "green": (40, 160, 70),
}

FONT_SIZES = [26, 31, 36, 41, 46, 51, 56, 66, 76]

STICKER_FILL_COLORS = {
    "Hot Pink": (255, 20, 147), "Blue": (30, 100, 220), "Yellow": (255, 215, 0),
    "Green": (40, 160, 70), "Lime": (170, 255, 0), "White": (255, 255, 255),
    "Grey": (160, 160, 160), "Purple": (150, 60, 200),
}

STICKER_TEXTS = [
    "Random", "None", "Custom", "#J4F", "I HATE Photos!", "AHHHH!", "LOL!", "ROFL!",
    "BAE!", "143!", "OMG!", "SO MUCH FUN!", "WHAT!?", "PARTY TIME!",
    "SELFIE TIME!", "#BFF", "BEST DAY EVER!",
]

STICKER_SHAPES = ["Random", "Bubble", "Star", "Cloud", "Heart"]

# 180+ sayings - generated via combination for brevity + variety
_BASE_SAYINGS = [
    "Smile big!", "Caught in 4K!", "Picture perfect!", "Say cheese!",
    "Good times!", "Making memories!", "Best day ever!", "Pure joy!",
    "Living my best life!", "Vibin'!", "So much fun!", "Squad goals!",
    "Candid moment!", "Flash mob!", "Framed forever!", "Memory unlocked!",
    "Just vibes!", "Golden hour!", "Snap happy!", "This is us!",
    "Click & giggle!", "Lights, camera, fun!", "Forever young!",
    "Carpe diem!", "Shine bright!", "Good vibes only!", "Stay golden!",
    "Epic moment!", "Laugh out loud!", "You and me!", "Perfectly imperfect!",
    "Unforgettable!", "Throwback ready!", "Chasing sunsets!", "Dream big!",
    "Adventure awaits!", "Here for the memories!", "Keep it real!",
    "Capturing magic!", "Life in color!", "Wild and free!", "Stay weird!",
    "All smiles!", "Happy accident!", "Picture this!", "Moment of bliss!",
    "Shutterbug!", "Totally snap-worthy!", "Flashback starts here!",
    "One for the books!",
]
_SUFFIXES = ["", " :)", "!!", " forever", " today", " always", " <3", " yay"]
SAYINGS = []
for b in _BASE_SAYINGS:
    for s in _SUFFIXES:
        SAYINGS.append((b + s).strip())
SAYINGS = list(dict.fromkeys(SAYINGS))  # dedupe, preserve order
while len(SAYINGS) < 180:
    SAYINGS.append(random.choice(_BASE_SAYINGS))

# ======================================================================
# FILTER FUNCTIONS (operate on PIL Image, return PIL Image)
# ======================================================================

def f_none(img):
    return img

def f_bw(img):
    return ImageOps.grayscale(img).convert("RGB")

def f_cinematic(img):
    img = ImageEnhance.Contrast(img).enhance(1.25)
    img = ImageEnhance.Color(img).enhance(0.85)
    r, g, b = img.split()
    b = b.point(lambda i: min(255, i * 1.1))
    r = r.point(lambda i: i * 0.95)
    img = Image.merge("RGB", (r, g, b))
    return img

def f_vintage(img):
    img = ImageEnhance.Color(img).enhance(0.6)
    img = ImageEnhance.Contrast(img).enhance(0.9)
    sepia = Image.new("RGB", img.size, (112, 66, 20))
    return Image.blend(img, sepia, 0.2)

def f_watercolor(img):
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img = img.filter(ImageFilter.EDGE_ENHANCE)
    return ImageEnhance.Color(img).enhance(1.3)

def f_crosshatch(img):
    gray = ImageOps.grayscale(img)
    edges = gray.filter(ImageFilter.FIND_EDGES)
    return ImageOps.invert(edges).convert("RGB")

def f_glitch(img):
    img = img.copy()
    r, g, b = img.split()
    w, h = img.size
    shift = w // 50 or 1
    r = ImageOps.offset(r, shift, 0)
    b = ImageOps.offset(b, -shift, 0)
    return Image.merge("RGB", (r, g, b))

def f_beauty(img):
    img = img.filter(ImageFilter.SMOOTH)
    img = ImageEnhance.Brightness(img).enhance(1.08)
    return ImageEnhance.Contrast(img).enhance(1.05)

def f_cartoon(img):
    img2 = img.convert("RGB").quantize(colors=24).convert("RGB")
    edges = ImageOps.grayscale(img).filter(ImageFilter.FIND_EDGES)
    edges = edges.point(lambda i: 255 if i > 40 else 0)
    img2 = ImageEnhance.Color(img2).enhance(1.6)
    out = Image.composite(Image.new("RGB", img.size, (0, 0, 0)), img2,
                           ImageOps.invert(edges))
    return out

def f_oilpaint(img):
    img = img.filter(ImageFilter.ModeFilter(size=7))
    img = ImageEnhance.Contrast(img).enhance(1.2)
    return ImageEnhance.Color(img).enhance(1.3)

def f_pencil_sketch(img):
    gray = ImageOps.grayscale(img)
    inv = ImageOps.invert(gray)
    blur = inv.filter(ImageFilter.GaussianBlur(21))
    sketch = Image.blend(gray, ImageOps.invert(blur), 0.5)
    return sketch.convert("RGB")

def f_charcoal(img):
    gray = ImageOps.grayscale(img)
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edges = ImageEnhance.Contrast(edges).enhance(2.0)
    return ImageOps.invert(edges).convert("RGB")

def f_pastel(img):
    img = ImageEnhance.Color(img).enhance(0.6)
    return ImageEnhance.Brightness(img).enhance(1.15)

def f_popart(img):
    return img.convert("RGB").quantize(colors=4).convert("RGB")

def f_neon(img):
    edges = img.filter(ImageFilter.FIND_EDGES)
    img = ImageEnhance.Color(img).enhance(1.8)
    return Image.blend(img, edges, 0.4)

def f_cyberpunk(img):
    r, g, b = img.split()
    r = r.point(lambda i: min(255, i * 1.3))
    b = b.point(lambda i: min(255, i * 1.3))
    img = Image.merge("RGB", (r, g, b))
    return ImageEnhance.Contrast(img).enhance(1.2)

def f_blur(img):
    return img.filter(ImageFilter.GaussianBlur(5))

def f_sharpen(img):
    return ImageEnhance.Sharpness(img).enhance(2.5)

def f_emboss(img):
    return img.filter(ImageFilter.EMBOSS).convert("RGB")

def f_edge_detect(img):
    return img.filter(ImageFilter.FIND_EDGES)

def f_solarize(img):
    return ImageOps.solarize(img, threshold=128)

def f_pixelate(img):
    small = img.resize((img.width // 16, img.height // 16), Image.NEAREST)
    return small.resize(img.size, Image.NEAREST)

def f_hdr(img):
    img = ImageEnhance.Contrast(img).enhance(1.3)
    img = ImageEnhance.Color(img).enhance(1.3)
    return ImageEnhance.Sharpness(img).enhance(1.5)

def f_vignette(img):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((-w * 0.3, -h * 0.3, w * 1.3, h * 1.3), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(w // 6))
    black = Image.new("RGB", (w, h), (0, 0, 0))
    return Image.composite(img, black, mask)

def f_film_grain(img):
    import numpy as np
    arr = np.array(img).astype(int)
    noise = np.random.randint(-25, 25, arr.shape)
    arr = (arr + noise).clip(0, 255).astype("uint8")
    return Image.fromarray(arr)

def f_mirror(img):
    return ImageOps.mirror(img)

def f_autumn(img):
    r, g, b = img.split()
    r = r.point(lambda i: min(255, i * 1.2 + 15))
    g = g.point(lambda i: i * 0.9)
    b = b.point(lambda i: i * 0.6)
    return Image.merge("RGB", (r, g, b))

def f_winter(img):
    r, g, b = img.split()
    b = b.point(lambda i: min(255, i * 1.25))
    r = r.point(lambda i: i * 0.85)
    return Image.merge("RGB", (r, g, b))

def f_summer(img):
    img = ImageEnhance.Brightness(img).enhance(1.15)
    return ImageEnhance.Color(img).enhance(1.3)

def f_spring(img):
    r, g, b = img.split()
    g = g.point(lambda i: min(255, i * 1.2))
    return Image.merge("RGB", (r, g, b))

def f_sunset(img):
    r, g, b = img.split()
    r = r.point(lambda i: min(255, i * 1.3))
    g = g.point(lambda i: i * 1.05)
    b = b.point(lambda i: i * 0.7)
    return Image.merge("RGB", (r, g, b))

def f_night(img):
    img = ImageEnhance.Brightness(img).enhance(0.55)
    r, g, b = img.split()
    b = b.point(lambda i: min(255, i * 1.2))
    return Image.merge("RGB", (r, g, b))


FILTERS = {
    "None": f_none,
    "Random Filter": None,  # handled specially
    "Black & White": f_bw,
    "Cinematic": f_cinematic,
    "Vintage": f_vintage,
    "Watercolor": f_watercolor,
    "Cross-hatch": f_crosshatch,
    "Glitch": f_glitch,
    "Beauty Mode": f_beauty,
    "Cartoon": f_cartoon,
    "Oil Painting": f_oilpaint,
    "Pencil Sketch": f_pencil_sketch,
    "Charcoal": f_charcoal,
    "Pastel": f_pastel,
    "Pop Art": f_popart,
    "Neon": f_neon,
    "Cyberpunk": f_cyberpunk,
    "Blur": f_blur,
    "Sharpen": f_sharpen,
    "Emboss": f_emboss,
    "Edge Detect": f_edge_detect,
    "Solarize": f_solarize,
    "Pixelate": f_pixelate,
    "HDR": f_hdr,
    "Vignette": f_vignette,
    "Film Grain": f_film_grain,
    "Mirror": f_mirror,
    "Autumn": f_autumn,
    "Winter": f_winter,
    "Summer": f_summer,
    "Spring": f_spring,
    "Sunset": f_sunset,
    "Night": f_night,
}

FILTER_NAMES = list(FILTERS.keys())
_REAL_FILTER_NAMES = [n for n in FILTER_NAMES if n not in ("None", "Random Filter")]


def apply_filter(img, name):
    try:
        if name == "Random Filter":
            name = random.choice(_REAL_FILTER_NAMES)
        func = FILTERS.get(name, f_none)
        return func(img)
    except Exception as e:
        print(f"[Filter Error] {name}: {e}")
        return img


# ======================================================================
# STICKER DRAWING
# ======================================================================

def draw_bubble(draw, box, fill, outline, width=4):
    x0, y0, x1, y1 = box
    radius = int((x1 - x0) * 0.2)
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    tail = [(x0 + (x1 - x0) * 0.2, y1 - 2),
            (x0 + (x1 - x0) * 0.05, y1 + (y1 - y0) * 0.25),
            (x0 + (x1 - x0) * 0.35, y1 - 2)]
    draw.polygon(tail, fill=fill, outline=outline)

def draw_star(draw, box, fill, outline, width=4):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r_outer = (x1 - x0) / 2
    r_inner = r_outer * 0.45
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        r = r_outer if i % 2 == 0 else r_inner
        points.append((cx + r * math.cos(angle), cy - r * math.sin(angle)))
    draw.polygon(points, fill=fill, outline=outline, width=width)

def draw_cloud(draw, box, fill, outline, width=4):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    circles = [
        (x0 + w * 0.15, y0 + h * 0.5, w * 0.22),
        (x0 + w * 0.40, y0 + h * 0.3, w * 0.28),
        (x0 + w * 0.65, y0 + h * 0.35, w * 0.25),
        (x0 + w * 0.85, y0 + h * 0.55, w * 0.18),
    ]
    for cx, cy, r in circles:
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=outline, width=width)

def draw_heart(draw, box, fill, outline, width=4):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    w = x1 - x0
    h = y1 - y0
    points = []
    for t in range(0, 360, 5):
        rad = math.radians(t)
        x = 16 * math.sin(rad) ** 3
        y = -(13 * math.cos(rad) - 5 * math.cos(2 * rad) -
              2 * math.cos(3 * rad) - math.cos(4 * rad))
        points.append((cx + x * (w / 34), y0 + h / 2 + y * (h / 34)))
    draw.polygon(points, fill=fill, outline=outline, width=width)

STICKER_SHAPE_FUNCS = {
    "Bubble": draw_bubble,
    "Star": draw_star,
    "Cloud": draw_cloud,
    "Heart": draw_heart,
}


def add_sticker(canvas, text_option, shape_option, fill_color, text_color,
                 font_path, font_size, custom_text=""):
    """Draws a sticker in the top-right corner, overlapping the image."""
    if text_option == "None":
        return canvas

    text = text_option
    if text_option == "Random":
        choices = [t for t in STICKER_TEXTS if t not in ("Random", "None", "Custom")]
        text = random.choice(choices)
    elif text_option == "Custom":
        text = custom_text.strip() if custom_text and custom_text.strip() else "..."

    shape = shape_option
    if shape == "Random":
        shape = random.choice([s for s in STICKER_SHAPES if s != "Random"])

    draw = ImageDraw.Draw(canvas)
    w, h = canvas.size
    size = int(w * 0.38)
    x1 = w - int(size * 0.25)
    y0 = int(h * -0.02)
    box = (x1 - size, y0, x1, y0 + size)

    shape_func = STICKER_SHAPE_FUNCS.get(shape, draw_bubble)
    shape_func(draw, box, fill_color, (0, 0, 0), width=4)

    try:
        font = ImageFont.truetype(font_path, max(16, int(font_size * 0.6)))
    except Exception:
        font = ImageFont.load_default()

    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > size * 0.7 and line:
            lines.append(line)
            line = word
        else:
            line = test
    if line:
        lines.append(line)

    total_h = sum(draw.textbbox((0, 0), ln, font=font)[3] for ln in lines)
    y = cy - total_h / 2
    for ln in lines:
        bbox = draw.textbbox((0, 0), ln, font=font)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        draw.text((cx - lw / 2, y), ln, font=font, fill=text_color)
        y += lh + 2

    return canvas


# ======================================================================
# POLAROID COMPOSITION
# ======================================================================

def fit_image(img, target_w, target_h):
    """Resize/crop image to fill target box, preserving aspect ratio (cover-fit)."""
    src_ratio = img.width / img.height
    tgt_ratio = target_w / target_h
    if src_ratio > tgt_ratio:
        new_h = target_h
        new_w = int(new_h * src_ratio)
    else:
        new_w = target_w
        new_h = int(new_w / src_ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def create_polaroid(photos, mode, border_mode, border_color, border_image_path):
    """
    photos: list of PIL Images (already filtered)
    mode: 'Single', '2X', '3X'
    Returns composed polaroid PIL Image.
    """
    canvas = Image.new("RGB", (POLAROID_W, POLAROID_H), border_color)

    if border_mode == "Image Background" and border_image_path and os.path.exists(border_image_path):
        try:
            bg = Image.open(border_image_path).convert("RGB")
            bg = fit_image(bg, POLAROID_W, POLAROID_H)
            canvas.paste(bg, (0, 0))
        except Exception as e:
            print(f"[Border Image Error] {e}")

    photo_area_w = POLAROID_W - 2 * BORDER
    photo_area_h = POLAROID_H - BORDER - BOTTOM_BORDER

    if mode == "Single":
        img = fit_image(photos[0], photo_area_w, photo_area_h)
        canvas.paste(img, (BORDER, BORDER))

    elif mode == "2X":
        each_w = (photo_area_w - SEP) // 2
        img1 = fit_image(photos[0], each_w, photo_area_h)
        img2 = fit_image(photos[1], each_w, photo_area_h)
        canvas.paste(img1, (BORDER, BORDER))
        canvas.paste(img2, (BORDER + each_w + SEP, BORDER))

    elif mode == "3X":
        top_h = int(photo_area_h * 0.6)
        bottom_h = photo_area_h - top_h - SEP
        top_img = fit_image(photos[0], photo_area_w, top_h)
        canvas.paste(top_img, (BORDER, BORDER))

        each_w = (photo_area_w - SEP) // 2
        img2 = fit_image(photos[1], each_w, bottom_h)
        img3 = fit_image(photos[2], each_w, bottom_h)
        y_bottom = BORDER + top_h + SEP
        canvas.paste(img2, (BORDER, y_bottom))
        canvas.paste(img3, (BORDER + each_w + SEP, y_bottom))

    return canvas


def add_text_to_polaroid(canvas, text, text_color, font_size, mode, font_path=FONT_PATH):
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype(font_path, font_size)
        date_font = ImageFont.truetype(font_path, max(18, int(font_size * 0.45)))
    except Exception:
        font = ImageFont.load_default()
        date_font = font

    bottom_y = POLAROID_H - BOTTOM_BORDER
    text_y = bottom_y + 20
    if mode == "3X":
        text_y = bottom_y + 10  # tighter to avoid overlap

    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((POLAROID_W - tw) / 2, text_y), text, font=font, fill=text_color)

    date_str = datetime.now().strftime("%B %d, %Y")
    dbbox = draw.textbbox((0, 0), date_str, font=date_font)
    dw = dbbox[2] - dbbox[0]
    date_y = text_y + (bbox[3] - bbox[1]) + 15
    draw.text(((POLAROID_W - dw) / 2, date_y), date_str, font=date_font, fill=text_color)

    return canvas


# ======================================================================
# MAIN APPLICATION
# ======================================================================

class PolaroidApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📸 Polaroid Camera Fun!")
        self.root.configure(bg="#FFE5B4")
        self.root.geometry("1400x900")

        self.cap = None
        self.cap_lock = threading.Lock()
        self.camera_index = 0
        self.current_frame = None  # PIL image, latest camera frame
        self.result_image = None   # last composed polaroid (PIL)
        self.output_folder = PICTURES_FOLDER
        self.countdown_active = False
        self.last_saved_path = None

        self._setup_styles()
        self._build_gui()
        self._open_camera(0)
        self._update_preview_loop()

    # ------------------------------------------------------------
    # STYLING
    # ------------------------------------------------------------
    def _setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TLabel", background="#FFE5B4", font=("Comic Sans MS", 11))
        style.configure("TFrame", background="#FFE5B4")
        style.configure("TButton", font=("Comic Sans MS", 11, "bold"), padding=6)
        style.configure("Big.TButton", font=("Comic Sans MS", 16, "bold"), padding=12)
        style.configure("TCombobox", font=("Comic Sans MS", 10))

    # ------------------------------------------------------------
    # GUI LAYOUT
    # ------------------------------------------------------------
    def _build_gui(self):
        root = self.root

        # Row 1 ---------------------------------------------------
        row1 = ttk.Frame(root)
        row1.grid(row=0, column=0, columnspan=4, sticky="we", padx=10, pady=5)

        ttk.Label(row1, text="📷 Camera:").pack(side="left", padx=5)
        self.camera_var = tk.StringVar(value="Camera 0")
        camera_combo = ttk.Combobox(row1, textvariable=self.camera_var,
                                     values=[f"Camera {i}" for i in range(4)],
                                     state="readonly", width=12)
        camera_combo.pack(side="left", padx=5)
        camera_combo.bind("<<ComboboxSelected>>", self._on_camera_change)

        ttk.Label(row1, text="🖼️ Picture Mode:").pack(side="left", padx=5)
        self.mode_var = tk.StringVar(value="Single")
        mode_combo = ttk.Combobox(row1, textvariable=self.mode_var,
                                   values=["Single", "2X", "3X"], state="readonly", width=10)
        mode_combo.pack(side="left", padx=5)

        # Row 2 ---------------------------------------------------
        row2 = ttk.Frame(root)
        row2.grid(row=1, column=0, columnspan=4, sticky="we", padx=10, pady=5)

        ttk.Label(row2, text="✨ Filter:").pack(side="left", padx=5)
        self.filter_var = tk.StringVar(value="None")
        ttk.Combobox(row2, textvariable=self.filter_var, values=FILTER_NAMES,
                     state="readonly", width=16).pack(side="left", padx=5)

        ttk.Label(row2, text="💬 Text Mode:").pack(side="left", padx=5)
        self.text_mode_var = tk.StringVar(value="Random")
        text_mode_combo = ttk.Combobox(row2, textvariable=self.text_mode_var,
                                        values=["Random", "From List", "Custom"],
                                        state="readonly", width=10)
        text_mode_combo.pack(side="left", padx=5)
        text_mode_combo.bind("<<ComboboxSelected>>", self._on_text_mode_change)

        self.text_list_var = tk.StringVar(value=SAYINGS[0])
        self.text_list_combo = ttk.Combobox(row2, textvariable=self.text_list_var,
                                             values=SAYINGS, state="disabled", width=18)
        self.text_list_combo.pack(side="left", padx=5)

        self.custom_text_var = tk.StringVar()
        self.custom_text_entry = ttk.Entry(row2, textvariable=self.custom_text_var,
                                            width=18, state="disabled")
        self.custom_text_entry.pack(side="left", padx=5)

        ttk.Label(row2, text="🎨 Color:").pack(side="left", padx=5)
        self.text_color_var = tk.StringVar(value="black")
        ttk.Combobox(row2, textvariable=self.text_color_var,
                     values=list(TEXT_COLORS.keys()), state="readonly", width=8).pack(side="left", padx=5)

        ttk.Label(row2, text="🔠 Size:").pack(side="left", padx=5)
        self.font_size_var = tk.IntVar(value=41)
        ttk.Combobox(row2, textvariable=self.font_size_var,
                     values=FONT_SIZES, state="readonly", width=5).pack(side="left", padx=5)

        row2b = ttk.Frame(root)
        row2b.grid(row=2, column=0, columnspan=4, sticky="we", padx=10, pady=5)

        ttk.Label(row2b, text="🏷️ Sticker Text:").pack(side="left", padx=5)
        self.sticker_text_var = tk.StringVar(value="Random")
        sticker_text_combo = ttk.Combobox(row2b, textvariable=self.sticker_text_var, values=STICKER_TEXTS,
                                           state="readonly", width=16)
        sticker_text_combo.pack(side="left", padx=5)
        sticker_text_combo.bind("<<ComboboxSelected>>", self._on_sticker_text_mode_change)

        self.sticker_custom_text_var = tk.StringVar()
        self.sticker_custom_entry = ttk.Entry(row2b, textvariable=self.sticker_custom_text_var,
                                               width=16, state="disabled")
        self.sticker_custom_entry.pack(side="left", padx=5)

        ttk.Label(row2b, text="🔵 Sticker Shape:").pack(side="left", padx=5)
        self.sticker_shape_var = tk.StringVar(value="Random")
        ttk.Combobox(row2b, textvariable=self.sticker_shape_var, values=STICKER_SHAPES,
                     state="readonly", width=10).pack(side="left", padx=5)

        ttk.Label(row2b, text="🎨 Sticker Fill:").pack(side="left", padx=5)
        self.sticker_fill_var = tk.StringVar(value="Hot Pink")
        ttk.Combobox(row2b, textvariable=self.sticker_fill_var,
                     values=list(STICKER_FILL_COLORS.keys()), state="readonly", width=10).pack(side="left", padx=5)

        # Row 3 ---------------------------------------------------
        row3 = ttk.Frame(root)
        row3.grid(row=3, column=0, columnspan=4, sticky="we", padx=10, pady=5)

        ttk.Label(row3, text="📁 Output Folder:").pack(side="left", padx=5)
        self.output_folder_var = tk.StringVar(value=self.output_folder)
        ttk.Entry(row3, textvariable=self.output_folder_var, width=35).pack(side="left", padx=5)
        ttk.Button(row3, text="Browse", command=self._browse_output_folder).pack(side="left", padx=5)

        ttk.Label(row3, text="🖼️ Border Mode:").pack(side="left", padx=5)
        self.border_mode_var = tk.StringVar(value="Solid Color")
        border_combo = ttk.Combobox(row3, textvariable=self.border_mode_var,
                                     values=["Solid Color", "Image Background"],
                                     state="readonly", width=15)
        border_combo.pack(side="left", padx=5)

        self.border_image_var = tk.StringVar()
        ttk.Entry(row3, textvariable=self.border_image_var, width=25).pack(side="left", padx=5)
        ttk.Button(row3, text="Choose Image", command=self._browse_border_image).pack(side="left", padx=5)

        # Row 4 --------------------------------------------------
        row4 = ttk.Frame(root)
        row4.grid(row=4, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        root.grid_rowconfigure(4, weight=1)

        preview_frame = ttk.Frame(row4)
        preview_frame.pack(side="left", expand=True, fill="both", padx=10)
        ttk.Label(preview_frame, text="🎥 Live Preview").pack()
        self.preview_label = ttk.Label(preview_frame, background="black")
        self.preview_label.pack(expand=True, fill="both")

        result_frame = ttk.Frame(row4)
        result_frame.pack(side="left", expand=True, fill="both", padx=10)
        ttk.Label(result_frame, text="🖼️ Result").pack()
        self.result_label = ttk.Label(result_frame, background="white")
        self.result_label.pack(expand=True, fill="both")

        self.countdown_label = ttk.Label(preview_frame, text="", font=("Comic Sans MS", 40, "bold"),
                                          foreground="red")
        self.countdown_label.pack()

        # Row 5 --------------------------------------------------
        row5 = ttk.Frame(root)
        row5.grid(row=5, column=0, columnspan=4, pady=15)

        self.take_picture_btn = ttk.Button(row5, text="📸 Take Picture", style="Big.TButton",
                                            command=self._on_take_picture)
        self.take_picture_btn.pack(side="left", padx=20)

        print_frame = ttk.Frame(row5)
        print_frame.pack(side="left", padx=20)
        ttk.Label(print_frame, text="📄 Paper Size:").pack(side="left")
        self.paper_size_var = tk.StringVar(value="4x6")
        ttk.Combobox(print_frame, textvariable=self.paper_size_var,
                     values=["2.5x3.5", "4x6", "5x7", "8x10"], state="readonly", width=8).pack(side="left", padx=5)
        ttk.Button(print_frame, text="🖨️ Print", command=self._on_print).pack(side="left", padx=5)

    def _on_text_mode_change(self, event=None):
        mode = self.text_mode_var.get()
        self.text_list_combo.config(state="readonly" if mode == "From List" else "disabled")
        self.custom_text_entry.config(state="normal" if mode == "Custom" else "disabled")

    def _on_sticker_text_mode_change(self, event=None):
        mode = self.sticker_text_var.get()
        self.sticker_custom_entry.config(state="normal" if mode == "Custom" else "disabled")

    def _browse_output_folder(self):
        folder = filedialog.askdirectory(initialdir=self.output_folder)
        if folder:
            self.output_folder = folder
            self.output_folder_var.set(folder)

    def _browse_border_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            self.border_image_var.set(path)

    # ------------------------------------------------------------
    # CAMERA HANDLING
    # ------------------------------------------------------------
    def _on_camera_change(self, event=None):
        idx_str = self.camera_var.get().replace("Camera ", "")
        try:
            idx = int(idx_str)
        except ValueError:
            idx = 0
        self._open_camera(idx)

    def _open_camera(self, index):
        try:
            with self.cap_lock:
                if self.cap is not None:
                    self.cap.release()
                self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
                opened = self.cap.isOpened()
            if not opened:
                messagebox.showerror("Camera Error", f"Could not open Camera {index}.")
                self.cap = None
                return
            self.camera_index = index
        except Exception as e:
            messagebox.showerror("Camera Error", f"Error opening camera: {e}")
            self.cap = None

    def _update_preview_loop(self):
        """Continuously updates the live preview, even during countdown/capture."""
        if self.cap is not None and self.cap.isOpened():
            try:
                with self.cap_lock:
                    ret, frame = self.cap.read()
                if ret:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pil_img = Image.fromarray(frame_rgb)
                    self.current_frame = pil_img
                    preview_img = pil_img.copy()
                    preview_img.thumbnail((560, 420))
                    tk_img = ImageTk.PhotoImage(preview_img)
                    self.preview_label.configure(image=tk_img)
                    self.preview_label.image = tk_img
            except Exception as e:
                print(f"[Preview Error] {e}")
        self.root.after(30, self._update_preview_loop)

    def _capture_frame(self):
        """Grab a fresh frame directly from camera (thread-safe)."""
        if self.cap is None or not self.cap.isOpened():
            return None
        try:
            with self.cap_lock:
                ret, frame = self.cap.read()
            if not ret:
                return None
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return Image.fromarray(frame_rgb)
        except Exception as e:
            print(f"[Capture Error] {e}")
            return None

    # ------------------------------------------------------------
    # PICTURE TAKING FLOW
    # ------------------------------------------------------------
    def _on_take_picture(self):
        if self.countdown_active:
            return
        self.take_picture_btn.config(state="disabled")
        threading.Thread(target=self._take_picture_flow, daemon=True).start()

    def _take_picture_flow(self):
        self.countdown_active = True
        mode = self.mode_var.get()
        num_shots = {"Single": 1, "2X": 2, "3X": 3}.get(mode, 1)

        photos = []
        try:
            for i in range(num_shots):
                self._run_countdown(5)
                self._show_smile_message(1.5 if i == 0 else 1.0)
                frame = self._capture_frame()
                if frame is None:
                    raise RuntimeError("Failed to capture frame from camera.")
                filtered = apply_filter(frame, self.filter_var.get())
                photos.append(filtered)
                self._clear_countdown()

            self._assemble_and_save(photos, mode)

        except Exception as e:
            print(f"[Capture Flow Error] {e}")
        finally:
            self.countdown_active = False
            self.root.after(0, lambda: self.take_picture_btn.config(state="normal"))

    def _run_countdown(self, seconds):
        for s in range(seconds, 0, -1):
            self.root.after(0, lambda s=s: self.countdown_label.config(text=str(s)))
            time.sleep(1)

    def _show_smile_message(self, duration):
        self.root.after(0, lambda: self.countdown_label.config(text="Smile! 😄"))
        time.sleep(duration)

    def _clear_countdown(self):
        self.root.after(0, lambda: self.countdown_label.config(text=""))

    def _resolve_text(self):
        mode = self.text_mode_var.get()
        if mode == "Random":
            return random.choice(SAYINGS)
        elif mode == "From List":
            return self.text_list_var.get()
        elif mode == "Custom":
            return self.custom_text_var.get() or "..."
        return ""

    def _assemble_and_save(self, photos, mode):
        try:
            border_mode = self.border_mode_var.get()
            border_color = (255, 255, 255)
            border_image_path = self.border_image_var.get()

            canvas = create_polaroid(photos, mode, border_mode, border_color, border_image_path)

            # Sticker
            sticker_text = self.sticker_text_var.get()
            sticker_shape = self.sticker_shape_var.get()
            sticker_fill = STICKER_FILL_COLORS.get(self.sticker_fill_var.get(), (255, 20, 147))
            text_color = TEXT_COLORS.get(self.text_color_var.get(), (0, 0, 0))
            font_size = int(self.font_size_var.get())
            sticker_custom_text = self.sticker_custom_text_var.get()

            canvas = add_sticker(canvas, sticker_text, sticker_shape, sticker_fill,
                                  text_color, FONT_PATH, font_size,
                                  custom_text=sticker_custom_text)

            # Text + date
            text = self._resolve_text()
            canvas = add_text_to_polaroid(canvas, text, text_color, font_size, mode)

            self.result_image = canvas
            self._display_result(canvas)
            self._save_image(canvas, mode)

        except Exception as e:
            print(f"[Assemble Error] {e}")

    def _display_result(self, canvas):
        def update():
            preview = canvas.copy()
            preview.thumbnail((560, 650))
            tk_img = ImageTk.PhotoImage(preview)
            self.result_label.configure(image=tk_img)
            self.result_label.image = tk_img
        self.root.after(0, update)

    def _save_image(self, canvas, mode):
        try:
            folder = self.output_folder_var.get() or PICTURES_FOLDER
            os.makedirs(folder, exist_ok=True)
            filter_name = self.filter_var.get().lower().replace(" ", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"polaroid_{mode.lower()}_{filter_name}_{timestamp}.jpg"
            full_path = os.path.join(folder, filename)
            canvas.convert("RGB").save(full_path, "JPEG", quality=95)
            print(f"Saved: {full_path}")
            self.last_saved_path = full_path
        except Exception as e:
            print(f"[Save Error] {e}")

    # ------------------------------------------------------------
    # PRINTING
    # ------------------------------------------------------------
    def _on_print(self):
        if self.result_image is None:
            return
        try:
            paper = self.paper_size_var.get()
            dims = {
                "2.5x3.5": (2.5, 3.5), "4x6": (4, 6),
                "5x7": (5, 7), "8x10": (8, 10),
            }[paper]
            dpi = 300
            target_w = int(dims[0] * dpi)
            target_h = int(dims[1] * dpi)

            img = self.result_image.copy()
            img_ratio = img.width / img.height
            paper_ratio = target_w / target_h
            if (img_ratio > 1) != (paper_ratio > 1):
                img = img.rotate(90, expand=True)

            fitted = fit_image(img, target_w, target_h)
            temp_path = os.path.join(self.output_folder_var.get() or PICTURES_FOLDER,
                                      "_print_temp.jpg")
            fitted.save(temp_path, "JPEG", quality=95)

            os.startfile(temp_path, "print")
        except Exception as e:
            print(f"[Print Error] {e}")

    def on_close(self):
        if self.cap is not None:
            with self.cap_lock:
                self.cap.release()
        self.root.destroy()


# ======================================================================
# ENTRY POINT
# ======================================================================

def main():
    root = tk.Tk()
    app = PolaroidApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()

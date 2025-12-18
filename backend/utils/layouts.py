# backend/utils/layouts.py
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import Union
import os

# =========================================================
# GENERIC HELPERS
# =========================================================

def load_font(font_path: str, size: int) -> Union[ImageFont.FreeTypeFont, ImageFont.ImageFont]:
    """Safely load a TTF font with fallback."""
    try:
        return ImageFont.truetype(font_path, size)
    except OSError:
        return ImageFont.load_default()


def auto_font_size(
    text: str,
    max_width: int,
    max_height: int,
    font_path: str = "arial.ttf",
    start_size: int = 80,
    min_size: int = 12,
) -> Union[ImageFont.FreeTypeFont, ImageFont.ImageFont]:
    """Automatically reduce font size until text fits the given box."""
    for size in range(start_size, min_size - 1, -2):
        font = load_font(font_path, size)
        bbox = font.getbbox(text)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if w <= max_width and h <= max_height:
            return font
    return load_font(font_path, min_size)


def pick_best_text_color(bg_color: tuple[int, int, int]) -> tuple[int, int, int]:
    """Return black or white depending on background brightness."""
    r, g, b = bg_color
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    return (0, 0, 0) if brightness > 160 else (255, 255, 255)


def auto_margins(size: tuple[int, int], scale: float = 0.06) -> int:
    """Responsive padding based on canvas size."""
    return int(min(size) * scale)


def resize_to_fit(image: Image.Image, max_width: int, max_height: int) -> Image.Image:
    """Resize image while preserving aspect ratio."""
    ow, oh = image.size
    ratio = min(max_width / ow, max_height / oh)
    return image.resize((int(ow * ratio), int(oh * ratio)), resample=Image.Resampling.LANCZOS)


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: Union[ImageFont.FreeTypeFont, ImageFont.ImageFont],
    canvas_width: int,
    y: int,
    color: tuple[int, int, int],
) -> None:
    """Draw horizontally centered text at y."""
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((canvas_width - w) // 2, y), text, fill=color, font=font)



def pill(
    draw: ImageDraw.ImageDraw,
    x: float,
    y: float,
    w: float,
    h: float,
    fill: tuple[int, int, int],
    radius: float = 25,
) -> None:
    """Draw a rounded pill/rectangle."""
    draw.rounded_rectangle(
        (x, y, x + w, y + h),
        radius=radius,
        fill=fill,
    )

# =========================================================
# TEMPLATE 1 — CLEAN MINIMAL
# =========================================================

def template_clean_minimal(
    processed_img_path: str,
    out_path: str,
    tagline: str,
    offer: str,
    bg_color: tuple[int, int, int] = (255, 255, 255),
    size: tuple[int, int] = (1080, 1080),
) -> None:

    canvas = Image.new("RGBA", size, bg_color + (255,))
    draw = ImageDraw.Draw(canvas)
    pad = auto_margins(size)

    product = Image.open(processed_img_path).convert("RGBA")
    product = resize_to_fit(product, int(size[0] * 0.70), int(size[1] * 0.55))
    canvas.paste(product, ((size[0] - product.width) // 2, pad + 80), product)

    text_color = pick_best_text_color(bg_color)
    tagline_font = auto_font_size(tagline, size[0] - pad * 2, 160)
    offer_font = auto_font_size(offer, size[0] - pad * 2, 200)

    draw_centered_text(draw, tagline, tagline_font, size[0], pad, text_color)

    bbox = draw.textbbox((0, 0), offer, font=offer_font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    pill_pad = 25
    pw, ph = w + pill_pad * 2, h + pill_pad * 2
    ox = (size[0] - pw) // 2
    oy = size[1] - ph - pad

    pill(draw, ox, oy, pw, ph, (255, 60, 60), radius=40)
    draw.text((ox + pill_pad, oy + pill_pad), offer, fill=(255, 255, 255), font=offer_font)

    canvas.save(out_path)


# =========================================================
# TEMPLATE 2 — SPLIT MODERN
# =========================================================

def template_split_layout(
    processed_img_path: str,
    out_path: str,
    tagline: str,
    offer: str,
    brand_color: tuple[int, int, int] = (30, 144, 255),
    size: tuple[int, int] = (1080, 1080),
) -> None:

    canvas = Image.new("RGBA", size, (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    pad = auto_margins(size)

    right_w = int(size[0] * 0.40)
    draw.rectangle((size[0] - right_w, 0, size[0], size[1]), fill=brand_color)

    product = Image.open(processed_img_path).convert("RGBA")
    product = resize_to_fit(product, int(size[0] * 0.55), int(size[1] * 0.75))
    canvas.paste(product, (pad, (size[1] - product.height) // 2), product)

    text_color = pick_best_text_color(brand_color)
    tagline_font = auto_font_size(tagline, right_w - pad * 2, 200)
    offer_font = auto_font_size(offer, right_w - pad * 2, 200)

    tx = size[0] - right_w + pad
    ty = int(pad * 1.5)

    draw.text((tx, ty), tagline, fill=text_color, font=tagline_font)
    draw.text((tx, ty + 160), offer, fill=text_color, font=offer_font)

    canvas.save(out_path)


# =========================================================
# TEMPLATE 3 — HERO BADGE
# =========================================================

def template_hero_badge(
    processed_img_path: str,
    out_path: str,
    tagline: str,
    offer: str,
    badge_color: tuple[int, int, int] = (255, 69, 0),
    size: tuple[int, int] = (1080, 1080),
) -> None:

    canvas = Image.new("RGBA", size, (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    pad = auto_margins(size)

    product = Image.open(processed_img_path).convert("RGBA")
    product = resize_to_fit(product, int(size[0] * 0.58), int(size[1] * 0.75))
    canvas.paste(product, (pad, (size[1] - product.height) // 2), product)

    tagline_font = auto_font_size(tagline, int(size[0] * 0.32), 200)
    draw.text((pad + product.width + pad, pad), tagline, fill=(0, 0, 0), font=tagline_font)

    badge = int(min(size) * 0.22)
    bx = pad + product.width + pad
    by = pad + 260

    draw.ellipse((bx, by, bx + badge, by + badge), fill=badge_color)

    offer_font = auto_font_size(offer, int(badge * 0.8), int(badge * 0.8))
    offer_color = pick_best_text_color(badge_color)

    bbox = draw.textbbox((0, 0), offer, font=offer_font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    draw.text((bx + (badge - w) // 2, by + (badge - h) // 2), offer, fill=offer_color, font=offer_font)

    canvas.save(out_path)


# =========================================================
# TEMPLATE 4 — GRADIENT GLOW (Premium)
# =========================================================

def template_gradient_glow(
    processed_img_path: str,
    out_path: str,
    tagline: str,
    offer: str,
    brand_color: tuple[int, int, int] = (255, 100, 80),
    size: tuple[int, int] = (1080, 1080),
) -> None:

    canvas = Image.new("RGBA", size, (0, 0, 0, 255))
    pad = auto_margins(size)

    grad = Image.new("RGBA", size)
    gd = ImageDraw.Draw(grad)
    for y in range(size[1]):
        col = (
            brand_color[0] + (20 - brand_color[0]) * y // size[1],
            brand_color[1] + (20 - brand_color[1]) * y // size[1],
            brand_color[2] + (20 - brand_color[2]) * y // size[1],
            255,
        )
        gd.line([(0, y), (size[0], y)], fill=col)

    canvas = Image.alpha_composite(canvas, grad)
    draw = ImageDraw.Draw(canvas)

    product = Image.open(processed_img_path).convert("RGBA")
    product = resize_to_fit(product, int(size[0] * 0.70), int(size[1] * 0.65))
    canvas.paste(product, ((size[0] - product.width) // 2, pad + 100), product)

    tagline_font = auto_font_size(tagline, size[0] - pad * 2, 170)
    offer_font = auto_font_size(offer, size[0] - pad * 2, 200)

    draw_centered_text(draw, tagline, tagline_font, size[0], pad, (255, 255, 255))

    bbox = draw.textbbox((0, 0), offer, font=offer_font)
    w, h = bbox[2] - bbox[0] + 30, bbox[3] - bbox[1] + 30
    ox = (size[0] - w) // 2
    oy = size[1] - h - pad * 2

    glow = Image.new("RGBA", size)
    gd2 = ImageDraw.Draw(glow)
    gd2.ellipse((ox - 20, oy - 20, ox + w + 20, oy + h + 20), fill=(255, 255, 255, 80))
    glow = glow.filter(ImageFilter.GaussianBlur(25))

    canvas = Image.alpha_composite(canvas, glow)
    draw = ImageDraw.Draw(canvas)
    draw.text((ox + w // 8, oy), offer, font=offer_font, fill=(0, 0, 0))

    canvas.save(out_path)


# =========================================================
# TEMPLATE 5 — NEON BADGE (Premium)
# =========================================================

def template_neon_badge(
    processed_img_path: str,
    out_path: str,
    tagline: str,
    offer: str,
    neon_color: tuple[int, int, int] = (0, 255, 180),
    size: tuple[int, int] = (1080, 1080),
) -> None:

    canvas = Image.new("RGBA", size, (20, 20, 20, 255))
    draw = ImageDraw.Draw(canvas)
    pad = auto_margins(size)

    product = Image.open(processed_img_path).convert("RGBA")
    product = resize_to_fit(product, int(size[0] * 0.70), int(size[1] * 0.70))
    canvas.paste(product, ((size[0] - product.width) // 2, pad + 120), product)

    tagline_font = auto_font_size(tagline, size[0] - pad * 2, 160)
    draw_centered_text(draw, tagline, tagline_font, size[0], pad, (255, 255, 255))

    badge = int(min(size) * 0.28)
    bx = size[0] - badge - pad
    by = size[1] - badge - pad * 2

    glow = Image.new("RGBA", size)
    gd = ImageDraw.Draw(glow)
    gd.ellipse((bx, by, bx + badge, by + badge), fill=neon_color + (60,))
    glow = glow.filter(ImageFilter.GaussianBlur(25))

    canvas = Image.alpha_composite(canvas, glow)
    draw = ImageDraw.Draw(canvas)
    draw.ellipse((bx, by, bx + badge, by + badge), outline=neon_color, width=8)

    offer_font = auto_font_size(offer, int(badge * 0.8), int(badge * 0.8))
    bbox = draw.textbbox((0, 0), offer, font=offer_font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    draw.text((bx + (badge - w) // 2, by + (badge - h) // 2), offer, fill=(0, 0, 0), font=offer_font)

    canvas.save(out_path)


# =========================================================
# TEMPLATE 6 — DIAGONAL SPLIT (Premium)
# =========================================================

def template_diagonal_split(
    processed_img_path: str,
    out_path: str,
    tagline: str,
    offer: str,
    brand_color: tuple[int, int, int] = (40, 40, 40),
    size: tuple[int, int] = (1080, 1080),
) -> None:

    canvas = Image.new("RGBA", size, (255, 255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    pad = auto_margins(size)

    diag = Image.new("RGBA", size)
    d = ImageDraw.Draw(diag)
    d.polygon(
        [
            (0, 0),
            (size[0], 0),
            (size[0], int(size[1] * 0.55)),
            (0, int(size[1] * 0.30)),
        ],
        fill=brand_color,
    )

    canvas = Image.alpha_composite(canvas, diag)

    product = Image.open(processed_img_path).convert("RGBA")
    product = resize_to_fit(product, int(size[0] * 0.55), int(size[1] * 0.70))
    canvas.paste(product, (pad, size[1] - product.height - pad), product)

    text_color = pick_best_text_color(brand_color)
    tagline_font = auto_font_size(tagline, size[0] - pad * 3, 200)
    offer_font = auto_font_size(offer, size[0] - pad * 3, 160)

    draw.text((pad * 2, int(pad * 1.6)), tagline, fill=text_color, font=tagline_font)
    draw.text((pad * 2, int(pad * 1.6 + 180)), offer, fill=text_color, font=offer_font)

    canvas.save(out_path)

from typing import List, Tuple
import os

RGB = Tuple[int, int, int]

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROCESSED_FOLDER = os.path.join(ROOT, "processed")
CREATIVES_FOLDER = os.path.join(ROOT, "creatives")

os.makedirs(CREATIVES_FOLDER, exist_ok=True)

from .layouts import (
    template_clean_minimal,
    template_split_layout,
    template_hero_badge,
    template_gradient_glow,
    template_neon_badge,
    template_diagonal_split,
)

SIZES = {
    "square": (1080, 1080),
    "portrait": (1080, 1350),
    "landscape": (1920, 1080),
}


def normalize_rgb(color) -> RGB:
    if isinstance(color, str):
        color = color.lstrip("#")
        return (
            int(color[0:2], 16),
            int(color[2:4], 16),
            int(color[4:6], 16),
        )
    return tuple(color[:3])


def generate_all_creatives(
    processed_filename: str,
    tagline: str,
    offer: str,
    colors: List[str],
):
    in_path = os.path.join(PROCESSED_FOLDER, processed_filename)

    brand_color: RGB = normalize_rgb(colors[0]) if colors else (255, 0, 0)
    results = []

    for size_name, size in SIZES.items():
        clean = f"{size_name}_clean.png"
        split = f"{size_name}_split.png"
        hero = f"{size_name}_hero.png"
        gradient = f"{size_name}_gradient.png"
        neon = f"{size_name}_neon.png"
        diagonal = f"{size_name}_diagonal.png"

        template_clean_minimal(in_path, os.path.join(CREATIVES_FOLDER, clean), tagline, offer, brand_color, size)
        template_split_layout(in_path, os.path.join(CREATIVES_FOLDER, split), tagline, offer, brand_color, size)
        template_hero_badge(in_path, os.path.join(CREATIVES_FOLDER, hero), tagline, offer, brand_color, size)
        template_gradient_glow(in_path, os.path.join(CREATIVES_FOLDER, gradient), tagline, offer, brand_color, size)
        template_neon_badge(in_path, os.path.join(CREATIVES_FOLDER, neon), tagline, offer, brand_color, size)
        template_diagonal_split(in_path, os.path.join(CREATIVES_FOLDER, diagonal), tagline, offer, brand_color, size)

        results.append({
            "size": size_name,
            "clean_template": clean,
            "split_template": split,
            "hero_template": hero,
            "gradient_template": gradient,
            "neon_template": neon,
            "diagonal_template": diagonal,
        })

    return results

from colorthief import ColorThief
from colorsys import rgb_to_hls, hls_to_rgb
from typing import List, Tuple

RGB = Tuple[int, int, int]


def extract_palette(path: str, n: int = 5) -> List[RGB]:
    ct = ColorThief(path)
    palette = ct.get_palette(color_count=n)
    return [tuple(c) for c in palette]


def to_hex(rgb: RGB) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def complementary(rgb: RGB) -> RGB:
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = rgb_to_hls(r, g, b)
    h = (h + 0.5) % 1.0
    r2, g2, b2 = hls_to_rgb(h, l, s)
    return int(r2 * 255), int(g2 * 255), int(b2 * 255)

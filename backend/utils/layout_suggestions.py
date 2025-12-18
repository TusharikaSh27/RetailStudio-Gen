from typing import Sequence, Dict, Tuple, Union

RGB = Tuple[int, int, int]
Color = Union[str, RGB]


def _normalize_rgb(color: Color) -> RGB:
    if isinstance(color, str):
        hex_color = color.lstrip("#")
        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16),
        )

    if isinstance(color, tuple) and len(color) == 3:
        return color

    return (128, 128, 128)


def _brightness(color: Color) -> float:
    r, g, b = _normalize_rgb(color)
    return 0.299 * r + 0.587 * g + 0.114 * b


def suggest_layout(
    aspect_ratio: float,
    colors: Sequence[Color],
) -> Dict[str, list[str]]:

    suggestions = {
        "recommended_layouts": [],
        "text_guidelines": [],
        "color_guidelines": [],
        "alignment_guidelines": [],
        "warnings": [],
    }

    if aspect_ratio > 1.3:
        suggestions["recommended_layouts"].append("Hero Right Layout")
    elif aspect_ratio < 0.8:
        suggestions["recommended_layouts"].append("Vertical Layout")
    else:
        suggestions["recommended_layouts"].append("Centered Layout")

    if colors:
        if _brightness(colors[0]) < 90:
            suggestions["color_guidelines"].append("Use light text")
        else:
            suggestions["color_guidelines"].append("Use dark text")

    suggestions["text_guidelines"].append("Keep headline under 14 words")
    suggestions["alignment_guidelines"].append("Use rule of thirds")

    return suggestions

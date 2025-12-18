from PIL import Image
import numpy as np

def simple_validator(image_path, expected_regions):
    """
    Upgraded non-AI validator:
    - Checks color correctness
    - Checks contrast
    - Checks brightness
    """

    try:
        img = Image.open(image_path).convert("RGB")
        arr = np.array(img)

        score = 0
        max_score = len(expected_regions) * 3  # each region has 3 checks

        for region in expected_regions:
            x, y, w, h = region["bbox"]
            target_color = np.array(region["color"])

            box = arr[y:y+h, x:x+w]

            # 1️⃣ COLOR SIMILARITY
            avg_color = np.mean(box, axis=(0, 1))
            if np.linalg.norm(avg_color - target_color) < 80:
                score += 1

            # 2️⃣ CONTRAST
            if box.std() > 25:
                score += 1

            # 3️⃣ BRIGHTNESS
            brightness = np.mean(box)
            if 60 < brightness < 230:
                score += 1

        return round((score / max_score) * 100, 2)

    except Exception as e:
        print("Validator error:", e)
        return 0
 
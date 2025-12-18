from rembg import remove
from PIL import Image
import io
import os


def remove_background(upload_path: str, output_path: str) -> None:
    with Image.open(upload_path).convert("RGBA") as img:
        result = remove(img)

        if isinstance(result, bytes):
            result = Image.open(io.BytesIO(result)).convert("RGBA")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        result.save(output_path, format="PNG")

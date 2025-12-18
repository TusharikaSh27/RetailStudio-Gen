import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from PIL import Image

from utils.background import remove_background
from utils.colors import extract_palette
from utils.text_gen import generate_creative_text
from utils.templates_engine import generate_all_creatives
from utils.layout_suggestions import suggest_layout

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed")
CREATIVES_FOLDER = os.path.join(BASE_DIR, "creatives")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(CREATIVES_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Backend running"


@app.route("/processed/<path:filename>")
def serve_processed(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)


@app.route("/creatives/<path:filename>")
def serve_creatives(filename):
    return send_from_directory(CREATIVES_FOLDER, filename)


@app.route("/generate-creatives", methods=["POST"])
def generate_creatives():
    try:
        image = request.files.get("image")
        if not image or not image.filename:
            return jsonify({"error": "image missing"}), 400

        filename = secure_filename(image.filename)
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(upload_path)

        with Image.open(upload_path) as img:
            w, h = img.size
            aspect_ratio = w / h if h else 1.0

        processed_filename = f"no_bg_{os.path.splitext(filename)[0]}.png"
        processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)

        remove_background(upload_path, processed_path)

        palette = extract_palette(processed_path)
        colors_hex = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in palette]

        layout = suggest_layout(aspect_ratio, colors_hex)

        text = generate_creative_text(
            product="Product",
            category="General",
            colors=colors_hex,
        )

        creatives = generate_all_creatives(
            processed_filename,
            text.get("tagline", "Amazing Deal"),
            text.get("offer_text", "Limited Offer"),
            colors_hex,
        )

        base = request.host_url.rstrip("/")

        return jsonify({
            "success": True,
            "processed_image_url": f"{base}/processed/{processed_filename}",
            "colors": colors_hex,
            "layout_suggestions": layout,
            "creatives": creatives,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)

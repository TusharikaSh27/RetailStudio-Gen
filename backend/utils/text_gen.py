import json
from groq import Groq

client = Groq(api_key="")


def generate_creative_text(product, category, colors):
    prompt = f"""
    You are a creative retail ad copy generator.

    Generate short, catchy, high-conversion marketing text.

    Input:
    - Product: {product}
    - Category: {category}
    - Brand Colors: {colors}

    OUTPUT STRICTLY IN THIS JSON FORMAT:

    {{
        "tagline": "...",
        "short_caption": "...",
        "offer_text": "...",
        "seo_keywords": ["...", "...", "..."]
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()

    # ---- Safe JSON parsing ----
    try:
        result = json.loads(raw)
    except Exception:
        # AI may prepend text like "Sure! Here is JSON:"
        try:
            json_start = raw.find("{")
            json_end = raw.rfind("}") + 1
            cleaned = raw[json_start:json_end]
            result = json.loads(cleaned)
        except Exception:
            # Final fallback
            result = {
                "tagline": "Amazing Offer Just For You!",
                "short_caption": "Upgrade your lifestyle today.",
                "offer_text": "Limited-time deal. Hurry up!",
                "seo_keywords": []
            }

    # ------------- RETURN FORMAT FIXED -------------
    return result

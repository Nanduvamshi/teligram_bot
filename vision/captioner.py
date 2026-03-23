import base64
import ollama
from config import OLLAMA_VISION_MODEL


def describe_image(image_bytes: bytes) -> dict:
    b64_image = base64.b64encode(image_bytes).decode("utf-8")

    response = ollama.chat(
        model=OLLAMA_VISION_MODEL,
        messages=[{
            "role": "user",
            "content": (
                "Describe this image in one concise sentence. "
                "Then on a new line, list exactly 3 keyword tags separated by commas. "
                "Format:\nCaption: <your caption>\nTags: <tag1>, <tag2>, <tag3>"
            ),
            "images": [b64_image],
        }],
    )

    text = response["message"]["content"]
    return _parse_response(text)


def _parse_response(text: str) -> dict:
    caption = text.strip()
    tags = []

    lines = text.strip().split("\n")
    for line in lines:
        line_lower = line.lower().strip()
        if line_lower.startswith("caption:"):
            caption = line.split(":", 1)[1].strip()
        elif line_lower.startswith("tags:") or line_lower.startswith("tag:"):
            tag_str = line.split(":", 1)[1].strip()
            tags = [t.strip() for t in tag_str.split(",") if t.strip()]

    if not tags:
        words = caption.split()
        tags = [w.strip(".,!") for w in words[:3]]

    return {"caption": caption, "tags": tags[:3]}

import json
import os

from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

SYSTEM_PROMPT = """
You are an AI road infrastructure inspector.

Analyze the uploaded road image.

Return ONLY valid JSON.

Schema:

{
    "incident_type":"",
    "severity":"",
    "confidence":0,
    "summary":""
}

Incident types:

- Pothole
- Waterlogging
- Accident
- Signal Failure
- Blocked Road
- Construction
- Normal Road

Severity:

Low

Medium

High

Critical

Confidence should be between 0 and 100.

Do not return markdown.

Do not explain anything."""

def analyze_image(image_path : str):
    image = image.open(image_path)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        content=[
            SYSTEM_PROMPT,
            image
        ]
    )

    try:
        result = json.loads(response.text)
    except Exception:
        result={
            "incident_type": "Unknown",
            "Severity": "Unknown",
            "confidence":0,
            "summary": response.text,
            "embedding": "..."
        }

    return result

if __name__ == "__main__":
    result = analyze_image("static/uploads/sample.jpg")
    print(result)
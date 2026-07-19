import os
import json
import base64
from groq import Groq

# Keeps the exact client instantiation pattern
client = Groq(api_key="GROQ_API_KEY")

def analyze_image(image_path: str) -> dict:
    """
    Analyzes a road infrastructure image using Groq, maintaining the exact
    original structure and exception pattern of the pipeline.
    """
    try:
        # Keeps image processing clean and native
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        
        # Exact conversion of the content generation pattern
        response = client.chat.completions.create(
            model="qwen/qwen3.6-27b",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Analyze this road infrastructure damage image. "
                                "Provide your answer strictly as a JSON object with these exact keys:\n"
                                "{\n"
                                '  "incident_type": "Pothole, Waterlogging, Faded Markings, Streetlight Failure, or Debris",\n'
                                '  "severity": "Low, Medium, High, or Critical",\n'
                                '  "confidence": 0.95,\n'
                                '  "summary": "A clear, concise, 1-sentence description of the road issue."\n'
                                "}\n"
                                "Do not include any extra text or conversational markdown wrappers."
                            )
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        # Exact response dictionary translation pattern
        result_text = response.choices[0].message.content
        return json.loads(result_text)
        
    except Exception as e:
        # If the pipeline crashes, it raises the exact transparent error you requested
        raise e
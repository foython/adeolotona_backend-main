from PIL import Image
from io import BytesIO
import base64
import google.generativeai as genai
import json

def image_to_base64(img):
    """Converts PIL Image object to base64-encoded string"""
    buffered = BytesIO()
    img.save(buffered, format="JPEG")  # Save image to buffer as JPEG
    return base64.b64encode(buffered.getvalue()).decode()  # Convert to base64


def run_analyze_hair(uploaded_images):
    """
    Analyzes hair using the Gemini model and returns the results as JSON.
    uploaded_images: dict containing PIL Image objects
    """
    # Configure the Gemini model
    genai.configure(api_key="AIzaSyCFfTSOhpnzn-b01MEGY_KaxWy8UKt7SZI")
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

    # Prepare the images in Base64 format
    image_parts = []
    for key in ['front', 'back', 'up_front']:
        if key in uploaded_images:
            base64_image = image_to_base64(uploaded_images[key])
            image_parts.append({
                "mime_type": "image/jpeg",
                "data": base64_image
            })


    prompt = f"""
    You are an AI specializing in hair analysis. Given the images provided (as Base64), provide a detailed hair analysis in JSON format with the following structure under "analysis_report":

    {{
      "analysis_report": {{
        "hair_type": {{
          "classification": "Hair type classification (e.g., 2A-2B)",
          "description": "Description of the hair type (e.g., Fine to medium texture, slight wave to loose curls, prone to frizz)"
        }},
        "characteristics": {{
          "length_estimate": "Estimated length of the hair (short, medium, long)",
          "scalp_visibility": "Visibility of the scalp, e.g., thinning or healthy",
          "protective_style": "Whether the hair is in a protective style (or 'Not applicable')"
        }},
        "health_score": "Health score out of 100 (e.g., 45)",
        "conditions": {{
          "dryness": {{
            "level": "Level of dryness (e.g., None, Mild, Possible)",
            "insight": "Short insight on why this level is chosen"
          }},
          "frizz": {{
            "level": "Level of frizz (e.g., Low, Potentially Low)",
            "insight": "Short insight on frizz condition"
          }},
          "split_ends": {{
            "level": "Level of split ends (e.g., Not Discernible, Mild)",
            "insight": "Insight regarding the presence of split ends"
          }},
          "shrinkage": {{
            "level": "Level of shrinkage (e.g., Low, Moderate)",
            "insight": "Insight into shrinkage based on hair type"
          }},
          "breakage": {{
            "level": "Level of breakage (e.g., None, Possible)",
            "insight": "Insight on possible breakage"
          }},
          "thinning": {{
            "level": "Level of thinning (e.g., Mild, Moderate, Severe)",
            "insight": "Insight on hair thinning, if present, and potential causes"
          }}
        }}
      }},
      "tips": [
        "Tip 1: Personalized hair care tip for this user",
        "Tip 2: Another hair care tip",
        "Tip 3: More advice for this user"
      ],
      "routine": {{
        "daily_routine": [
          "Step 1: Description of daily step",
          "Step 2: Description of another daily step"
        ],
        "monthly_routine": [
          "Step 1: Description of monthly step",
          "Step 2: Description of another monthly step"
        ],
        "washday": [
          {{
            "step_name": "Step Name",
            "step_description": "Step description"
          }},
          {{
            "step_name": "Another Step",
            "step_description": "Description of this step"
          }}
        ]
      }}
    }}

    Use the images to infer these conditions. If anything is unclear or cannot be fully assessed, provide your best guess, but do not leave any field empty. Never say 'not detected', 'unclear', 'not visible', etc.

    User Data:
    {json.dumps(uploaded_images, indent=2)}
    """

    # Combine the prompt and images into the content for the API call
    content = [prompt] + image_parts

    # Get the response from Gemini
    response = model.generate_content(content)
    response_text = response.text

    # Extract JSON from the response
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.find("```", json_start)
        json_text = response_text[json_start:json_end].strip()
    else:
        start_idx = response_text.find("{")
        end_idx = response_text.rfind("}") + 1
        json_text = response_text[start_idx:end_idx]

    # Parse and return the result as a JSON object
    result = json.loads(json_text)
    return result
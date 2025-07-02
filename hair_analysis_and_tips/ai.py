def call_ai(uploaded_images, user_data):
    data = {

        "analysis_report": "Your hair is dry and needs moisturizing.",

        "tips": "Use a deep conditioner once a week.",

        "routine": {

            "daily_routine": "Moisturize every morning.",

            "monthly_routine": "Trim split ends and clarify scalp.",

            "washday": [

                {

                    "step_name": "Shampoo",

                    "step_description": "Use sulfate-free shampoo."

                },

                {

                    "step_name": "Condition",

                    "step_description": "Leave-in for 5 minutes."

                }

            ]

        }

    }

    return data

 
import google.generativeai as genai
import json
from PIL import Image
import base64
from io import BytesIO

def image_to_base64(img):
    """Converts PIL Image object to base64-encoded string"""
    buffered = BytesIO()
    img.save(buffered, format="JPEG")  # Save image to buffer as JPEG
    return base64.b64encode(buffered.getvalue()).decode()  # Convert to base64
 
 
def run_analyze_hair(uploaded_images, user_data=None):
    """
    Analyze hair from 3 uploaded images and user_data.
    uploaded_images: dict with keys 'front', 'back', 'up_front' or 'curl_pattern' and image bytes as values
    user_data: dict of user-provided hair info
    Returns: Dict with keys: analysis_report (markdown string), tips (list), routine (dict)
    """
    #Gemini
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
    You are an expert AI in hair care and analysis.
    
    You will receive three hair images (Base64, front/back/curl or up_front) and user_data (JSON).
    Return your answer strictly in the following JSON format:
    
    
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
    
    
    Use the images to infer hair type, length, health, and condition as much as possible. Use the user_data for any additional info or to help make assumptions if images are ambiguous.
    Your answer must strictly follow the JSON format above.
    Do not ever output a string for 'tips', only a JSON list.
    Never return more than one answer—just the JSON object, nothing else.
    
    User Data:
    {json.dumps(user_data, indent=2)}
    """
 
 
    content = [prompt] + image_parts
 
    response = model.generate_content(content)
    response_text = response.text
 
    # Extract JSON
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.find("```", json_start)
        json_text = response_text[json_start:json_end].strip()
    else:
        start_idx = response_text.find("{")
        end_idx = response_text.rfind("}") + 1
        json_text = response_text[start_idx:end_idx]
 
    result = json.loads(json_text)
    return result
 
 
# # Example usage:
# uploaded_images = {
#     'front': open('front.jpg', 'rb').read(),
#     'back': open('back.jpg', 'rb').read(),
#     'curl_pattern': open('curl.jpg', 'rb').read()
# }
# user_data = { ... }
# result = analyze_hair_with_gemini(uploaded_images, user_data)
# print(result)
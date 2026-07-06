import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

# 1. Initialization & Authentication
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Explicitly pass the key to bypass the ADC token clash
client = genai.Client(api_key=api_key) 

# 2. Mock Semantic Cache (MLOps Cost-Saving Bypass)
def check_semantic_cache(user_text):
    mock_cache = ["street light broken on 5th", "pothole on main crossroad"]
    if any(phrase in user_text.lower() for phrase in mock_cache):
        return True
    return False

# 3. Core Inference Engine
def process_grievance(user_text, image_file=None, model_name: str = "gemini-2.5-flash"):
    # Semantic Cache Check
    if check_semantic_cache(user_text):
        return '{"category": "Cache Hit", "severity": "N/A", "summary": "Issue already reported. Ticket #4928 linked.", "assigned_department": "System"}'

    # System Prompting for JSON enforcement
    # 2. Inference Engine (Strict Geospatial Enforcement)
    system_instruction = (
        "You are an expert civic infrastructure routing agent for a smart city dashboard. "
        "Analyze the text and image (if provided). Output a valid JSON object with:\n"
        "- 'category': (e.g., Road Hazards, Sanitation, Utilities)\n"
        "- 'severity': (Low, Medium, High)\n"
        "- 'summary': 1-sentence summary.\n"
        "- 'assigned_department': The municipal department.\n"
        "- 'latitude': Extract exact latitude ONLY if a specific city, highly recognizable landmark, or exact street is mentioned. If the location is vague (e.g., 'local cafeteria', 'main road') or unidentifiable, you MUST output JSON null (not a string). Do not guess.\n"
        "- 'longitude': Extract exact longitude ONLY if a specific city, highly recognizable landmark, or exact street is mentioned. If vague, MUST output JSON null. Do not guess."
    )
    
    contents = [f"Citizen Report: {user_text}"]
    
    # Multimodal Integration
    if image_file is not None:
        img = Image.open(image_file)
        contents.append(img)
        
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
            )
        )
        return response.text
    except Exception as e:
        return f"{{\"error\": \"{str(e)}\"}}"
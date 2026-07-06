import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

# 1. Initialization & Authentication
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) 

# 2. Mock Semantic Cache
def check_semantic_cache(user_text):
    mock_cache = ["street light broken on 5th", "pothole on main crossroad"]
    if any(phrase in user_text.lower() for phrase in mock_cache):
        return True
    return False

# 3. Core Autonomous Agent Engine (Now Nationally Scalable)
def process_grievance(user_text, state, district, image_file=None, model_name: str = "gemini-2.5-flash"):
    if check_semantic_cache(user_text):
        return '{"category": "Cache Hit", "severity": "N/A", "summary": "Issue already reported.", "assigned_department": "System"}'

    # --- DYNAMIC NATIONAL PROMPT ---
    # The AI uses the state and district to infer local civic architecture automatically.
    system_instruction = (
        f"You are an advanced, autonomous civic infrastructure routing agent operating for {district}, {state}, India. "
        "Your task is to analyze raw, unstructured citizen reports and extract highly specific, localized administrative data.\n\n"
        "Output a strictly valid JSON object containing exactly these fields:\n"
        "- 'category': Use precise municipal domains (e.g., 'Electrical Infrastructure', 'Road Network & Civil Works', 'Solid Waste Management', 'Water Supply & Sewerage', 'Public Safety & Emergency').\n"
        "- 'severity': Classify the triage urgency (Low, Medium, High) based on immediate structural danger or public risk.\n"
        "- 'summary': Provide a crisp, 1-sentence administrative summary.\n"
        f"- 'assigned_department': Determine the precise local agency for {state} and {district}. Use your internal knowledge to name the correct state electricity board (e.g., APCPDCL for AP, BESCOM for Karnataka), water board, or local municipal corporation (e.g., {district} Municipal Corporation).\n"
        f"- 'location_query': Extract the named landmark or street. CRITICAL RULE: You MUST format this string specifically for a Map API by extracting the landmark and ALWAYS appending ', {district}, {state}, India' to the end (e.g., 'St. Josephs Degree College, {district}, {state}, India'). If the report is completely vague, output JSON null."
    )
    
    contents = [f"Citizen Report: {user_text}"]
    
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
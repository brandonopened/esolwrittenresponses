import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL = "gpt-4o"

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_response(text):
    prompt = f"""
    Analyze the following special education response text. For each category, find and extract EXACT quotes that demonstrate that concept. Include the student's name with each quote.

    Text to analyze: {text}

    Return a JSON object with exactly this structure:
    {{
        "predetermined_codes": {{
            "Academic Language Support": ["Student Name: 'exact quote'"],
            "Grammar Support": ["Student Name: 'exact quote'"],
            "Content Knowledge Support": ["Student Name: 'exact quote'"],
            "Collaboration with Teachers": ["Student Name: 'exact quote'"],
            "Student Engagement": ["Student Name: 'exact quote'"],
            "Assessment of Language Proficiency": ["Student Name: 'exact quote'"]
        }},
        "emergent_codes": {{
            "Perceptions of Language Acquisition": ["Student Name: 'exact quote'"],
            "Perceived Challenges": ["Student Name: 'exact quote'"],
            "Innovative Practices": ["Student Name: 'exact quote'"],
            "Perceptions of Error": ["Student Name: 'exact quote'"]
        }}
    }}

    Critical Instructions:
    1. ONLY use exact, word-for-word quotes from the text - NO paraphrasing or summarizing
    2. Each quote must be prefixed with the student's name
    3. Put quotes in 'single quotes' to clearly delineate them
    4. If multiple relevant quotes exist, include them as separate entries in the array
    5. If no relevant quote exists for a category, use ["No direct quote found"]
    6. Do not interpret or explain the quotes - just provide them exactly as written
    """

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert in analyzing special education responses. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        # Parse the JSON response
        import json
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        return {
            "predetermined_codes": {
                "error": f"Analysis failed: {str(e)}"
            },
            "emergent_codes": {
                "error": f"Analysis failed: {str(e)}"
            }
        }

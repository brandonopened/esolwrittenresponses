import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL = "gpt-4o"

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_response(text):
    prompt = f"""
    Analyze the following special education response text. For each category, find and extract EXACT quotes that demonstrate that concept.

    Text to analyze: {text}

    Return a JSON object with exactly this structure:
    {{
        "predetermined_codes": {{
            "Academic Language Support": ["Student Name: 'exact quote from text'"],
            "Grammar Support": ["Student Name: 'exact quote from text'"],
            "Content Knowledge Support": ["Student Name: 'exact quote from text'"],
            "Collaboration with Teachers": ["Student Name: 'exact quote from text'"],
            "Student Engagement": ["Student Name: 'exact quote from text'"],
            "Assessment of Language Proficiency": ["Student Name: 'exact quote from text'"]
        }},
        "emergent_codes": {{
            "Perceptions of Language Acquisition": ["Student Name: 'exact quote from text'"],
            "Perceived Challenges": ["Student Name: 'exact quote from text'"],
            "Innovative Practices": ["Student Name: 'exact quote from text'"],
            "Perceptions of Error": ["Student Name: 'exact quote from text'"]
        }}
    }}

    Critical Instructions:
    1. ONLY use exact, word-for-word quotes from the text - NO paraphrasing or summarizing
    2. Each quote MUST be formatted exactly as: "Student Name: 'exact quote'"
    3. The student's name must be extracted from the text and included before each quote
    4. Put the actual quote in 'single quotes' after the student name and colon
    5. If multiple relevant quotes exist for a category, include them as separate entries in the array
    6. If no relevant quote exists for a category, use ["No direct quote found"]
    7. Do not add any interpretation or explanation - only exact quotes
    8. Preserve all original punctuation and formatting within the quotes
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

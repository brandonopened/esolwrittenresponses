import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL = "gpt-4o"

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_response(text):
    prompt = f"""
    Extract relevant quotes from the following special education response text for each category.
    For each category, provide direct quotes from the text along with the student's name.
    Do not summarize - use exact quotes only.
    
    Text to analyze: {text}
    
    Return a JSON object with exactly this structure:
    {{
        "predetermined_codes": {{
            "Academic Language Support": "Student Name: <exact quote>",
            "Grammar Support": "Student Name: <exact quote>",
            "Content Knowledge Support": "Student Name: <exact quote>",
            "Collaboration with Teachers": "Student Name: <exact quote>",
            "Student Engagement": "Student Name: <exact quote>",
            "Assessment of Language Proficiency": "Student Name: <exact quote>"
        }},
        "emergent_codes": {{
            "Perceptions of Language Acquisition": "Student Name: <exact quote>",
            "Perceived Challenges": "Student Name: <exact quote>",
            "Innovative Practices": "Student Name: <exact quote>",
            "Perceptions of Error": "Student Name: <exact quote>"
        }}
    }}
    
    Instructions:
    1. Include the student's name before each quote
    2. Use exact quotes from the text, do not paraphrase or summarize
    3. If multiple relevant quotes exist, separate them with newlines
    4. If no relevant quote exists for a category, respond with "No direct quote found"
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

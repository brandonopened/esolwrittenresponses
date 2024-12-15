import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL = "gpt-4o"

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_response(text):
    prompt = f"""
    Analyze the following special education response text and identify relevant content for each category.
    Provide specific text snippets and explanations for each code.
    
    Text to analyze: {text}
    
    Return a JSON object with exactly this structure:
    {{
        "predetermined_codes": {{
            "Academic Language Support": "explanation here",
            "Grammar Support": "explanation here",
            "Content Knowledge Support": "explanation here",
            "Collaboration with Teachers": "explanation here",
            "Student Engagement": "explanation here",
            "Assessment of Language Proficiency": "explanation here"
        }},
        "emergent_codes": {{
            "Perceptions of Language Acquisition": "explanation here",
            "Perceived Challenges": "explanation here",
            "Innovative Practices": "explanation here",
            "Perceptions of Error": "explanation here"
        }}
    }}
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

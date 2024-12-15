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
    
    Please analyze the text for the following categories and provide results in JSON format:
    
    Predetermined Codes:
    - Academic Language Support
    - Grammar Support
    - Content Knowledge Support
    - Collaboration with Teachers
    - Student Engagement
    - Assessment of Language Proficiency
    
    Emergent Codes:
    - Perceptions of Language Acquisition
    - Perceived Challenges
    - Innovative Practices
    - Perceptions of Error
    
    Format the response as a JSON object with two main keys: 'predetermined_codes' and 'emergent_codes',
    each containing the relevant findings for their respective categories.
    """

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert in analyzing special education responses."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return {
            "predetermined_codes": {
                "error": f"Analysis failed: {str(e)}"
            },
            "emergent_codes": {
                "error": f"Analysis failed: {str(e)}"
            }
        }

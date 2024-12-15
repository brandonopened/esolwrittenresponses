import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL = "gpt-4o"

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_response(text, custom_categories=None):
    # Initialize custom categories if not provided
    custom_categories = custom_categories or []
    
    # Build the prompt in parts to avoid f-string issues
    base_prompt = "Analyze the following special education response text. For each category, find and extract EXACT quotes that demonstrate that concept. Include the student's name with each quote.\n\n"
    
    categories_text = "Additional Custom Categories: " + (', '.join(custom_categories) if custom_categories else 'None') + "\n\n"
    
    analysis_text = "Text to analyze: " + text + "\n\n"
    
    json_structure = '''Return a JSON object with this structure:
{
    "predetermined_codes": {
        "Academic Language Support": "Student Name: 'exact quote'",
        "Grammar Support": "Student Name: 'exact quote'",
        "Content Knowledge Support": "Student Name: 'exact quote'",
        "Collaboration with Teachers": "Student Name: 'exact quote'",
        "Student Engagement": "Student Name: 'exact quote'",
        "Assessment of Language Proficiency": "Student Name: 'exact quote'"
    },
    "emergent_codes": {
        "Perceptions of Language Acquisition": "Student Name: 'exact quote'",
        "Perceived Challenges": "Student Name: 'exact quote'",
        "Innovative Practices": "Student Name: 'exact quote'",
        "Perceptions of Error": "Student Name: 'exact quote'"
    },
    "custom_codes": {
'''

    # Add custom categories to JSON structure
    if custom_categories:
        custom_codes = ',\n'.join(f'        "{cat}": "Student Name: \'exact quote\'"' for cat in custom_categories)
        json_structure += custom_codes + '\n    }\n}'
    else:
        json_structure += '    }\n}'

    instructions = '''

Critical Instructions:
1. ONLY use exact, word-for-word quotes from the text - NO paraphrasing or summarizing
2. Each quote must be prefixed with the student's name
3. Put quotes in 'single quotes' to clearly delineate them
4. If multiple relevant quotes exist, separate them with semicolons
5. If no relevant quote exists for a category, use "No direct quote found"
6. Do not interpret or explain the quotes - just provide them exactly as written'''

    # Combine all parts of the prompt
    full_prompt = base_prompt + categories_text + analysis_text + json_structure + instructions

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert in analyzing special education responses. Always respond with valid JSON."},
                {"role": "user", "content": full_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        # Parse the JSON response
        import json
        result = json.loads(response.choices[0].message.content)
        
        # Ensure custom_codes exists in the result
        if 'custom_codes' not in result:
            result['custom_codes'] = {}
            
        return result
    except Exception as e:
        return {
            "predetermined_codes": {
                "error": f"Analysis failed: {str(e)}"
            },
            "emergent_codes": {
                "error": f"Analysis failed: {str(e)}"
            },
            "custom_codes": {} #Adding empty custom_codes in case of error.
        }

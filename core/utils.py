from google import genai
from django.conf import settings
import json


client = genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_quiz_questions(topic, num_questions, difficulty):
    prompt = f"""
    Generate {num_questions} MCQs on "{topic}" with difficulty {difficulty}.

    STRICT RULES:
    - Exactly 4 options per question
    - Only ONE correct answer
    - Return ONLY valid JSON (no markdown, no explanation outside JSON)

    Format:
    [
      {{
        "question": "text",
        "difficulty": "{difficulty}",
        "explanation": "short explanation",
        "options": [
          {{"text": "...", "is_correct": false}},
          {{"text": "...", "is_correct": true}},
          {{"text": "...", "is_correct": false}},
          {{"text": "...", "is_correct": false}}
        ]
      }}
    ]
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        
        content = response.text

        if not content:
            raise ValueError("Empty response from Gemini")

        content = content.strip()

        
        if content.startswith("```"):
            content = content.split("```")[1].strip()

        
        if content.startswith("json"):
            content = content[4:].strip()

        return json.loads(content)

    except json.JSONDecodeError:
        raise ValueError("Failed to parse JSON from Gemini response")

    except Exception as e:
        raise ValueError(f"Gemini API failed: {str(e)}")
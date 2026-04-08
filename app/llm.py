import os
from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PROMPT = """
You are a strict B2B sales intelligence system.

Analyze the company data and return ONLY VALID JSON.

Format:
{
  "company_overview": "",
  "core_service": "",
  "target_customer": "",
  "b2b_qualified": "Yes/No",
  "sales_questions": ["", "", ""]
}

Rules:
- No extra text
- Be precise
- If unsure, infer intelligently
"""

def analyze_with_llm(content):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": content[:5000]}
            ],
            temperature=0.2
        )

        text = response.choices[0].message.content

        return json.loads(text)

    except Exception as e:
        print("LLM Error:", e)

        return {
            "company_overview": "Unknown",
            "core_service": "Unknown",
            "target_customer": "Unknown",
            "b2b_qualified": "No",
            "sales_questions": [
                "What services do you offer?",
                "Who are your customers?",
                "Do you work with businesses?"
            ]
        }
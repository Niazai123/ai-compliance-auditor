from openai import OpenAI
import os
from dotenv import load_dotenv
from utils import industry_context_map, region_context_map

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_audit_prompt(text, industry='general', regions=['global'], content_type='text'):
    industry_context = industry_context_map.get(industry, 'general content')
    region_context = ", ".join([region_context_map.get(r, 'global') for r in regions])

    return f"""
You are a senior cultural compliance expert with expertise in {industry_context} for global markets.

ANALYZE this {content_type} content for cultural compliance targeting: {region_context}

Content to analyze: "{text}"

Respond ONLY in valid JSON format:
{{
  "overall_risk_score": 0-100,
  "compliance_status": "approved|needs_review|rejected",
  "confidence_level": 0.0-1.0,
  "issues": [...],
  "positive_aspects": [...],
  "alternative_suggestions": {{
    "conservative_version": "...",
    "inclusive_version": "...",
    "regional_adaptations": {{}}
  }},
  "industry_specific_notes": "...",
  "estimated_fix_time": "...",
  "priority_fixes": [...]
}}
"""

def get_audit_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are CulturalGuard AI, an expert in global cultural compliance auditing."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=3000,
       
    )
    return response.choices[0].message.content

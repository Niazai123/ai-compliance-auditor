from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from auditor import generate_audit_prompt, get_audit_response
import json

app = FastAPI()

class AuditRequest(BaseModel):
    text: str
    industry: str = 'general'
    target_regions: list[str] = ['global']
    content_type: str = 'text'

@app.get("/")
def welcome():
    return {"message": "Welcome to the Cultural Compliance Auditor API. Visit /docs to try it."}

@app.post("/audit")
async def audit_content(data: AuditRequest):
    if len(data.text) < 5 or len(data.text) > 50000:
        raise HTTPException(status_code=400, detail="Text must be between 5 and 50,000 characters.")

    try:
        prompt = generate_audit_prompt(data.text, data.industry, data.target_regions, data.content_type)
        raw = get_audit_response(prompt)

        # Print raw output for debugging
        print("=== RAW GPT RESPONSE ===")
        print(raw)

        # Clean response if wrapped in Markdown ```json``` block
        if raw.strip().startswith("```json"):
            raw = raw.strip().removeprefix("```json").removesuffix("```").strip()

        # Attempt to parse JSON
        response = json.loads(raw)

    except json.JSONDecodeError as jde:
        raise HTTPException(status_code=500, detail=f"AI Error: Invalid JSON format from model: {str(jde)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")

    return {
        "success": True,
        "audit_result": response
    }

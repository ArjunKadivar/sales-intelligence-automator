from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import asyncio

from app.scraper import scrape_website
from app.llm import analyze_with_llm
from app.lead_processor import normalize_lead

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_ui():
    return FileResponse("frontend/index.html")


class LeadRequest(BaseModel):
    leads: List[str]


async def process_lead(lead: str):
    print(f"\n Processing: {lead}")

    content = await scrape_website(lead)

    ai_generated = False

    # Fallback
    if not content:
        print(" Using AI fallback")
        content = lead
        ai_generated = True

    analysis = analyze_with_llm(content)

    if not analysis:
        return {
            "lead": lead,
            "error": "LLM failed"
        }

    return {
        "lead": lead,
        "analysis": analysis,
        "ai_generated": ai_generated
    }


@app.post("/analyze")
async def analyze(request: LeadRequest):
    tasks = [process_lead(lead) for lead in request.leads]
    results = await asyncio.gather(*tasks)

    return {"results": results}
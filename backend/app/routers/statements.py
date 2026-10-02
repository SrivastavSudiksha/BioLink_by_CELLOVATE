"""Problem statement generator."""
from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

import logging

from backend.app.services import ncbi
from backend.app.services.statements_data import PAPERS, match_statement

router = APIRouter()
log = logging.getLogger("biolink.statements")


class StatementRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=300)
    use_pubmed: bool = False


@router.get("/list")
def list_problems():
    return {
        "count": len(PAPERS),
        "problems": [
            {"id": p["id"], "problem": p["problem"], "statement": p["statement"]} for p in PAPERS
        ],
    }


@router.post("/generate")
async def generate(body: StatementRequest):
    p = match_statement(body.topic)
    out = {
        "research_problem": p["problem"],
        "problem_statement": p["statement"],
        "why_it_matters": p["why"],
        "current_gap": p["gap"],
        "proposed_ai_solution": p["solution"],
        "approach": p["approach"],
        "data_sources": p["data"],
        "expected_outcome": p["outcome"],
        "cite": p["cite"],
        "title": p["title"],
        "id": p["id"],
        "disclaimer": "Research/educational template — validate against primary literature.",
        "pubmed": [],
    }
    if body.use_pubmed:
        try:
            term = f"{body.topic} AND (diabetes OR cancer) AND (prediction OR model OR machine learning)"
            pmids = await ncbi.pubmed_search(term, retmax=3)
            out["pubmed"] = await ncbi.pubmed_summaries(pmids)
        except Exception:
            log.warning("PubMed lookup failed", exc_info=True)
            out["pubmed_error"] = "PubMed lookup unavailable"
    return out

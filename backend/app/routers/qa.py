import asyncio
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.config import get_settings
from backend.app.services import kb, ncbi

router = APIRouter()
log = logging.getLogger("biolink.qa")
DISCLAIMER = (
    "Research and educational use only. This is not medical advice, diagnosis, or treatment recommendation. "
    "Consult a qualified physician for personal health decisions."
)


class QARequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=500)
    use_pubmed: bool = True
    retmax: int = Field(5, ge=1, le=10)


class Citation(BaseModel):
    label: str
    url: str | None = None


class QAResponse(BaseModel):
    answer: str
    citations: list[Citation]
    source: str
    in_scope: bool
    disclaimer: str = DISCLAIMER


@router.post("/ask", response_model=QAResponse)
async def ask(body: QARequest):
    settings = get_settings()
    q = body.question.strip()
    if len(q) > settings.max_query_len:
        raise HTTPException(400, "Query too long")

    if not kb.in_scope(q):
        return QAResponse(
            answer=(
                "This assistant is limited to cancer- and diabetes-related research topics. "
                "Try questions about BRCA, TP53, MODY, T2D genetics, cross-dataset models, or biomarkers."
            ),
            citations=[],
            source="scope_filter",
            in_scope=False,
        )

    hit = kb.match_kb(q)
    citations: list[Citation] = []
    parts: list[str] = []
    source = "kb"

    if hit:
        parts.append(hit["answer"])
        for s in hit["sources"]:
            citations.append(Citation(label=s))

    if body.use_pubmed:
        try:
            term = f'({q}) AND (cancer OR diabetes OR neoplasm OR "type 2 diabetes")'
            pmids = await ncbi.pubmed_search(term, retmax=body.retmax)
            if pmids:
                papers, abstracts = await asyncio.gather(
                    ncbi.pubmed_summaries(pmids),
                    ncbi.pubmed_abstracts(pmids[:1]),
                )
                if papers:
                    source = "kb+pubmed" if hit else "pubmed"
                    lines = ["Related PubMed literature (titles):"]
                    for i, p in enumerate(papers, 1):
                        lines.append(f"[{i}] {p['title']} ({p.get('pubdate', '')}) — {p['url']}")
                        citations.append(
                            Citation(label=f"PMID:{p['pmid']} — {p['title'][:80]}", url=p["url"])
                        )
                    top = pmids[0]
                    if top in abstracts:
                        snippet = abstracts[top][:400].replace("\n", " ")
                        lines.append(f"\nAbstract snippet (PMID {top}): {snippet}…")
                    parts.append("\n".join(lines))
        except Exception:
            log.warning("PubMed lookup failed", exc_info=True)
            parts.append("(Live PubMed lookup is temporarily unavailable. Showing curated knowledge only.)")

    if not parts:
        return QAResponse(
            answer=(
                "No strong match in the curated knowledge base and no PubMed hits. "
                "Try: BRCA1, TP53, MODY, TCF7L2, cross-dataset diabetes, SHAP, GLP-1."
            ),
            citations=[],
            source="none",
            in_scope=True,
        )

    answer = "\n\n".join(parts) + f"\n\n{DISCLAIMER}"
    return QAResponse(answer=answer, citations=citations, source=source, in_scope=True)

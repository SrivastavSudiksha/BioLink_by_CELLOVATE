"""Grounded Q&A — curated KB + optional live PubMed. No diagnosis."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.config import get_settings
from backend.app.services import kb, ncbi

router = APIRouter()
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

    # 1) Curated KB
    hit = kb.match_kb(q)
    citations: list[Citation] = []
    parts: list[str] = []
    source = "kb"

    if hit:
        parts.append(hit["answer"])
        for s in hit["sources"]:
            citations.append(Citation(label=s))

    # 2) Live PubMed (optional)
    papers = []
    if body.use_pubmed:
        try:
            # Bias search toward cancer/diabetes
            term = f"({q}) AND (cancer OR diabetes OR neoplasm OR \"type 2 diabetes\")"
            pmids = await ncbi.pubmed_search(term, retmax=body.retmax)
            if pmids:
                papers = await ncbi.pubmed_summaries(pmids)
                abstracts = await ncbi.pubmed_abstracts(pmids[:3])
                if papers:
                    source = "kb+pubmed" if hit else "pubmed"
                    lines = ["Related PubMed literature (titles):"]
                    for i, p in enumerate(papers, 1):
                        lines.append(f"[{i}] {p['title']} ({p.get('pubdate', '')}) — {p['url']}")
                        citations.append(
                            Citation(label=f"PMID:{p['pmid']} — {p['title'][:80]}", url=p["url"])
                        )
                    # Short abstract snippet for top hit
                    top = pmids[0]
                    if top in abstracts:
                        snippet = abstracts[top][:400].replace("\n", " ")
                        lines.append(f"\nAbstract snippet (PMID {top}): {snippet}…")
                    parts.append("\n".join(lines))
        except Exception as e:
            parts.append(f"\n(PubMed lookup unavailable: {str(e)[:120]}. Showing curated knowledge only.)")

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

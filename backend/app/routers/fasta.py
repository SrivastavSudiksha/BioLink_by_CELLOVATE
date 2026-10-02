import logging

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field

from backend.app.config import get_settings
from backend.app.services import fasta_svc, ncbi

router = APIRouter()
log = logging.getLogger("biolink.fasta")


class FastaRequest(BaseModel):
    sequence: str = Field(..., min_length=1, max_length=get_settings().max_fasta_bytes)
    gene_lookup: str | None = Field(
        None, max_length=30, description="Optional gene symbol for NCBI Gene summary (e.g. TP53, BRCA1, GCK)"
    )


async def _analyze(text: str) -> dict:
    try:
        return await run_in_threadpool(fasta_svc.analyze_fasta, text)
    except ValueError as e:
        raise HTTPException(400, str(e)) from e


async def _gene(symbol: str | None):
    if not symbol or not symbol.strip():
        return None
    try:
        return await ncbi.gene_summary(symbol)
    except ValueError:
        return {"error": "Invalid gene symbol"}
    except Exception:
        log.warning("Gene lookup failed for %s", symbol[:30], exc_info=True)
        return {"error": "Gene lookup unavailable"}


@router.post("/analyze")
async def analyze(body: FastaRequest):
    result = await _analyze(body.sequence)
    return {**result, "gene": await _gene(body.gene_lookup)}


@router.post("/analyze-file")
async def analyze_file(file: UploadFile = File(...), gene_lookup: str | None = None):
    limit = get_settings().max_fasta_bytes
    raw = await file.read(limit + 1)
    if len(raw) > limit:
        raise HTTPException(413, "File too large")
    result = await _analyze(raw.decode("utf-8", errors="replace"))
    return {**result, "gene": await _gene(gene_lookup), "filename": file.filename}

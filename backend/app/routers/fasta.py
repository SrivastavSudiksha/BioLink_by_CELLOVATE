"""FASTA analysis endpoints."""
from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from backend.app.services import fasta_svc, ncbi

router = APIRouter()


class FastaRequest(BaseModel):
    sequence: str = Field(..., min_length=1)
    gene_lookup: str | None = Field(
        None, description="Optional gene symbol for NCBI Gene summary (e.g. TP53, BRCA1, GCK)"
    )


@router.post("/analyze")
async def analyze(body: FastaRequest):
    try:
        result = fasta_svc.analyze_fasta(body.sequence)
    except ValueError as e:
        raise HTTPException(400, str(e)) from e

    gene = None
    if body.gene_lookup:
        try:
            gene = await ncbi.gene_summary(body.gene_lookup.strip())
        except Exception as e:
            gene = {"error": str(e)[:200]}

    return {**result, "gene": gene}


@router.post("/analyze-file")
async def analyze_file(
    file: UploadFile = File(...),
    gene_lookup: str | None = None,
):
    raw = await file.read()
    try:
        text = raw.decode("utf-8", errors="replace")
    except Exception as e:
        raise HTTPException(400, f"Could not read file: {e}") from e
    try:
        result = fasta_svc.analyze_fasta(text)
    except ValueError as e:
        raise HTTPException(400, str(e)) from e
    gene = None
    if gene_lookup:
        try:
            gene = await ncbi.gene_summary(gene_lookup.strip())
        except Exception as e:
            gene = {"error": str(e)[:200]}
    return {**result, "gene": gene, "filename": file.filename}

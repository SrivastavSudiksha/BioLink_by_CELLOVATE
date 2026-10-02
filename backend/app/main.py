"""BioAI Assistant API — research/educational use only."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.config import get_settings
from backend.app.routers import qa, fasta, statements, code_studio

settings = get_settings()

app = FastAPI(
    title="BioAI Assistant",
    description=(
        "Explainable AI for cancer & diabetes **research**. "
        "Not a medical device. No diagnosis or treatment advice."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(qa.router, prefix="/api/qa", tags=["Grounded Q&A"])
app.include_router(fasta.router, prefix="/api/fasta", tags=["FASTA Analyzer"])
app.include_router(statements.router, prefix="/api/statements", tags=["Problem Statements"])
app.include_router(code_studio.router, prefix="/api/code", tags=["Code Studio"])


@app.get("/")
def root():
    return {
        "name": "BioAI Assistant",
        "status": "ok",
        "disclaimer": "Research and educational use only — not a medical device.",
        "docs": "/docs",
        "modules": ["/api/qa", "/api/fasta", "/api/statements", "/api/code"],
    }


@app.get("/api/health")
def health():
    return {"status": "healthy", "ncbi_email_set": bool(settings.ncbi_email)}


@app.exception_handler(Exception)
async def unhandled(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal error", "message": str(exc)[:200]},
    )

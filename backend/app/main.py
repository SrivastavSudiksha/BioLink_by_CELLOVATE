import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.app.config import get_settings
from backend.app.routers import code_studio, fasta, qa, statements
from backend.app.security import RateLimiter, apply_security_headers
from backend.app.services import ncbi

settings = get_settings()
VERSION = "1.1.0"

logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
log = logging.getLogger("biolink")
limiter = RateLimiter(settings.rate_limit_per_minute)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await ncbi.startup()
    yield
    await ncbi.shutdown()


app = FastAPI(
    title="BioLink",
    description=(
        "Explainable AI for cancer & diabetes **research**. "
        "Not a medical device. No diagnosis or treatment advice."
    ),
    version=VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.enable_docs else None,
    redoc_url=None,
    openapi_url="/openapi.json" if settings.enable_docs else None,
)

app.add_middleware(GZipMiddleware, minimum_size=1024)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
    max_age=600,
)


@app.middleware("http")
async def guard(request: Request, call_next):
    path = request.url.path
    rid = uuid.uuid4().hex[:12]
    is_api = path.startswith("/api/")

    if is_api and request.method != "OPTIONS":
        length = request.headers.get("content-length")
        if length and length.isdigit() and int(length) > settings.max_fasta_bytes + 4096:
            response = JSONResponse(status_code=413, content={"detail": "Payload too large"})
            apply_security_headers(request, response)
            return response
        if path != "/api/health" and settings.rate_limit_per_minute > 0:
            ip = request.client.host if request.client else "unknown"
            ok, retry = limiter.check(ip)
            if not ok:
                response = JSONResponse(
                    status_code=429,
                    content={"detail": "Too many requests"},
                    headers={"Retry-After": str(retry)},
                )
                apply_security_headers(request, response)
                return response

    start = time.perf_counter()
    response = await call_next(request)
    apply_security_headers(request, response)
    response.headers["X-Request-ID"] = rid
    if is_api:
        log.info(
            "%s %s %s %.0fms rid=%s",
            request.method,
            path,
            response.status_code,
            (time.perf_counter() - start) * 1000,
            rid,
        )
    return response


@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    log.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(qa.router, prefix="/api/qa", tags=["Grounded Q&A"])
app.include_router(fasta.router, prefix="/api/fasta", tags=["FASTA Analyzer"])
app.include_router(statements.router, prefix="/api/statements", tags=["Problem Statements"])
app.include_router(code_studio.router, prefix="/api/code", tags=["Code Studio"])


@app.get("/api/health", include_in_schema=False)
def health():
    return {"status": "healthy", "version": VERSION}


@app.get("/api", include_in_schema=False)
def api_root():
    return {
        "name": "BioLink",
        "version": VERSION,
        "disclaimer": "Research and educational use only — not a medical device.",
        "modules": ["/api/qa", "/api/fasta", "/api/statements", "/api/code"],
    }


frontend = settings.frontend_path
if settings.serve_frontend and frontend.is_dir():
    app.mount("/", StaticFiles(directory=frontend, html=True), name="frontend")

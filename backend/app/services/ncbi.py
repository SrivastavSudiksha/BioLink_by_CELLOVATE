import asyncio
import logging
import re
import xml.etree.ElementTree as ET
from typing import Any

import httpx

from backend.app.config import get_settings

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
log = logging.getLogger("biolink.ncbi")
SYMBOL_RE = re.compile(r"^[A-Za-z0-9._-]{1,30}$")
RETRY_STATUS = {429, 500, 502, 503, 504}

_client: httpx.AsyncClient | None = None
_lock = asyncio.Lock()
_next_slot = 0.0


class NCBIError(Exception):
    pass


async def startup() -> None:
    global _client
    s = get_settings()
    _client = httpx.AsyncClient(
        timeout=httpx.Timeout(s.ncbi_timeout),
        headers={"User-Agent": f"{s.ncbi_tool}/1.0"},
        limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
    )


async def shutdown() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


async def _throttle() -> None:
    global _next_slot
    gap = 0.11 if get_settings().ncbi_api_key else 0.35
    async with _lock:
        now = asyncio.get_running_loop().time()
        wait = max(0.0, _next_slot - now)
        _next_slot = max(now, _next_slot) + gap
    if wait:
        await asyncio.sleep(wait)


def _params(**extra: Any) -> dict[str, Any]:
    s = get_settings()
    p: dict[str, Any] = {"tool": s.ncbi_tool, "email": s.ncbi_email, "retmode": "json"}
    if s.ncbi_api_key:
        p["api_key"] = s.ncbi_api_key
    p.update({k: v for k, v in extra.items() if v is not None})
    return p


async def _get(endpoint: str, params: dict[str, Any]) -> httpx.Response:
    if _client is None:
        await startup()
    last: Exception | None = None
    for attempt in range(3):
        await _throttle()
        try:
            r = await _client.get(f"{BASE}/{endpoint}", params=params)
        except (httpx.TimeoutException, httpx.TransportError) as e:
            last = e
            await asyncio.sleep(0.5 * (attempt + 1))
            continue
        if r.status_code in RETRY_STATUS:
            last = NCBIError(f"HTTP {r.status_code}")
            await asyncio.sleep(0.8 * (attempt + 1))
            continue
        try:
            r.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise NCBIError(f"HTTP {r.status_code}") from e
        return r
    log.warning("NCBI request failed after retries: %s", last)
    raise NCBIError("NCBI unavailable") from last


async def pubmed_search(query: str, retmax: int = 5) -> list[str]:
    r = await _get(
        "esearch.fcgi",
        _params(db="pubmed", term=query, retmax=retmax, sort="relevance"),
    )
    return r.json().get("esearchresult", {}).get("idlist", []) or []


async def pubmed_summaries(pmids: list[str]) -> list[dict[str, Any]]:
    if not pmids:
        return []
    r = await _get("esummary.fcgi", _params(db="pubmed", id=",".join(pmids)))
    result = r.json().get("result", {})
    out = []
    for pmid in pmids:
        item = result.get(pmid)
        if not item or pmid == "uids":
            continue
        out.append(
            {
                "pmid": pmid,
                "title": item.get("title") or "",
                "source": item.get("source") or item.get("fulljournalname") or "",
                "pubdate": item.get("pubdate") or "",
                "authors": [a.get("name") for a in (item.get("authors") or [])[:5] if a.get("name")],
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            }
        )
    return out


async def pubmed_abstracts(pmids: list[str]) -> dict[str, str]:
    if not pmids:
        return {}
    r = await _get(
        "efetch.fcgi",
        _params(db="pubmed", id=",".join(pmids), retmode="xml", rettype="abstract"),
    )
    try:
        root = ET.fromstring(r.text)
    except ET.ParseError as e:
        raise NCBIError("Invalid XML from NCBI") from e
    abstracts: dict[str, str] = {}
    for article in root.findall(".//PubmedArticle"):
        pmid_el = article.find(".//PMID")
        pmid = pmid_el.text if pmid_el is not None else None
        texts = []
        for abs_text in article.findall(".//Abstract/AbstractText"):
            label = abs_text.get("Label")
            t = "".join(abs_text.itertext()).strip()
            if t:
                texts.append(f"{label}: {t}" if label else t)
        if pmid and texts:
            abstracts[pmid] = "\n".join(texts)
    return abstracts


async def gene_summary(symbol: str) -> dict[str, Any] | None:
    symbol = (symbol or "").strip()
    if not SYMBOL_RE.match(symbol):
        raise ValueError("Invalid gene symbol")
    r = await _get(
        "esearch.fcgi",
        _params(db="gene", term=f"{symbol}[sym] AND human[orgn]", retmax=1),
    )
    ids = r.json().get("esearchresult", {}).get("idlist", []) or []
    if not ids:
        return None
    gid = ids[0]
    r2 = await _get("esummary.fcgi", _params(db="gene", id=gid))
    item = r2.json().get("result", {}).get(gid, {})
    return {
        "gene_id": gid,
        "name": item.get("name") or symbol,
        "description": item.get("description") or "",
        "summary": (item.get("summary") or "")[:1200],
        "url": f"https://www.ncbi.nlm.nih.gov/gene/{gid}",
    }

"""NCBI E-utilities client (PubMed, Gene). Research use; respect rate limits."""
from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any

import httpx

from backend.app.config import get_settings

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def _params(**extra: Any) -> dict[str, Any]:
    s = get_settings()
    p: dict[str, Any] = {
        "tool": s.ncbi_tool,
        "email": s.ncbi_email,
        "retmode": "json",
    }
    if s.ncbi_api_key:
        p["api_key"] = s.ncbi_api_key
    p.update({k: v for k, v in extra.items() if v is not None})
    return p


async def pubmed_search(query: str, retmax: int = 5) -> list[str]:
    """Return list of PMIDs for a query (cancer/diabetes scoped by caller if needed)."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.get(
            f"{BASE}/esearch.fcgi",
            params=_params(db="pubmed", term=query, retmax=retmax, sort="relevance"),
        )
        r.raise_for_status()
        data = r.json()
        return data.get("esearchresult", {}).get("idlist", []) or []


async def pubmed_summaries(pmids: list[str]) -> list[dict[str, Any]]:
    if not pmids:
        return []
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.get(
            f"{BASE}/esummary.fcgi",
            params=_params(db="pubmed", id=",".join(pmids)),
        )
        r.raise_for_status()
        data = r.json()
        result = data.get("result", {})
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
                    "authors": [
                        a.get("name") for a in (item.get("authors") or [])[:5] if a.get("name")
                    ],
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                }
            )
        return out


async def pubmed_abstracts(pmids: list[str]) -> dict[str, str]:
    """Fetch abstracts via efetch XML."""
    if not pmids:
        return {}
    async with httpx.AsyncClient(timeout=45.0) as client:
        r = await client.get(
            f"{BASE}/efetch.fcgi",
            params={
                **_params(db="pubmed", id=",".join(pmids), retmode="xml", rettype="abstract"),
                "retmode": "xml",
            },
        )
        r.raise_for_status()
        root = ET.fromstring(r.text)
        abstracts: dict[str, str] = {}
        for article in root.findall(".//PubmedArticle"):
            pmid_el = article.find(".//PMID")
            pmid = pmid_el.text if pmid_el is not None else None
            texts = []
            for abs_text in article.findall(".//Abstract/AbstractText"):
                label = abs_text.get("Label")
                t = "".join(abs_text.itertext()).strip()
                if not t:
                    continue
                texts.append(f"{label}: {t}" if label else t)
            if pmid and texts:
                abstracts[pmid] = "\n".join(texts)
        return abstracts


async def gene_summary(symbol: str) -> dict[str, Any] | None:
    """Lookup human gene by symbol via esearch + esummary."""
    term = f"{symbol}[sym] AND human[orgn]"
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.get(
            f"{BASE}/esearch.fcgi",
            params=_params(db="gene", term=term, retmax=1),
        )
        r.raise_for_status()
        ids = r.json().get("esearchresult", {}).get("idlist", []) or []
        if not ids:
            return None
        gid = ids[0]
        r2 = await client.get(
            f"{BASE}/esummary.fcgi",
            params=_params(db="gene", id=gid),
        )
        r2.raise_for_status()
        item = r2.json().get("result", {}).get(gid, {})
        return {
            "gene_id": gid,
            "name": item.get("name") or symbol,
            "description": item.get("description") or "",
            "summary": (item.get("summary") or "")[:1200],
            "url": f"https://www.ncbi.nlm.nih.gov/gene/{gid}",
        }

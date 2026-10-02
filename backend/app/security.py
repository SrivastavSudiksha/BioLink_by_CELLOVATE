import time
from collections import deque

from fastapi import Request
from fastapi.responses import Response


class RateLimiter:
    def __init__(self, limit: int, window: float = 60.0):
        self.limit = limit
        self.window = window
        self.hits: dict[str, deque[float]] = {}
        self._last_sweep = time.monotonic()

    def check(self, key: str) -> tuple[bool, int]:
        now = time.monotonic()
        if now - self._last_sweep > self.window:
            self._sweep(now)
        q = self.hits.setdefault(key, deque())
        cutoff = now - self.window
        while q and q[0] <= cutoff:
            q.popleft()
        if len(q) >= self.limit:
            return False, max(1, int(self.window - (now - q[0])))
        q.append(now)
        return True, 0

    def _sweep(self, now: float) -> None:
        cutoff = now - self.window
        for k in [k for k, q in self.hits.items() if not q or q[-1] <= cutoff]:
            del self.hits[k]
        self._last_sweep = now


CSP = (
    "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
    "script-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; "
    "frame-ancestors 'none'; form-action 'self'"
)

DOC_PREFIXES = ("/docs", "/redoc", "/openapi.json")


def apply_security_headers(request: Request, response: Response) -> None:
    h = response.headers
    h["X-Content-Type-Options"] = "nosniff"
    h["X-Frame-Options"] = "DENY"
    h["Referrer-Policy"] = "strict-origin-when-cross-origin"
    h["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if not request.url.path.startswith(DOC_PREFIXES):
        h["Content-Security-Policy"] = CSP
    proto = request.headers.get("x-forwarded-proto", request.url.scheme)
    if proto == "https":
        h["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    path = request.url.path
    if path.startswith("/api/"):
        h["Cache-Control"] = "no-store"
    elif path.endswith((".css", ".js", ".jpg", ".jpeg", ".png", ".svg", ".ico", ".webp")):
        h.setdefault("Cache-Control", "public, max-age=3600")
    else:
        h.setdefault("Cache-Control", "no-cache")

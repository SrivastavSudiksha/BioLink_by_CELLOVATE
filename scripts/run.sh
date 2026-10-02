#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH="${PYTHONPATH:-}:$(pwd)"
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env — set NCBI_EMAIL before live PubMed calls."
fi
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8000}"
if [ "${1:-prod}" = "dev" ]; then
  exec uvicorn backend.app.main:app --reload --host "$HOST" --port "$PORT"
fi
exec uvicorn backend.app.main:app --host "$HOST" --port "$PORT" --workers "${WEB_CONCURRENCY:-2}" --proxy-headers

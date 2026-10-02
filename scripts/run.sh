#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
export PYTHONPATH="${PYTHONPATH:-}:$(pwd)"
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env — set NCBI_EMAIL before live PubMed calls."
fi
exec uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

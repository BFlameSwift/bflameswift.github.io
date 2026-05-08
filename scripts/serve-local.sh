#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST="${HOST:-localhost}"
PORT="${PORT:-4000}"

cd "$ROOT_DIR"

if ! command -v bundle >/dev/null 2>&1; then
  echo "Error: Bundler is not installed or not in PATH."
  echo "Install dependencies first, then run: bundle install"
  exit 1
fi

if command -v lsof >/dev/null 2>&1 && lsof -iTCP:"$PORT" -sTCP:LISTEN -nP >/dev/null 2>&1; then
  echo "Error: port $PORT is already in use."
  lsof -iTCP:"$PORT" -sTCP:LISTEN -nP
  echo
  echo "Use another port, for example:"
  echo "  PORT=4001 scripts/serve-local.sh"
  exit 1
fi

echo "Starting local Jekyll preview..."
echo "URL: http://$HOST:$PORT"
echo

bundle exec jekyll serve -H "$HOST" --port "$PORT" "$@"

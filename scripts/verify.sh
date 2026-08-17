#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"

python3 -m venv .venv
uv pip install --python .venv/bin/python -r requirements-dev.txt

for verification_pass in 1 2; do
  echo "Verification pass ${verification_pass}/2"
  .venv/bin/python -m py_compile contracts/semantic_drift_oracle.py
  .venv/bin/genvm-lint check contracts/semantic_drift_oracle.py
  PATH="$project_root/.venv/bin:$PATH" .venv/bin/genvm-lint typecheck contracts/semantic_drift_oracle.py
  .venv/bin/python -m pytest tests/direct -v --tb=short
done

# SlotFit reproduction image (ADR-0005).
# Builds the web bundle, syncs the locked Python environment and serves the API
# with the UI on port 8000. Synthetic data only; the container contacts nothing.

# ---- stage 1: web bundle -----------------------------------------------------
FROM node:24-slim AS web
WORKDIR /app/web
COPY web/package.json web/package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY web/ ./
RUN npm run build

# ---- stage 2: python runtime ------------------------------------------------
FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH=/app/src \
    SLOTFIT_REVIEW_DATABASE=/data/slotfit.db
COPY --from=ghcr.io/astral-sh/uv:0.9 /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY src/ ./src/
COPY tests/ ./tests/
# Publication-contract tests read the public texts, so they ship with the image.
COPY README.md SECURITY.md LICENSE ./
COPY docs/ ./docs/
COPY web/tests/ ./web/tests/
COPY specs/ ./specs/
COPY aidlc-docs/ ./aidlc-docs/
COPY --from=web /app/web/dist ./web/dist
RUN mkdir -p /data
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" || exit 1
CMD ["uvicorn", "slotfit.composition:app", "--host", "0.0.0.0", "--port", "8000"]

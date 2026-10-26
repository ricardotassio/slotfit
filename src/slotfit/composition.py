"""Composition root: the only module that chooses concrete adapters and wires them together.

Everything else depends on abstractions or on layers below it. Entry points:
``uvicorn slotfit.composition:app`` and ``create_app`` for tests and tools.
"""

from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from slotfit.adapters.api.routes import (
    APPLICATION_DESCRIPTION,
    APPLICATION_TITLE,
    APPLICATION_VERSION,
    get_review_repository,
    register,
)
from slotfit.adapters.persistence.sqlite_review_repository import SQLiteReviewRepository

REVIEW_DATABASE_ENV = "SLOTFIT_REVIEW_DATABASE"
DEFAULT_REVIEW_DATABASE = Path("artifacts/reviews/slotfit.db")
WEB_DIST = Path("web/dist")


def review_database_path() -> Path:
    return Path(os.environ.get(REVIEW_DATABASE_ENV, str(DEFAULT_REVIEW_DATABASE)))


def create_app(
    review_database: Path | None = None,
    web_dist: Path | None = WEB_DIST,
) -> FastAPI:
    """Build the application: API routes, the SQLite review log and, when built, the web UI."""
    app = FastAPI(
        title=APPLICATION_TITLE,
        version=APPLICATION_VERSION,
        description=APPLICATION_DESCRIPTION,
    )
    repository = SQLiteReviewRepository(review_database or review_database_path())
    app.dependency_overrides[get_review_repository] = lambda: repository
    register(app)
    if web_dist is not None and (web_dist / "index.html").exists():
        app.mount("/", StaticFiles(directory=web_dist, html=True), name="web")
    return app


app = create_app()

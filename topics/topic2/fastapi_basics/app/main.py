"""FastAPI app factory and route registration."""

from fastapi import FastAPI

from app.api.routes_analysis import router as analysis_router
from app.api.routes_health import router as health_router
from app.api.routes_placeholders import router as placeholders_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Financial AI Demo API",
        description="Topic 2: thin HTTP layer over Topic 1 rule-based analysis.",
        version="0.1.0",
    )
    app.include_router(health_router)
    app.include_router(analysis_router)
    app.include_router(placeholders_router)
    return app


app = create_app()

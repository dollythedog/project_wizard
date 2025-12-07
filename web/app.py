"""
FastAPI application for Project Wizard v3.0.

Main web interface for project management and AI-powered document generation.
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path

from app.services.database import init_database

# Initialize FastAPI app
app = FastAPI(
    title="Project Wizard",
    description="AI Project Operating System",
    version="3.0.0"
)

# Set up paths
WEB_DIR = Path(__file__).parent
STATIC_DIR = WEB_DIR / "static"
TEMPLATES_DIR = WEB_DIR / "templates"

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


# Initialize database on startup
@app.on_event("startup")
def startup_event():
    """Initialize database when app starts."""
    init_database()
    print("FastAPI application started")


# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Landing page."""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# Import routes
from web.routes import projects, generate, proforma

# Include routers
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(generate.router, prefix="/generate", tags=["generate"])
app.include_router(proforma.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "web.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

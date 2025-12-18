"""FastAPI application for Ripple Idea."""

import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from claude_client import ClaudeClient
from models import (
    ErrorResponse,
    HealthResponse,
    IdeaGenerateRequest,
    IdeaGenerateResponse,
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Ripple Idea API",
    description="波紋のようにアイデアを広げるAPIサービス",
    version="1.0.0",
)

# CORS configuration
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
allow_origins = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # Alternative dev server
    frontend_url,
]

# Remove duplicates while preserving order
allow_origins = list(dict.fromkeys(allow_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Claude client (lazy loading)
_claude_client: ClaudeClient | None = None


def get_claude_client() -> ClaudeClient:
    """Get or create Claude client instance."""
    global _claude_client
    if _claude_client is None:
        _claude_client = ClaudeClient()
    return _claude_client


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="ok")


@app.post(
    "/api/ideas/generate",
    response_model=IdeaGenerateResponse,
    responses={
        500: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
    tags=["Ideas"],
)
async def generate_ideas(request: IdeaGenerateRequest) -> IdeaGenerateResponse:
    """
    Generate creative ideas based on the parent content.

    This endpoint takes a parent idea/theme and generates multiple
    related ideas using Claude AI.
    """
    logger.info(f"Generating {request.count} ideas for: {request.parent_content[:50]}...")

    try:
        client = get_claude_client()
        ideas = await client.generate_ideas(
            theme=request.parent_content,
            context=request.context,
            count=request.count,
        )

        logger.info(f"Successfully generated {len(ideas)} ideas")
        return IdeaGenerateResponse(ideas=ideas)

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise HTTPException(
            status_code=503,
            detail="API configuration error. Please check server configuration."
        )

    except RuntimeError as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate ideas. Please try again."
        )

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred."
        )


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Ripple Idea API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True,
    )

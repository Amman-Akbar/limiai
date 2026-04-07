from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify exact domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount versioned API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["monitoring"])
async def health():
    """Health check endpoint for cloud orchestration (ECP, GKE, ECS)."""
    return {"status": "healthy", "version": settings.VERSION}
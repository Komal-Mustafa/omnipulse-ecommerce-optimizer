from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router

app = FastAPI(
    title="OmniPulse API — Enterprise E-Commerce Optimizer",
    version="1.0.0",
    description="Microservice API for e-commerce return profiling and order verification"
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "OmniPulse Optimizer API",
        "version": "1.0.0"
    }

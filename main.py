from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.upload import router as upload_router

from api.routes import router

app = FastAPI(
    title="RoadPulse API",
    description="AI-powered Traffic & Road Infrastructure Intelligence System",
    version="1.0.0",
    debug=True
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all API routes
app.include_router(router)
app.include_router(upload_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to RoadPulse API",
        "status": "Running"
    }
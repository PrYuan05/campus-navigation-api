from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import the router we wrote
from app.api.routes import router as api_router

# Initialize the FastAPI application
app = FastAPI(
    title="Campus Navigation API", 
    description="This is an open-source backend for a campus route planning system"
)

# Set up CORS (allow frontend web pages to call)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the API router to the application and add a /api prefix
app.include_router(api_router, prefix="/api")

# Hey Hey Just Call it a day!
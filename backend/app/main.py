from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="INTELLITWIN",
    description=(
        "AI-Driven Smart Building Digital Twin "
        "for Predictive Analytics, Scenario Intelligence "
        "and Decision Support"
    ),
    version="0.1.0",
)

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
# During development React will run on localhost:5173.
# This allows the frontend to communicate with FastAPI.
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# ROOT
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "project": "INTELLITWIN",
        "title": "AI-Driven Smart Building Digital Twin",
        "version": "0.1.0",
        "status": "running",
    }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "INTELLITWIN backend",
    }
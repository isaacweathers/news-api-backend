from fastapi import FastAPI
from app.routers import articles
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers (endpoints)
app.include_router(articles.router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the News API!"}

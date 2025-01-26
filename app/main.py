from fastapi import FastAPI
from app.routers import articles

# Initialize FastAPI app
app = FastAPI()

# Include routers (endpoints)
app.include_router(articles.router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the News API!"}

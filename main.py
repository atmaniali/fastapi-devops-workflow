from fastapi import FastAPI

app = FastAPI(
    title="My FastAPI Application",    
    description="This is a sample FastAPI application.",
    version="0.1.0",
)

@app.get("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}

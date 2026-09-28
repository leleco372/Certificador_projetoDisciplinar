from fastapi import FastAPI

from app.api.v1.api import api_router

app = FastAPI()

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )
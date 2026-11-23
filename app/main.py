from fastapi import FastAPI
from app.core.configs import settings
from app.api.v1.api import api_router

app = FastAPI(title="Projeto Certificação", version="1.0.0", description="API RESTful para gestão acadêmica, cursos, matrículas e certificação.")

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
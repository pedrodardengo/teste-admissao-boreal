from fastapi import FastAPI

from src.auth import auth_router

app = FastAPI(title="Teste para Boreal", version="0.1.0")
# app.add_exception_handler(Exception, handler)


app.include_router(auth_router.router)

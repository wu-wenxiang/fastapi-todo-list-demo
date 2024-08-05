from fastapi import APIRouter

from . import hello, todoelems

api_router = APIRouter()

api_router.include_router(hello.router, prefix="/hello", tags=["Hello"])
api_router.include_router(todoelems.router, prefix="/todoelems", tags=["Todoelems"])

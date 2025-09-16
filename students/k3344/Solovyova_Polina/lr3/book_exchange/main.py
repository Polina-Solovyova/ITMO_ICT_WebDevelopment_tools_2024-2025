from fastapi import FastAPI, HTTPException, Query
from app.api import users, auth, userbooks, books, exchanges
from app.core.db import init_db
import requests
import os

app = FastAPI(title="Book Exchange API")

# Создание таблиц (только для разработки)
init_db()

# Роутеры
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(books.router, prefix="/api/books", tags=["books"])
app.include_router(userbooks.router, prefix="/api/userbooks", tags=["userbooks"])
app.include_router(exchanges.router, prefix="/api/exchanges", tags=["exchanges"])


@app.get("/")
def read_root():
    return {"message": "Book Exchange API"}


# URL парсер-сервиса внутри Docker-сети
PARSER_SERVICE_URL = "http://parser:8000"


@app.post("/parse")
def parse(size: int = Query(10, ge=1), slice: int = Query(1, ge=1)):
    try:
        response = requests.post(
            f"{PARSER_SERVICE_URL}/parse",
            params={"size": size, "slice": slice},
            timeout=10
        )
        response.raise_for_status()
        return {"ok": True, "result": response.json()}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Parser service unavailable: {str(e)}")


@app.post("/parse_url")
def parse_url(url: str = Query(..., description="URL to parse")):
    try:
        response = requests.post(
            f"{PARSER_SERVICE_URL}/parse_url",
            params={"url": url},
            timeout=10
        )
        response.raise_for_status()
        return {"ok": True, "result": response.json()}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Parser service unavailable: {str(e)}")

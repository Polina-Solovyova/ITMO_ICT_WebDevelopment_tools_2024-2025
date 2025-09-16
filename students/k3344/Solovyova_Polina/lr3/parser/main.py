import os

from fastapi import FastAPI, HTTPException, Query
import requests
from bs4 import BeautifulSoup

app = FastAPI(title="Parser Service")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/parse_url")
def parse_url(url: str = Query(..., description="URL to parse")):
    """
    Загружает страницу по URL и возвращает основные данные:
    - title страницы
    - длину контента
    - первые 500 символов HTML
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch URL: {str(e)}")

    content = response.text
    soup = BeautifulSoup(content, "lxml")
    title = soup.title.string if soup.title else "No title"

    return {
        "ok": True,
        "url": url,
        "title": title,
        "content_length": len(content),
        "preview": content[:500]
    }

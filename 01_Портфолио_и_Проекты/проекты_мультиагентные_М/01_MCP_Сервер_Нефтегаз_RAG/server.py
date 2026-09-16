import os
import sys
import logging
from typing import Any

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from qdrant_client import QdrantClient

load_dotenv()

POLZA_API_KEY = os.getenv("POLZA_API_KEY")
POLZA_BASE_URL = os.getenv("POLZA_BASE_URL", "https://polza.ai/api/v1")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "neftgas2")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "qwen/qwen3-embedding-8b")

_required = {
    "POLZA_API_KEY": POLZA_API_KEY,
    "QDRANT_URL": QDRANT_URL,
    "QDRANT_API_KEY": QDRANT_API_KEY,
}
_missing = [k for k, v in _required.items() if not v]
if _missing:
    raise RuntimeError(f"Missing required env variables: {_missing}")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger("oilgas-rag-mcp")

qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=30)

mcp = FastMCP("oilgas-rag")


def embed_query(text: str) -> list[float]:

    url = f"{POLZA_BASE_URL}/embeddings"
    headers = {
        "Authorization": f"Bearer {POLZA_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": EMBEDDING_MODEL,
        "input": text,
    }

    with httpx.Client(timeout=30) as client:
        resp = client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

    vector = data["data"][0]["embedding"]
    if len(vector) != 4096:
        log.warning(
            f"Unexpected vector size: got {len(vector)}, expected 4096"
        )
    return vector


@mcp.tool()
def search_oilgas_docs(query: str, top_k: int = 5) -> str:

    if not query or not query.strip():
        return "Ошибка: пустой запрос."
    top_k = max(1, min(top_k, 20))

    log.info(f"Search: query='{query[:80]}...', top_k={top_k}")

    try:
        vector = embed_query(query)
    except httpx.HTTPError as e:
        log.error(f"Embedding failed: {e}")
        return f"Ошибка векторизации запроса: {e}"
    except Exception as e:
        log.error(f"Unexpected error during embedding: {e}")
        return f"Внутренняя ошибка при векторизации: {e}"

    try:
        results = qdrant.query_points(
            collection_name=QDRANT_COLLECTION,
            query=vector,
            limit=top_k,
            with_payload=True,
        ).points
    except Exception as e:
        log.error(f"Qdrant search failed: {e}")
        return f"Ошибка поиска в Qdrant: {e}"

    if not results:
        return "Ничего не найдено в базе по этому запросу."

    blocks = []
    for i, point in enumerate(results, start=1):
        payload = point.payload or {}

        text = (
            payload.get("content")
            or payload.get("text")
            or payload.get("page_content")
            or str(payload)
        )
        metadata = payload.get("metadata", {})
        source_info = []
        if isinstance(metadata, dict):
            if metadata.get("source"):
                source_info.append(f"source: {metadata['source']}")
            if metadata.get("page") is not None:
                source_info.append(f"page: {metadata['page']}")
        source_str = " | ".join(source_info) if source_info else "no metadata"

        blocks.append(
            f"=== Результат {i} (score: {point.score:.4f}) ===\n"
            f"[{source_str}]\n"
            f"{text}\n"
        )

    return "\n".join(blocks)


if __name__ == "__main__":
    log.info(
        f"Starting oilgas-rag MCP server. "
        f"Collection: {QDRANT_COLLECTION}, Model: {EMBEDDING_MODEL}"
    )
    mcp.run(transport="stdio")
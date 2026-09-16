# OilGas RAG MCP Server

MCP-сервер для семантического поиска по нефтегазовой технической документации (ГОСТы, регламенты, инженерные стандарты). Подключается к Claude Desktop через stdio-транспорт, предоставляет один tool — `search_oilgas_docs` — для поиска по векторной базе Qdrant.

## Что это

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) — открытый протокол Anthropic для интеграции LLM с внешними данными и инструментами. С декабря 2025 передан в Linux Foundation Agentic AI Foundation. OpenAI adopted его через Agents SDK.

Этот сервер — обёртка над собственной RAG-базой по нефтегазовой документации (~1000 векторов). Через MCP я могу из Claude Desktop задавать вопросы по ГОСТам и получать ответы со ссылками на конкретные документы.

## Архитектура

Claude Desktop (MCP host)
↓ stdio + JSON-RPC
oilgas-rag MCP server (этот код)
↓ embed query
polza.ai (Qwen3-Embedding-8B → vector 4096)
↓ semantic search
Qdrant Cloud (cosine, top-k retrieval)
↓ return chunks with metadata
formatted response → Claude

## Стек

- **Python 3.13** + `mcp` (FastMCP)
- **httpx** — async-ready HTTP-клиент к polza.ai
- **qdrant-client** — официальный SDK Qdrant
- **Qwen3-Embedding-8B** (4096 dim) — multilingual embeddings через polza.ai
- **Qdrant Cloud** — vector database с cosine distance

## Установка и запуск

```bash
# Клонировать репозиторий
git clone https://github.com/Lavrentiy123/projects.git
cd projects/01_Портфолио_и_Проекты/проекты_мультиагентные_М/01_MCP_Сервер_Нефтегаз_RAG

# Виртуальное окружение
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux

# Зависимости
pip install -r requirements.txt

# Конфигурация
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux
# Заполни .env реальными ключами polza.ai и Qdrant

# Запуск standalone (для проверки)
python server.py
```

## Подключение к Claude Desktop

Открой `claude_desktop_config.json`:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

Добавь в `mcpServers`:

```json
{
  "mcpServers": {
    "oilgas-rag": {
      "command": "C:\\path\\to\\oilgas-rag-mcp\\venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\oilgas-rag-mcp\\server.py"]
    }
  }
}
```

Перезапусти Claude Desktop. Tool появится автоматически.

## Использование в Claude Desktop

После подключения можно спрашивать на естественном языке:

> "Найди в нефтегазовых документах информацию о максимальном пластовом давлении"

Claude вызовет `search_oilgas_docs(query="максимальное пластовое давление")` и получит top-5 чанков с метаданными.

## Production-практики в коде

- Все ключи через `os.getenv()`, никаких hardcoded secrets
- Валидация обязательных env-переменных при старте (fail fast)
- Логи в stderr (stdout зарезервирован для JSON-RPC)
- HTTP timeout 30 сек на embedding и Qdrant
- Валидация входных параметров: `top_k` ограничен диапазоном [1, 20]
- Graceful errors как строки, не raise — MCP-клиент получает понятное сообщение
- Гибкий парсинг payload (поддержка `content`, `text`, `page_content`)
- Извлечение source и page из metadata для цитирования

## Возможные улучшения

- [ ] Retry через `tenacity` на embedding и Qdrant вызовах
- [ ] Кеш embeddings для повторных запросов
- [ ] Дополнительные tools: `list_documents`, `get_chunk_by_id`
- [ ] Hybrid search (BM25 + dense)
- [ ] Reranking (Cross-Encoder)

## Демо

48-секундное видео: подключение MCP-сервера к Claude Desktop и запрос к базе нефтегазовой документации.

[Смотреть демо](https://drive.google.com/file/d/1JmXZjh_m-nanUmWK5dky2XdcOCowM972/view)

## Лицензия

MIT — используйте как угодно.

## Контакты

Лаборатория промышленного ИИ (Industrial AI Lab)
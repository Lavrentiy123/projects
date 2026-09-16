# RAG Bot — Oil & Gas Documentation

Telegram-бот для семантического поиска по нефтегазовой технической документации (ГОСТы, регламенты, инженерные стандарты). Юзер загружает PDF — бот индексирует в векторную базу. На вопрос — возвращает ответ из документов с отказом, если информации нет.

**Заменяет 3-4 часа ручного поиска по документам на 30-60 секунд.**

## Архитектура

Двухуровневая LLM-архитектура с tool calling:
Indexing flow:
Telegram Trigger → If(document?) → Get file → Extract PDF →
Split 50K chars → Loop Over Items → Recursive Character Splitter (2500/800) →
Qwen3-Embedding-8B (4096 dim) → Qdrant insertQuery flow:
Telegram Trigger → AI Agent (GPT-5-mini, orchestrator)
→ Tool: Answer questions with a vector store
→ Qwen3-Embedding-8B (query → vector)
→ Qdrant top-8 retrieval (cosine)
→ Gemini 2.5 Flash Lite (synthesize from chunks)
→ Markdown cleanup
→ Telegram chunking (4096 char limit)
→ Send response

## Стек

- **Orchestration:** n8n
- **Interface:** Telegram Bot API
- **Embeddings:** Qwen3-Embedding-8B (4096 dim) via polza.ai
- **Vector DB:** Qdrant Cloud (cosine, top-8)
- **Orchestrator LLM:** GPT-5-mini via polza.ai
- **Synthesizer LLM:** Gemini 2.5 Flash Lite via polza.ai
- **Memory:** Simple Memory (session by Telegram user_id)

## Архитектурные решения

### Двухуровневая LLM-архитектура (orchestrator + synthesizer)
- **GPT-5-mini** как агент-оркестратор: принимает решение о вызове tool, форматирует финальный ответ
- **Gemini 2.5 Flash Lite** внутри tool: синтезирует ответ из 8 чанков с большим контекстом
- **Trade-off:** дороже single-agent (+1 LLM call), но качество выше — модели специализированы

### top_k = 8
- Широкий контекст для технической документации с длинными определениями и таблицами
- **Trade-off:** избыточно для точечных запросов, в production лучше адаптивный top_k через query classification

### Chunk size 2500 / overlap 800
- Большие чанки сохраняют контекст таблиц и списков
- Большой overlap страхует от разрезания смысловых блоков
- Это **результат debugging'а OOM-ошибок** на n8n-cloud free tier (см. ниже)

### System prompt с anti-hallucination правилами
- Жёсткое правило «отвечать ТОЛЬКО из knowledge base»
- При пустом retrieval — честный отказ, без выдумывания
- Запрет на использование training knowledge для domain-вопросов

## История одного бага

**Симптом:** Workflow падал на больших PDF (200+ страниц).

**Первая гипотеза:** «маленькие чанки плохие». Увеличил chunk_size до 2500 — частично помогло.

**Реальный root cause:** через n8n Executions нашёл `run out of memory`. Проблема не в чанках как таковых, а в архитектурном паттерне: **все чанки разом держатся в памяти** во время обработки. На n8n-cloud free tier лимит памяти быстро упирается.

**Workaround:**
1. Двухуровневая нарезка: JS-код сначала делит extracted text на куски по 50K символов
2. `Loop Over Items` обрабатывает их последовательно
3. Только после этого Recursive Splitter делит на финальные чанки 2500/800

**Правильное production-решение:** streaming-индексация в Python с Celery — читать PDF постранично, embeddinging on-the-fly, не держать всё в памяти. Этот workaround — следствие ограничений n8n-cloud free tier.

## Технические детали

### Telegram markdown cleanup
LLM генерирует ответы в markdown, но Telegram MarkdownV2 требует строгого escape спецсимволов (`_`, `*`, `[`, `]`, `~`, `` ` ``, `>`, `#` и других). LLM это часто не соблюдают — Telegram возвращает `400 Bad Request: can't parse entities`.

**Решение:** убираем markdown через `replace()` перед отправкой. Проще и устойчивее, чем escape всех спецсимволов.

### 4096-character chunking
Telegram limit на одно сообщение — 4096 символов. JS-код режет длинные ответы на части.

### Memory с custom session key
Memory привязана к `message.from.id` — каждый пользователь имеет свою историю диалога, не мешая другим.

## Метрики (pet-проект)

- **Cost per indexing:** ~0.23₽ за PDF 176 страниц
- **Cost per query:** ~0.30₽ (0.07₽ Gemini + 0.25₽ GPT)
- **Latency индексации:** 56 чанков ~15 сек, 190 чанков ~27 сек
- **Recall@8 / faithfulness:** не замерял (осознанный пробел — для production нужен eval-pipeline)

## Установка

### Требования
- n8n self-hosted или n8n-cloud
- Аккаунт Qdrant Cloud с коллекцией `neftgas2` (vector size 4096, distance cosine)
- API-ключ polza.ai (или другого OpenAI-compatible провайдера)
- Telegram Bot token

### Шаги
1. Импортируй `workflow.json` в n8n (Workflows → Import from File)
2. Подключи credentials:
   - **Telegram API** (Bot token из @BotFather)
   - **OpenAI account** для polza.ai (Base URL: `https://polza.ai/api/v1`, API key)
   - **Qdrant account** (URL и API key из Qdrant Cloud)
3. Активируй
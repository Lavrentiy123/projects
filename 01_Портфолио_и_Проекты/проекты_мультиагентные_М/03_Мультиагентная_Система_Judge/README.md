# Multi-Agent Code Generation & Review System

Многоагентная система для генерации production-ready кода через Telegram. Получает задачу на естественном языке, декомпозирует её, генерирует код, ревьюит и итеративно улучшает до 3 циклов.

Реализует паттерн **evaluator-optimizer + iterative refinement** из [Anthropic "Building Effective Agents"](https://www.anthropic.com/engineering/building-effective-agents) с дополнительным **model diversity** на итерациях.

## Что это решает

Один LLM-вызов часто даёт код с дефектами: пропущенный edge case, неправильная сигнатура, опечатка в логике. Простой вариант — попросить LLM «проверь себя» — не работает: модель подыгрывает себе.

Эта система разделяет роли между разными моделями:
- **MAIN** (Gemini) — анализ ТЗ, декомпозиция, заполнение пропущенных требований assumptions
- **CODER** (3 разные модели на 3 итерациях) — генерация кода
- **REVIEWER** (Gemini) — статический code review против ТЗ
- **CRITICAL EVALUATOR** (GPT-5-mini) — выносит финальный вердикт `/ok` или `/critical`

## Архитектура

Три отдельных n8n workflow, связанных через `executeWorkflow`:
┌─────────────────────────────────────────────────┐
│  MAIN (orchestrator)                            │
│  Telegram trigger → /main /coder /review router │
│  → MAIN AGENT (Gemini): декомпозиция ТЗ         │
│  → tag splitter (self-healing retry до 3 раз)   │
│  → executeWorkflow → CODER                       │
└─────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────┐
│  CODER (iterative refinement loop)              │
│                                                 │
│  ITERATION 1:                                   │
│    CODER (MiniMax M2.5) генерирует              │
│    → парсинг ===CODE_START===/===CODE_END===   │
│    → REVIEWER (Gemini) статический анализ       │
│    → CRITICAL EVALUATOR (GPT-5-mini) /ok|/crit  │
│    /ok → конец, отдать пользователю             │
│    /critical → следующая итерация               │
│                                                 │
│  ITERATION 2: CODER2 (MiniMax) с правками        │
│  ITERATION 3: CODER3 (Haiku 4.5) с правками     │
│                                                 │
│  Если 3 итерации не сошлись → "Все пропало"     │
│  + последний код + список правок                │
└─────────────────────────────────────────────────┘
↑
┌─────────────────────────────────────────────────┐
│  REVIEWER (standalone, для прямой /review)      │
│  Скачивает код из Telegram → REVIEWER (Gemini)  │
│  → файл-отчёт                                   │
└─────────────────────────────────────────────────┘

## Стек

- **Orchestration:** n8n (3 workflow + executeWorkflow inter-workflow calls)
- **Interface:** Telegram Bot API (3 команды: `/main`, `/coder`, `/review`)
- **Models (через polza.ai):**
  - Gemini 2.5 Flash Lite — orchestrator, reviewer, tag-fixer
  - MiniMax M2.5 — coder iterations 1, 2
  - Claude Haiku 4.5 — coder iteration 3
  - GPT-5-mini — critical evaluator (LLM-as-judge)
- **Live progress:** Telegram editMessageText (обновление одного сообщения)
- **Structured output:** delimiters `===CODE_START===` / `===CODE_END===` (легче парсить, чем markdown fences)

## Архитектурные решения

### Model diversity на итерациях
Разные модели имеют разные слабости. Если MiniMax стабильно делает один и тот же тип ошибки на задаче — повторный прогон MiniMax её не исправит. Haiku 4.5 на 3-й итерации даёт «другой взгляд».

**Trade-off:** дороже single-model подхода, но качество выше при сложных задачах.

### Critical evaluator как отдельная LLM-судья
Reviewer (Gemini) пишет подробный отчёт, но **решение** «отдавать или возвращать» делегировано отдельной модели (GPT-5-mini). Это снижает риск, что reviewer «подыгрывает» сам себе.

**Trade-off:** +1 LLM-вызов за итерацию (дороже), но решение более устойчивое.

### Self-healing retry на парсере тегов
LLM иногда забывает поставить теги `/coder` и `/review`. Вместо краша — отдельный agent «ПРАВЕР ТЕГОВ» переразмечает текст. Если 3 попытки не помогли — graceful error.

**Trade-off:** +1-2 LLM-вызова в случае сбоя.

### 3 копии coder-workflow внутри одного файла
Это **костыль под ограничение n8n** — нельзя сделать настоящий цикл с переменным числом итераций.

В Python это был бы чистый цикл:
```python
for iteration in range(MAX_ITERATIONS):
code = coder(task, previous_code, fixes)
review = reviewer(task, code)
verdict = critical_evaluator(task, code, review)
if verdict == "/ok":
return code
return graceful_failure(code, fixes)
```

В n8n три копии coder-workflow живут в одном файле с разными моделями. Это **архитектурно слабая** часть проекта — упоминается на собесе как trade-off скорости прототипирования.

### Live progress через editMessageText
Длинная задача (3 итерации, ~2 минут) требует фидбека пользователю. Вместо спама новыми сообщениями — обновляем **одно** сообщение через `editMessageText`:
- "Кодер подготовил первый код..."
- "Тестировщик дает первую обратную связь..."
- "Отдаем код на внесение правок..."
- ...
- В конце сообщение удаляется через `deleteMessage`

Реализовано через `Merge` ноды между этапами — chooseBranch паттерн.

## Команды

В Telegram-чате:

- `/main <задача>` — полный цикл: декомпозиция → генерация → ревью → итерации
- `/coder <ТЗ>` — только генерация кода без ревью (быстрее, дешевле)
- `/review <код или файл>` — только статический review без генерации

## Установка

### Требования
- n8n self-hosted или n8n-cloud (рекомендую self-hosted — workflows тяжёлые)
- API-ключ polza.ai (или OpenAI-compatible с доступом к Gemini, MiniMax, Haiku, GPT)
- Telegram Bot tokens (можно один, но лучше отдельные для MAIN, CODER, REVIEWER — если хочешь раздельную авторизацию)
- Telegram chat/group ID для отправки результатов

### Шаги
1. **Импортируй workflow в n8n в правильном порядке:**
   - Сначала `03-reviewer.workflow.json` → запомни его n8n workflow ID
   - Потом `02-coder.workflow.json` → запомни его n8n workflow ID
   - В JSON `02-coder` найди `YOUR_REVIEWER_WORKFLOW_ID` и подставь реальный ID REVIEWER
   - В последнюю очередь импортируй `01-main.workflow.json`
   - В JSON `01-main` подставь реальные ID `YOUR_REVIEWER_WORKFLOW_ID` и `YOUR_CODER_WORKFLOW_ID`

2. **Замени плейсхолдеры в каждом файле:**
   - `YOUR_TELEGRAM_CHAT_ID` → ID твоей группы/чата (получить через [@userinfobot](https://t.me/userinfobot))

3. **Подключи credentials в n8n:**
   - **Telegram API** для каждой ноды (MAIN, CODER, REVIEWER боты)
   - **OpenAI account** с base URL `https://polza.ai/api/v1` и API key

4. Активируй все три workflow.

5. В Telegram отправь команду:
/main напиши Python-скрипт парсящий CSV и выводящий топ-5 строк по столбцу revenue

## Метрики (для понимания масштаба)

- **Время полного цикла `/main`:** 60-120 секунд (зависит от количества итераций)
- **Стоимость одной задачи:** ~1-5 ₽ (3 итерации × ~1₽ за итерацию + orchestrator)
- **Сходимость:** ~70% задач закрываются на 1-2 итерации, ~25% доходят до 3-й, ~5% «всё пропало»

⚠️ Цифры приблизительные, eval pipeline на 50+ задач ещё не построен (см. ниже).

## Что бы сделал иначе для production

- **LangGraph + Python** вместо n8n — настоящий state machine с циклом, тестируемость, легче дебажить
- **Pydantic structured output** вместо delimiters `===CODE_START===` — более надёжный парсинг
- **Eval pipeline:** evalset из 50 задач разной сложности → метрики (success rate, avg iterations, cost per success, fail patterns)
- **Кеширование** через хэш ТЗ — частые повторные запросы не должны платить заново
- **Параллельный coder** на 1-й итерации (3 модели одновременно → выбираем лучший) вместо последовательных итераций
- **Tracing через LangSmith / Langfuse** — сейчас приходится копаться в n8n Executions

## Связанные проекты

- [oilgas-rag-mcp](https://github.com/ВАШ_НИК/oilgas-rag-mcp) — Python MCP-сервер для семантического поиска
- [n8n-ai-projects/rag-bot](../rag-bot) — RAG по нефтегазовой документации

## Лицензия

MIT
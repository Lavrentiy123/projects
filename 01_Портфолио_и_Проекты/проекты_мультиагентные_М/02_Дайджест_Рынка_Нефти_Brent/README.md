# Oil Market Digest — Automated Brent Analytics Channel

Автоматический Telegram-канал с почасовым выпуском аналитики по нефтяному рынку Brent. Каждый час публикует график цены, метрики (volatility, SMA), дайджест свежих новостей и LLM-аналитику с прогнозом в трёх сценариях.

**Заменяет 3-4 часа ручного мониторинга в день на автоматическую публикацию.**

## Что публикуется каждый час

1. **График Brent** за 6 месяцев (PNG, 12×8) с MA-7, MA-30 и дневными изменениями в %
2. **Метрики**: текущая цена, среднее за 6 мес, max/min с датами, тренд за месяц, volatility (30 дней и 6 месяцев)
3. **Дайджест 25 новостей** из Google News RSS (саммари через Gemini)
4. **Аналитика** с двухуровневой LLM: разведка → техника → фундаментал → 3 сценария с вероятностями (сумма = 100%) → карта триггеров → резюме

## Архитектура
Schedule Trigger (hourly)
↓
├─→ HTTP Request: Google News RSS (oil+gas industry)
│    → XML parser → Split → Limit 25 → JS-формат
│    → AI Agent #1 (Gemini 2.5 Flash Lite, news summarizer)
│    → markdown cleanup
│
├─→ HTTP Request: Flask backend /brent?format=image
│    → matplotlib PNG (двухпанельный график)
│    → Telegram sendPhoto
│
└─→ HTTP Request: Flask backend /brent/detailed
→ JSON метрики (volatility, SMA, change_1m_pct, daily последних 30 дней)
→ 2 пути:
├─→ Telegram sendMessage (raw метрики)
└─→ Merge с дайджестом новостей (см. ниже)
Merge (новости + метрики + 30 дней daily) → JS-комбинация в один prompt
→ AI Agent #2 (Gemini, system prompt на 6 шагов)
Шаг 1: Разведка данных
Шаг 2: Технический анализ (SMA, volatility, моментум)
Шаг 3: Фундаментальный анализ новостей (классификация по векторам)
Шаг 4: 3 сценария с вероятностями (∑=100%)
Шаг 5: Карта рисков и триггеров
Шаг 6: Итоговое резюме для руководителя
→ markdown cleanup → chunking 4000 chars → Telegram sendMessage
Логирование запуска → Google Sheets (timestamp, status, news_count, execution_id)

## Стек

### n8n часть
- **Orchestration:** n8n (hourly Schedule Trigger, 3 параллельных HTTP-потока)
- **News source:** Google News RSS (без API-ключа, работает напрямую)
- **LLM (через polza.ai):** Gemini 2.5 Flash Lite — для обоих агентов (суммаризатор + аналитик)
- **Delivery:** Telegram Bot API (sendPhoto + sendMessage)
- **Observability:** Google Sheets (лог каждого запуска)

### Python backend
- **Flask** (не FastAPI — для простоты)
- **pandas** — `rolling(window=N).mean()` для SMA, `pct_change().std()` для volatility
- **matplotlib** с Agg backend (без GUI), render в `BytesIO` → `send_file`
- **numpy** — `np.random.normal` + `np.cumsum` для синтетического fallback

### Hosting
- **Backend:** PythonAnywhere free tier
- **n8n:** n8n-cloud free tier

## Архитектурные решения

### Двухуровневая LLM-архитектура
- **Gemini #1 (суммаризатор)** обрабатывает 25 новостей → сжатый дайджест
- **Gemini #2 (аналитик)** получает дайджест + метрики + 30 дней daily → 6-шаговый анализ

**Trade-off:** дешевле и качественнее, чем «один LLM проглотит всё». Каждая модель работает с уже релевантным контекстом, не отвлекается на parsing.

### Структурированный системный промпт на 6 шагов
Промпт у `AI Agent1` — это soft structured output без Pydantic. Заставляет LLM последовательно выполнить:
1. Разведка → 2. Техника → 3. Фундаментал → 4. Три сценария с вероятностями → 5. Триггеры → 6. Резюме

**Trade-off:** длинный промпт (~3000 токенов системы), но gain в качестве рассуждения и предсказуемости формата.

### Свой Python backend для метрик
Считать `rolling().mean()` или `pct_change().std()` в n8n JavaScript — громоздко. Логично вынести в pandas. Плюс matplotlib генерирует красивые графики, чего n8n native не умеет.

**Trade-off:** дополнительная инфраструктура (PythonAnywhere), но огромный gain в выразительности кода.

### Observability через Google Sheets
n8n-cloud free tier не даёт нормального доступа к логам выполнений старше пары дней. Каждый запуск логируется в Google Sheets с `execution_id` для дебага.

## Известные ограничения

### 🔴 Yahoo Finance API заблокирован whitelist'ом PythonAnywhere
PythonAnywhere free tier разрешает egress только на whitelisted домены — `query1.finance.yahoo.com` в whitelist'е нет. Нельзя автоматически тянуть свежие котировки.

**Workaround:** CSV обновляется вручную (или через cron-задачу на VPS, который пересохраняет файл).

**Production-решение:** перенести на VPS без whitelist'а или добавить второй источник данных как fallback (Alpha Vantage, Twelve Data).

### 🔴 Graceful fallback на синтетику срабатывает тихо
Если CSV недоступен / повреждён, `get_brent_data()` возвращает синтетику (`np.random.normal` + `np.cumsum`) с пометкой "Моделирование" в источнике. **Но LLM-аналитик делает серьёзный анализ синтетических данных, и пользователь получает бессмысленный прогноз.**

**Это плохое архитектурное решение.** Правильно:
- HTTP 503 при недоступности источника
- Баннер «данные устарели на N часов» с timestamp последнего успешного pull
- Опционально — ML-модель предсказывает значение по тренду, но **никогда** случайные числа

### 🟡 Нет eval-pipeline для калибровки LLM-сценариев
Промпт говорит «вероятности должны суммироваться к 100%», но качество калибровки никогда не замерялось — нужен evalset из 50+ исторических ситуаций с известными outcomes.

## Установка

### Backend (Python + Flask)

```bash
cd oil-market-digest
pip install flask pandas matplotlib numpy

# Подложи свой CSV с историческими данными Brent
# Формат: date,price
# Источник: yfinance ticker BZ=F (https://finance.yahoo.com/quote/BZ%3DF/history)

# Открой flask-backend.py и поправь путь:
# df = pd.read_csv('/path/to/your/data/brent_data.csv')

python flask-backend.py
# Сервис на http://127.0.0.1:5000
```

Endpoints:
- `GET /brent` — JSON с базовыми метриками
- `GET /brent?format=image` — PNG график 12×8 (двухпанельный)
- `GET /brent/detailed` — JSON со всеми метриками + daily за 30 дней

### n8n workflow

1. Импортируй `workflow.json` в n8n
2. Замени плейсхолдеры:
   - `YOUR_TELEGRAM_CHANNEL_ID` → ID твоего канала (получить через [@userinfobot](https://t.me/userinfobot))
   - `YOUR_GOOGLE_SHEET_ID` → ID Google Sheet для логов
   - `YOUR_BACKEND_URL.example.com` → URL твоего Flask-сервиса
3. Подключи credentials:
   - **Telegram API** (Bot token из @BotFather, бот добавлен админом в канал)
   - **OpenAI account** для polza.ai (Base URL: `https://polza.ai/api/v1`, API key)
   - **Google Sheets** OAuth для логирования
4. Активируй workflow → каждый час публикация

## Метрики (для понимания масштаба)

- **Latency:** ~30-60 секунд на полный цикл (RSS, Flask, 2 LLM, Telegram)
- **Cost:** ~0.5-1 ₽ за публикацию (2 Gemini Flash Lite)
- **Объём:** 25 новостей × 1 раз в час × 24 часа = 600 публикаций в день

## Что бы сделал иначе для production

- **VPS + cron-task** обновляет CSV/SQLite раз в час, не зависит от ручного pull
- **FastAPI вместо Flask** — async, лучше под concurrent запросы
- **Второй источник данных** как fallback (Alpha Vantage, Twelve Data, EIA API)
- **Eval pipeline** для калибровки вероятностей LLM-сценариев на исторических ситуациях
- **Промпты в git** с версионированием (сейчас в системном промпте — никакой истории изменений)
- **Кеширование LLM** по hash новостей (если новости не изменились — переиспользуем предыдущий анализ)
- **Pydantic для structured output** — сейчас формат сценариев и триггеров в свободной форме, парсинг невозможен

## Связанные проекты

- [01_MCP_Сервер_Нефтегаз_RAG](../01_MCP_Сервер_Нефтегаз_RAG) — FastMCP-сервер для семантического поиска
- [03_Мультиагентная_Система_Judge](../03_Мультиагентная_Система_Judge) — мультиагентная система самокритики и арбитража
- [04_RAG_Бот_Нефтегаз_Документы](../04_RAG_Бот_Нефтегаз_Документы) — RAG по нефтегазовой документации и регламентам ГНВП

## Лицензия

MIT
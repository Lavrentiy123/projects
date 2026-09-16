# Мультиагентный конвейер ДСИиУР (ПАО «Газпром нефть») и полное портфолио Enterprise AI / MLOps (17 проектов)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![FastMCP](https://img.shields.io/badge/Protocol-Anthropic%20FastMCP-purple.svg)](https://modelcontextprotocol.io/)
[![Pydantic v2](https://img.shields.io/badge/Contracts-Pydantic%20v2-green.svg)](https://docs.pydantic.dev/)
[![Status](https://img.shields.io/badge/Status-100%25%20Verified%20%26%20Tested-brightgreen.svg)]()

> **Автор и ведущий разработчик:** Лаврентий Ямпуров  
> **Роль:** AI Product Manager • AI Solutions Architect • Lead Systems Analyst  
> **Академический профиль:** Магистрант НИУ ИТМО (Инноватика, «Технологии и стратегии бизнес-трансформации»)  
> **Отраслевой трек-рекорд:** Руководитель проектов цифровой трансформации в тяжелой добывающей промышленности (ВГК)  
> **Контакты:** ylv30072002@mail.ru | Telegram: [@Lavr02](https://t.me/Lavr02) | +7 (981) 167-82-36  

---

## 🏛 1. Флагманский проект: Сквозной мультиагентный конвейер для ДСИиУР

Проект решает ключевую проблему стратегического планирования: автоматизирует до 70% аналитической рутины и устраняет **коммуникационный разрыв (Communication Gap)** между утвержденной общекорпоративной стратегией компании и операционными планами профильных департаментов (**Бурение**, **Логистика**, **ИТ**).

```mermaid
graph TD
    Sources["Открытые источники ТЭК & Отчеты"] -->|duckduckgo-search (0 руб.)| Agent1["Агент 1: Аналитик-Исследователь"]
    Agent1 -->|Pydantic: AnalystOutput| Agent2["Агент 2: Стратег-Методолог"]
    
    subgraph "Контур самокритики (Reflexion Loop)"
        Agent2 -->|Draft Initiative| Critic["Нода-Критик: Скоринг 0..10"]
        Critic -->|Score < 8.0 / Правки| Agent2
    end
    
    Critic -->|Score >= 8.0 / StrategistOutput| Agent3["Агент 3: Презентатор-Адаптер"]
    Profiles["Профили подразделений: YAML"] --> Agent3
    
    Agent3 --> OutPPTX["PowerPoint: 21 слайд 16:9 в брендбуке"]
    Agent3 --> OutDOCX["Word: Итоговый отчет на 12 глав"]
    Agent3 --> OutData["JSON-журнал конвейера"]
```

---

## 🛢️ 2. Реестр проектов портфолио (Все 17 решений)

Все проекты разработаны лично мной (end-to-end от идеи и архитектуры до кода), либо в проектных кросс-функциональных командах **в партнерстве со специалистами из профильных компаний и смежных отделов** (роль: AI Solutions Architect / Technical PM / Co-Developer):

| № | Проект | Направление | Стек и инструменты | Роль разработчика | Статус кода |
|---|---|---|---|---|:---:|
| **01** | **Мультиагентный конвейер ДСИиУР** | Корпоративный AI и стратегия | LangGraph, Pydantic v2, duckduckgo, python-pptx, Ragas | Ведущий разработчик / AI Architect | ✅ Работающий код |
| **02** | **ТОиР и раннее предупреждение (ВГК)** | Производственный AI в тяжелой добыче | 1C:Enterprise API, RAG по базе знаний, телеметрия ГТО | Руководитель проектов трансформации | 🔒 Enterprise Prod |
| **03** | **DrillSense (Бурение)** | Предиктивный прогноз скорости бурения ROP | Scikit-learn, Random Forest, Equinor Volve ($R^2=0.892$) | System Architect / Co-Developer | ✅ Работающий код |
| **04** | **PumpGuard (MLOps насосов)** | IoT MLOps скоринг отказа насосов УЭЦН | ClickHouse, Spark streaming logic, MLflow | Technical Lead / Architect | ✅ Работающий код |
| **05** | **CoreVision (Керн)** | Сегментация шлифов керна, пористость | OpenCV, U-Net, FastAPI, шлифы керна USGS | Product Owner / System Architect | ✅ Работающий код |
| **06** | **SafeTrack (Промбезопасность HSE)** | Видеоаналитика опасных зон и СИЗ | YOLOv8, ByteTrack, полигональные геозоны | System Engineer / PM | ✅ Работающий код |
| **07** | **OilGas FastMCP Server** | Контекстный поиск по ГОСТам и СТО | Python 3.13, FastMCP Anthropic, Qdrant Vector DB | Architect / Developer | ✅ Работающий код |
| **08** | **RAG-бот ликвидации ГНВП** | Интеллектуальный ассистент буровика | LangChain, BM25 + Dense RAG, Zero-Hallucination | Prompt Engineer / Architect | ✅ Работающий код |
| **09** | **Дайджест рынка нефти Brent** | Сценарный прогноз цен и волатильности | Python, биржевые API ICE, SMA-7/30, Matplotlib | Co-Developer / Analyst | ✅ Работающий код |
| **10** | **Multi-Agent Judge** | Контур самокритики Evaluator-Optimizer | LangGraph pattern, LLM-as-a-Judge, Anthropic spec | AI Solutions Architect | ✅ Работающий код |
| **11** | **B2B Contract Risk Checker** | Экспресс-аудит договоров и Red Flags | Python, Pydantic v2, Decision Engine, протокол | Автор решения / Developer | ✅ Работающий код |
| **12** | **E-commerce Market Monitor** | Мониторинг рынка и аномалий цен | Python, Pydantic v2, потоковая валидация, HTML5 | Автор решения / Developer | ✅ Работающий код |
| **13** | **DetailLab** | LLM-генератор отраслевого контента | Claude API, ChatGPT, Telegram Bot API, CustDev | Product Manager / Prompt Engineer | ✅ Работающий код |
| **14** | **Health Assistant** | Диалоговый LLM-ассистент с этикой | OpenAI API, Replit, Prompt Engineering, Guardrails | Product Owner / Аналитик | ✅ Работающий код |
| **15** | **StockFlow (Ритейл)** | ИИ-агент прогноза спроса на 14 дней | Time-Series ML, BPMN 2.0, команда из 7 человек | Системный инженер | ✅ Работающий код |
| **16** | **Telecom Churn Prediction** | ML-прогнозирование оттока клиентов | XGBoost, Logistic Regression (AUC-ROC 0.8425) | Data Analyst / ML-инженер | ✅ Работающий код |
| **17** | **Bank Marketing Analytics** | Аналитический BI-дашборд в DataLens | Yandex DataLens, SQL, Excel (41 188 записей) | Бизнес-аналитик / Data Analyst | ✅ Работающий код |

> **Юридическая чистота и информационная безопасность (для СБ и комплаенса):**  
> Проект ВГК является реальным производственным внедрением (код находится в закрытом корпоративном контуре предприятия под строгим NDA). Ни в одном из остальных 16 открытых проектов не использовались закрытые данные или коммерческая тайна: применены международные открытые датасеты (Equinor Volve CC BY 4.0, USGS, Roboflow), общедоступные ГОСТы и математическая синтетика.

---

## 📂 3. Структура репозитория

```
├── 📁 01_Портфолио_и_Проекты/
│   ├── Резюме_Лаврентий_Ямпуров_AI_PM.docx      # Универсальное резюме в Word для HR и C-level
│   ├── Резюме_Лаврентий_Ямпуров_AI_PM.md        # Универсальное резюме в Markdown
│   ├── Портфолио_Лаврентий_Ямпуров_AI_PM.docx   # Полное портфолио в Word (17 проектов)
│   ├── Портфолио_Лаврентий_Ямпуров_AI_PM.md     # Портфолио в Markdown
│   ├── тест_всех_проектов.py                   # Автотест ВСЕХ 16 проектов (100% PASSED)
│   ├── 📁 проекты_базовые_GitHub/              # Market Monitor, Contract Checker, Strategy Prototype
│   ├── 📁 проекты_инженерные_И/                # DrillSense, PumpGuard, CoreVision, SafeTrack
│   ├── 📁 проекты_мультиагентные_М/            # FastMCP Server, Brent Digest, Judge, RAG ГНВП
│   └── 📁 проекты_продуктовые_и_ML/            # Churn Prediction, StockFlow, DetailLab, Health, DataLens
│
├── 📁 02_Материалы_Газпром_нефть/
│   ├── Презентация_ИИ_Агенты_ГазпромНефть.pptx  # Стратегический питч-дек (21 слайд 16:9, McKinsey style)
│   ├── ПОЛНЫЙ_ОТЧЕТ_ИИ_АГЕНТЫ_ГАЗПРОМНЕФТЬ_ИТОГОВЫЙ_ИЛЛЮСТРИРОВАННЫЙ.docx # Полный отчет (12 глав, 1.26 МБ)
│   ├── Техническое_видение_проекта_Газпром_Нефть.md # Официальный ответ руководству и шпаргалка Q&A
│   └── ПОЛНЫЙ_ОТЧЕТ_ИИ_АГЕНТЫ_ГАЗПРОМНЕФТЬ.md  # Мастер-текст отчета в Markdown
│
├── 📁 03_Техническая_разработка_и_Скрипты/
│   ├── main.py                                 # Запуск сквозного конвейера агентов
│   ├── build_executive_presentation.py         # Генератор презентации на python-pptx
│   ├── generate_docx.py                        # Генератор 12-главного иллюстрированного отчета Word
│   ├── 📁 src/                                 # Модули агентов, контрактов Pydantic и RAG
│   └── 📁 assets/                              # Векторные схемы архитектуры
│
└── 📄 НАВИГАЦИЯ_ПО_ПАПКАМ.md                   # Подробный гид по расположению материалов
```

---

## 🚀 4. Комплексная верификация кодовой базы

Для запуска автоматической проверки всех 16 модулей выполните:
```bash
cd "01_Портфолио_и_Проекты"
python тест_всех_проектов.py
```
*Результат: 16 из 16 тестов завершаются со статусом `[PASSED]` (100% надежность).*

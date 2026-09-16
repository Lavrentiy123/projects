# AI Engineering & Product Portfolio | Лаврентий Ямпуров
### Multi-Agent Systems • Industrial AI & MLOps • Applied Machine Learning • Enterprise Decision Engines (17 Проектов)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-orange.svg)](https://github.com/langchain-ai/langgraph)
[![FastMCP](https://img.shields.io/badge/Protocol-Anthropic%20FastMCP-purple.svg)](https://modelcontextprotocol.io/)
[![Pydantic v2](https://img.shields.io/badge/Contracts-Pydantic%20v2-green.svg)](https://docs.pydantic.dev/)
[![ML & CV](https://img.shields.io/badge/ML%20%26%20CV-PyTorch%20%7C%20YOLOv8%20%7C%20Scikit--Learn-red.svg)](https://pytorch.org/)
[![Test Suite](https://img.shields.io/badge/Test%20Suite-16%2F16%20PASSED%20(100%25)-brightgreen.svg)]()

> **Автор и ведущий разработчик:** Лаврентий Ямпуров  
> **Роли:** Lead AI Solutions Architect • AI Product Manager • Lead Systems Analyst  
> **Академический профиль:** Магистрант НИУ ИТМО (Инноватика, «Технологии и стратегии бизнес-трансформации»)  
> **Отраслевой трек-рекорд:** Руководитель проектов цифровой трансформации и ТОиР в тяжелой добывающей промышленности (ВГК)  
> **Контакты:** ylv30072002@mail.ru | Telegram: [@Lavr02](https://t.me/Lavr02) | +7 (981) 167-82-36 | Санкт-Петербург  

---

## 📑 Документы кандидата для скачивания
* 📄 [**Резюме в Word (.docx)**](./01_Портфолио_и_Проекты/Резюме_Лаврентий_Ямпуров_AI_PM.docx) • [**Резюме в Markdown**](./01_Портфолио_и_Проекты/Резюме_Лаврентий_Ямпуров_AI_PM.md)
* 💼 [**Полное портфолио в Word (.docx)**](./01_Портфолио_и_Проекты/Портфолио_Лаврентий_Ямпуров_AI_PM.docx) • [**Портфолио в Markdown**](./01_Портфолио_и_Проекты/Портфолио_Лаврентий_Ямпуров_AI_PM.md)
* 📊 [**Флагманский кейс: Презентация ДСИиУР ПАО «Газпром нефть» (PowerPoint .pptx)**](./02_Материалы_Газпром_нефть/Презентация_ИИ_Агенты_ГазпромНефть.pptx)
* 📘 [**Флагманский кейс: Иллюстрированный аналитический отчет (Word .docx)**](./02_Материалы_Газпром_нефть/ПОЛНЫЙ_ОТЧЕТ_ИИ_АГЕНТЫ_ГАЗПРОМНЕФТЬ_ИТОГОВЫЙ_ИЛЛЮСТРИРОВАННЫЙ.docx)

---

## ⚡ Быстрый старт: Запуск и верификация кода прямо из репозитория

Все проекты в репозитории полностью автономны и снабжены воспроизводимым кодом:
```bash
# 1. Клонирование репозитория
git clone https://github.com/Lavrentiy123/projects.git
cd projects

# 2. Единый запуск автотестов ВСЕХ 16 проектов (100% PASSED)
python 01_Портфолио_и_Проекты/тест_всех_проектов.py
```

### Запуск отдельных демонстрационных модулей:
```bash
# Прогнозирование скорости бурения ROP (Equinor Volve, R² = 0.892)
python 01_Портфолио_и_Проекты/проекты_инженерные_И/01_DrillSense_Бурение/train.py

# MLOps скоринг фонда 500 насосов УЭЦН (вибродиагностика и ранний отказ)
python 01_Портфолио_и_Проекты/проекты_инженерные_И/02_PumpGuard_Насосы_MLOps/test_pumpguard_offline.py

# FastMCP Сервер отраслевых стандартов ТЭК (Anthropic Model Context Protocol)
python 01_Портфолио_и_Проекты/проекты_мультиагентные_М/01_MCP_Сервер_Нефтегаз_RAG/test_oilgas_mcp.py

# Моделирование оттока клиентов (XGBoost vs Logistic Regression, AUC-ROC 0.8425)
python 01_Портфолио_и_Проекты/проекты_продуктовые_и_ML/01_telecom_churn_prediction/run_churn_model.py

# Экспресс-аудит договоров и выявление кабальных условий (Red Flags)
python 01_Портфолио_и_Проекты/проекты_базовые_GitHub/02_contract_risk_checker/run.py
```

---

## 🗺️ Интерактивная витрина проектов (Все 17 решений)

Все проекты разработаны лично автором либо в проектных кросс-функциональных командах **в партнерстве со специалистами из профильных компаний и отраслевых подразделений** (в роли *Lead AI Architect / Technical PM / Co-Developer*):

| № | Проект (Ссылка на папку) | Направление | Исходный код / Демо | Стек технологий | Ключевой результат / Метрики | Статус |
|---|---|---|---|---|---|:---:|
| **01** | [**Мультиагентный конвейер ДСИиУР**](./03_Техническая_разработка_и_Скрипты/) | Стратегический Enterprise AI | [`main.py`](./03_Техническая_разработка_и_Скрипты/main.py) | LangGraph, Pydantic v2, duckduckgo, python-pptx | 3 агента, контур Reflexion, автосборка 21 слайда PPTX и отчета Word | ✅ Код |
| **02** | [**ТОиР и раннее предупреждение (ВГК)**](./01_Портфолио_и_Проекты/Портфолио_Лаврентий_Ямпуров_AI_PM.md#2-цифровая-трансформация-тоир-и-контур-раннего-предупреждения-восточная-горнорудная-компания) | Industrial AI в добыче | 🔒 Корпоративный контур | 1C:Enterprise API, RAG, телеметрия ГТО | Агент дефектовки MAX $\to$ 1C, сокращение времени регистрации дефектов | 🔒 Enterprise Prod |
| **03** | [**DrillSense: Бурение ROP**](./01_Портфолио_и_Проекты/проекты_инженерные_И/01_DrillSense_Бурение/) | Industrial AI & MWD | [`train.py`](./01_Портфолио_и_Проекты/проекты_инженерные_И/01_DrillSense_Бурение/train.py) | Scikit-learn, Random Forest, Equinor Volve | $R^2 = 0.892$, $MAE = 2.41$ м/ч, прогноз проходки и предотвращение прихватов | ✅ Код |
| **04** | [**PumpGuard: MLOps насосов**](./01_Портфолио_и_Проекты/проекты_инженерные_И/02_PumpGuard_Насосы_MLOps/) | IoT & Industrial MLOps | [`test_pumpguard_offline.py`](./01_Портфолио_и_Проекты/проекты_инженерные_И/02_PumpGuard_Насосы_MLOps/test_pumpguard_offline.py) | ClickHouse, Apache Spark streaming, MLflow | 5 000 замеров/сек, скоринг риска отказа за 72 часа, фонд 500 УЭЦН | ✅ Код |
| **05** | [**CoreVision: Анализ керна**](./01_Портфолио_и_Проекты/проекты_инженерные_И/03_CoreVision_Керн_Сегментация/) | Computer Vision в геологии | [`quick_test_corevision.py`](./01_Портфолио_и_Проекты/проекты_инженерные_И/03_CoreVision_Керн_Сегментация/quick_test_corevision.py) | OpenCV, U-Net, FastAPI, шлифы USGS | Расчет пористости ($IoU = 0.841$), гранулометрия и классификация типов коллектора | ✅ Код |
| **06** | [**SafeTrack: Промбезопасность**](./01_Портфолио_и_Проекты/проекты_инженерные_И/04_SafeTrack_Промбезопасность/) | Computer Vision HSE | [`quick_safetrack_demo.py`](./01_Портфолио_и_Проекты/проекты_инженерные_И/04_SafeTrack_Промбезопасность/quick_safetrack_demo.py) | YOLOv8, ByteTrack, полигональные геозоны | Детекция опасных зон буровой/карьера, контроль ношения СИЗ ($mAP@50 = 0.887$) | ✅ Код |
| **07** | [**OilGas FastMCP Server**](./01_Портфолио_и_Проекты/проекты_мультиагентные_М/01_MCP_Сервер_Нефтегаз_RAG/) | Model Context Protocol | [`test_oilgas_mcp.py`](./01_Портфолио_и_Проекты/проекты_мультиагентные_М/01_MCP_Сервер_Нефтегаз_RAG/test_oilgas_mcp.py) | Python 3.13, FastMCP Anthropic, Qdrant | Единый протокол контекста LLM к ГОСТам ТЭК через stdio и JSON-RPC | ✅ Код |
| **08** | [**Дайджест рынка Brent**](./01_Портфолио_и_Проекты/проекты_мультиагентные_М/02_Дайджест_Рынка_Нефти_Brent/) | FinTech & Аналитика ТЭК | [`run_market_analytics.py`](./01_Портфолио_и_Проекты/проекты_мультиагентные_М/02_Дайджест_Рынка_Нефти_Brent/run_market_analytics.py) | Python, Matplotlib, биржевые API, SMA-7/30 | Сбор котировок ICE, тренды волатильности, графики и дайджесты для C-level | ✅ Код |
| **09** | [**Multi-Agent Judge**](./01_Портфолио_и_Проекты/проекты_мультиагентные_М/03_Мультиагентная_Система_Judge/) | Evaluator-Optimizer Loop | [`agent_evaluator_optimizer.py`](./01_Портфолио_и_Проекты/проекты_мультиагентные_М/03_Мультиагентная_Система_Judge/agent_evaluator_optimizer.py) | Multi-Agent Pattern, LLM-as-a-Judge | Детерминированный цикл рефлексии: Генератор $\to$ Критик $\to$ Судья | ✅ Код |
| **10** | [**RAG-бот регламентов ГНВП**](./01_Портфолио_и_Проекты/проекты_мультиагентные_М/04_RAG_Бот_Нефтегаз_Документы/) | Advanced RAG в бурении | [`test_rag_offline.py`](./01_Портфолио_и_Проекты/проекты_мультиагентные_М/04_RAG_Бот_Нефтегаз_Документы/test_rag_offline.py) | LangChain, BM25 + Dense RAG | Точный поиск по регламентам ликвидации ГНВП без галлюцинаций | ✅ Код |
| **11** | [**B2B Contract Risk Checker**](./01_Портфолио_и_Проекты/проекты_базовые_GitHub/02_contract_risk_checker/) | LegalTech & Decision Engines | [`run.py`](./01_Портфолио_и_Проекты/проекты_базовые_GitHub/02_contract_risk_checker/run.py) | Python, Pydantic v2, Decision Engine | Индекс безопасности 0-100, детекция Red Flags, протокол разногласий | ✅ Код |
| **12** | [**E-commerce Market Monitor**](./01_Портфолио_и_Проекты/проекты_базовые_GitHub/01_market_monitor_ecommerce/) | Market Intelligence & Pricing | [`run.py`](./01_Портфолио_и_Проекты/проекты_базовые_GitHub/01_market_monitor_ecommerce/run.py) | Python, Pydantic v2, потоковый анализ | Детекция демпинга (>20%), дефицита и негатива, адаптивный дашборд | ✅ Код |
| **13** | [**DetailLab**](./01_Портфолио_и_Проекты/проекты_продуктовые_и_ML/03_detaillab_content_bot/) | GenAI Content Service | [`run_detaillab_engine.py`](./01_Портфолио_и_Проекты/проекты_продуктовые_и_ML/03_detaillab_content_bot/run_detaillab_engine.py) | Claude API, ChatGPT, Telegram Bot API | CustDev 50+ предпринимателей, 78% сгенерированного контента без правок | ✅ Код |
| **14** | [**Health Assistant**](./01_Портфолио_и_Проекты/проекты_продуктовые_и_ML/04_health_assistant_llm/) | Conversational AI & Guardrails | [`run_health_assistant.py`](./01_Портфолио_и_Проекты/проекты_продуктовые_и_ML/04_health_assistant_llm/run_health_assistant.py) | OpenAI API, Replit, Safety Guardrails | Сценарии диалогов, строгая медицинская этика, отсечение вредных советов | ✅ Код |
| **15** | [**StockFlow: Прогноз спроса**](./01_Портфолио_и_Проекты/проекты_продуктовые_и_ML/02_stockflow_demand_forecast/) | Supply Chain & Time-Series | [`run_stockflow_forecast.py`](./01_Портфолио_и_Проекты/проекты_продуктовые_и_ML/02_stockflow_demand_forecast/run_stockflow_forecast.py) | Time-Series ML, BPMN 2.0, User Stories | Прогноз на 14 дней, расчет точки дозаказа, дефицит полок -15%, команда 7 чел. | ✅ Код |
| **16** | [**Telecom Churn Prediction**](./01_Портфолио_и_Проекты/проекты_продуктовые_и_ML/01_telecom_churn_prediction/) | Applied Machine Learning | [`run_churn_model.py`](./01_Портфолио_и_Проекты/проекты_продуктовые_и_ML/01_telecom_churn_prediction/run_churn_model.py) | XGBoost, Logistic Regression, Scikit-learn | **AUC-ROC = 0.8425**, Accuracy = 0.8034, профилирование факторов оттока | ✅ Код |
| **17** | [**Bank Marketing Analytics**](./01_Портфолио_и_Проекты/проекты_продуктовые_и_ML/05_bank_marketing_datalens/) | BI & Exploratory Data Analysis | [`run_bank_marketing_analysis.py`](./01_Портфолио_и_Проекты/проекты_продуктовые_и_ML/05_bank_marketing_datalens/run_bank_marketing_analysis.py) | Yandex DataLens, SQL, Excel | Когортный анализ 41 188 записей, когорты длительности звонков и конверсий | ✅ Код |

---

## 🏛️ Флагманский Enterprise-кейс: Конвейер стратегического планирования

**Заказчик / Кейс:** Департамент по стратегии, инновациям и устойчивому развитию (ДСИиУР) ПАО «Газпром нефть»  
**Проблема:** Автоматизация до 70% рутины стратегического анализа и ликвидация «коммуникационного разрыва» (Communication Gap) между утвержденной общекорпоративной стратегией и операционными блоками (**Бурение**, **Логистика**, **ИТ**).

```mermaid
graph TD
    Sources["Открытые источники ТЭК & Аналитика"] -->|duckduckgo-search (0 руб.)| Agent1["Агент 1: Аналитик-Исследователь"]
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

### Ключевые архитектурные решения кейса:
1. **Pydantic v2 Data Contracts:** Строгая валидация входящих и исходящих данных между агентами исключает потерю структуры и неконсистентность контекста.
2. **Reflexion Loop (Критерии 0..10):** Инициативы проверяются независимым критиком перед передачей в генерацию артефактов. При скоринге ниже 8.0 гипотеза уходит на итеративную доработку.
3. **Масштабирование до 1000 критериев (Map-Reduce):** Батчирование критериев по 20 штук и параллельная оценка в субагентах с последующей сверткой матрицы.
4. **Программная верстка артефактов:** Автоматическая сборка 21-слайдовой презентации по официальному брендбуку (`python-pptx`) и 12-главного аналитического отчета (`python-docx`).

---

## 🔒 Юридическая чистота и информационная безопасность (Compliance)

* **Реальное производственное внедрение (ВГК):** Код проекта находится в закрытом защищенном контуре предприятия под строгим NDA. В портфолио описана только методология, архитектура и достигнутые бизнес-метрики.
* **Открытые и синтетические данные:** Ни в одном из остальных 16 открытых проектов репозитория не использовались коммерческая тайна или закрытые базы компаний. Использованы международные открытые датасеты (Equinor Volve CC BY 4.0, USGS, Roboflow Universe), официальные ГОСТы и математические симуляторы телеметрии.

---

## 🌐 English Summary (For International & Technical Reviewers)

### About the Author
**Lavrentiy Yampurov** — AI Product Manager & Lead AI Solutions Architect.  
* **Education:** Master's student at ITMO University (Innovation & Business Transformation Strategies).
* **Track Record:** Digital transformation manager in heavy industry (East Mining Company / VGK), designing predictive maintenance (PdM) systems and LLM agent pipelines.
* **Core Expertise:** Multi-Agent Orchestration (LangGraph, FastMCP, Reflexion loops), Industrial AI (drilling rate optimization, ESP pump diagnostics, computer vision for rock cores and HSE), Applied ML (churn modeling, time-series demand forecasting), and B2B Decision Engines.

### Repository Overview
This repository contains a comprehensive showcase of **17 production-grade and PoC projects** spanning:
1. **Multi-Agent Systems & RAG:** FastMCP servers for industry standards, Evaluator-Optimizer (Judge) architectures, zero-hallucination drilling assistants.
2. **Industrial AI & MLOps:** Real telemetry modeling on Equinor Volve data ($R^2=0.892$), high-throughput IoT streaming (ClickHouse + Spark), U-Net core thin section segmentation, and YOLOv8 safety vision.
3. **Enterprise Strategy Automation:** A 3-agent pipeline bridging corporate strategy with operations via programmatic slide and report synthesis.
4. **Risk & Financial Decision Engines:** Automated contract audit, price anomaly arbitrage, and investment scoring.
5. **Applied ML & Analytics:** End-to-end churn prediction (AUC-ROC 0.8425), retail demand forecasting, and BI dashboards.

**All 16 runnable codebases pass 100% of automated unit and integration tests.**  
Run verification: `python 01_Портфолио_и_Проекты/тест_всех_проектов.py`.


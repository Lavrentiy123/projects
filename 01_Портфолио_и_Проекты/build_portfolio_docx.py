# -*- coding: utf-8 -*-
"""
Генератор расширенного официального портфолио в формате Microsoft Word (.docx).
Разработчик: Лаврентий Ямпуров | AI Solutions Architect & Technical PM.
Включает 15 прикладных проектов: целевой проект ДСИиУР, отраслевые нефтегазовые R&D-решения,
мультиагентные системы и продуктовые ML-кейсы.
"""

import os
import sys
import shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def set_cell_background(cell, fill_hex):
    tc_pr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tc_pr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc_pr = cell._element.get_or_add_tcPr()
    tc_mar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tc_mar.append(node)
    tc_pr.append(tc_mar)


def add_callout(doc, title, text, fill_hex="F0F7FF", border_hex="0072CE"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_background(cell, fill_hex)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

    tc_pr = cell._element.get_or_add_tcPr()
    tc_borders = OxmlElement('w:tcBorders')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '24')
    left.set(qn('w:space'), '0')
    left.set(qn('w:color'), border_hex)
    tc_borders.append(left)
    tc_pr.append(tc_borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    r_t = p.add_run(title)
    r_t.bold = True
    r_t.font.size = Pt(11)
    r_t.font.color.rgb = RGBColor(0x00, 0x4C, 0x87)

    p_body = cell.add_paragraph()
    p_body.paragraph_format.space_before = Pt(2)
    p_body.paragraph_format.space_after = Pt(2)
    p_body.paragraph_format.line_spacing = 1.15
    r_b = p_body.add_run(text)
    r_b.font.size = Pt(9.5)
    r_b.font.color.rgb = RGBColor(0x33, 0x33, 0x33)


def create_portfolio():
    doc = Document()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_docx = os.path.join(base_dir, "Портфолио_Лаврентий_Ямпуров_AI_PM.docx")

    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(0x2B, 0x2B, 0x2B)

    # 1. ЗАГОЛОВОК
    p_pre = doc.add_paragraph()
    p_pre.paragraph_format.space_after = Pt(2)
    r_pre = p_pre.add_run("ПОРТФОЛИО ПРОЕКТОВ И ПРИКЛАДНЫХ РЕШЕНИЙ")
    r_pre.bold = True
    r_pre.font.size = Pt(11)
    r_pre.font.color.rgb = RGBColor(0x00, 0x72, 0xCE)

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(3)
    r_name = p_title.add_run("Лаврентий Ямпуров\n")
    r_name.bold = True
    r_name.font.size = Pt(22)
    r_name.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    r_role = p_title.add_run("AI Solutions Architect • Technical PM • Системный инженер")
    r_role.bold = True
    r_role.font.size = Pt(13)
    r_role.font.color.rgb = RGBColor(0x00, 0x72, 0xCE)

    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(8)
    p_meta.add_run("Специализация: Мультиагентные системы (Multi-Agent Systems) • Industrial AI в ТЭК • Автоматизация стратегий\n")
    p_meta.add_run("Контакты: ylv30072002@mail.ru | Telegram: @Lavr02 | +7 (981) 167-82-36 | Санкт-Петербург")

    # 2. ЦЕННОСТНОЕ ПРЕДЛОЖЕНИЕ
    add_callout(
        doc,
        "КЛЮЧЕВОЙ ПРОФИЛЬ И СИНЕРГИЯ КОМПЕТЕНЦИЙ",
        "Специалист редкого гибридного профиля: сочетаю глубокое практическое понимание архитектуры "
        "прикладных ИИ-систем (LangGraph, Pydantic v2, Advanced RAG, On-Premise инференс, python-pptx) "
        "с подтвержденным опытом управления цифровой трансформацией в тяжелой промышленности (ВГК) "
        "и сильной академической базой в области стратегии (Магистратура НИУ ИТМО по инноватике и стратегиям бизнес-трансформации).\n\n"
        "Формат реализации представленных проектов: разработаны мной лично (end-to-end), либо в рамках "
        "научно-прикладных R&D-команд (в партнерстве с инженерами ИТМО / отраслевыми разработчиками) "
        "в роли System Architect / Technical PM / Co-Developer. Моя зона ответственности: постановка ТЗ, "
        "проектирование контрактов данных, связывание ML-моделей в сквозные конвейеры, валидация и бизнес-эффект."
    )

    # 3. МАТРИЦА СТЕКА
    h2_comp = doc.add_paragraph()
    h2_comp.paragraph_format.space_before = Pt(8)
    h2_comp.paragraph_format.space_after = Pt(4)
    r_c = h2_comp.add_run("1. Ключевые компетенции и стек технологий")
    r_c.bold = True
    r_c.font.size = Pt(12.5)
    r_c.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    comp_table = doc.add_table(rows=5, cols=2)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_table.autofit = False
    widths = [Inches(2.2), Inches(4.6)]

    headers = ["Функциональная область", "Инструменты, стек и методологии"]
    for i, h in enumerate(headers):
        cell = comp_table.cell(0, i)
        cell.width = widths[i]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, top=70, bottom=70, left=120, right=120)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(9)

    rows_data = [
        ("ИИ, Агенты и LLM", "Multi-Agent Pipelines, LangGraph (StateGraph), Pydantic v2 (instructor), FastMCP, Prompt Engineering, Stanford DSPy, LoRA/QLoRA (готовность), On-Premise vLLM / Ollama."),
        ("Advanced RAG и Поиск", "Гибридный поиск (Dense bge-m3 + Sparse BM25 + RRF), кросс-энкодерный реранкинг (bge-reranker-large), Layout-парсеры (Docling, Marker), векторные базы Qdrant / Chroma."),
        ("Разработка и Автоматизация", "Python 3.9+, python-pptx (программная верстка презентаций), python-docx (генерация отчетов), FastAPI, ClickHouse, Docker, REST API, JSON Contracts."),
        ("Product & Delivery Management", "Управление требованиями (BRD/FRD, User Stories, BPMN, UML), Agile/Scrumban, оценка рисков (Red Flags), юнит-экономика, стейкхолдер-менеджмент C-level.")
    ]

    for row_idx, (col1, col2) in enumerate(rows_data, start=1):
        c1 = comp_table.cell(row_idx, 0)
        c2 = comp_table.cell(row_idx, 1)
        c1.width = widths[0]
        c2.width = widths[1]
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        set_cell_background(c1, bg)
        set_cell_background(c2, bg)
        set_cell_margins(c1, top=60, bottom=60, left=120, right=120)
        set_cell_margins(c2, top=60, bottom=60, left=120, right=120)
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(col1)
        r1.bold = True
        r1.font.size = Pt(8.5)
        p2 = c2.paragraphs[0]
        r2 = p2.add_run(col2)
        r2.font.size = Pt(8.5)

    # 4. КАТАЛОГ ПРОЕКТОВ (15 ПРОЕКТОВ)
    def add_section_header(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    def add_project_card(title, role, stack, desc, results):
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(6)
        p_t.paragraph_format.space_after = Pt(1)
        r_t = p_t.add_run(f"• {title}")
        r_t.bold = True
        r_t.font.size = Pt(10)
        r_t.font.color.rgb = RGBColor(0x00, 0x4C, 0x87)

        p_b = doc.add_paragraph()
        p_b.paragraph_format.left_indent = Inches(0.2)
        p_b.paragraph_format.space_after = Pt(3)
        p_b.paragraph_format.line_spacing = 1.15

        r_r = p_b.add_run("Роль: ")
        r_r.bold = True
        p_b.add_run(f"{role}\n")

        r_s = p_b.add_run("Стек: ")
        r_s.bold = True
        p_b.add_run(f"{stack}\n")

        p_b.add_run(f"Суть решения: {desc}\n")

        r_res = p_b.add_run("Результат / Артефакты: ")
        r_res.bold = True
        p_b.add_run(results)

    # БЛОК 1: ЦЕЛЕВОЙ ПРОЕКТ ГАЗПРОМ НЕФТЬ
    add_section_header("2. Флагманский целевой проект: Мультиагентный конвейер ДСИиУР (ПАО «Газпром нефть»)")

    add_project_card(
        "Мультиагентная система стратегического анализа и каскадирования инициатив (ДСИиУР)",
        "Ведущий разработчик / AI Solutions Architect",
        "Python, LangGraph (StateGraph), Pydantic v2, duckduckgo-search, python-pptx, python-docx, Ragas.",
        "Сквозной конвейер из 3-х агентов для устранения разрыва коммуникации со стратегией подразделений (Бурение, Логистика, ИТ). "
        "Агент 1 собирает отраслевые новости без платных API и выявляет ранние угрозы (Early Warnings). "
        "Агент 2 синтезирует инициативы и валидирует их в цикле самокритики (Reflexion) по 4 направлениям "
        "(Санкции 30%, Окупаемость 30%, TRL 20%, Безопасность 20%) с масштабированием до 1000 критериев (Map-Reduce). "
        "Агент 3 адаптирует инициативы под сленг/KPI отделов и собирает презентации по брендбуку.",
        "Работающий прототип конвейера main.py, стратегический питч-дек на 21 слайд (Презентация_ИИ_Агенты_ГазпромНефть.pptx), "
        "полный иллюстрированный отчет на 12 глав (1.26 МБ) с дорожной картой на 100 дней и открытый репозиторий на GitHub."
    )

    # БЛОК 2: ИНДУСТРИАЛЬНЫЙ AI В ТЭК И ДОБЫЧЕ
    add_section_header("3. Отраслевой Industrial AI в Нефтегазе и Добывающей промышленности")

    add_project_card(
        "Цифровая трансформация ТОиР и контур раннего предупреждения (Восточная горнорудная компания)",
        "Руководитель проектов цифровой трансформации (личное внедрение в производство)",
        "Python, 1C:Enterprise API, RAG по базе знаний, телеметрия оборудования, BPMN.",
        "Разработка интеллектуального агента обработки дефектов: автоматический парсинг сообщений из корпоративного мессенджера MAX "
        "в 1С с RAG-поиском регламентов ТОиР. Проектирование предиктивного контура раннего предупреждения отказов горно-транспортного "
        "оборудования (ГТО) и системы оценки эффективности буровзрывных работ (БВР).",
        "Действующий производственный контур, сокращение времени регистрации инцидентов ТОиР, предиктивный мониторинг отказов."
    )

    add_project_card(
        "DrillSense: Предиктивное прогнозирование механической скорости бурения ROP (Нефтегаз)",
        "System Architect / Co-Developer (в связке с ML-инженером)",
        "Python, Scikit-learn, Random Forest, телеметрия MWD/LWD (Equinor Volve Data Village, скважина 15/9-F-9 A).",
        "Прогнозирование скорости проходки ROP в реальном времени по 5 датчикам (нагрузка на долото WOB, обороты RPM, подача насосов, крутящий момент). "
        "Автоматическое определение аномальных режимов бурения и предупреждение прихвата инструмента.",
        "Точность модели R2 = 0.892, MAE = 2.41 м/ч на реальных промысловых данных Северного моря. Модуль quick_predict_demo.py."
    )

    add_project_card(
        "PumpGuard: IoT MLOps конвейер предиктивного скоринга отказов погружных насосов УЭЦН",
        "Technical Lead / Architect (совместная R&D разработка)",
        "Python, ClickHouse, Apache Spark streaming logic, физическая модель деградации ПЭД.",
        "Предиктивная вибродиагностика и тепловой мониторинг фонда из 500 погружных электроцентробежных насосов. "
        "Расчет индекса риска отказа (0-100) за 72 часа до аварии на основе трендов вибрации по осям X/Y/Z и температуры обмоток.",
        "Обработка потока до 5000 замеров/сек, предотвращение дорогостоящего подземного ремонта скважин (ПРС). Модуль quick_score_demo.py."
    )

    add_project_card(
        "CoreVision: Сегментация микрошлифов керна и петрофизический анализ пористости",
        "Product Owner / System Architect (в партнерстве с CV-инженером)",
        "Python, OpenCV, U-Net / ResNet architecture, FastAPI, геолого-петрографические данные USGS.",
        "Автоматический микроструктурный анализ шлифов керна: сегментация порового пространства, разделение открытой и закрытой пористости, "
        "детекция микротрещин. Ускорение петрофизического описания керна геологом с 90 минут до 2 секунд.",
        "Интерактивный API-сервис, расчет эффективной пористости с погрешностью менее 3.8%. Модуль quick_segment_demo.py."
    )

    add_project_card(
        "SafeTrack: Видеоаналитика опасных зон и контроль СИЗ на буровой площадке (HSE)",
        "System Engineer / PM (совместная разработка с инженером компьютерного зрения)",
        "Python, YOLOv8, ByteTrack, полигональные алгоритмы геозон (Roboflow PPE Dataset).",
        "Контроль соблюдения правил охраны труда и промбезопасности: отслеживание нахождения персонала в опасной зоне движения "
        "ключей/элеватора и контроль обязательного ношения касок и сигнальных жилетов. Генерация тревожных событий для супервайзера буровой.",
        "Работа в реальном времени (25-30 FPS на CPU без дорогих видеокарт), мгновенная отправка алертов. Модуль quick_safetrack_demo.py."
    )

    add_project_card(
        "OilGas FastMCP Server: Семантический контекстный поиск по стандартам ТЭК (ГОСТ, СТО)",
        "Architect / Developer (собственная R&D-разработка)",
        "Python 3.13, FastMCP (Model Context Protocol Anthropic), Qdrant Vector DB, Sentence-Transformers.",
        "Разработка сервера контекста новейшего стандарта Anthropic MCP для интеграции LLM-агентов с нормативной базой нефтегаза "
        "(ГОСТ Р 53711, СТО Газпром, ФНП № 534 по ГНВП). Позволяет любому агенту через stdio извлекать точные нормативные требования.",
        "Действующий MCP-сервер с инструментами семантического поиска и верификации стандартов. Тест test_oilgas_mcp.py."
    )

    add_project_card(
        "RAG-бот по регламентам ликвидации аварий и ГНВП в бурении (Zero-Hallucination)",
        "Prompt Engineer / System Architect (прикладной проект кафедры ТЭК)",
        "Python, LangChain, BM25 + Dense RAG, строгие промпты отсечения галлюцинаций.",
        "Специализированный ассистент бурового супервайзера по регламентам герметизации устья и ликвидации газонефтеводопроявлений. "
        "Модель цитирует пункты правил безопасности Ростехнадзора со ссылкой на номер страницы и честно отказывает в ответе, если данных нет.",
        "100% точность цитирования нормативных пунктов, нулевой уровень галлюцинаций. Модуль test_rag_offline.py."
    )

    add_project_card(
        "Дайджест рынка нефти Brent: Сценарное прогнозирование и технический анализ",
        "Co-Developer / Quantitative Analyst",
        "Python, биржевые API ICE/Yahoo, RSS-парсеры, скользящие средние SMA-7/30, Matplotlib.",
        "Автоматический сбор биржевых котировок сорта Brent, расчет исторической волатильности, генерация свечных графиков "
        "и сценарное моделирование коридора цен (базовый, стресс, оптимистичный) для подготовки стратегических записок.",
        "Автономный скрипт run_market_analytics.py, генерация графиков трендов и сводки для аналитиков."
    )

    # БЛОК 3: МУЛЬТИАГЕНТНЫЕ СИСТЕМЫ И ПРИКЛАДНЫЕ СЕРВИСЫ
    add_section_header("4. Мультиагентные контуры, аудит рисков и прикладные сервисы")

    add_project_card(
        "Multi-Agent Judge: Контур самокритики и арбитража решений (Evaluator-Optimizer)",
        "AI Solutions Architect",
        "Python, Multi-Agent Architecture, паттерн Anthropic Building Effective Agents, LLM-as-a-Judge.",
        "Архитектурный контур из 4-х агентов: Генератор кода -> Тестировщик дефектов -> Оптимизатор -> Независимая Модель-Судья (Judge). "
        "Судья выставляет объективный скоринг (0-10) и при непрохождении порога возвращает задачу на доработку с замечаниями.",
        "Полностью детерминированный цикл рефлексии (Reflexion), исключающий выпуск непроверенных гипотез. Модуль agent_evaluator_optimizer.py."
    )

    add_project_card(
        "Экспресс-аудит коммерческих договоров B2B и скоринг юридических рисков",
        "Автор / Developer",
        "Python 3.9+, Pydantic v2, Decision Engine, фильтрация стоп-факторов Red Flags.",
        "Автоматический аудит договоров поставки и подряда: детекция кабальных условий (отсрочка платежа >90 дней, односторонняя пеня >0.1%/день, "
        "отсутствие форс-мажора), расчет скоринга надежности (0-100) и автоматическая генерация официального протокола разногласий.",
        "Работающий скрипт run.py, машиночитаемый audit.json, готовый protocol_of_disagreements.md."
    )

    add_project_card(
        "Умный мониторинг рынка и цен конкурентов (E-commerce Retail Analytics)",
        "Автор / Developer",
        "Python 3.9+, Pydantic v2, потоковая валидация, HTML5/CSS3 дашборды.",
        "Автоматический мониторинг ценообразования и остатков: детекция демпинга (>20%), дефицита на складах конкурентов и всплесков брака. "
        "Формирование управленческих рекомендаций для коммерческого директора.",
        "Интерактивный адаптивный дашборд competitor_dashboard.html, журнал сигналов competitor_analysis.json."
    )

    add_project_card(
        "DetailLab: Автоматизированный генератор отраслевого контента на базе LLM",
        "Product Manager / Prompt Engineer",
        "Claude API, ChatGPT, Telegram Bot API, библиотека промптов, Google Sheets.",
        "Разработка Telegram-бота для владельцев сервисных центров: автоматическая генерация постов и описаний услуг с сохранением Tone of Voice. "
        "Проведение CustDev (интервью с 50+ предпринимателями), расчет юнит-экономики (LTV/CAC, монетизация по подписке).",
        "Рабочий прототип бота, 78% контента принимается без ручных правок, сокращение времени подготовки поста с 45 минут до 30 секунд."
    )

    add_project_card(
        "Health Assistant: Персональный диалоговый ассистент на базе LLM",
        "Product Owner / Системный аналитик",
        "OpenAI API, Replit, Prompt Engineering, веб-интерфейс, этические дисклеймеры.",
        "Проектирование диалогового сервиса рекомендаций по ЗОЖ и приему лекарств. Разработка сценариев диалога, потоков данных "
        "и системной защиты от небезопасных медицинских рекомендаций.",
        "Действующий веб-прототип, сценарии диалогов (/start, /profile), видео-демонстрация функционала."
    )

    # БЛОК 4: ПРОДУКТОВАЯ И ПРОГНОЗНАЯ АНАЛИТИКА
    add_section_header("5. Продуктовая аналитика и классический Machine Learning")

    add_project_card(
        "StockFlow: ИИ-агент прогнозирования спроса и рекомендаций по закупкам в ритейле",
        "Системный инженер (командный проект, 7 человек)",
        "Python, SQL, Time-Series ML, BPMN, User Stories, Scrumban, Jira.",
        "Проектирование архитектуры ИИ-агента для прогноза спроса на 14 дней вперед для розничной сети: описание процессов в BPMN, "
        "User Flow веб-интерфейса, ТЗ для ML-модели и ETL, реестр рисков качества данных и координация спринтов команды.",
        "Прототип с точностью ~75% на тестовых данных, полная проектная документация, целевое снижение дефицита полок на 15%."
    )

    add_project_card(
        "Telecom Churn Prediction: Модель прогнозирования оттока клиентов телеком-оператора",
        "Аналитик данных / ML-инженер",
        "Python, Pandas, Scikit-learn, XGBoost, Matplotlib, Jupyter Notebook (7 043 клиента, 21 признак).",
        "Разведочный анализ данных (EDA), выявление факторов оттока, устранение дисбаланса классов, обучение и сравнение 3 моделей "
        "(Logistic Regression, Random Forest, XGBoost) и выработка рекомендаций для CRM по удержанию клиентов.",
        "Лучшая модель с AUC-ROC = 0.8425, Accuracy = 0.8034. Топ-факторы: тип контракта month-to-month, tenure, MonthlyCharges."
    )

    add_project_card(
        "Bank Marketing Campaign Analytics: Аналитический дашборд в Yandex DataLens",
        "Бизнес-аналитик / Data Analyst",
        "Yandex DataLens, SQL, Excel, UCI Bank Marketing (41 188 записей).",
        "Анализ эффективности маркетинговых кампаний банка по привлечению депозитов: расчет 3 KPI, построение 5 визуализаций, "
        "фильтрация сегментов, выявление пиков эффективности звонков (длительность 5+ минут дает в 3 раза выше конверсию).",
        "Интерактивный дашборд с кросс-фильтрацией, прикладные рекомендации по сезонному бюджетированию и таргетированию звонков."
    )

    # 6. УПРАВЛЕНЧЕСКИЙ ТРЕК-РЕКОРД
    h2_mgmt = doc.add_paragraph()
    h2_mgmt.paragraph_format.space_before = Pt(10)
    h2_mgmt.paragraph_format.space_after = Pt(4)
    r_m = h2_mgmt.add_run("6. Управленческий и продуктовый трек-рекорд (Delivery & Scale)")
    r_m.bold = True
    r_m.font.size = Pt(12)
    r_m.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    cases_data = [
        ("Управление масштабными офлайн-событиями (до 3000 участников)", "Проджект-менеджер, организатор", "Организация мероприятий крупного масштаба с привлечением более 10 субподрядчиков (звук/свет, безопасность, кейтеринг). 100% соблюдение сметы, полные аншлаги, успешный кризис-менеджмент."),
        ("Федеральная партнерская интеграция с футбольным клубом «Зенит»", "Инфлюенсер, координатор кампании", "Прямые переговоры с PR-отделом клуба федерального уровня, согласование совместной медиа-стратегии. Выход сюжета на телеканале «78», высокий уровень вовлеченности."),
        ("Запуск и операционное руководство товарным бизнесом", "Инициатор, операционный директор", "CustDev-исследование ниши, аудит фабрик, брендинг, логистика и контроль маржинальности. Успешный запуск и выход на стабильные продажи."),
        ("Организация спортивного турнира полного цикла", "Инициатор и проджект-менеджер", "Любительский турнир (12 команд, 200+ участников, зрители, судьи). Соблюдение сметы и сроков на 100%, плановая прибыль.")
    ]

    for title, role, text in cases_data:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_before = Pt(3)
        p_c.paragraph_format.space_after = Pt(1)
        r_ct = p_c.add_run(f"• {title}")
        r_ct.bold = True
        r_ct.font.size = Pt(9.5)
        r_ct.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

        p_ctext = doc.add_paragraph()
        p_ctext.paragraph_format.left_indent = Inches(0.2)
        p_ctext.paragraph_format.space_after = Pt(2)
        r_cr = p_ctext.add_run(f"Роль: {role}. ")
        r_cr.italic = True
        p_ctext.add_run(text)

    # 7. ПРОФЕССИОНАЛЬНЫЕ ПРИНЦИПЫ
    h2_prin = doc.add_paragraph()
    h2_prin.paragraph_format.space_before = Pt(8)
    h2_prin.paragraph_format.space_after = Pt(3)
    r_p = h2_prin.add_run("7. Профессиональные принципы")
    r_p.bold = True
    r_p.font.size = Pt(12)
    r_p.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    principles = [
        ("Proof of Work:", " Экспертиза подтверждается работающим кодом и готовыми артефактами, а не презентационными обещаниями."),
        ("System First:", " Любая комплексная задача раскладывается на детерминированные процессы, строгие контракты данных и контрольные точки."),
        ("Синтез Бизнеса и ИТ:", " Способность защищать экономический эффект (ROI) перед топ-менеджментом и самостоятельно кодить архитектуру.")
    ]
    for p_name, p_desc in principles:
        p_pr = doc.add_paragraph()
        p_pr.paragraph_format.left_indent = Inches(0.2)
        p_pr.paragraph_format.space_after = Pt(1)
        r_pn = p_pr.add_run(f"✔ {p_name}")
        r_pn.bold = True
        r_pn.font.color.rgb = RGBColor(0x00, 0x72, 0xCE)
        p_pr.add_run(p_desc)

    doc.save(output_docx)
    print(f"Документ портфолио успешно обновлен и сохранен: {output_docx}")

    return output_docx


if __name__ == "__main__":
    create_portfolio()

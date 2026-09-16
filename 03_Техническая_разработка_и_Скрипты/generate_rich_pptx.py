import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Corporate Color Palette
NAVY_BLUE = RGBColor(0, 51, 102)     # #003366
PRIMARY_BLUE = RGBColor(0, 121, 194) # #0079C2
DARK_TEXT = RGBColor(30, 41, 59)     # #1E293B
LIGHT_BG = RGBColor(244, 247, 251)   # #F4F7FB
WHITE = RGBColor(255, 255, 255)
CARD_BG = RGBColor(235, 243, 250)    # #EBF3FA
BORDER_COLOR = RGBColor(200, 218, 235)
ACCENT_GREEN = RGBColor(16, 149, 106)
ACCENT_ORANGE = RGBColor(220, 100, 30)

ASSETS_DIR = os.path.abspath("c:/Users/Lavrentiy/Desktop/газпром/assets")

def add_header(slide, title_text, category="ДСИиУР ПАО «ГАЗПРОМ НЕФТЬ» | АРХИТЕКТУРА ИИ-АГЕНТОВ"):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(8.4), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_cat = tf.paragraphs[0]
    r_cat = p_cat.add_run()
    r_cat.text = category.upper()
    r_cat.font.size = Pt(10)
    r_cat.font.bold = True
    r_cat.font.color.rgb = PRIMARY_BLUE
    
    p_title = tf.add_paragraph()
    r_title = p_title.add_run()
    r_title.text = title_text
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY_BLUE

def add_card(slide, left, top, width, height, title, content_lines, border_color=PRIMARY_BLUE, bg_color=CARD_BG):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.18)
    tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.15)
    tf.margin_bottom = Inches(0.15)
    
    p_t = tf.paragraphs[0]
    r_t = p_t.add_run()
    r_t.text = title
    r_t.font.bold = True
    r_t.font.size = Pt(13)
    r_t.font.color.rgb = NAVY_BLUE
    
    for line in content_lines:
        p_c = tf.add_paragraph()
        p_c.space_before = Pt(4)
        r_c = p_c.add_run()
        r_c.text = line
        r_c.font.size = Pt(10)
        r_c.font.color.rgb = DARK_TEXT

def create_rich_presentation():
    prs = Presentation()
    prs.slide_width = Inches(10.0)
    prs.slide_height = Inches(5.625) # 16:9 widescreen
    blank_layout = prs.slide_layouts[6]

    # ==================== SLIDE 1: Title Slide ====================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(10), Inches(5.625))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_BLUE
    bg1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(8.0), Inches(3.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p1_0 = tf1.paragraphs[0]
    r1_0 = p1_0.add_run()
    r1_0.text = "ДЕПАРТАМЕНТ ПО СТРАТЕГИИ, ИННОВАЦИЯМ И УСТОЙЧИВОМУ РАЗВИТИЮ (ДСИиУР)"
    r1_0.font.size = Pt(11)
    r1_0.font.bold = True
    r1_0.font.color.rgb = PRIMARY_BLUE
    
    p1_1 = tf1.add_paragraph()
    p1_1.space_before = Pt(12)
    r1_1 = p1_1.add_run()
    r1_1.text = "Сквозная система ИИ-агентов для стратегической аналитики"
    r1_1.font.size = Pt(26)
    r1_1.font.bold = True
    r1_1.font.color.rgb = WHITE
    
    p1_2 = tf1.add_paragraph()
    p1_2.space_before = Pt(8)
    r1_2 = p1_2.add_run()
    r1_2.text = "Практическая архитектура, мировые бенчмарки и наглядные кейсы реализации\n(Аналитик → Стратег → Презентатор)"
    r1_2.font.size = Pt(14)
    r1_2.font.color.rgb = RGBColor(190, 215, 240)

    p1_3 = tf1.add_paragraph()
    p1_3.space_before = Pt(18)
    r1_3 = p1_3.add_run()
    r1_3.text = "Разработчик: Лаврентий | Октябрь – Декабрь | Внешний R&D-контур с готовностью к On-Premise"
    r1_3.font.size = Pt(11)
    r1_3.font.color.rgb = WHITE

    # ==================== SLIDE 2: Проблематика и Целевое состояние ====================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Проблематика и бизнес-цели проекта")
    add_card(s2, Inches(0.8), Inches(1.5), Inches(4.0), Inches(3.6),
             "Вызовы традиционного процесса (As-Is)",
             ["• До 70% времени аналитика уходит на механическую рутину: сбор новостей, вычитка сотен страниц PDF-отчетов, ручной перенос в Excel.",
              "• Огромный информационный шум: сложно вовремя заметить критические рыночные шоки («черных лебедей»).",
              "• Коммуникационный разрыв: 100-страничная общая стратегия не воспринимается конкретными отделами (Логистика, ИТ, Бурение) — им нужны понятные адресные слайды."],
             border_color=ACCENT_ORANGE)
    add_card(s2, Inches(5.2), Inches(1.5), Inches(4.0), Inches(3.6),
             "Целевое состояние системы (To-Be)",
             ["• Автономный агентный мониторинг: круглосуточный парсинг открытых источников, дайджесты и сигналы раннего предупреждения.",
              "• Сценарное моделирование: ИИ-Стратег синтезирует стратегию и проверяет ее через модуль самокритики (Reflexion).",
              "• Адресная каскадная сборка: ИИ-Презентатор фильтрует инициативы под конкретный отдел и программно собирает презентации .pptx по брендбуку."],
             border_color=ACCENT_GREEN)

    # ==================== SLIDE 3: БЕНЧМАРК: McKinsey Lilli & BCG GeneAI (С КАРТИНКОЙ) ====================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Мировые бенчмарки: McKinsey Lilli & BCG GeneAI Slide Factory", "DEEP RESEARCH & МИРОВОЙ ОПЫТ")
    
    # Text on left
    add_card(s3, Inches(0.8), Inches(1.4), Inches(3.8), Inches(3.8),
             "Как это делают лидеры консалтинга",
             ["• McKinsey Lilli Platform:",
              "  - Агрегирует 100 000+ исследований и отчетов.",
              "  - Синтезирует аналитические мемо за 2 часа вместо 2 недель.",
              "  - Строгий трекинг первоисточников (100% citation tracking).",
              "\n• BCG GeneAI Slide Factory:",
              "  - Конвейер из агентов: Исследователь → Факт-чекер → Дизайнер верстки.",
              "  - Прямой экспорт в редактируемый PowerPoint (OpenXML/python-pptx).",
              "  - Без галлюцинаций и с сохранением корпоративных мастер-слайдов."],
             border_color=PRIMARY_BLUE)
    
    # Image on right
    img_bench = os.path.join(ASSETS_DIR, "consulting_benchmarks_real.png")
    if os.path.exists(img_bench):
        s3.shapes.add_picture(img_bench, Inches(4.8), Inches(1.4), width=Inches(4.6), height=Inches(3.8))

    # ==================== SLIDE 4: СКВОЗНАЯ АРХИТЕКТУРА 3-Х АГЕНТОВ (С КАРТИНКОЙ) ====================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Сквозная архитектура системы: 3 этапа и потоки данных", "АРХИТЕКТУРНЫЙ ДИЗАЙН СИСТЕМЫ")
    
    # Image top / center
    img_arch = os.path.join(ASSETS_DIR, "architecture_flow_ru.png")
    if os.path.exists(img_arch):
        s4.shapes.add_picture(img_arch, Inches(0.8), Inches(1.35), width=Inches(8.4), height=Inches(2.6))
        
    # Cards below
    add_card(s4, Inches(0.8), Inches(4.05), Inches(2.6), Inches(1.35),
             "1. Агент-Аналитик",
             ["• Сбор новостей и годовых PDF",
              "• Сигналы раннего предупреждения",
              "• Бенчмарк конкурентов (Pydantic)"],
             border_color=PRIMARY_BLUE)
    add_card(s4, Inches(3.7), Inches(4.05), Inches(2.6), Inches(1.35),
             "2. Агент-Стратег",
             ["• Синтез стратегии (SWOT/PESTEL)",
              "• Контур Reflexion (Критик рисков)",
              "• Дорожная карта инициатив"],
             border_color=PRIMARY_BLUE)
    add_card(s4, Inches(6.6), Inches(4.05), Inches(2.6), Inches(1.35),
             "3. Агент-Презентатор",
             ["• Профили отделов (YAML)",
              "• Смысловая адаптация целей",
              "• Сборка .pptx и мемо"],
             border_color=PRIMARY_BLUE)

    # ==================== SLIDE 5: ДАШБОРД АНАЛИТИКА / UI (С КАРТИНКОЙ) ====================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Интерфейс платформы: Дашборд аналитических справок и сигналов", "ПРАКТИЧЕСКИЙ КЕЙС / UI PROTOTYPE")
    
    img_ui = os.path.join(ASSETS_DIR, "ui_dashboard_ru.png")
    if os.path.exists(img_ui):
        s5.shapes.add_picture(img_ui, Inches(0.8), Inches(1.4), width=Inches(5.3), height=Inches(3.8))
        
    add_card(s5, Inches(6.3), Inches(1.4), Inches(2.9), Inches(3.8),
             "Что видит пользователь",
             ["1. Навигация по 3 агентам в левом сайдбаре.",
              "2. Сводка сырьевых рынков (Urals, СПГ, фрахт).",
              "3. Сигналы раннего предупреждения с грейдами критичности (High / Medium).",
              "4. Бенчмарки конкурентов (Роснефть, Лукойл, BP).",
              "5. Кнопка 'Generate Department Slide Deck' — моментальный экспорт презентации для нужного отдела."],
             border_color=PRIMARY_BLUE)

    # ==================== SLIDE 6: Агент 1 Детально (RAG + Early Warnings) ====================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Агент 1: Рыночный Аналитик — Advanced RAG и сигналы рисков", "ДЕТАЛИЗАЦИЯ: АГЕНТ 1")
    add_card(s6, Inches(0.8), Inches(1.5), Inches(4.0), Inches(3.6),
             "Инженерия данных и Advanced RAG",
             ["• Парсинг отчетов со сложной версткой: библиотека Docling (IBM) корректно извлекает таблицы финансовых показателей ТЭК в Markdown, исключая слипание колонок.",
              "• Гибридный поиск (Hybrid Search):",
              "  Score = α * VectorDense + (1-α) * BM25Sparse.",
              "  BM25 находит точные аббревиатуры (ГРП, УПН, СПГ), а Dense — семантические смыслы.",
              "• Re-ranking: кросс-энкодер bge-reranker отсекает 80% шума перед отправкой в LLM."],
             border_color=PRIMARY_BLUE)
    add_card(s6, Inches(5.2), Inches(1.5), Inches(4.0), Inches(3.6),
             "Продукты Агента 1",
             ["1. Ежемесячный отраслевой дайджест: макроэкономика, спрос, регуляторика.",
              "2. Аналитическая записка по теме: глубокий анализ конкретной технологии или рынка.",
              "3. Сигналы раннего предупреждения (Early Warning Signals): детекция санкционных запретов, дефицита танкеров или критических сбоев в поставках.",
              "4. Карта стратегий конкурентов: матрица сопоставления шагов лидеров отрасли."],
             border_color=PRIMARY_BLUE)

    # ==================== SLIDE 7: ОРКЕСТРАЦИЯ В LANGGRAPH STUDIO (С КАРТИНКОЙ) ====================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Оркестрация в коде: Граф состояний в LangGraph Studio", "ТЕХНИЧЕСКАЯ РЕАЛИЗАЦИЯ")
    
    img_lg = os.path.join(ASSETS_DIR, "langgraph_studio_ru.png")
    if os.path.exists(img_lg):
        s7.shapes.add_picture(img_lg, Inches(0.8), Inches(1.4), width=Inches(5.3), height=Inches(3.8))
        
    add_card(s7, Inches(6.3), Inches(1.4), Inches(2.9), Inches(3.8),
             "Почему именно LangGraph",
             ["• Детерминированный StateGraph: граф состояний четко контролирует переходы между узлами.",
              "• Цикл Reflexion (Критик): Агент-Стратег находится в петле обратной связи с нодой Critic до достижения оценки >= 8.0.",
              "• Строгий State Inspection: справа видна JSON-схема состояния на каждом шаге.",
              "• Checkpointing: возможность отката и ручной правки аналитиком (Human-in-the-Loop)."],
             border_color=PRIMARY_BLUE)

    # ==================== SLIDE 8: Агент 2 Детально (Стратег) ====================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Агент 2: Корпоративный Стратег — Синтез и модуль критики", "ДЕТАЛИЗАЦИЯ: АГЕНТ 2")
    add_card(s8, Inches(0.8), Inches(1.5), Inches(4.0), Inches(3.6),
             "Стратегические фреймворки",
             ["• Синтез рыночной фактуры: сопоставление данных Агента 1 с долгосрочными целями компании (горизонт 2026–2030 гг.).",
              "• Применение классических методологий:",
              "  - SWOT-анализ (силы/слабости vs возможности/угрозы).",
              "  - PESTEL-анализ макросреды.",
              "  - Матрица Ансоффа (диверсификация и новые рынки).",
              "• Формирование инициатив: декомпозиция на конкретные проекты с целевыми KPI."],
             border_color=PRIMARY_BLUE)
    add_card(s8, Inches(5.2), Inches(1.5), Inches(4.0), Inches(3.6),
             "Паттерн Reflexion (Generator-Critic)",
             ["• Нода-Генератор: формулирует драфт стратегической инициативы (например, 'Развитие собственного арктического флота').",
              "• Нода-Критик (Роль Риск-офицера):",
              "  - Проверяет санкционные риски верфей.",
              "  - Оценивает капиталоемкость (CAPEX).",
              "  - Ищет узкие места в сроках реализации.",
              "• Выход: валидированная программа стратегических инициатив без утопических идей."],
             border_color=PRIMARY_BLUE)

    # ==================== SLIDE 8.1: Нода Критики — 100-1000 критериев ====================
    s8_crit = prs.slides.add_slide(blank_layout)
    add_header(s8_crit, "Нода Критики: Откуда берутся веса и масштабирование до 1000 критериев", "МЕТОДОЛОГИЯ РИСК-СКОРИНГА")
    add_card(s8_crit, Inches(0.8), Inches(1.5), Inches(4.0), Inches(3.6),
             "Откуда берутся веса и правила в MVP?",
             ["• Установочная встреча с руководством ДСИиУР:",
              "  Вопрос: «По каким причинам вы бракуете стратегические инициативы?»",
              "• 4 ключевых фактора нефтегазового сектора:",
              "  1. Санкции и импортозамещение (вес 30%)",
              "  2. Срок окупаемости и CAPEX (вес 30%)",
              "  3. Технологическая зрелость TRL >= 7 (вес 20%)",
              "  4. Регуляторные риски и ESG (вес 20%)",
              "• Формула: Total = Σ (Вес_i × Оценка_i)",
              "• Порог прохода: при Score < 8.0 инициатива идет на второй круг доработки."],
             border_color=PRIMARY_BLUE)
    add_card(s8_crit, Inches(5.2), Inches(1.5), Inches(4.0), Inches(3.6),
             "Что делать, если критериев 100 или 1000?",
             ["• Ошибка 'в лоб': подача 1000 пунктов в 1 промпт ломает внимание LLM (Lost in the Middle).",
              "• Архитектурное решение — Иерархический Map-Reduce:",
              "  1. Группировка в 4 макро-блока (Финансы, Санкции/Импорт, Производство/Флот, ESG/Право).",
              "  2. Параллельные под-ноды: 4 специализированных критика проверяют только свой блок чеклиста.",
              "  3. Жесткие стоп-факторы (Red Flags): при прямом запрете санкций — немедленный отсев (Score 0) без траты токенов!",
              "  4. Взвешенная сумма баллов блоков детерминированной математической функцией в коде."],
             border_color=ACCENT_ORANGE)

    # ==================== SLIDE 9: Агент 3 и ПРИМЕР СЛАЙДА ДЛЯ ОТДЕЛА (С КАРТИНКОЙ) ====================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Агент 3: Сборка презентаций — Реальный пример слайда для отдела", "ПРАКТИЧЕСКИЙ РЕЗУЛЬТАТ: АГЕНТ 3")
    
    img_dept = os.path.join(ASSETS_DIR, "department_slide_ru.png")
    if os.path.exists(img_dept):
        s9.shapes.add_picture(img_dept, Inches(0.8), Inches(1.4), width=Inches(5.3), height=Inches(3.8))
        
    add_card(s9, Inches(6.3), Inches(1.4), Inches(2.9), Inches(3.8),
             "Как это работает на практике",
             ["• Каскадирование цели STRAT-04: общая корпоративная стратегия переведена на язык Департамента логистики.",
              "• Метрики и KPI отдела: снижение ставки фрахта на -12%, рост утилизации танкеров Arc7 на +18%, бункеровка СПГ.",
              "• Пирамида Минто: ясный вывод в заголовке, фактура и карта маршрутов Севморпути.",
              "• Полная автоматизация: слайд собран скриптом python-pptx по корпоративному мастер-шаблону."],
             border_color=PRIMARY_BLUE)

    # ==================== SLIDE 10: Архитектурные контракты (Pydantic) ====================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Связка компонентов: Типобезопасные контракты Pydantic", "ИНЖЕНЕРНЫЕ КОНТРАКТЫ ДАННЫХ")
    add_card(s10, Inches(0.8), Inches(1.5), Inches(4.0), Inches(3.6),
             "Почему это критично?",
             ["• Главная ошибка агентных систем — передача сырого текста между агентами. Это приводит к разрыву логики и галлюцинациям.",
              "• Все 3 агента связаны строгими Pydantic v2 схемами:",
              "  - AnalystOutput (справка, дайджест, сигналы, бенчмарки).",
              "  - StrategistOutput (инициативы, SWOT, риски, сроки).",
              "  - DepartmentReport (слайды, мемо, целевые KPI).",
              "• Библиотека Instructor гарантирует 100% валидность JSON от LLM."],
             border_color=PRIMARY_BLUE)
    add_card(s10, Inches(5.2), Inches(1.5), Inches(4.0), Inches(3.6),
             "Пример структуры Pydantic-контракта",
             ["class EarlyWarningSignal(BaseModel):",
              "    title: str = Field(description='Суть сигнала')",
              "    severity: Literal['High', 'Medium', 'Low']",
              "    impact_area: str = Field('Логистика / Бурение')",
              "    evidence: str = Field('Цитата из источника')",
              "\nclass StrategicInitiative(BaseModel):",
              "    id: str = Field('STRAT-01')",
              "    target_depts: List[str]",
              "    kpis: Dict[str, str]",
              "    mitigation_plan: str"],
             border_color=PRIMARY_BLUE)

    # ==================== SLIDE 10.1: Человекочитаемые форматы (Не только JSON) ====================
    s10_human = prs.slides.add_slide(blank_layout)
    add_header(s10_human, "Человекочитаемые форматы на выходе: Готовые файлы для аналитиков", "АВТОНОМНОСТЬ И АРТЕФАКТЫ")
    add_card(s10_human, Inches(0.8), Inches(1.5), Inches(4.0), Inches(3.6),
             "Офисные форматы для человека",
             ["• Аналитики не работают с сырым кодом JSON!",
              "• Каждый агент параллельно генерирует документы:",
              "  1. Агент 1 (Аналитик):",
              "     - analyst_digest.docx (сводный отчет с таблицами)",
              "     - market_memo.html (веб-справка с первоисточниками)",
              "     - early_warnings.xlsx (таблица сигналов для Excel)",
              "  2. Агент 2 (Стратег):",
              "     - strategy_memo.docx (полное инвест-ТЭО / паспорт)",
              "     - swot_matrix.html (интерактивная матрица)",
              "  3. Агент 3 (Презентатор):",
              "     - strategy_presentation.pptx (готовые слайды)",
              "     - executive_briefing.pdf (версия для печати)."],
             border_color=PRIMARY_BLUE)
    add_card(s10_human, Inches(5.2), Inches(1.5), Inches(4.0), Inches(3.6),
             "Автономный режим работы (Standalone)",
             ["• Нет жесткой привязки к полному циклу пайплайна:",
              "• Аналитик может запускать любого агента отдельно:",
              "  - Утренний мониторинг рынка? Запуск только Агента 1 → готовый Word за 40 секунд.",
              "  - Проверка собственного отчета? Загрузка файла в Агента 2 → оценка рисков и замечания Критика.",
              "  - Сборка слайдов под другой отдел? Запуск Агента 3 с указанием другого профиля YAML.",
              "• Полная свобода действий сотрудника ДСИиУР."],
             border_color=ACCENT_GREEN)

    # ==================== SLIDE 10.2: Консольное рабочее место аналитика (CLI) ====================
    s10_cli = prs.slides.add_slide(blank_layout)
    add_header(s10_cli, "Рабочее место аналитика: Команды запуска в Windows CLI", "КОНСОЛЬ И УПРАВЛЕНИЕ")
    add_card(s10_cli, Inches(0.8), Inches(1.5), Inches(4.0), Inches(3.6),
             "Команды в C:\\Users\\Lavrentiy\\Desktop\\газпром>",
             ["• Активация среды: .\\venv\\Scripts\\activate",
              "• Запуск полного цикла (все 3 агента):",
              "  python run_pipeline.py --topic 'Арктическая логистика'",
              "• Автономный запуск мониторинга (Агент 1):",
              "  python run_agent1_analyst.py --query 'Цены СПГ' --export docx",
              "• Оценка своего отчета (Агент 2):",
              "  python run_agent2_strategist.py --input-file custom.pdf",
              "• Сборка презентации (Агент 3):",
              "  python run_agent3_presenter.py --department logistics"],
             border_color=PRIMARY_BLUE)
    add_card(s10_cli, Inches(5.2), Inches(1.5), Inches(4.0), Inches(3.6),
             "Каталог готовых результатов: папка output/",
             ["• Все сгенерированные файлы сохраняются локально:",
              "  C:\\Users\\Lavrentiy\\Desktop\\газпром\\output\\",
              "  ├── analyst_digest.docx",
              "  ├── market_memo.html",
              "  ├── early_warnings.xlsx",
              "  ├── strategy_memo.docx",
              "  └── strategy_presentation.pptx",
              "• Открытие в 1 клик или командой из консоли:",
              "  start output\\strategy_presentation.pptx",
              "  start output\\analyst_digest.docx"],
             border_color=PRIMARY_BLUE)

    # ==================== SLIDE 11: Технологический стек платформы ====================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Технологический стек платформы и роль каждого компонента", "ТЕХНОЛОГИЧЕСКИЙ СТЕК")
    add_card(s11, Inches(0.8), Inches(1.5), Inches(2.7), Inches(3.6),
             "Оркестрация и Логика",
             ["• LangGraph: циклический граф состояний, память сессии, Human-in-the-Loop.",
              "• Pydantic v2 + Instructor: типобезопасные контракты и валидация JSON.",
              "• LiteLLM: универсальный шлюз к 100+ LLM."],
             border_color=PRIMARY_BLUE)
    add_card(s11, Inches(3.65), Inches(1.5), Inches(2.7), Inches(3.6),
             "Данные и Поиск",
             ["• Docling (IBM): парсинг сложных PDF с сохранением таблиц в Markdown.",
              "• Tavily API: специализированный веб-поиск для RAG без рекламы.",
              "• Qdrant / ChromaDB: векторное хранилище в локальном Docker."],
             border_color=PRIMARY_BLUE)
    add_card(s11, Inches(6.5), Inches(1.5), Inches(2.7), Inches(3.6),
             "Генерация и Интерфейс",
             ["• python-pptx: векторная программная сборка презентаций.",
              "• Marp: рендеринг Markdown в слайды.",
              "• Streamlit / Chainlit: интерактивный веб-дашборд для руководства."],
             border_color=PRIMARY_BLUE)

    # ==================== SLIDE 12: Безопасность и On-Premise ====================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Безопасность и архитектурный мост в On-Premise контур", "БЕЗОПАСНОСТЬ И ВНЕДРЕНИЕ")
    add_card(s12, Inches(0.8), Inches(1.5), Inches(4.0), Inches(3.6),
             "Фаза 1: Внешний контур (PoC Сентябрь-Декабрь)",
             ["• 100% открытые и синтетические данные: в облачные API передаются только публичные новости и смоделированные кейсы.",
              "• Нулевой риск для коммерческой тайны компании.",
              "• Максимальная скорость разработки: запуск без многомесячных согласований со службой безопасности."],
             border_color=ACCENT_GREEN)
    add_card(s12, Inches(5.2), Inches(1.5), Inches(4.0), Inches(3.6),
             "Фаза 2: Перенос во внутренний контур (On-Prem)",
             ["• Model-Agnostic архитектура: код не привязан к облачным сервисам.",
              "• Локальные модели на GPU серверах компании: развертывание Qwen 2.5 (32B/72B) или DeepSeek-V3 через vLLM / TGI.",
              "• Смена одной строки в .env: система переключается на внутренний URL без переписывания логики агентов."],
             border_color=NAVY_BLUE)

    # ==================== SLIDE 13: Метрики и Контроль качества ====================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Фреймворк метрик качества и контроль галлюцинаций", "ОЦЕНКА И ТЕСТИРОВАНИЕ")
    add_card(s13, Inches(0.8), Inches(1.5), Inches(4.0), Inches(3.6),
             "Метрики RAG (Ragas Framework)",
             ["• Faithfulness (> 0.95): процент фактов в справке, строго подтвержденных цитатами из первоисточников.",
              "• Answer Relevancy (> 0.90): семантическое соответствие справки поставленному бизнес-вопросу.",
              "• Context Precision (> 0.85): отсутствие информационного шума в найденных фрагментах отчетов."],
             border_color=PRIMARY_BLUE)
    add_card(s13, Inches(5.2), Inches(1.5), Inches(4.0), Inches(3.6),
             "Бизнес-метрики стратегии",
             ["• Actionability Score: конкретность шагов (наличие подразделения, сроков, целевых метрик).",
              "• Adoption Rate: доля тезисов презентации, оставленных экспертом-аналитиком без ручных правок.",
              "• Пирамида тестов: Unit-тесты контрактов → Интеграция графа в LangGraph → LLM-as-a-judge."],
             border_color=PRIMARY_BLUE)

    # ==================== SLIDE 14: Дорожная карта (Сентябрь – Декабрь) ====================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Дорожная карта реализации проекта (Сентябрь – Декабрь)", "ПЛАН РЕАЛИЗАЦИИ")
    add_card(s14, Inches(0.6), Inches(1.5), Inches(2.0), Inches(3.6),
             "Сентябрь",
             ["• Агент 1: Аналитик",
              "• Парсинг PDF (Docling)",
              "• Гибридный RAG + Поиск",
              "• Детектор Early Warnings",
              "• Тесты на открытых данных"],
             border_color=PRIMARY_BLUE)
    add_card(s14, Inches(2.9), Inches(1.5), Inches(2.0), Inches(3.6),
             "Октябрь",
             ["• Агент 2: Стратег",
              "• Контур Reflexion (Критик)",
              "• Промпты SWOT/PESTEL",
              "• Генератор инициатив",
              "• Верификация рисков"],
             border_color=PRIMARY_BLUE)
    add_card(s14, Inches(5.2), Inches(1.5), Inches(2.0), Inches(3.6),
             "Ноябрь",
             ["• Агент 3: Презентатор",
              "• Библиотека профилей отделов",
              "• Модуль python-pptx",
              "• Наполнение шаблонов",
              "• Тесты каскадирования"],
             border_color=PRIMARY_BLUE)
    add_card(s14, Inches(7.5), Inches(1.5), Inches(2.0), Inches(3.6),
             "Декабрь",
             ["• Финал и Демо",
              "• Streamlit UI дашборд",
              "• Методология для ДО",
              "• Подготовка к On-Prem",
              "• Защита перед C-level"],
             border_color=ACCENT_GREEN)

    # ==================== SLIDE 15: Чек-лист для старта ====================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Чек-лист вводных данных для старта проекта", "РЕСУРСЫ И СТАРТ")
    add_card(s15, Inches(0.8), Inches(1.5), Inches(8.4), Inches(3.6),
             "Что необходимо запросить у команды ДСИиУР на первой установочной встрече:",
             ["1. 2–3 эталонных исторических аналитических отчета ДСИиУР («золотой стандарт» структуры, глубины и корпоративного стиля).",
              "2. Официальный корпоративный .pptx шаблон с мастер-слайдами, цветовой палитрой и шрифтами «Газпром нефти».",
              "3. Список 2–3 пилотных подразделений (например: блок Логистики, блок Бурения, блок ИТ) для первичного тестирования Агента 3.",
              "4. Перечень приоритетных открытых отраслевых источников (сайты министерств, агентства Cbonds, Интерфакс-ТЭК, Neftegaz.ru).",
              "5. Лимиты на API-ключи (Claude 3.5 Sonnet, GPT-4o, Tavily) или тестовая виртуальная машина для стенда разработки."],
             border_color=PRIMARY_BLUE)

    # ==================== SLIDE 15.1: Доработка и масштабирование (Roadmap 2026+) ====================
    s15_scale = prs.slides.add_slide(blank_layout)
    add_header(s15_scale, "План доработки и масштабирования каждого агента (Roadmap 2026+)", "РАЗВИТИЕ СИСТЕМЫ ПОСЛЕ ДЕКАБРЯ")
    add_card(s15_scale, Inches(0.6), Inches(1.5), Inches(2.8), Inches(3.6),
             "Агент 1: Аналитик 2026+",
             ["• 24/7 CRON-демон: непрерывный фоновый мониторинг рынков и авто-апдейт Qdrant.",
              "• Платные отраслевые базы: подключение терминалов Argus Media, S&P Platts, Cbonds, таможни ФТС.",
              "• Моментальные PUSH-алерты: отправка High-severity сигналов в корпоративный мессенджер.",
              "• Time-Series прогнозирование: ML-модели (Chronos/Prophet) для коридоров цен и ставок фрахта."],
             border_color=PRIMARY_BLUE)
    add_card(s15_scale, Inches(3.6), Inches(1.5), Inches(2.8), Inches(3.6),
             "Агент 2: Стратег 2026+",
             ["• 'Виртуальный совет директоров': консилиум агентов (CFO, Главный инженер, Юрист) спорит по методологии Дельфи.",
              "• Расчет финмодели: вызов Python-калькулятора DCF (авторасчет NPV, IRR, окупаемости, стресс-тесты).",
              "• Семантический аудит портфеля: проверка на дублирование с существующими инвестпроектами компании.",
              "• Многосценарное моделирование: прогноз эффектов при колебаниях курса валют и ставок ЦБ."],
             border_color=PRIMARY_BLUE)
    add_card(s15_scale, Inches(6.6), Inches(1.5), Inches(2.8), Inches(3.6),
             "Агент 3: Презентатор 2026+",
             ["• Интерактивные BI-порталы: генерация веб-дашбордов с возможностью провала в первоисточник (Drill-down).",
              "• Векторная авто-инфографика: программная отрисовка карт Севморпути, диаграмм Ганта и waterfall-графиков.",
              "• Масштабирование на 50+ ДО: единый каталог YAML-профилей для НПЗ, сбытовых и добывающих обществ.",
              "• Human-in-the-Loop DSPy: автоматическая донастройка промптов на истории оценок руководства."],
             border_color=ACCENT_GREEN)

    # ==================== SLIDE 16: Русскоязычные видеоматериалы ====================
    s16_v = prs.slides.add_slide(blank_layout)
    add_header(s16_v, "База знаний: Русскоязычные видеокурсы и лекции (YouTube)", "ОБУЧЕНИЕ И БАЗА ЗНАНИЙ")
    add_card(s16_v, Inches(0.8), Inches(1.5), Inches(4.0), Inches(1.7),
             "Мультиагенты и LangGraph на русском",
             ["• ODS / Data Fest: «Мультиагентные системы на базе LLM: от концепции до кода».",
              "• Практикум: создание детерминированных графов состояний на Python с циклами Reflexion."],
             border_color=PRIMARY_BLUE)
    add_card(s16_v, Inches(5.2), Inches(1.5), Inches(4.0), Inches(1.7),
             "Advanced RAG и поиск на русском",
             ["• Karpov.Courses: «Как устроен RAG: от наивного поиска до Production».",
              "• HighLoad++: гибридный поиск BM25 + Dense, слияние RRF и кросс-энкодеры bge-reranker."],
             border_color=PRIMARY_BLUE)
    add_card(s16_v, Inches(0.8), Inches(3.35), Inches(4.0), Inches(1.75),
             "Опыт Сбера и закрытый контур",
             ["• Sber AI / GigaChain: доклады по оркестрации агентов внутри защищенного корпоративного периметра.",
              "• HighLoad DevOps: поднятие vLLM серверов на локальных GPU."],
             border_color=PRIMARY_BLUE)
    add_card(s16_v, Inches(5.2), Inches(3.35), Inches(4.0), Inches(1.75),
             "Оценка качества и генерация слайдов",
             ["• Метрики Ragas и DeepEval: тестирование точности RAG и отсутствие галлюцинаций.",
              "• Автоматизация python-pptx: программная сборка презентаций по мастер-шаблону."],
             border_color=PRIMARY_BLUE)

    # ==================== SLIDE 17: Финал ====================
    s16 = prs.slides.add_slide(blank_layout)
    bg16 = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(10), Inches(5.625))
    bg16.fill.solid()
    bg16.fill.fore_color.rgb = NAVY_BLUE
    bg16.line.fill.background()

    tb16 = s16.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(8.0), Inches(2.6))
    tf16 = tb16.text_frame
    tf16.word_wrap = True
    
    p16_0 = tf16.paragraphs[0]
    r16_0 = p16_0.add_run()
    r16_0.text = "ГОТОВНОСТЬ К РЕАЛИЗАЦИИ И СТАРТУ"
    r16_0.font.size = Pt(12)
    r16_0.font.bold = True
    r16_0.font.color.rgb = PRIMARY_BLUE
    
    p16_1 = tf16.add_paragraph()
    p16_1.space_before = Pt(10)
    r16_1 = p16_1.add_run()
    r16_1.text = "Спасибо за внимание! Готов к запуску проекта."
    r16_1.font.size = Pt(26)
    r16_1.font.bold = True
    r16_1.font.color.rgb = WHITE
    
    p16_2 = tf16.add_paragraph()
    p16_2.space_before = Pt(14)
    r16_2 = p16_2.add_run()
    r16_2.text = "Кандидат / Разработчик: Лаврентий\nКонтакты: Telegram | Телефон | Репозиторий проекта"
    r16_2.font.size = Pt(13)
    r16_2.font.color.rgb = RGBColor(190, 215, 240)

    out_path = os.path.abspath("c:/Users/Lavrentiy/Desktop/газпром/Презентация_ИИ_Агенты_ГазпромНефть.pptx")
    prs.save(out_path)
    print(f"Rich presentation saved to: {out_path}")

if __name__ == "__main__":
    create_rich_presentation()

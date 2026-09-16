# -*- coding: utf-8 -*-
"""
Генератор презентации стратегического консалтингового уровня (McKinsey / BCG style)
для проекта внедрения сквозных ИИ-агентов в ДСИиУР ПАО «Газпром нефть».
Widescreen 16:9 (13.333" x 7.5"), строгая иерархия, высокая читаемость.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Corporate Color Palette (Газпром нефть + Top Tier Strategy Consulting)
NAVY = RGBColor(0, 45, 90)           # #002D5A - Главный темно-синий
GAZPROM_BLUE = RGBColor(0, 121, 194) # #0079C2 - Фирменный синий
DARK_TEXT = RGBColor(30, 41, 59)     # #1E293B - Высококонтрастный текст
SLATE_MUTED = RGBColor(100, 116, 139)# #64748B - Подзаголовки и трекеры
BG_LIGHT = RGBColor(248, 250, 252)   # #F8FAFC - Фоновый цвет слайдов
WHITE = RGBColor(255, 255, 255)      # #FFFFFF - Карточки
BORDER_SLATE = RGBColor(203, 213, 225)# #CBD5E1 - Тонкие границы карточек
EMERALD = RGBColor(16, 149, 106)     # #10956A - Акцент успеха / экономии
AMBER = RGBColor(217, 119, 6)        # #D97706 - Акцент предупреждений

ASSETS_DIR = os.path.abspath("c:/Users/Lavrentiy/Desktop/газпром/assets")
OUTPUT_PPTX = os.path.abspath("c:/Users/Lavrentiy/Desktop/газпром/Презентация_ИИ_Агенты_ГазпромНефть.pptx")

def apply_background(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_LIGHT
    bg.line.fill.background()
    return bg

def add_header(slide, action_title, tracker="ДСИиУР ПАО «ГАЗПРОМ НЕФТЬ» | АРХИТЕКТУРА ИИ-АГЕНТОВ", takeaway=None):
    """
    McKinsey/BCG standard header block:
    1. Tracker / Category (10pt, uppercase bold, Gazprom Blue)
    2. Action Headline (18-20pt, bold Navy, full sentence with takeaway)
    3. Optional Executive Subtitle (11pt, slate muted)
    """
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.0))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_track = tf.paragraphs[0]
    r_track = p_track.add_run()
    r_track.text = tracker.upper()
    r_track.font.size = Pt(9.5)
    r_track.font.bold = True
    r_track.font.color.rgb = GAZPROM_BLUE

    p_title = tf.add_paragraph()
    p_title.space_before = Pt(3)
    r_title = p_title.add_run()
    r_title.text = action_title
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY

    if takeaway:
        p_sub = tf.add_paragraph()
        p_sub.space_before = Pt(2)
        r_sub = p_sub.add_run()
        r_sub.text = takeaway
        r_sub.font.size = Pt(11)
        r_sub.font.color.rgb = SLATE_MUTED

def add_card(slide, left, top, width, height, title, bullet_items, accent_color=GAZPROM_BLUE):
    """
    Consulting container:
    - Pure white card with thin subtle slate border
    - Accent colored bar on top (4pt)
    - Bold lead-ins for each bullet point
    """
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = BORDER_SLATE
    card.line.width = Pt(1)

    # Accent top bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent_color
    bar.line.fill.background()

    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.20)
    tf.margin_bottom = Inches(0.15)

    p_t = tf.paragraphs[0]
    r_t = p_t.add_run()
    r_t.text = title
    r_t.font.bold = True
    r_t.font.size = Pt(13)
    r_t.font.color.rgb = NAVY

    for item in bullet_items:
        p = tf.add_paragraph()
        p.space_before = Pt(6)
        if isinstance(item, tuple):
            lead, body = item
            r_lead = p.add_run()
            r_lead.text = lead + " "
            r_lead.font.bold = True
            r_lead.font.size = Pt(10.5)
            r_lead.font.color.rgb = DARK_TEXT

            r_body = p.add_run()
            r_body.text = body
            r_body.font.size = Pt(10.5)
            r_body.font.color.rgb = DARK_TEXT
        else:
            r = p.add_run()
            r.text = item
            r.font.size = Pt(10.5)
            r.font.color.rgb = DARK_TEXT

def add_kpi_card(slide, left, top, width, height, number_text, label_text, subtext=None, color=GAZPROM_BLUE):
    """Big metric callout card for executive dashboards"""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = BORDER_SLATE
    card.line.width = Pt(1)

    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.12)
    tf.margin_bottom = Inches(0.1)

    p_num = tf.paragraphs[0]
    p_num.alignment = PP_ALIGN.CENTER
    r_num = p_num.add_run()
    r_num.text = number_text
    r_num.font.bold = True
    r_num.font.size = Pt(32)
    r_num.font.color.rgb = color

    p_lbl = tf.add_paragraph()
    p_lbl.alignment = PP_ALIGN.CENTER
    p_lbl.space_before = Pt(2)
    r_lbl = p_lbl.add_run()
    r_lbl.text = label_text
    r_lbl.font.bold = True
    r_lbl.font.size = Pt(10)
    r_lbl.font.color.rgb = NAVY

    if subtext:
        p_sub = tf.add_paragraph()
        p_sub.alignment = PP_ALIGN.CENTER
        p_sub.space_before = Pt(1)
        r_sub = p_sub.add_run()
        r_sub.text = subtext
        r_sub.font.size = Pt(8.5)
        r_sub.font.color.rgb = SLATE_MUTED

def add_image_slide(slide, image_filename, card_title, bullet_items, takeaway_subtitle=None):
    """Standard split-screen slide: large high-res diagram on left, structured commentary on right"""
    img_path = os.path.join(ASSETS_DIR, image_filename)
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(0.8), Inches(1.6), width=Inches(6.8), height=Inches(5.3))
    
    add_card(slide, Inches(7.8), Inches(1.6), Inches(4.733), Inches(5.3), card_title, bullet_items, accent_color=GAZPROM_BLUE)

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==================== SLIDE 1: Title Slide (Executive Dark Navy) ====================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    # Blue top accent line
    bar1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = GAZPROM_BLUE
    bar1.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(10.9), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    r0 = p0.add_run()
    r0.text = "ДЕПАРТАМЕНТ ПО СТРАТЕГИИ, ИННОВАЦИЯМ И УСТОЙЧИВОМУ РАЗВИТИЮ (ДСИиУР)"
    r0.font.bold = True
    r0.font.size = Pt(12)
    r0.font.color.rgb = GAZPROM_BLUE

    p1 = tf1.add_paragraph()
    p1.space_before = Pt(14)
    r1 = p1.add_run()
    r1.text = "Сквозная система мультиагентного ИИ\nдля стратегической аналитики и планирования"
    r1.font.bold = True
    r1.font.size = Pt(32)
    r1.font.color.rgb = WHITE

    p2 = tf1.add_paragraph()
    p2.space_before = Pt(16)
    r2 = p2.add_run()
    r2.text = "Архитектурный проект, стек технологий, методология внедрения и план перехода в On-Premise"
    r2.font.size = Pt(15)
    r2.font.color.rgb = RGBColor(200, 220, 240)

    p3 = tf1.add_paragraph()
    p3.space_before = Pt(28)
    r3 = p3.add_run()
    r3.text = "Кандидат / Ведущий разработчик: Лаврентий  |  Горизонт PoC: Сентябрь – Декабрь  |  Локация: СПб, Почтамтская, 3-5"
    r3.font.size = Pt(11.5)
    r3.font.color.rgb = RGBColor(160, 190, 220)

    # ==================== SLIDE 2: Executive Summary ====================
    s2 = prs.slides.add_slide(blank_layout)
    apply_background(s2)
    add_header(s2, 
               "Executive Summary: Автоматизация аналитики и устранение разрыва со стратегией отделов",
               "ПРОБЛЕМАТИКА И ЦЕЛЕВЫЕ ЭФФЕКТЫ",
               "Система переводит рутинную подготовку стратегических материалов на конвейер автономных ИИ-агентов")

    add_kpi_card(s2, Inches(0.8), Inches(1.6), Inches(3.6), Inches(1.3), "70%", "Сокращение рутины", "Высвобождение времени аналитиков", color=GAZPROM_BLUE)
    add_kpi_card(s2, Inches(4.8), Inches(1.6), Inches(3.6), Inches(1.3), "< 2 часов", "Скорость драфта инициативы", "Вместо 2 недель ручной компиляции", color=EMERALD)
    add_kpi_card(s2, Inches(8.8), Inches(1.6), Inches(3.733), Inches(1.3), "3 агента", "Сквозная цепочка ценности", "Аналитик -> Стратег -> Презентатор", color=GAZPROM_BLUE)

    add_card(s2, Inches(0.8), Inches(3.1), Inches(5.6), Inches(3.8),
             "Текущие вызовы процесса аналитики в ДСИиУР",
             [("• Высокая трудоемкость мониторинга:", "До 70% рабочего времени уходит на сбор новостей, ручной парсинг сотен страниц отчетов и перенос таблиц."),
              ("• Риск пропуска критических сигналов:", "Скрытые санкционные ограничения на верфи или дефицит судов часто выявляются с запозданием."),
              ("• Разрыв коммуникации (Communication Gap):", "Профильные подразделения (Бурение, Логистика, ИТ) не имеют времени читать 100-страничные стратегии."),
              ("• Ручная верстка слайдов:", "Аналитики тратят часы на механическое форматирование презентаций в PowerPoint.")],
             accent_color=AMBER)

    add_card(s2, Inches(6.8), Inches(3.1), Inches(5.733), Inches(3.8),
             "Целевое решение: Сквозная мультиагентная фабрика",
             [("• Агент 1 (Аналитик):", "Непрерывный сбор открытых данных, детектор сигналов раннего предупреждения и бесплатный веб-поиск."),
              ("• Агент 2 (Стратег):", "Сценарный синтез инициатив (SWOT/PESTEL) и нода критики Reflexion с отсевом нереалистичных гипотез."),
              ("• Агент 3 (Презентатор):", "Каскадирование общекорпоративной цели на профиль подразделения и автоматическая сборка .pptx."),
              ("• Полная автономность:", "Каждый агент генерирует готовые файлы Word, HTML и PPTX для моментального использования сотрудниками.")],
             accent_color=EMERALD)

    # ==================== SLIDE 3: Мировые бенчмарки (McKinsey & BCG) ====================
    s3 = prs.slides.add_slide(blank_layout)
    apply_background(s3)
    add_header(s3,
               "Мировые бенчмарки: Архитектура объединяет практику McKinsey Lilli и BCG GeneAI",
               "DEEP RESEARCH & МИРОВОЙ ОПЫТ",
               "Опыт лидеров стратегического консалтинга доказывает эффективность агентных конвейеров над единичными чат-ботами")
    add_image_slide(s3, "consulting_benchmarks_real.png",
                    "Ключевые бенчмарки и выводы для проекта Газпром нефти",
                    [("• McKinsey & Company (Lilli):", "Внутренняя платформа аккумулирует 100 000+ исследований. Агенты выдают синтезированное мемо со ссылками на первоисточники за 2 часа вместо 2 недель."),
                     ("• Boston Consulting Group (BCG GeneAI):", "Паттерн 'Фабрика слайдов' — отказ от диффузионных картинок в пользу строгой векторной OpenXML сборки презентаций."),
                     ("• Нефтегазовый сектор (Saudi Aramco, Shell):", "Модели Aramco Metis ведут непрерывный мониторинг рынков сырья и танкерного флота, предупреждая о санкциях."),
                     ("• Наша адаптация для ДСИиУР:", "Объединяем McKinsey Lilli (RAG-синтез аналитики) и BCG (векторный python-pptx), исключая платные сервисы за счет бесплатного duckduckgo-search.")])

    # ==================== SLIDE 4: Сквозная архитектура ====================
    s4 = prs.slides.add_slide(blank_layout)
    apply_background(s4)
    add_header(s4,
               "Сквозная архитектура системы: 3 специализированных агента и потоки данных",
               "АРХИТЕКТУРНЫЙ ДИЗАЙН СИСТЕМЫ",
               "Детерминированный конвейер передачи типизированных состояний от открытых данных до адресных презентаций")
    add_image_slide(s4, "architecture_flow_ru.png",
                    "Сквозная логика передачи данных между агентами",
                    [("• Этап 1 (Аналитик):", "Парсит отраслевые PDF через Docling и осуществляет бесплатный веб-поиск. Формирует контракт AnalystOutput."),
                     ("• Этап 2 (Стратег):", "Принимает аналитику, синтезирует инициативы и прогоняет их через цикл критики (Reflexion) до балла >= 8.0."),
                     ("• Этап 3 (Презентатор):", "Считывает профиль департамента (YAML) и собирает презентацию в корпоративном мастер-шаблоне python-pptx."),
                     ("• Двойной вывод:", "На каждом шаге формируется строгий JSON для системы и готовые документы Word/PPTX для аналитика.")])

    # ==================== SLIDE 5: Интерфейс аналитика ====================
    s5 = prs.slides.add_slide(blank_layout)
    apply_background(s5)
    add_header(s5,
               "Рабочее пространство аналитика: Прототип интерактивного дашборда ДСИиУР",
               "ПРАКТИЧЕСКИЙ КЕЙС / UI PROTOTYPE",
               "Единый центр мониторинга рыночных котировок, сигналов раннего предупреждения и генерации материалов")
    add_image_slide(s5, "ui_dashboard_ru.png",
                    "Функциональные возможности интерфейса Streamlit",
                    [("• Котировки и котировочные коридоры:", "Визуализация динамики Urals, Brent, фрахта танкеров Arc7 и природного газа в реальном времени."),
                     ("• Реестр Early Warning Signals:", "Автоматическая классификация угроз по степени риска (High/Medium/Low) с доказательной базой."),
                     ("• Конструктор инициатив:", "Возможность загрузить собственный PDF-отчет для изолированной сессионной оценки Стратегом."),
                     ("• Экспорт артефактов в 1 клик:", "Скачивание сводного дайджеста Word, интерактивного HTML-мемо и готовых слайдов PowerPoint.")])

    # ==================== SLIDE 6: Агент 1 Детально ====================
    s6 = prs.slides.add_slide(blank_layout)
    apply_background(s6)
    add_header(s6,
               "Агент 1: Рыночный Аналитик — Advanced RAG, сигналы рисков и бесплатный поиск",
               "ДЕТАЛИЗАЦИЯ: АГЕНТ 1",
               "Автономный сбор фактуры без использования дорогостоящих платных API поиска")

    add_card(s6, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.3),
             "1. Сбор данных и бесплатный поиск",
             [("• Бесплатный поиск duckduckgo-search:", "Используется открытая библиотека Python. 0 рублей затрат, без регистрации, кредитных карт и API-ключей."),
              ("• Парсинг сложных PDF через Docling:", "Интеллектуальное извлечение многоколоночных таблиц и графиков из годовых отчетов ТЭК в Markdown."),
              ("• Векторная база Qdrant в Docker:", "Локальное хранение семантических чанков с возможностью мгновенного переноса в закрытый контур компании."),
              ("• Гибридный поиск (Hybrid RAG):", "Объединение BM25 и векторного поиска гарантирует точное нахождение названий верфей и цифр.")],
             accent_color=GAZPROM_BLUE)

    add_card(s6, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.3),
             "2. Детектор сигналов раннего предупреждения",
             [("• Выявление скрытых угроз:", "Агент детектирует ранние признаки санкций, срыва сроков верфей или логистических заторов."),
              ("• Классификация критичности:", "Присвоение статусов Severity: High, Medium, Low."),
              ("• Доказательная база (Evidence):", "Каждый сигнал содержит точную прямую цитату из первоисточника с указанием даты и автора."),
              ("• Рекомендации к действию:", "Формулирование превентивных мер (например: 'Провести ревизию доступного ледового флота').")],
             accent_color=AMBER)

    add_card(s6, Inches(8.8), Inches(1.6), Inches(3.733), Inches(5.3),
             "3. Выходной машинный контракт",
             [("• Строгая валидация Pydantic v2:", "Гарантия 100% отсутствия синтаксических ошибок в структуре ответа."),
              ("• Структура контракта AnalystOutput:",
               "  - industry_digest (сводный обзор)\n"
               "  - analytical_memo (детальная справка)\n"
               "  - warning_signals (список сигналов)\n"
               "  - competitor_benchmarks (проекты)"),
              ("• Человекочитаемые артефакты:", "Параллельно создаются analyst_digest.docx и early_warnings.xlsx для моментальной работы аналитика.")],
             accent_color=GAZPROM_BLUE)

    # ==================== SLIDE 7: Оркестрация в коде ====================
    s7 = prs.slides.add_slide(blank_layout)
    apply_background(s7)
    add_header(s7,
               "Оркестрация в коде: Детерминированный граф состояний в LangGraph Studio",
               "ТЕХНИЧЕСКАЯ РЕАЛИЗАЦИЯ",
               "LangGraph обеспечивает полный контроль над переходами, памятью сессии и циклом самопроверки")
    add_image_slide(s7, "langgraph_studio_ru.png",
                    "Преимущества графовой оркестрации LangGraph",
                    [("• Детерминированный StateGraph:", "В отличие от хаотичных цепочек CrewAI/AutoGen, граф строго регламентирует порядок выполнения шагов."),
                     ("• Петля Reflexion (Критик):", "Агент-Стратег циклически дорабатывает инициативу до тех пор, пока оценка риска не превысит 8.0/10."),
                     ("• Инспекция состояния (State Inspection):", "Справа в окне отладки видна полная схема Pydantic JSON на каждом шаге исполнения графа."),
                     ("• Human-in-the-Loop:", "Возможность приостановить выполнение графа для ручной валидации экспертом ДСИиУР перед отправкой презентации.")])

    # ==================== SLIDE 8: Агент 2 Детально ====================
    s8 = prs.slides.add_slide(blank_layout)
    apply_background(s8)
    add_header(s8,
               "Агент 2: Корпоративный Стратег — Синтез инициатив и модуль критики Reflexion",
               "ДЕТАЛИЗАЦИЯ: АГЕНТ 2",
               "Трансформация сырой рыночной аналитики в сбалансированные стратегические инициативы")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "1. Стратегические матрицы и пирамида Минто",
             [("• Синтез рыночной фактуры:", "Сопоставление данных Агента 1 с долгосрочными целями компании (горизонт 2026–2030 гг.)."),
              ("• Применение SWOT и PESTEL анализа:", "Агент структурирует сильные и слабые стороны компании против рыночных возможностей и угроз макросреды."),
              ("• Матрица Ансоффа:", "Определение вектора развития: углубление текущих рынков vs запуск новых технологических цепочек."),
              ("• Принцип Пирамиды Минто:", "Главный вывод и тезис формируются первыми, затем приводятся логические аргументы и числовая фактура.")],
             accent_color=GAZPROM_BLUE)

    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.3),
             "2. Паттерн Reflexion (Generator-Critic)",
             [("• Нода-Генератор:", "Формулирует первичный черновик стратегической инициативы (например: 'Построить 15 собственных танкеров Arc7 до 2027 года')."),
              ("• Нода-Критик (Роль Риск-офицера):", "Анализирует черновик на реализуемость. Вердикт: 'Сроки нереалистичны, верфи перегружены. Оценка: 5.2/10. Отклонено.'"),
              ("• Итеративная доработка:", "Генератор правит инициативу с учетом замечаний Критика."),
              ("• Валидированная инициатива (Оценка 8.8/10):", "STRAT-04: Заключение долгосрочных тайм-чартеров на суда Arc4/Arc5 с ледокольной проводкой. Принято!")],
             accent_color=EMERALD)

    # ==================== SLIDE 9: Нода Критики и 1000 критериев ====================
    s9 = prs.slides.add_slide(blank_layout)
    apply_background(s9)
    add_header(s9,
               "Нода Критики: Формирование рубрикатора и масштабирование на 100–1000 критериев",
               "МЕТОДОЛОГИЯ РИСК-СКОРИНГА",
               "Иерархическая декомпозиция и параллельный Map-Reduce исключают деградацию логики нейросети")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Откуда берутся веса и правила оценки в MVP?",
             [("• Установочная сессия с руководством ДСИиУР:", "Веса не придумываются программистом. На старте задается вопрос: 'По каким 3–5 причинам комитет обычно бракует инициативы?'"),
              ("• 4 базовых фактора нефтегазового сектора:",
               "  1. Санкции и импортозамещение (вес 30%)\n"
               "  2. Срок окупаемости и объем CAPEX (вес 30%)\n"
               "  3. Технологическая зрелость TRL >= 7 (вес 20%)\n"
               "  4. Промбезопасность и экология ESG (вес 20%)"),
              ("• Формула взвешенного скоринга:", "Total = 0.30*Санкции + 0.30*Окупаемость + 0.20*TRL + 0.20*Экология."),
              ("• Порог прохода: >= 8.0/10.", "При балле < 8.0 LangGraph возвращает инициативу Генератору.")],
             accent_color=GAZPROM_BLUE)

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.3),
             "Масштабирование: Что делать при 100 или 1000 критериев?",
             [("• Ошибка подачи 'в лоб':", "Подача 1000 критериев в один промпт приводит к эффекту Lost in the Middle, галлюцинациям и потере критических условий."),
              ("• 1. Иерархическая группировка по 4 макро-блокам:", "Финансы/CAPEX (40 критериев), Санкции/Импорт (50 критериев), Производство/Флот (40 критериев), Экология/ESG (30 критериев)."),
              ("• 2. Параллельные под-ноды критиков (Map-Reduce):", "4 независимых узла параллельно проверяют инициативу только по своему чеклисту."),
              ("• 3. Жесткие стоп-факторы (Red Flags):", "При выявлении прямого санкционного запрета выставляется отсев (Score 0) без траты токенов на остальные 950 пунктов!"),
              ("• 4. Детерминированная агрегация в коде:", "Итоговый балл считается математической формулой в Python без сбоев LLM.")],
             accent_color=AMBER)

    # ==================== SLIDE 10: Агент 3 и пример слайда ====================
    s10 = prs.slides.add_slide(blank_layout)
    apply_background(s10)
    add_header(s10,
               "Агент 3: Сборка презентаций — Реальный пример слайда для Департамента логистики",
               "ПРАКТИЧЕСКИЙ РЕЗУЛЬТАТ: АГЕНТ 3",
               "Автоматическая трансляция общекорпоративной цели в адресные KPI профильного подразделения")
    add_image_slide(s10, "department_slide_ru.png",
                    "Разбор сгенерированного слайда презентации",
                    [("• Адресная адаптация под профиль отдела:", "Общая стратегия STRAT-04 переведена на профессиональный язык Департамента логистики и морского транспорта."),
                     ("• Четкие целевые KPI подразделения:", "Снижение ставки фрахта на -12%, рост утилизации флота Arc7 на +18%, рост доли экологичного СПГ-топлива."),
                     ("• Принцип Пирамиды Минто:", "В заголовке вынесен главный управленческий вывод, ниже приведены аргументы и карта маршрутов СМП."),
                     ("• 100% векторная сборка python-pptx:", "Слайд собран по официальному мастер-шаблону. Все тексты, таблицы и цифры полностью редактируются руками.")])

    # ==================== SLIDE 11: Контракты Pydantic ====================
    s11 = prs.slides.add_slide(blank_layout)
    apply_background(s11)
    add_header(s11,
               "Контракты данных: Гарантия надежности связки через Pydantic v2 и Instructor",
               "ИНЖЕНЕРНЫЕ КОНТРАКТЫ ДАННЫХ",
               "Строгая типизация исключает разрыв контекста и превращает агентов в надежный промышленный конвейер")

    add_card(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Почему передача сырого текста — архитектурный тупик",
             [("• Проблема текстовых цепочек:", "Когда агенты обмениваются неструктурированным текстом, накапливаются ошибки, плывут цифры и теряются факты."),
              ("• Строгие Pydantic v2 схемы:", "Все 3 агента связаны жесткими контрактами данных: AnalystOutput, StrategistOutput, DepartmentReport."),
              ("• Библиотека Instructor:", "Гарантирует, что модель вернет валидный JSON, строго соответствующий схеме, с автоматическим повтором при сбое."),
              ("• Валидация типов 'на лету':", "Каждое поле (сроки, ставки фрахта, уровень риска) проверяется компилятором Python перед передачей дальше.")],
             accent_color=GAZPROM_BLUE)

    add_card(s11, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.3),
             "Архитектура Pydantic-контрактов в коде",
             [("• Схема сигнала раннего предупреждения:",
               "class EarlyWarningSignal(BaseModel):\n"
               "    title: str = Field(description='Суть сигнала')\n"
               "    severity: Literal['High', 'Medium', 'Low']\n"
               "    impact_area: str = Field('Логистика / Бурение')\n"
               "    evidence: str = Field('Цитата из источника')\n"
               "    recommended_action: str"),
              ("• Схема стратегической инициативы:",
               "class StrategicInitiative(BaseModel):\n"
               "    initiative_id: str = Field('STRAT-04')\n"
               "    title: str\n"
               "    objective: str\n"
               "    target_departments: List[str]\n"
               "    kpis: Dict[str, str]\n"
               "    mitigation_plan: str")],
             accent_color=GAZPROM_BLUE)

    # ==================== SLIDE 12: Человекочитаемые форматы ====================
    s12 = prs.slides.add_slide(blank_layout)
    apply_background(s12)
    add_header(s12,
               "Человекочитаемые форматы на выходе: Готовые документы для работы аналитиков",
               "АВТОНОМНОСТЬ И АРТЕФАКТЫ",
               "Аналитики не работают с кодом JSON: каждый агент создает полноценные офисные файлы Word, HTML, Excel и PPTX")

    add_card(s12, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Офисные артефакты для каждого агента",
             [("• Агент 1 (Аналитик):",
               "  1. analyst_digest.docx — сводный дайджест с таблицами\n"
               "  2. market_memo.html — интерактивная веб-справка с ссылками\n"
               "  3. early_warnings.xlsx — реестр сигналов для Excel"),
              ("• Агент 2 (Стратег):",
               "  1. strategy_memo.docx — полный инвестиционный паспорт\n"
               "  2. swot_matrix.html — наглядная SWOT-матрица\n"
               "  3. critic_log.docx — протокол замечаний Ноды-Критика"),
              ("• Агент 3 (Презентатор):",
               "  1. strategy_presentation.pptx — векторные слайды\n"
               "  2. executive_briefing.pdf — распечатка для руководства")],
             accent_color=GAZPROM_BLUE)

    add_card(s12, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.3),
             "Автономный режим работы (Standalone Mode)",
             [("• Независимость компонентов:", "Аналитик не обязан каждый раз запускать всю цепочку из 3 агентов!"),
              ("• Быстрый утренний мониторинг:", "Нужна только сводка по ценам нефти и фрахту? Запуск Агента 1 -> готовый дайджест Word через 40 секунд."),
              ("• Оценка собственного отчета:", "Есть сторонний PDF-документ? Загрузка в Агента 2 -> оценка рисков и протокол замечаний Критика."),
              ("• Сборка презентации под другой отдел:", "Запуск Агента 3 с указанием другого профиля YAML (например, Бурение вместо Логистики)."),
              ("• Полная свобода сотрудника:", "Агент выступает персональным цифровым ассистентом под конкретную задачу дня.")],
             accent_color=EMERALD)

    # ==================== SLIDE 13: Рабочее место аналитика (CLI) ====================
    s13 = prs.slides.add_slide(blank_layout)
    apply_background(s13)
    add_header(s13,
               "Рабочее место аналитика: Управление через Windows CLI и каталог готовых файлов",
               "КОНСОЛЬ И УПРАВЛЕНИЕ",
               "Удобные консольные команды запуска и автоматическое сохранение артефактов в локальную папку")

    add_card(s13, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Консольные команды в C:\\Users\\Lavrentiy\\Desktop\\газпром>",
             [("• Активация рабочего окружения:",
               "cd C:\\Users\\Lavrentiy\\Desktop\\газпром\n"
               ".\\venv\\Scripts\\activate"),
              ("• Запуск полного сквозного цикла (3 агента):",
               "python run_pipeline.py --topic 'Арктическая логистика СМП'"),
              ("• Автономный запуск мониторинга (Агент 1):",
               "python run_agent1_analyst.py --query 'Цены СПГ' --export docx,html"),
              ("• Оценка своей гипотезы / отчета (Агент 2):",
               "python run_agent2_strategist.py --input-file custom.pdf --export docx"),
              ("• Сборка презентации под отдел (Агент 3):",
               "python run_agent3_presenter.py --department logistics")],
             accent_color=GAZPROM_BLUE)

    add_card(s13, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.3),
             "Каталог готовых результатов: папка output/",
             [("• Структура локального каталога output/:",
               "C:\\Users\\Lavrentiy\\Desktop\\газпром\\output\\\n"
               "├── analyst_digest.docx         <-- Дайджест Word\n"
               "├── market_memo.html            <-- Веб-справка в браузере\n"
               "├── early_warnings.xlsx         <-- Реестр для Excel\n"
               "├── strategy_memo.docx          <-- Инвест-паспорт Word\n"
               "└── strategy_presentation.pptx  <-- Презентация PowerPoint"),
              ("• Мгновенное открытие файлов из консоли:",
               "start output\\strategy_presentation.pptx\n"
               "start output\\analyst_digest.docx"),
              ("• Полная интеграция с Windows:", "Файлы открываются стандартным двойным кликом в Microsoft Office.")],
             accent_color=GAZPROM_BLUE)

    # ==================== SLIDE 14: Технологический стек ====================
    s14 = prs.slides.add_slide(blank_layout)
    apply_background(s14)
    add_header(s14,
               "Технологический стек платформы: Обоснование выбора и отсутствие лишних затрат",
               "ТЕХНОЛОГИЧЕСКИЙ СТЕК",
               "Сбалансированная архитектура: надежная оркестрация, бесплатный поиск и отсутствие привязки к вендору")

    add_card(s14, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.3),
             "1. Оркестрация и контракты",
             [("• LangGraph (LangChain AI):", "Построение детерминированных графов, циклы Reflexion, управление памятью и Human-in-the-Loop."),
              ("• Pydantic v2 + Instructor:", "Строгая валидация типов, гарантия получения валидного JSON от моделей без поломки пайплайна."),
              ("• Без лишних оберток:", "Отказ от нестабильных надстроек CrewAI/AutoGen в пользу полного контроля логики.")],
             accent_color=GAZPROM_BLUE)

    add_card(s14, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.3),
             "2. Данные и бесплатный поиск",
             [("• duckduckgo-search (Python):", "Бесплатный веб-поиск новостей и котировок ТЭК. 0 рублей затрат, без API-ключей и кредитных карт."),
              ("• Docling (IBM) / Marker:", "Интеллектуальный парсинг сложных отраслевых PDF с сохранением таблиц в Markdown."),
              ("• Qdrant / ChromaDB:", "Локальное векторное хранилище в Docker, обеспечивающее мгновенный перенос в прод.")],
             accent_color=EMERALD)

    add_card(s14, Inches(8.8), Inches(1.6), Inches(3.733), Inches(5.3),
             "3. Слой LLM и генерация",
             [("• Model-Agnostic архитектура:", "Использование единого OpenAI-совместимого протокола. Переход на On-Prem vLLM сменой 1 строчки в .env."),
              ("• python-pptx:", "Программное наполнение официального корпоративного мастер-шаблона PowerPoint векторными фигурами."),
              ("• Streamlit UI:", "Быстрое создание интерактивного веб-дашборда для демонстрации руководству компании.")],
             accent_color=GAZPROM_BLUE)

    # ==================== SLIDE 15: Безопасность и On-Premise ====================
    s15 = prs.slides.add_slide(blank_layout)
    apply_background(s15)
    add_header(s15,
               "Безопасность и On-Premise: Разделение контуров и перенос на серверы компании",
               "БЕЗОПАСНОСТЬ И ВНЕДРЕНИЕ",
               "Быстрый R&D на открытых данных с архитектурной гарантией бесшовного переноса в закрытый контур")

    add_card(s15, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Фаза 1: Внешний контур (PoC Сентябрь–Декабрь)",
             [("• 100% открытые и синтетические данные:", "В облачные API передаются только публичные новости, котировки бирж и смоделированные кейсы."),
              ("• Нулевой риск для коммерческой тайны:", "Конфиденциальные внутренние данные компании физически не попадают во внешний интернет."),
              ("• Максимальная скорость разработки:", "Запуск проекта и демонстрация ценности без многомесячных согласований со службой безопасности компании."),
              ("• Изоляция кода:", "Кодовая база не содержит хардкода адресов облачных провайдеров.")],
             accent_color=GAZPROM_BLUE)

    add_card(s15, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.3),
             "Фаза 2: Перенос во внутренний контур (On-Premise)",
             [("• Model-Agnostic архитектура:", "Кодовая база изначально готова к работе с локальными моделями через OpenAI-совместимый протокол."),
              ("• Локальные LLM на серверах компании:", "Развертывание открытых моделей Qwen 2.5 (32B/72B) или DeepSeek-V3 на внутренних GPU через сервер vLLM."),
              ("• Переключение за 1 минуту:", "В файле .env меняется одна строка: LLM_BASE_URL='http://vllm-cluster.corp:8000/v1' без изменения кода агентов."),
              ("• Полная автономность:", "Система работает внутри изолированного контура компании без выхода во внешнюю сеть.")],
             accent_color=EMERALD)

    # ==================== SLIDE 16: Метрики и контроль качества ====================
    s16 = prs.slides.add_slide(blank_layout)
    apply_background(s16)
    add_header(s16,
               "Система метрик и контроль галлюцинаций: От алгоритмов Ragas до бизнес-эффекта",
               "ОЦЕНКА И ТЕСТИРОВАНИЕ",
               "Многоуровневый контроль исключает выдуманные факты и гарантирует высокую ценность инициатив")

    add_card(s16, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "Метрики качества RAG (Ragas Framework)",
             [("• Faithfulness (> 0.95) — Фактологическая верность:", "Процент утверждений в справке, строго подтвержденных цитатами первоисточников. Исключает галлюцинации."),
              ("• Answer Relevancy (> 0.90) — Релевантность ответа:", "Семантическое соответствие справки поставленному бизнес-вопросу без ухода в абстракции."),
              ("• Context Precision (> 0.85) — Точность контекста:", "Доля полезных чанков среди всех переданных в модель, отсеивающая информационный шум."),
              ("• Автоматическое тестирование:", "Регулярный прогон тестов на синтетических бенчмарках при каждом обновлении промптов.")],
             accent_color=GAZPROM_BLUE)

    add_card(s16, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.3),
             "Бизнес-метрики и пирамида тестирования",
             [("• Actionability Score:", "Оценка конкретности шагов: наличие ответственного подразделения, сроков реализации и целевых числовых KPI."),
              ("• Adoption Rate (Коэффициент принятия):", "Доля сгенерированных тезисов, принятых экспертами ДСИиУР без ручной переделки."),
              ("• Пирамида тестирования агентных систем:",
               "  1. Unit-тесты контрактов Pydantic (типы и парсинг)\n"
               "  2. Интеграционные тесты переходов графа в LangGraph\n"
               "  3. LLM-as-a-Judge (автоматический скоринг синтетики)\n"
               "  4. Human Evaluation (ежемесячная калибровка экспертами)")],
             accent_color=GAZPROM_BLUE)

    # ==================== SLIDE 17: Дорожная карта ====================
    s17 = prs.slides.add_slide(blank_layout)
    apply_background(s17)
    add_header(s17,
               "Дорожная карта реализации проекта: 4 последовательных спринта (Сентябрь – Декабрь)",
               "ПЛАН РЕАЛИЗАЦИИ",
               "Поэтапный ввод агентов в эксплуатацию с регулярной демонстрацией промежуточных результатов")

    add_card(s17, Inches(0.8), Inches(1.6), Inches(2.7), Inches(5.3),
             "Сентябрь: Агент 1",
             [("• Развертывание стенда:", "Настройка среды Python и векторной базы Qdrant."),
              ("• Бесплатный веб-поиск:", "Интеграция библиотеки duckduckgo-search."),
              ("• Парсинг отчетов ТЭК:", "Настройка Docling для таблиц PDF."),
              ("• Детектор Early Warnings:", "Алгоритм выявления скрытых рисков."),
              ("• Тесты на открытых данных:", "Валидация точности справки.")],
             accent_color=GAZPROM_BLUE)

    add_card(s17, Inches(3.75), Inches(1.6), Inches(2.7), Inches(5.3),
             "Октябрь: Агент 2",
             [("• Разработка Стратега:", "Промпты SWOT, PESTEL и пирамиды Минто."),
              ("• Контур Reflexion:", "Создание Ноды-Критика в LangGraph."),
              ("• Калибровка весов:", "Настройка 4 базовых критериев оценки."),
              ("• Генератор инициатив:", "Автоматический драфт паспортов проектов."),
              ("• Устранение утопий:", "Отсев нереалистичных гипотез.")],
             accent_color=GAZPROM_BLUE)

    add_card(s17, Inches(6.7), Inches(1.6), Inches(2.7), Inches(5.3),
             "Ноябрь: Агент 3",
             [("• Профили отделов:", "Каталог YAML для Бурения, Логистики и ИТ."),
              ("• Модуль python-pptx:", "Скрипт сборки слайдов по мастер-шаблону."),
              ("• Авто-каскадирование:", "Трансляция целей стратегии в KPI отделов."),
              ("• Тестирование верстки:", "Проверка шрифтов, цветов и отступов."),
              ("• Экспорт артефактов:", "Генерация Word, HTML и PPTX.")],
             accent_color=GAZPROM_BLUE)

    add_card(s17, Inches(9.65), Inches(1.6), Inches(2.883), Inches(5.3),
             "Декабрь: Финал и Демо",
             [("• Интеграция дашборда:", "Веб-интерфейс Streamlit для руководства."),
              ("• Сквозное демо (E2E):", "Запуск полного конвейера перед C-level."),
              ("• Методология для ДО:", "Регламент тиражирования на дочерние общества."),
              ("• План On-Premise:", "Пакет документации для ИБ и MLOps."),
              ("• Защита результатов:", "Подведение итогов пилотного этапа.")],
             accent_color=EMERALD)

    # ==================== SLIDE 18: Чек-лист запросов к заказчику ====================
    s18 = prs.slides.add_slide(blank_layout)
    apply_background(s18)
    add_header(s18,
               "Чек-лист для старта проекта: 6 ключевых запросов к команде ДСИиУР",
               "РЕСУРСЫ И СТАРТ",
               "Исчерпывающий перечень вводных данных, необходимых для успешного запуска разработки на установочной сессии")

    add_card(s18, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.3),
             "1. Материалы, шаблоны и пилотные отделы",
             [("• 1. 2–3 эталонных аналитических отчета (PDF/DOCX):", "Обезличенные исторические дайджесты ДСИиУР, признанные 'золотым стандартом' структуры, глубины и стиля."),
              ("• 2. Официальный мастер-шаблон презентаций (.pptx):", "Файл со стандартной сеткой, фирменными шрифтами, цветовой палитрой и мастер-слайдами 'Газпром нефти'."),
              ("• 3. Пилотные департаменты и контакты экспертов:",
               "  - 2–3 пилотных блока: Бурение, Логистика, ИТ\n"
               "  - 30-минутные установочные интервью с аналитиками для сбора профессионального сленга и терминов\n"
               "  - Примеры их локальных регламентов, ключевых KPI (проходка, ставка фрахта, uptime) и типовых слайдов")],
             accent_color=GAZPROM_BLUE)

    add_card(s18, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.3),
             "2. Источники, доступы и критерии оценки",
             [("• 4. Перечень приоритетных открытых источников:", "Отраслевые порталы, сайты министерств (Минэнерго, Минпромторг), агентства (Интерфакс-ТЭК, Cbonds, Neftegaz.ru), за которыми команда следит регулярно."),
              ("• 5. Лимиты на API-ключи ТОЛЬКО для языковых моделей:",
               "  - Бюджет только на вызовы LLM (Claude 3.5 Sonnet / GPT-4o)\n"
               "  - 0 рублей расходов на платные поисковики, так как поиск работает на бесплатной библиотеке duckduckgo-search\n"
               "  - Тестовая виртуальная машина для развертывания стенда"),
              ("• 6. Критерии Инвестиционного комитета компании:", "Список 3–5 ключевых причин отклонения проектов (для точной калибровки весов и порогов в Ноде-Критике Агента 2).")],
             accent_color=EMERALD)

    # ==================== SLIDE 19: Roadmap 2026+ ====================
    s19 = prs.slides.add_slide(blank_layout)
    apply_background(s19)
    add_header(s19,
               "План доработки и масштабирования каждого агента после декабря (Roadmap 2026+)",
               "РАЗВИТИЕ СИСТЕМЫ ПОСЛЕ ДЕКАБРЯ",
               "Переход от пилотного PoC к полнофункциональной промышленной платформе стратегического управления")

    add_card(s19, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.3),
             "Агент 1: Аналитик 2026+",
             [("• 24/7 Онлайн-демон (CRON):", "Непрерывный фоновый мониторинг рынков каждые 30 минут и авто-апдейт базы Qdrant."),
              ("• Платные терминалы ТЭК:", "Подключение через API специализированных баз: Argus Media, S&P Platts, Cbonds, таможни ФТС."),
              ("• Моментальные PUSH-алерты:", "Мгновенная отправка High-severity сигналов тревоги в корпоративный чат или Telegram."),
              ("• Прогнозирование рядов (ML):", "Модели Prophet/Chronos для предиктивного моделирования коридоров цен и ставок фрахта.")],
             accent_color=GAZPROM_BLUE)

    add_card(s19, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.3),
             "Агент 2: Стратег 2026+",
             [("• 'Виртуальный совет директоров':", "Консилиум агентов (CFO, Главный инженер, Санкционный юрист) дебатирует по методу Дельфи."),
              ("• Расчет финмодели (Tool Calling):", "Вызов Python-калькулятора DCF: автоматический расчет NPV, IRR, окупаемости и стресс-тесты."),
              ("• Аудит портфеля компании:", "Семантическая сверка с базой текущих инвестпроектов компании для исключения каннибализации бюджетов."),
              ("• Сценарное моделирование:", "Прогноз эффектов при колебаниях курсов валют и ставок ЦБ.")],
             accent_color=GAZPROM_BLUE)

    add_card(s19, Inches(8.8), Inches(1.6), Inches(3.733), Inches(5.3),
             "Агент 3: Презентатор 2026+",
             [("• Интерактивные BI-порталы:", "Генерация интерактивных веб-дашбордов с возможностью провала в первоисточник (Drill-down)."),
              ("• Векторная авто-инфографика:", "Программное построение карт Севморпути, диаграмм Ганта и waterfall-графиков формирования EBITDA."),
              ("• Тиражирование на 50+ ДО:", "Единый каталог YAML-профилей для всех НПЗ, сбытовых и добывающих предприятий компании."),
              ("• Human-in-the-Loop DSPy:", "Автоматическая донастройка промптов на истории оценок руководства.")],
             accent_color=EMERALD)

    # ==================== SLIDE 20: База знаний (Видеокурсы) ====================
    s20 = prs.slides.add_slide(blank_layout)
    apply_background(s20)
    add_header(s20,
               "База знаний: Русскоязычные видеокурсы, лекции ведущих ML-школ и доклады (YouTube)",
               "ОБУЧЕНИЕ И БАЗА ЗНАНИЙ",
               "Отобранные лекции и доклады с HighLoad++, Data Fest, ODS и Сбера по ключевым технологиям проекта")

    add_card(s20, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.55),
             "1. Мультиагенты и LangGraph на русском",
             [("• ODS / Data Fest:", "«Мультиагентные системы на базе LLM: от концепции до кода». Архитектура взаимодействия агентов и паттерны Supervisor."),
              ("• LangGraph на практике:", "Построение детерминированных графов состояний на Python с циклами самопроверки Reflexion.")],
             accent_color=GAZPROM_BLUE)

    add_card(s20, Inches(6.8), Inches(1.6), Inches(5.733), Inches(2.55),
             "2. Advanced RAG и гибридный поиск",
             [("• Karpov.Courses (Hard ML):", "«Как устроен RAG: от наивного поиска до Production». Разбор эмбеддингов, чанкинга и косинусной близости."),
              ("• HighLoad++ Конференция:", "Гибридный поиск BM25 + Dense, слияние рангов RRF и кросс-энкодеры bge-reranker против галлюцинаций.")],
             accent_color=GAZPROM_BLUE)

    add_card(s20, Inches(0.8), Inches(4.35), Inches(5.6), Inches(2.55),
             "3. Корпоративный опыт Сбера и On-Premise",
             [("• Sber AI / GigaChain:", "Официальный опыт Сбера по оркестрации агентных сценариев в закрытом контуре без интернета."),
              ("• DevOps Conf / HighLoad:", "Развертывание серверов инференса vLLM и квантование моделей Qwen 2.5 / DeepSeek на внутренних GPU.")],
             accent_color=GAZPROM_BLUE)

    add_card(s20, Inches(6.8), Inches(4.35), Inches(5.733), Inches(2.55),
             "4. Оценка качества Ragas и генерация слайдов",
             [("• Тестирование RAG на русском:", "Расчет метрик Faithfulness, Answer Relevance и бенчмаркинг точности ответов без галлюцинаций."),
              ("• Автоматизация python-pptx:", "Практическое руководство по созданию презентаций из кода Python по мастер-шаблону компании.")],
             accent_color=GAZPROM_BLUE)

    # ==================== SLIDE 21: Финал ====================
    s21 = prs.slides.add_slide(blank_layout)
    bg21 = s21.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg21.fill.solid()
    bg21.fill.fore_color.rgb = NAVY
    bg21.line.fill.background()

    bar21 = s21.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
    bar21.fill.solid()
    bar21.fill.fore_color.rgb = GAZPROM_BLUE
    bar21.line.fill.background()

    tb21 = s21.shapes.add_textbox(Inches(1.2), Inches(2.0), Inches(10.9), Inches(4.0))
    tf21 = tb21.text_frame
    tf21.word_wrap = True

    p21_0 = tf21.paragraphs[0]
    r21_0 = p21_0.add_run()
    r21_0.text = "ГОТОВНОСТЬ К РЕАЛИЗАЦИИ И СТАРТУ"
    r21_0.font.bold = True
    r21_0.font.size = Pt(13)
    r21_0.font.color.rgb = GAZPROM_BLUE

    p21_1 = tf21.add_paragraph()
    p21_1.space_before = Pt(14)
    r21_1 = p21_1.add_run()
    r21_1.text = "Спасибо за внимание! Готов к запуску проекта."
    r21_1.font.bold = True
    r21_1.font.size = Pt(32)
    r21_1.font.color.rgb = WHITE

    p21_2 = tf21.add_paragraph()
    p21_2.space_before = Pt(16)
    r21_2 = p21_2.add_run()
    r21_2.text = (
        "Комплексный отчет в Word, структурированный Markdown и архитектурный код подготовлены.\n"
        "Готов ответить на вопросы и приступить к первому установочному спринту с командой ДСИиУР."
    )
    r21_2.font.size = Pt(15)
    r21_2.font.color.rgb = RGBColor(200, 220, 240)

    p21_3 = tf21.add_paragraph()
    p21_3.space_before = Pt(24)
    r21_3 = p21_3.add_run()
    r21_3.text = "Кандидат / Разработчик: Лаврентий  |  ПАО «Газпром нефть»  |  Санкт-Петербург, 2026"
    r21_3.font.size = Pt(12)
    r21_3.font.color.rgb = RGBColor(160, 190, 220)

    prs.save(OUTPUT_PPTX)
    print(f"Top-tier consulting presentation successfully generated: {OUTPUT_PPTX}")

if __name__ == "__main__":
    build_presentation()

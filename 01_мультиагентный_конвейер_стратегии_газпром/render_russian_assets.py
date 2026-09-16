import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Setup output directory
ASSETS_DIR = os.path.abspath("c:/Users/Lavrentiy/Desktop/газпром/assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Set font family for Russian
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Calibri', 'Tahoma']
plt.rcParams['axes.unicode_minus'] = False

# Colors
NAVY = "#003366"
BLUE = "#0079C2"
LIGHT_BLUE = "#EBF3FA"
DARK_GRAY = "#1E293B"
GRAY = "#64748B"
LIGHT_GRAY = "#F1F5F9"
WHITE = "#FFFFFF"
GREEN = "#109566"
ORANGE = "#DC641E"
RED = "#EF4444"
BORDER = "#CBD5E1"

# -------------------------------------------------------------
# 1. АРХИТЕКТУРА 3-Х АГЕНТОВ НА РУССКОМ ЯЗЫКЕ
# -------------------------------------------------------------
def draw_architecture_flow_ru():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#0F172A")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Title
    ax.text(8, 8.4, "СКВОЗНАЯ АРХИТЕКТУРА 3-Х ИИ-АГЕНТОВ", color=WHITE, fontsize=20, fontweight='bold', ha='center')
    ax.text(8, 8.0, "ДСИиУР ПАО «Газпром нефть» | Конвейер: Аналитик → Стратег → Презентатор", color="#94A3B8", fontsize=12, ha='center')

    # Stage 1
    rect1 = patches.FancyBboxPatch((0.8, 1.8), 4.2, 5.7, boxstyle="round,pad=0.2", fc="#1E293B", ec=BLUE, lw=2)
    ax.add_patch(rect1)
    ax.text(2.9, 7.1, "ЭТАП 1: АНАЛИТИК", color=BLUE, fontsize=14, fontweight='bold', ha='center')
    ax.text(2.9, 6.7, "Сбор данных и ранние сигналы", color="#94A3B8", fontsize=10, ha='center')
    
    t1 = ("• Мониторинг открытых источников:\n"
          "  Новости ТЭК, биржи, сайты министерств\n\n"
          "• Layout-Aware парсинг отчетов:\n"
          "  Docling (IBM) / Marker для PDF\n\n"
          "• Гибридный поиск (Hybrid RAG):\n"
          "  Dense векторы + BM25 слияние (RRF)\n\n"
          "• Реранкинг через bge-reranker:\n"
          "  Отсечение 85% шума и спама\n\n"
          "• Детектор сигналов тревоги:\n"
          "  Early Warning Signals (санкции, шоки)\n\n"
          "ВЫХОД: AnalystOutput (JSON)")
    ax.text(1.1, 3.2, t1, color=WHITE, fontsize=9.5, va='center')

    # Arrow 1 -> 2
    ax.annotate("", xy=(5.5, 4.65), xytext=(5.1, 4.65), arrowprops=dict(arrowstyle="->", color=BLUE, lw=3))

    # Stage 2
    rect2 = patches.FancyBboxPatch((5.7, 1.8), 4.4, 5.7, boxstyle="round,pad=0.2", fc="#1E293B", ec="#38BDF8", lw=2)
    ax.add_patch(rect2)
    ax.text(7.9, 7.1, "ЭТАП 2: СТРАТЕГ", color="#38BDF8", fontsize=14, fontweight='bold', ha='center')
    ax.text(7.9, 6.7, "Синтез стратегии и контур критики", color="#94A3B8", fontsize=10, ha='center')

    t2 = ("• Сопоставление с целями компании:\n"
          "  Горизонт 2026–2030, профиль рисков\n\n"
          "• Стратегические методологии:\n"
          "  SWOT, PESTEL, Матрица Ансоффа\n\n"
          "• Контур критики (Generator-Critic):\n"
          "  1) Генератор предлагает инициативу\n"
          "  2) Нода-Критик проверяет риски и CAPEX\n"
          "  3) Петля доработки до оценки >= 8.0\n\n"
          "• Формирование карты инициатив:\n"
          "  Декомпозиция на STRAT-01..N\n\n"
          "ВЫХОД: StrategyRoadmap (JSON)")
    ax.text(6.0, 3.2, t2, color=WHITE, fontsize=9.5, va='center')

    # Arrow 2 -> 3
    ax.annotate("", xy=(10.6, 4.65), xytext=(10.2, 4.65), arrowprops=dict(arrowstyle="->", color="#38BDF8", lw=3))

    # Stage 3
    rect3 = patches.FancyBboxPatch((10.8, 1.8), 4.4, 5.7, boxstyle="round,pad=0.2", fc="#1E293B", ec=GREEN, lw=2)
    ax.add_patch(rect3)
    ax.text(13.0, 7.1, "ЭТАП 3: ПРЕЗЕНТАТОР", color=GREEN, fontsize=14, fontweight='bold', ha='center')
    ax.text(13.0, 6.7, "Каскадирование и верстка .pptx", color="#94A3B8", fontsize=10, ha='center')

    t3 = ("• Профили подразделений (YAML):\n"
          "  ИТ, Логистика, Бурение, Капстрой\n\n"
          "• Селекция и адаптация смыслов:\n"
          "  Отбор только релевантных инициатив,\n"
          "  перевод на язык и термины отдела\n\n"
          "• Принцип пирамиды Минто:\n"
          "  Главный вывод в заголовке слайда,\n"
          "  затем фактура и показатели KPI\n\n"
          "• Автоматическая сборка в python-pptx:\n"
          "  Наполнение официального брендбука\n\n"
          "ВЫХОД: Адресные слайды .pptx и мемо")
    ax.text(11.1, 3.2, t3, color=WHITE, fontsize=9.5, va='center')

    # Footer note
    ax.text(8, 0.8, "Архитектура спроектирована как Model-Agnostic на базе LangGraph с мгновенным переносом в On-Premise контур", color="#64748B", fontsize=10, ha='center')

    plt.tight_layout()
    out = os.path.join(ASSETS_DIR, "architecture_flow_ru.png")
    plt.savefig(out, dpi=200, bbox_inches='tight')
    plt.close()
    print("Saved:", out)

# -------------------------------------------------------------
# 2. ДАШБОРД АНАЛИТИКА НА РУССКОМ ЯЗЫКЕ
# -------------------------------------------------------------
def draw_ui_dashboard_ru():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor("#0B132B")
    ax.set_facecolor("#0B132B")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Top Header
    header = patches.Rectangle((0, 8.1), 16, 0.9, fc="#1C2541")
    ax.add_patch(header)
    ax.text(0.6, 8.55, "ПАО «ГАЗПРОМ НЕФТЬ»", color=WHITE, fontsize=13, fontweight='bold', va='center')
    ax.text(3.8, 8.55, "|  Аналитическая платформа ИИ-агентов (ДСИиУР)", color="#94A3B8", fontsize=11, va='center')
    ax.text(15.4, 8.55, "Лаврентий (Аналитик)", color="#38BDF8", fontsize=10, ha='right', va='center')

    # Left Sidebar
    sidebar = patches.Rectangle((0, 0), 3.2, 8.1, fc="#111B34")
    ax.add_patch(sidebar)
    ax.text(0.4, 7.6, "ЭТАПЫ КОНВЕЙЕРА", color="#64748B", fontsize=9, fontweight='bold')

    s_items = [
        ("1. Рыночный Аналитик", "#0079C2", True),
        ("2. Корпоративный Стратег", "#64748B", False),
        ("3. Презентатор отделов", "#64748B", False),
    ]
    for i, (name, col, active) in enumerate(s_items):
        y = 7.0 - i * 0.9
        if active:
            box = patches.FancyBboxPatch((0.3, y - 0.25), 2.6, 0.6, boxstyle="round,pad=0.1", fc="#0079C2", ec="none")
            ax.add_patch(box)
            ax.text(0.5, y + 0.05, name, color=WHITE, fontsize=10, fontweight='bold')
        else:
            ax.text(0.5, y + 0.05, name, color="#94A3B8", fontsize=10)

    # Top Metrics Bar
    m_data = [
        ("Нефть Urals", "$88.42 / барр", "+1.2% за неделю", GREEN, 3.6),
        ("Природный газ (СПГ)", "$385 / тыс. м³", "-0.8% за сутки", RED, 7.6),
        ("Индекс ставок фрахта", "1 420 п.", "+3.4% за месяц", ORANGE, 11.6)
    ]
    for title, val, diff, dcol, x in m_data:
        mbox = patches.FancyBboxPatch((x, 6.7), 3.6, 1.1, boxstyle="round,pad=0.1", fc="#1C2541", ec=BORDER, lw=0.5)
        ax.add_patch(mbox)
        ax.text(x + 0.2, 7.45, title, color="#94A3B8", fontsize=9)
        ax.text(x + 0.2, 7.05, val, color=WHITE, fontsize=14, fontweight='bold')
        ax.text(x + 2.2, 7.05, diff, color=dcol, fontsize=9, fontweight='bold')

    # Main Left: Early Warnings
    ew_box = patches.FancyBboxPatch((3.6, 1.4), 6.5, 5.0, boxstyle="round,pad=0.1", fc="#1C2541", ec=BORDER, lw=0.5)
    ax.add_patch(ew_box)
    ax.text(3.9, 6.05, "СИГНАЛЫ РАННЕГО ПРЕДУПРЕЖДЕНИЯ (EARLY WARNINGS)", color=WHITE, fontsize=11, fontweight='bold')
    
    signals = [
        ("[КРИТИЧЕСКИЙ] Санкции против верфей и дефицит танкеров Arc7", 
         "Reuters: Включение в SDN-лист 3 верфей. Риск срыва графика поставок СПГ.", "Высокая критичность", RED, 5.3),
        ("[ВНИМАНИЕ] Скачок премий на военные риски в Красном море", 
         "Рост стоимости страхования танкеров на 28%. Перенаправление маршрутов.", "Средняя критичность", ORANGE, 4.0),
        ("[МОНИТОРИНГ] Новые регуляторные требования ЕС по учету метана", 
         "Ужесточение нормативов Scope 1 для экспортеров с 2027 года.", "Информационный", BLUE, 2.7)
    ]
    for title, desc, tag, col, y in signals:
        sbox = patches.FancyBboxPatch((3.8, y - 0.7), 6.1, 1.0, boxstyle="round,pad=0.08", fc="#111B34", ec="none")
        ax.add_patch(sbox)
        ax.text(4.0, y + 0.05, title, color=WHITE, fontsize=9, fontweight='bold')
        ax.text(4.0, y - 0.25, desc, color="#94A3B8", fontsize=8)
        # Badge
        tbox = patches.FancyBboxPatch((8.3, y - 0.05), 1.4, 0.28, boxstyle="round,pad=0.05", fc=col, ec="none")
        ax.add_patch(tbox)
        ax.text(9.0, y + 0.07, tag, color=WHITE, fontsize=7, fontweight='bold', ha='center')

    # Main Right: Competitor Benchmarks
    cb_box = patches.FancyBboxPatch((10.4, 2.7), 5.0, 3.7, boxstyle="round,pad=0.1", fc="#1C2541", ec=BORDER, lw=0.5)
    ax.add_patch(cb_box)
    ax.text(10.7, 6.05, "КАРТА СТРАТЕГИЙ КОНКУРЕНТОВ", color=WHITE, fontsize=11, fontweight='bold')

    benchmarks = [
        ("ПАО «НК «Роснефть»", "Проект Восток Ойл: контрактация 10 танкеров ледового класса на ССК Звезда.", 5.2),
        ("ПАО «ЛУКОЙЛ»", "Оптимизация балтийских коридоров и развитие перевалочных мощностей в Высоцке.", 4.2),
        ("Saudi Aramco", "Заключение прямых 10-летних спотовых контрактов на поставку углеводородов в Китай.", 3.2)
    ]
    for comp, action, y in benchmarks:
        ax.text(10.7, y + 0.15, comp, color="#38BDF8", fontsize=9.5, fontweight='bold')
        ax.text(10.7, y - 0.25, action, color="#CBD5E1", fontsize=8)

    # Bottom Right Button
    btn = patches.FancyBboxPatch((10.4, 1.4), 5.0, 1.0, boxstyle="round,pad=0.1", fc="#0079C2", ec="none")
    ax.add_patch(btn)
    ax.text(12.9, 1.9, "СФОРМИРОВАТЬ СЛАЙДЫ ДЛЯ ОТДЕЛА", color=WHITE, fontsize=10, fontweight='bold', ha='center')
    ax.text(12.9, 1.6, "Каскадирование стратегии в формат .pptx", color="#E0F2FE", fontsize=8, ha='center')

    plt.tight_layout()
    out = os.path.join(ASSETS_DIR, "ui_dashboard_ru.png")
    plt.savefig(out, dpi=200, bbox_inches='tight')
    plt.close()
    print("Saved:", out)

# -------------------------------------------------------------
# 3. LANGGRAPH STUDIO НА РУССКОМ ЯЗЫКЕ
# -------------------------------------------------------------
def draw_langgraph_studio_ru():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor("#0D1117")
    ax.set_facecolor("#0D1117")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Top Bar
    header = patches.Rectangle((0, 8.2), 16, 0.8, fc="#161B22")
    ax.add_patch(header)
    ax.text(0.5, 8.6, "LangGraph Studio | Проект: strategy_pipeline.py", color=WHITE, fontsize=12, fontweight='bold', va='center')
    ax.text(15.5, 8.6, "Режим отладки: StateGraph (Python)", color="#58A6FF", fontsize=10, ha='right', va='center')

    # Graph Canvas (Left)
    canvas = patches.Rectangle((0.5, 0.8), 9.8, 7.1, fc="#090D13", ec="#30363D", lw=1)
    ax.add_patch(canvas)
    ax.text(0.8, 7.5, "ВИЗУАЛИЗАЦИЯ ГРАФА АГЕНТОВ (STATE GRAPH)", color="#8B949E", fontsize=10, fontweight='bold')

    # Node 1: Analyst
    n1 = patches.FancyBboxPatch((1.0, 4.4), 2.2, 1.2, boxstyle="round,pad=0.1", fc="#1F2937", ec=GREEN, lw=2)
    ax.add_patch(n1)
    ax.text(2.1, 5.2, "✓ analyst_node", color=WHITE, fontsize=10, fontweight='bold', ha='center')
    ax.text(2.1, 4.7, "Сбор новостей и RAG", color="#9CA3AF", fontsize=8, ha='center')

    # Arrow 1 -> 2
    ax.annotate("", xy=(3.8, 5.0), xytext=(3.3, 5.0), arrowprops=dict(arrowstyle="->", color=GREEN, lw=2))

    # Node 2: Strategist
    n2 = patches.FancyBboxPatch((3.9, 4.4), 2.3, 1.2, boxstyle="round,pad=0.1", fc="#1F2937", ec=GREEN, lw=2)
    ax.add_patch(n2)
    ax.text(5.05, 5.2, "✓ strategist_node", color=WHITE, fontsize=10, fontweight='bold', ha='center')
    ax.text(5.05, 4.7, "Синтез инициатив", color="#9CA3AF", fontsize=8, ha='center')

    # Critic Loop (Reflexion)
    nc = patches.FancyBboxPatch((3.9, 2.2), 2.3, 1.2, boxstyle="round,pad=0.1", fc="#1F2937", ec=ORANGE, lw=2)
    ax.add_patch(nc)
    ax.text(5.05, 3.0, "critic_node", color=ORANGE, fontsize=10, fontweight='bold', ha='center')
    ax.text(5.05, 2.5, "Оценка рисков и CAPEX", color="#9CA3AF", fontsize=8, ha='center')

    # Reflexion arrows
    ax.annotate("", xy=(4.6, 3.5), xytext=(4.6, 4.3), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5))
    ax.text(4.1, 3.9, "Проверка", color=ORANGE, fontsize=7)
    ax.annotate("", xy=(5.5, 4.3), xytext=(5.5, 3.5), arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))
    ax.text(5.6, 3.9, "Балл >= 8.0", color=GREEN, fontsize=7)

    # Arrow 2 -> 3
    ax.annotate("", xy=(6.8, 5.0), xytext=(6.3, 5.0), arrowprops=dict(arrowstyle="->", color="#58A6FF", lw=2))

    # Node 3: Presenter
    n3 = patches.FancyBboxPatch((6.9, 4.4), 2.3, 1.2, boxstyle="round,pad=0.1", fc="#1F2937", ec="#58A6FF", lw=2)
    ax.add_patch(n3)
    ax.text(8.05, 5.2, "presenter_node", color=WHITE, fontsize=10, fontweight='bold', ha='center')
    ax.text(8.05, 4.7, "Каскадирование слайдов", color="#9CA3AF", fontsize=8, ha='center')

    # Branches to departments
    depts = [
        ("dept_logistics_pptx", 6.2),
        ("dept_it_pptx", 5.0),
        ("dept_drilling_pptx", 3.8)
    ]
    for dname, y in depts:
        ax.annotate("", xy=(9.8, y + 0.2), xytext=(9.3, 5.0), arrowprops=dict(arrowstyle="->", color="#58A6FF", lw=1.5))
        d_box = patches.FancyBboxPatch((9.9, y), 0.3, 0.4, boxstyle="round,pad=0.05", fc="#238636", ec="none")
        ax.add_patch(d_box)

    # Right Inspector Panel
    inspector = patches.Rectangle((10.7, 0.8), 4.8, 7.1, fc="#161B22", ec="#30363D", lw=1)
    ax.add_patch(inspector)
    ax.text(11.0, 7.5, "ИНСПЕКТОР СОСТОЯНИЯ (JSON / PYDANTIC)", color=WHITE, fontsize=10, fontweight='bold')
    
    json_text = (
        '{\n'
        '  "current_step": 3,\n'
        '  "active_node": "presenter_node",\n'
        '  "target_department": "Логистика",\n'
        '  "validated_initiative": {\n'
        '    "id": "STRAT-04",\n'
        '    "title": "Оптимизация СМП",\n'
        '    "critic_score": 8.8,\n'
        '    "kpi_freight_rate": "-12%",\n'
        '    "arc7_fleet_growth": "+18%"\n'
        '  },\n'
        '  "pptx_generation_status": "OK",\n'
        '  "output_file": "report_logistics.pptx"\n'
        '}'
    )
    ax.text(11.0, 5.0, json_text, color="#7EE787", fontfamily="monospace", fontsize=9, va='center')

    plt.tight_layout()
    out = os.path.join(ASSETS_DIR, "langgraph_studio_ru.png")
    plt.savefig(out, dpi=200, bbox_inches='tight')
    plt.close()
    print("Saved:", out)

# -------------------------------------------------------------
# 4. ГОТОВЫЙ СЛАЙД ПРЕЗЕНТАЦИИ НА РУССКОМ ЯЗЫКЕ
# -------------------------------------------------------------
def draw_department_slide_ru():
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor(WHITE)
    ax.set_facecolor(WHITE)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    # Top Brand Header
    h_bar = patches.Rectangle((0, 7.6), 16, 1.4, fc=NAVY)
    ax.add_patch(h_bar)
    ax.text(0.8, 8.45, "ПАО «ГАЗПРОМ НЕФТЬ»", color=WHITE, fontsize=14, fontweight='bold')
    ax.text(0.8, 8.0, "Стратегия логистики 2026–2030: Оптимизация флота Севморпути", color="#38BDF8", fontsize=18, fontweight='bold')
    ax.text(0.8, 7.65, "Каскадирование общекорпоративной инициативы STRAT-04 для Департамента логистики", color="#E2E8F0", fontsize=11)

    # Left Column: KPIs
    ax.text(0.8, 7.0, "КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ ЭФФЕКТИВНОСТИ (KPIs)", color=NAVY, fontsize=12, fontweight='bold')

    kpis = [
        ("Снижение ставки фрахта: -12%", 
         "Оптимизация тайм-чартеров и координация с ледоколами\nпозволяет сократить издержки на тонну нефти.", GREEN, 5.8),
        ("Рост утилизации танкеров Arc7: +18%", 
         "Ликвидация простоев за счет предиктивного анализа погоды\nи ледовой обстановки спутниковыми снимками.", BLUE, 4.4),
        ("Переход флота на СПГ-бункеровку: 45%", 
         "Снижение углеродного следа Scope 1 в арктической зоне\nи выполнение нормативов декарбонизации.", NAVY, 3.0)
    ]
    for title, desc, col, y in kpis:
        # Icon box
        ibox = patches.FancyBboxPatch((0.8, y - 0.4), 0.7, 0.7, boxstyle="round,pad=0.08", fc=col, ec="none")
        ax.add_patch(ibox)
        ax.text(1.15, y - 0.05, "★", color=WHITE, fontsize=14, ha='center', va='center')
        
        ax.text(1.8, y + 0.15, title, color=DARK_GRAY, fontsize=12, fontweight='bold')
        ax.text(1.8, y - 0.25, desc, color=GRAY, fontsize=10)

    # Right Column: Map Schematic
    map_box = patches.FancyBboxPatch((8.8, 1.2), 6.5, 6.0, boxstyle="round,pad=0.1", fc=LIGHT_BLUE, ec=BORDER, lw=1)
    ax.add_patch(map_box)
    ax.text(9.2, 6.8, "СХЕМА АРКТИЧЕСКИХ ЛОГИСТИЧЕСКИХ КОРИДОРОВ", color=NAVY, fontsize=11, fontweight='bold')

    # Points on map
    points = [
        ("Мурманск (Базовый хаб)", 9.5, 5.8),
        ("Сабетта (Перевалка Ямал)", 11.2, 5.3),
        ("Пролив Вилькицкого (Ледоколы)", 12.8, 4.8),
        ("Берингов пролив", 14.2, 4.0),
        ("Рынки АТР (Китай, Индия)", 13.5, 2.2)
    ]
    for name, px, py in points:
        ax.plot(px, py, 'o', color=BLUE, markersize=8)
        ax.text(px + 0.2, py - 0.05, name, color=DARK_GRAY, fontsize=9, fontweight='bold')
        
    # Route line
    pxs = [p[1] for p in points]
    pys = [p[2] for p in points]
    ax.plot(pxs, pys, '--', color=BLUE, lw=2.5)

    ax.text(9.2, 1.5, "• Маршрут круглогодичной навигации танкеров ледового класса Arc7\n• Сокращение плеча доставки на 14 дней по сравнению с Суэцким каналом", color=GRAY, fontsize=8.5)

    # Footer
    footer = patches.Rectangle((0, 0), 16, 0.6, fc=LIGHT_GRAY)
    ax.add_patch(footer)
    ax.text(0.8, 0.3, "Департамент логистики и морского транспорта | Конфиденциально | Страница 12", color=GRAY, fontsize=9, va='center')

    plt.tight_layout()
    out = os.path.join(ASSETS_DIR, "department_slide_ru.png")
    plt.savefig(out, dpi=200, bbox_inches='tight')
    plt.close()
    print("Saved:", out)

# -------------------------------------------------------------
# 5. МИРОВЫЕ КЕЙСЫ: MCKINSEY LILLI & BCG GENEAI (АУТЕНТИЧНЫЕ СХЕМЫ)
# -------------------------------------------------------------
def draw_consulting_benchmarks():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor("#0F172A")
    for ax in [ax1, ax2]:
        ax.set_facecolor("#1E293B")
        ax.axis('off')

    # Left: McKinsey Lilli
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.text(5, 9.2, "McKinsey Lilli Platform", color=WHITE, fontsize=16, fontweight='bold', ha='center')
    ax1.text(5, 8.6, "Enterprise Knowledge Retrieval & Synthesis", color="#38BDF8", fontsize=11, ha='center')

    lilli_boxes = [
        ("1. Knowledge Ingestion", "100,000+ past client studies, sector research,\nbenchmarking databases, interview transcripts", 7.0),
        ("2. Hybrid Neural Retrieval", "Dense embedding search + BM25 keyword matching\nwith Citation Engine (100% verifiable sources)", 5.2),
        ("3. Synthesis & Client-Ready Memo", "Automated executive summary generation,\nreducing initial synthesis from 2 weeks to 2 hours", 3.4)
    ]
    for title, desc, y in lilli_boxes:
        b = patches.FancyBboxPatch((0.8, y - 0.6), 8.4, 1.2, boxstyle="round,pad=0.1", fc="#0F172A", ec=BLUE, lw=1.5)
        ax1.add_patch(b)
        ax1.text(1.2, y + 0.25, title, color=WHITE, fontsize=11, fontweight='bold')
        ax1.text(1.2, y - 0.25, desc, color="#94A3B8", fontsize=9)

    # Right: BCG GeneAI
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.text(5, 9.2, "BCG GeneAI Slide Factory", color=WHITE, fontsize=16, fontweight='bold', ha='center')
    ax2.text(5, 8.6, "Multi-Agent Consulting Presentation Generation", color=GREEN, fontsize=11, ha='center')

    bcg_boxes = [
        ("1. Research & Facts Agent", "Extracts structured quantitative insights,\nkey numbers, competitor benchmarking data", 7.0),
        ("2. Fact-Checking & Critic Agent", "Validates claims against ground-truth reports;\nprevents hallucinations before layout phase", 5.2),
        ("3. Layout Engine (OpenXML / PPTX)", "Direct programmatic generation into editable\nMicrosoft PowerPoint slides in BCG corporate style", 3.4)
    ]
    for title, desc, y in bcg_boxes:
        b = patches.FancyBboxPatch((0.8, y - 0.6), 8.4, 1.2, boxstyle="round,pad=0.1", fc="#0F172A", ec=GREEN, lw=1.5)
        ax2.add_patch(b)
        ax2.text(1.2, y + 0.25, title, color=WHITE, fontsize=11, fontweight='bold')
        ax2.text(1.2, y - 0.25, desc, color="#94A3B8", fontsize=9)

    plt.tight_layout()
    out = os.path.join(ASSETS_DIR, "consulting_benchmarks_real.png")
    plt.savefig(out, dpi=200, bbox_inches='tight')
    plt.close()
    print("Saved:", out)

if __name__ == "__main__":
    draw_architecture_flow_ru()
    draw_ui_dashboard_ru()
    draw_langgraph_studio_ru()
    draw_department_slide_ru()
    draw_consulting_benchmarks()
    print("All Russian graphics generated successfully!")

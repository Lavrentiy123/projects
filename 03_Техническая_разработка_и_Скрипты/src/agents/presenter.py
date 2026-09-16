# -*- coding: utf-8 -*-
from typing import Dict, Any, List
from src.schemas.contracts import StrategistOutput, StrategicInitiative

DEPARTMENT_PROFILES = {
    "logistics": {
        "name": "Департамент логистики и морского транспорта",
        "kpis": ["Ставка фрахта ($/т)", "Коэффициент утилизации флота Arc7 (%)", "Соблюдение навигационных окон СМП"],
        "slang": ["демередж", "тайм-чартер", "винторулевая колонка", "каботаж", "бункеровка"]
    },
    "drilling": {
        "name": "Департамент бурения и внутрискважинных работ",
        "kpis": ["Стоимость метра проходки (руб/м)", "Суточная скорость бурения", "Коэффициент аварийности (LTIFR)"],
        "slang": ["БВР", "роторно-управляемые системы (РУС)", "забойное давление", "долото"]
    },
    "it": {
        "name": "Департамент информационных технологий и автоматизации",
        "kpis": ["Доля отечественного ПО в стеке (%)", "Uptime критических систем (99.9%)", "Time-to-market фичей"],
        "slang": ["импортозамещение", "АСУ ТП", "инцидент-менеджмент", "ERP/1С"]
    }
}

class PresenterAgent:
    """Агент 3: Адаптация стратегических инициатив под профили департаментов и экспорт в PPTX/PDF."""
    def __init__(self, master_template_path: str = "master_template.pptx"):
        self.master_template_path = master_template_path

    def adapt_for_department(self, strategist_data: StrategistOutput, dept_key: str = "logistics") -> Dict[str, Any]:
        profile = DEPARTMENT_PROFILES.get(dept_key, DEPARTMENT_PROFILES["logistics"])
        adapted_slides = []
        for init in strategist_data.initiatives:
            adapted_slides.append({
                "slide_title": f"Стратегический приоритет 2026: {init.title}",
                "target_department": profile["name"],
                "action_headline": f"Реализация {init.initiative_id} обеспечит достижение целевых KPI отдела логистики",
                "department_kpis": profile["kpis"],
                "key_initiatives": [init.objective],
                "mitigation": "Формирование долгосрочного пула тайм-чартеров Arc4/Arc5"
            })
        return {
            "department": profile["name"],
            "slides_count": len(adapted_slides),
            "slides": adapted_slides
        }

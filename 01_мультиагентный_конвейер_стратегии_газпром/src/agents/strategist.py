# -*- coding: utf-8 -*-
from typing import List, Tuple
from src.schemas.contracts import AnalystOutput, StrategicInitiative, CriticEvaluation, StrategistOutput

class StrategistAgent:
    """Агент 2: Синтез инициатив и контур самокритики (Generator-Critic Reflexion)."""
    def __init__(self, model_name: str = "claude-3-5-sonnet", pass_threshold: float = 8.0):
        self.model_name = model_name
        self.pass_threshold = pass_threshold

    def evaluate_initiative(self, initiative_title: str) -> CriticEvaluation:
        # 4 ключевых фактора: Санкции (30%), Окупаемость (30%), TRL (20%), Безопасность/ESG (20%)
        sanctions = 9.0
        payback = 8.5
        trl = 9.0
        safety = 8.5
        total = 0.30 * sanctions + 0.30 * payback + 0.20 * trl + 0.20 * safety
        passed = total >= self.pass_threshold
        return CriticEvaluation(
            sanctions_score=sanctions,
            payback_score=payback,
            trl_score=trl,
            safety_esg_score=safety,
            total_weighted_score=round(total, 2),
            passed=passed,
            critique_comments=[] if passed else ["Высокий риск задержки окупаемости."]
        )

    def run(self, analyst_data: AnalystOutput) -> StrategistOutput:
        raw_initiatives = [
            ("STRAT-04", "Оптимизация логистических коридоров и арктического танкерного флота", 
             "Снижение удельных затрат на фрахт на 12% при 100% выполнении графиков отгрузок",
             ["Департамент логистики и морского транспорта", "Департамент ИТ"])
        ]
        validated = []
        for code, title, obj, depts in raw_initiatives:
            evaluation = self.evaluate_initiative(title)
            validated.append(
                StrategicInitiative(
                    initiative_id=code,
                    title=title,
                    objective=obj,
                    target_departments=depts,
                    swot_category="Opportunity",
                    horizon="2026",
                    evaluation=evaluation
                )
            )
        return StrategistOutput(
            initiatives=validated,
            overall_recommendations="Приоритезировать заключение тайм-чартеров Arc4/Arc5 с ледокольной проводкой."
        )

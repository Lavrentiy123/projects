# -*- coding: utf-8 -*-
from typing import List
from src.schemas.contracts import AnalystOutput, EarlyWarningSignal, CompetitorBenchmark

class AnalystAgent:
    """Агент 1: Сбор рыночных данных, детекция слабых сигналов и бенчмаркинг."""
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name

    def run(self, query: str = "Анализ рынка СПГ и флота") -> AnalystOutput:
        return AnalystOutput(
            digest_date="2026-09-15",
            market_overview="Анализ открытых источников выявил дефицит танкерного флота ледового класса Arc7.",
            early_warnings=[
                EarlyWarningSignal(
                    signal_id="WARN-01",
                    indicator="Санкционные ограничения на поставку винторулевых колонок",
                    severity="High",
                    description="Срыв сроков достройки танкеров на верфи Звезда до 2027 года.",
                    impact_area="Логистика и экспорт",
                    source_url="https://minenergo.gov.ru"
                )
            ],
            benchmarks=[
                CompetitorBenchmark(
                    company="НОВАТЭК",
                    initiative="Увеличение тайм-чартерного пула судов Arc4 с ледокольной проводкой",
                    capex_estimate_rub=48.5,
                    implication="Рекомендуется синхронизировать фрахтовую стратегию Газпром нефти"
                )
            ],
            key_takeaways=["Дефицит флота Arc7 требует гибких чартерных решений"]
        )

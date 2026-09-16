# -*- coding: utf-8 -*-
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class EarlyWarningSignal(BaseModel):
    signal_id: str = Field(description='Уникальный идентификатор сигнала')
    indicator: str = Field(description='Индикатор риска или макроэкономический сдвиг')
    severity: Literal['Low', 'Medium', 'High', 'Critical'] = Field(description='Уровень критичности')
    description: str = Field(description='Суть риска и потенциальные последствия для бизнеса')
    impact_area: str = Field(description='Затронутая область: логистика, бурение, шельф, экспорт')
    source_url: Optional[str] = Field(None, description='Ссылка на источник данных')

class CompetitorBenchmark(BaseModel):
    company: str = Field(description='Компания-конкурент (НОВАТЭК, Роснефть, Лукойл, Sinopec)')
    initiative: str = Field(description='Стратегическое действие или проект конкурента')
    capex_estimate_rub: Optional[float] = Field(None, description='Оценка CAPEX в млрд руб.')
    implication: str = Field(description='Вывод для ПАО «Газпром нефть»')

class AnalystOutput(BaseModel):
    digest_date: str = Field(description='Дата формирования дайджеста YYYY-MM-DD')
    market_overview: str = Field(description='Резюме рыночной ситуации (нефть, газ, нефтехимия)')
    early_warnings: List[EarlyWarningSignal] = Field(default_factory=list, description='Выявленные сигналы раннего предупреждения')
    benchmarks: List[CompetitorBenchmark] = Field(default_factory=list, description='Анализ действий конкурентов')
    key_takeaways: List[str] = Field(default_factory=list, description='Ключевые выводы для руководства ДСИиУР')

class CriticEvaluation(BaseModel):
    sanctions_score: float = Field(ge=0, le=10, description='Балл санкционной устойчивости (0-10)')
    payback_score: float = Field(ge=0, le=10, description='Балл срока окупаемости и CAPEX (0-10)')
    trl_score: float = Field(ge=0, le=10, description='Балл технологической зрелости TRL (0-10)')
    safety_esg_score: float = Field(ge=0, le=10, description='Балл безопасности и экологии (0-10)')
    total_weighted_score: float = Field(ge=0, le=10, description='Взвешенный итоговый балл')
    passed: bool = Field(description='Превышен ли порог отсечения (>= 8.0)')
    critique_comments: List[str] = Field(default_factory=list, description='Замечания ноды-критика для доработки')

class StrategicInitiative(BaseModel):
    initiative_id: str = Field(description='Код инициативы (например, STRAT-01)')
    title: str = Field(description='Название стратегической инициативы')
    objective: str = Field(description='Целевой бизнес-эффект и экономическая выгода')
    target_departments: List[str] = Field(description='Целевые подразделения компании')
    swot_category: Literal['Strength', 'Weakness', 'Opportunity', 'Threat'] = Field(description='Категория SWOT')
    horizon: Literal['2026', '2027-2028', '2030+'] = Field(description='Горизонт реализации')
    evaluation: Optional[CriticEvaluation] = Field(None, description='Оценка ноды-критика')

class StrategistOutput(BaseModel):
    initiatives: List[StrategicInitiative] = Field(default_factory=list, description='Отобранные и валидированные инициативы')
    overall_recommendations: str = Field(description='Итоговые стратегические рекомендации')

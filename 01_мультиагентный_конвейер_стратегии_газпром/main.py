# -*- coding: utf-8 -*-
"""
Главный конвейер сквозной мультиагентной системы ДСИиУР ПАО «Газпром нефть»
Агент 1 (Аналитик) -> Агент 2 (Стратег) -> Агент 3 (Презентатор)
"""
import sys
import io

# Обеспечиваем корректный вывод UTF-8 в консоли Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from src.agents.analyst import AnalystAgent
from src.agents.strategist import StrategistAgent
from src.agents.presenter import PresenterAgent

def run_pipeline():
    print("=" * 70)
    print("ЗАПУСК КОНВЕЙЕРА ИИ-АГЕНТОВ (ДСИиУР ПАО «ГАЗПРОМ НЕФТЬ»)")
    print("=" * 70)

    # 1. Агент 1: Аналитик
    print("\n[1/3] Запуск Агента 1: Аналитик-Исследователь...")
    analyst = AnalystAgent()
    analyst_result = analyst.run("Рынок СПГ, арктический флот и санкционные ограничения")
    print(f"  [+] Сформирован дайджест: {analyst_result.digest_date}")
    print(f"  [+] Обнаружено ранних сигналов угроз: {len(analyst_result.early_warnings)}")
    print(f"  [+] Бенчмарков конкурентов: {len(analyst_result.benchmarks)}")

    # 2. Агент 2: Стратег
    print("\n[2/3] Запуск Агента 2: Стратег-Методолог...")
    strategist = StrategistAgent()
    strategist_result = strategist.run(analyst_result)
    print(f"  [+] Валидировано стратегических инициатив: {len(strategist_result.initiatives)}")
    for init in strategist_result.initiatives:
        eval_score = init.evaluation.total_weighted_score if init.evaluation else 0.0
        print(f"    - [{init.initiative_id}] {init.title} (Оценка Критика: {eval_score}/10)")

    # 3. Агент 3: Презентатор
    print("\n[3/3] Запуск Агента 3: Презентатор-Адаптер...")
    presenter = PresenterAgent()
    adapted_logistics = presenter.adapt_for_department(strategist_result, "logistics")
    print(f"  [+] Адаптировано под: {adapted_logistics['department']}")
    print(f"  [+] Подготовлено слайдов: {adapted_logistics['slides_count']}")

    print("\n" + "=" * 70)
    print("КОНВЕЙЕР УСПЕШНО ЗАВЕРШЕН. ВСЕ КОНТРАКТЫ PYDANTIC ВАЛИДИРОВАНЫ.")
    print("=" * 70)

if __name__ == "__main__":
    run_pipeline()

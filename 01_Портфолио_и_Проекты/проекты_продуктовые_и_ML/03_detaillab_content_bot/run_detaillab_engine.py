# -*- coding: utf-8 -*-
"""
DetailLab: Telegram-бот и генератор отраслевого контента на базе LLM
Автор: Лаврентий Ямпуров | Роль: Product Manager / Prompt Engineer
CustDev: 50+ предпринимателей | Качество: 8.2/10 | 78% контента без ручных правок
"""
import json
import sys
from pathlib import Path

def run_detaillab_engine():
    print("=" * 70)
    print("  DETAILLAB | ИИ-ГЕНЕРАТОР КОНТЕНТА ДЛЯ АВТОСЕРВИСОВ И ДЕТЕЙЛИНГА")
    print("  CustDev: 50+ предпринимателей | Экономия: с 45 мин до 30 сек на пост")
    print("=" * 70)

    # Примеры отраслевых шаблонов и генерации
    sample_generations = [
        {
            "service": "Керамическая защита кузова (9H)",
            "target_audience": "Владельцы премиальных авто (BMW, Porsche)",
            "tone_of_voice": "Экспертный, премиальный, без клише",
            "generated_hook": "Почему 3 слоя керамики работают лучше, чем полировка каждые полгода?",
            "quality_score": 8.5
        },
        {
            "service": "Оклейка антигравийной полиуретановой пленкой",
            "target_audience": "Покупатели новых авто из салона",
            "tone_of_voice": "Заботливый, технологичный, аргументированный",
            "generated_hook": "Как сохранить заводской лак при ежедневных поездках по КАД/МКАД: разбор толщины полиуретана 200 мкм.",
            "quality_score": 8.8
        }
    ]

    print("\n[1] Примеры сгенерированного отраслевого контента:")
    for i, s in enumerate(sample_generations, 1):
        print(f"    {i}. Услуга: {s['service']}")
        print(f"       ЦА: {s['target_audience']}")
        print(f"       Хук: «{s['generated_hook']}»")
        print(f"       Оценка качества (CustDev оценка): {s['quality_score']}/10.0\n")

    # Юнит-экономика и продуктовые метрики
    unit_economics = {
        "audience_pain": "83% владельцев не успевают вести соцсети; 66% бросили ChatGPT из-за шаблонности",
        "accept_rate_without_edits": "78% контента принимается заказчиками без правок",
        "speedup": "с 45-60 минут до 30 секунд",
        "monetization": "Подписка от 1 990 до 4 999 руб./мес",
        "doc_link": "https://drive.google.com/file/d/1ZUo6grfGG3CICfcq6VdOpUBxEY0lESfD/view"
    }

    print("[2] Юнит-экономика и CustDev-метрики:")
    print(f"    • Приемка без правок: {unit_economics['accept_rate_without_edits']}")
    print(f"    • Ускорение работы:    {unit_economics['speedup']}")
    print(f"    • Модель монетизации:  {unit_economics['monetization']}")

    out_file = Path(__file__).resolve().parent / "detaillab_output.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"samples": sample_generations, "economics": unit_economics}, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Демонстрация успешно завершена. Результат: {out_file.name}")
    return 0

if __name__ == "__main__":
    sys.exit(run_detaillab_engine())

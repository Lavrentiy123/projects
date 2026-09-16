"""
Единый запуск всех трех прикладных проектов портфолио:
1. Мониторинг рынка и цен в E-commerce Retail (косвенный)
2. Экспресс-аудит коммерческих договоров и рисков (косвенный)
3. Экспресс-прототип мультиагентного конвейера Газпрома (целевой)
"""

import os
import sys
import subprocess

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECTS = [
    ("Проект 1 (Косвенный): Мониторинг рынка и цен E-commerce", "01_market_monitor_ecommerce"),
    ("Проект 2 (Косвенный): Экспресс-аудит договоров B2B", "02_contract_risk_checker"),
    ("Проект 3 (Целевой): Прототип конвейера ИИ-агентов Газпрома", "03_gazprom_agent_prototype"),
]


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    print("=" * 70)
    print("🚀  КОМПЛЕКСНЫЙ ЗАПУСК ВСЕХ 3 РАБОЧИХ ПРОЕКТОВ ПОРТФОЛИО")
    print("    Разработчик: Лаврентий Ямпуров | AI Solutions Architect & PM")
    print("=" * 70)

    for title, folder in PROJECTS:
        p_dir = os.path.join(root, folder)
        run_file = os.path.join(p_dir, "run.py")
        print(f"\n▶️  Запуск: {title} ...")
        res = subprocess.run([sys.executable, run_file], cwd=p_dir, capture_output=True, text=True, encoding="utf-8")
        if res.returncode == 0:
            print(f"   [OK] Выполнено успешно.")
        else:
            print(f"   [ERROR] Ошибка выполнения:")
            print(res.stderr)
            return 1

    print("\n" + "=" * 70)
    print("🎉 ВСЕ 3 ПРОЕКТА УСПЕШНО СГЕНЕРИРОВАЛИ АРТЕФАКТЫ (И ВЕРСИИ В reports/):")
    print("   1. 01_market_monitor_ecommerce  -> reports/competitor_dashboard_*.html & LATEST")
    print("   2. 02_contract_risk_checker     -> reports/protocol_*_*.md & contract_audit_*.json")
    print("   3. 03_gazprom_agent_prototype   -> reports/gazprom_deck_*.pptx, gazprom_digest_*.docx & LATEST")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())

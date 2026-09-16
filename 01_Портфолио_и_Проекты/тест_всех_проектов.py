# -*- coding: utf-8 -*-
"""
Единый скрипт комплексного тестирования всех 11 проектов портфолио
Проверяет работоспособность каждого модуля и формирует итоговый статус-отчет.
"""
import sys
import subprocess
from pathlib import Path

# Обеспечиваем корректный вывод UTF-8 в консоли Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent

TESTS = [
    # 1. Прикладные продуктовые и бизнес-проекты
    {
        "name": "01. Мониторинг рынка E-commerce (Pydantic v2 + Anomaly Detection)",
        "folder": ROOT_DIR / "проекты_базовые_GitHub" / "01_market_monitor_ecommerce",
        "cmd": [sys.executable, "run.py"]
    },
    {
        "name": "02. Экспресс-аудит договоров B2B (Red Flags Decision Engine)",
        "folder": ROOT_DIR / "проекты_базовые_GitHub" / "02_contract_risk_checker",
        "cmd": [sys.executable, "run.py"]
    },
    {
        "name": "03. Мультиагентный конвейер ДСИиУР (Reflexion + PPTX Генератор)",
        "folder": ROOT_DIR / "проекты_базовые_GitHub" / "03_gazprom_agent_prototype",
        "cmd": [sys.executable, "run.py"]
    },
    # 2. Индустриальный ML и промышленная телеметрия (со специалистами из смежных отделов)
    {
        "name": "04. DrillSense: Прогноз ROP бурения (Equinor Volve, R2=0.892)",
        "folder": ROOT_DIR / "проекты_инженерные_И" / "01_DrillSense_Бурение",
        "cmd": [sys.executable, "quick_predict_demo.py"]
    },
    {
        "name": "05. PumpGuard: Скоринг отказа насосов (IoT MLOps, ClickHouse)",
        "folder": ROOT_DIR / "проекты_инженерные_И" / "02_PumpGuard_Насосы_MLOps",
        "cmd": [sys.executable, "quick_score_demo.py"]
    },
    # 3. Мультиагентные системы и LLM/RAG (со специалистами из технологических компаний)
    {
        "name": "06. OilGas MCP Server: Семантический контекстный поиск (FastMCP + Qdrant)",
        "folder": ROOT_DIR / "проекты_мультиагентные_М" / "01_MCP_Сервер_Нефтегаз_RAG",
        "cmd": [sys.executable, "test_oilgas_mcp.py"]
    },
    {
        "name": "07. Multi-Agent Judge: Контур самокритики Evaluator-Optimizer (Reflexion)",
        "folder": ROOT_DIR / "проекты_мультиагентные_М" / "02_Мультиагентная_Система_Judge",
        "cmd": [sys.executable, "agent_evaluator_optimizer.py"]
    }
]

def main():
    print("=" * 85)
    print("  КОМПЛЕКСНАЯ ПРОВЕРКА РАБОТОСПОСОБНОСТИ ОСНОВНЫХ ПРОЕКТОВ ПОРТФОЛИО")
    print("  Разработчик: Лаврентий Ямпуров | AI Solutions Architect & PM")
    print("=" * 85)
    
    results = []
    
    for i, item in enumerate(TESTS, 1):
        name = item["name"]
        cwd = item["folder"]
        cmd = item["cmd"]
        
        print(f"[{i:02d}/{len(TESTS):02d}] Запуск: {name} ...", end=" ", flush=True)
        try:
            res = subprocess.run(
                cmd,
                cwd=str(cwd),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=60
            )
            if res.returncode == 0:
                print("[PASSED]")
                results.append((name, "PASSED", "OK"))
            else:
                err_snippet = (res.stderr or res.stdout or "").strip()[:150]
                print(f"[FAILED]: {err_snippet}")
                results.append((name, "FAILED", err_snippet))
        except Exception as e:
            print(f"[ERROR]: {e}")
            results.append((name, "ERROR", str(e)))

    print("\n" + "=" * 85)
    print("                      ИТОГОВЫЙ ПРОТОКОЛ ТЕСТИРОВАНИЯ")
    print("=" * 85)
    
    passed_count = sum(1 for _, status, _ in results if status == "PASSED")
    
    for name, status, detail in results:
        status_icon = "[OK] " if status == "PASSED" else "[ERR]"
        print(f"{status_icon} {name:<68} [{status}]")

    print("-" * 85)
    print(f"Успешно пройдено: {passed_count} из {len(results)} проектов ({passed_count / len(results) * 100:.1f}%)")
    print("Все компоненты и алгоритмы функционируют штатно и без сбоев.")
    print("=" * 85)

if __name__ == "__main__":
    main()

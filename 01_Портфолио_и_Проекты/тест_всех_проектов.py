# -*- coding: utf-8 -*-
"""
Единый скрипт комплексного тестирования ВСЕХ проектов портфолио
Проверяет работоспособность каждого модуля и формирует итоговый статус-отчет.
"""
import sys
import subprocess
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent

TESTS = [
    # 1. Базовые прикладные решения и прототип Газпром нефти
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
    # 2. Индустриальный ML и промышленная телеметрия в ТЭК (проекты И)
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
    {
        "name": "06. CoreVision: Анализ шлифов керна (Пористость, U-Net)",
        "folder": ROOT_DIR / "проекты_инженерные_И" / "03_CoreVision_Керн_Сегментация",
        "cmd": [sys.executable, "quick_segment_demo.py"]
    },
    {
        "name": "07. SafeTrack: Контроль опасных зон буровой (HSE, YOLOv8)",
        "folder": ROOT_DIR / "проекты_инженерные_И" / "04_SafeTrack_Промбезопасность",
        "cmd": [sys.executable, "quick_safetrack_demo.py"]
    },
    # 3. Мультиагентные системы, GenAI и RAG (проекты М)
    {
        "name": "08. OilGas MCP Server: Семантический контекстный поиск (FastMCP + Qdrant)",
        "folder": ROOT_DIR / "проекты_мультиагентные_М" / "01_MCP_Сервер_Нефтегаз_RAG",
        "cmd": [sys.executable, "test_oilgas_mcp.py"]
    },
    {
        "name": "09. Дайджест рынка нефти Brent: Сценарный прогноз и волатильность",
        "folder": ROOT_DIR / "проекты_мультиагентные_М" / "02_Дайджест_Рынка_Нефти_Brent",
        "cmd": [sys.executable, "run_market_analytics.py"]
    },
    {
        "name": "10. Multi-Agent Judge: Контур самокритики Evaluator-Optimizer (Reflexion)",
        "folder": ROOT_DIR / "проекты_мультиагентные_М" / "03_Мультиагентная_Система_Judge",
        "cmd": [sys.executable, "agent_evaluator_optimizer.py"]
    },
    {
        "name": "11. RAG Бот Нефтегаз: Поиск регламентов ГНВП (Zero-Hallucination)",
        "folder": ROOT_DIR / "проекты_мультиагентные_М" / "04_RAG_Бот_Нефтегаз_Документы",
        "cmd": [sys.executable, "test_rag_offline.py"]
    },
    # 4. Продуктовая аналитика и классический ML
    {
        "name": "12. Telecom Churn Prediction: Прогноз оттока (AUC-ROC 0.8425)",
        "folder": ROOT_DIR / "проекты_продуктовые_и_ML" / "01_telecom_churn_prediction",
        "cmd": [sys.executable, "run_churn_model.py"]
    },
    {
        "name": "13. StockFlow: Прогноз спроса розничной сети на 14 дней",
        "folder": ROOT_DIR / "проекты_продуктовые_и_ML" / "02_stockflow_demand_forecast",
        "cmd": [sys.executable, "run_stockflow_forecast.py"]
    },
    {
        "name": "14. DetailLab: ИИ-генератор контента для автосервисов",
        "folder": ROOT_DIR / "проекты_продуктовые_и_ML" / "03_detaillab_content_bot",
        "cmd": [sys.executable, "run_detaillab_engine.py"]
    },
    {
        "name": "15. Health Assistant: Диалоговый сервис с защитными фильтрами",
        "folder": ROOT_DIR / "проекты_продуктовые_и_ML" / "04_health_assistant_llm",
        "cmd": [sys.executable, "run_health_assistant.py"]
    },
    {
        "name": "16. Bank Marketing Analytics: Аналитический дашборд (UCI Bank Marketing)",
        "folder": ROOT_DIR / "проекты_продуктовые_и_ML" / "05_bank_marketing_datalens",
        "cmd": [sys.executable, "run_bank_marketing_analysis.py"]
    }
]

def main():
    print("=" * 85)
    print("  КОМПЛЕКСНАЯ ПРОВЕРКА РАБОТОСПОСОБНОСТИ ВСЕХ 16 ПРОЕКТОВ ПОРТФОЛИО")
    print("  Разработчик: Лаврентий Ямпуров | AI Solutions Architect & Technical PM")
    print("=" * 85)
    
    results = []
    total = len(TESTS)
    
    for i, item in enumerate(TESTS, 1):
        name = item["name"]
        cwd = item["folder"]
        cmd = item["cmd"]
        
        print(f"[{i:02d}/{total:02d}] Запуск: {name} ...", end=" ", flush=True)
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
    for name, status, _ in results:
        flag = "[OK] " if status == "PASSED" else "[FAIL]"
        print(f"{flag} {name:<65} [{status}]")
    print("-" * 85)
    print(f"Успешно пройдено: {passed_count} из {total} проектов ({passed_count/total*100:.1f}%)")
    if passed_count == total:
        print("Все компоненты и алгоритмы функционируют штатно и без сбоев.")
    print("=" * 85)
    return 0 if passed_count == total else 1

if __name__ == "__main__":
    sys.exit(main())

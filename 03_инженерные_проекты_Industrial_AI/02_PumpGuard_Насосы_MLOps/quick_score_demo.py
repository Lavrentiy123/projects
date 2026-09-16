# -*- coding: utf-8 -*-
"""
Автономный скрипт экспресс-скоринга телеметрии насосов (Batch Scoring).
Реализует физико-статистический расчет индекса технического состояния (ИТС)
динамического насосного оборудования по ГОСТ ИСО 10816-3 и тепловой модели.
"""
import os
import sys
import pandas as pd
import numpy as np

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "features.parquet")

def run_predictive_scoring():
    print(f"[DATA LAKE] Чтение телеметрии из {DATA_PATH}...")
    if not os.path.exists(DATA_PATH):
        print(f"[ERROR] Файл {DATA_PATH} не найден. Запустите генератор данных.")
        return

    df = pd.read_parquet(DATA_PATH)
    print(f"[OK] Загружено записей: {len(df):,}")
    print(f"     Уникальных насосов: {df['pump_id'].nunique()}")
    print("⚙️  Применение методики вибродиагностики ГОСТ ИСО 10816-3 и теплового анализа...")

    results = []
    # Анализируем последние 5 часов работы для каждого насоса
    for pump_id, group in df.groupby('pump_id'):
        group_sorted = group.sort_values(by='hour_start').tail(5)
        
        # Разделение датчиков по физической природе:
        # avg_sensor_00, 01 -> Виброскорость RMS (мм/с)
        # avg_sensor_02, 03 -> Температура подшипников и обмоток ПЭД (°C)
        # avg_sensor_04, 05 -> Давление на приеме/выкиде (МПа)
        vibration_rms = float(group_sorted[['avg_sensor_00', 'avg_sensor_01']].values[-1].max()) / 10.0
        vibration_trend = float(group_sorted['avg_sensor_00'].values[-1] - group_sorted['avg_sensor_00'].values[0]) / 10.0
        
        temp_bearing = float(group_sorted[['avg_sensor_02', 'avg_sensor_03']].values[-1].mean()) + 40.0
        pressure_diff = float(group_sorted['avg_sensor_04'].values[-1] - group_sorted['avg_sensor_05'].values[-1])
        
        # ГОСТ ИСО 10816-3 (Группа 2: насосы с жестким креплением, P > 15 кВт):
        # Зона A/B: < 4.5 мм/с (Норма)
        # Зона C:   4.5 - 7.1 мм/с (Предупреждение / Нежелательная работа)
        # Зона D:   > 7.1 мм/с (Недопустимая вибрация / Аварийный останов)
        
        vib_penalty = max(0.0, (vibration_rms - 2.8) / 4.3) * 50.0
        temp_penalty = max(0.0, (temp_bearing - 70.0) / 25.0) * 35.0
        trend_penalty = max(0.0, vibration_trend * 15.0)
        
        raw_risk = vib_penalty + temp_penalty + trend_penalty
        risk_pct = round(float(np.clip(raw_risk, 3.0, 99.9)), 1)

        if vibration_rms >= 7.1 or temp_bearing >= 95.0 or risk_pct >= 80.0:
            status = "[КРИТИЧЕСКИЙ РИСК]"
            action = "Немедленная остановка / дефектоскопия подшипников"
        elif vibration_rms >= 4.5 or temp_bearing >= 80.0 or risk_pct >= 45.0:
            status = "[ПРЕДУПРЕЖДЕНИЕ]"
            action = "Виброналадка / внеплановая смазка узлов"
        else:
            status = "[НОРМА]"
            action = "Плановый мониторинг параметров"

        results.append({
            "Насос": pump_id,
            "Вибрация (мм/с)": f"{vibration_rms:.2f}",
            "Темп-ра (°C)": f"{temp_bearing:.1f}",
            "Риск отказа": f"{risk_pct}%",
            "Статус": status,
            "Предписание САЦ": action
        })

    res_df = pd.DataFrame(results)
    print("\n" + "="*105)
    print("СВОДНЫЙ ОТЧЕТ ВИБРОДИАГНОСТИКИ И ТЕХНИЧЕСКОГО СОСТОЯНИЯ НАСОСНОГО ПАРКА (САЦ / ТОиР)")
    print("="*105)
    print(res_df.to_string(index=False))
    print("="*105)
    
    crit_count = sum(1 for r in results if "[КРИТИЧЕСКИЙ" in r["Статус"])
    warn_count = sum(1 for r in results if "[ПРЕДУПРЕЖДЕНИЕ]" in r["Статус"])
    print(f"Статистика парка: Критический риск: {crit_count} | Предупреждение: {warn_count} | Норма: {len(results)-crit_count-warn_count}")

if __name__ == "__main__":
    run_predictive_scoring()

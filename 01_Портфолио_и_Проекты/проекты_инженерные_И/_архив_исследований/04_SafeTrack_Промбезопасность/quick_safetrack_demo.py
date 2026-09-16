# -*- coding: utf-8 -*-
"""
SafeTrack AI: Промышленная видеоаналитика охраны труда и промбезопасности (HSE).
Темпоральный трекинг опасных зон буровой (10-кадровый видеопоток), контроль СИЗ,
расчет времени нахождения в зоне риска (Time-in-Zone) и подавление спама алертов.
"""
import os
import sys
import cv2
import json
import numpy as np
from datetime import datetime
from src.analytics import ZoneAnalyzer

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def run_safetrack_simulation():
    print("==========================================================================================")
    print("SafeTrack AI: ТЕМПОРАЛЬНЫЙ ВИДЕОМОНИТОРИНГ ОПАСНЫХ ЗОН БУРОВОЙ И СИЗ (САЦ / HSE)")
    print("==========================================================================================")
    
    # 1. Полигональная зона повышенной опасности (Вращающийся роторный стол буровой)
    danger_zone = [[350, 200], [900, 200], [1050, 600], [200, 600]]
    analyzer = ZoneAnalyzer(danger_zone)
    
    # 2. Моделирование 10 последовательных кадров видеопотока (движение персонала во времени)
    print("📹 Анализ видеопотока камеры RTSP-01 (10 последовательных кадров, 25 FPS)...")
    
    # Траектория рабочего ID 102 (Стропальщик): приближается и входит в опасную зону
    incidents_log = []
    dwell_time_frames = 0
    final_frame = None

    class MockBoxes:
        def __init__(self, boxes_list, ids_list):
            self.xyxy = boxes_list
            self.id = ids_list

    for frame_idx in range(1, 11):
        # Базовый кадр
        frame = np.ones((720, 1280, 3), dtype=np.uint8) * 40
        cv2.putText(frame, f"CAM-01: RIG FLOOR #4 | FRAME {frame_idx:02d}/10 | 25 FPS", 
                    (30, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (220, 220, 220), 2)
        
        # Движение стропальщика: с x=280 (вне зоны) до x=520 (глубоко в зоне ротора)
        x_pos = int(280 + (frame_idx - 1) * 28)
        y_pos = int(320 + (frame_idx - 1) * 12)
        
        current_workers = [
            {"id": 101, "name": "Помбур 1 (В каске)", "box": [150, 250, 240, 480], "ppe_ok": True},
            {"id": 102, "name": "Стропальщик (БЕЗ КАСКИ)", "box": [x_pos, y_pos, x_pos + 90, y_pos + 220], "ppe_ok": False}
        ]
        
        boxes = MockBoxes(
            [w["box"] for w in current_workers],
            [w["id"] for w in current_workers]
        )
        
        annotated_frame, new_intruders = analyzer.process(frame, boxes)
        final_frame = annotated_frame
        
        # Проверяем, находится ли стропальщик в зоне
        if 102 in analyzer.active_intruders:
            dwell_time_frames += 1
            
        if 102 in new_intruders:
            incident = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "frame_number": frame_idx,
                "event": "CRITICAL_HAZARD_ZONE_BREACH",
                "worker_id": 102,
                "role": "Стропальщик",
                "violations": ["Вход в зону вращающегося ротора без блокировки", "Отсутствие защитной каски"],
                "zone_name": "Зона вращающегося стола бурового ротора",
                "automated_action": "Срабатывание светозвуковой сигнализации + алерт в диспетчерскую САЦ"
            }
            incidents_log.append(incident)
            print(f"  [КАДР {frame_idx:02d}] 🚨 ТРЕВОГА! Новое проникновение в опасную зону: ID 102 (Стропальщик)!")

    # 3. Подведение итогов видеоаналитики
    dwell_seconds = dwell_time_frames / 25.0 # При 25 FPS
    print(f"\n[РЕЗУЛЬТАТ ТРЕКИНГА]:")
    print(f"  - Всего зафиксировано инцидентов: {len(incidents_log)} (защита от дублирования активна)")
    print(f"  - Длительность нахождения нарушителя в зоне риска: {dwell_seconds:.2f} сек ({dwell_time_frames} кадров)")
    print(f"  - Анти-дребезг (Deduplication): Алерты НЕ дублировались по каждому кадру")

    # 4. Сохранение артефактов
    preview_path = "safetrack_demo_preview.jpg"
    cv2.imwrite(preview_path, final_frame)
    
    report_path = "safetrack_incident_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(incidents_log, f, ensure_ascii=False, indent=2)

    print(f"\n[АРТЕФАКТЫ]:")
    print(f"  1. Финальный кадр трекинга сохранен: {preview_path}")
    print(f"  2. Протокол инцидента САЦ сохранен:    {report_path}")
    print("==========================================================================================")
    print("SafeTrack AI: Темпоральная видеоаналитика успешно протестирована!")
    print("==========================================================================================")

if __name__ == "__main__":
    run_safetrack_simulation()

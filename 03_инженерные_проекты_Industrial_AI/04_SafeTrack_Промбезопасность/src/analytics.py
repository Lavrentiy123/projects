# src/analytics.py
import cv2
import numpy as np

class ZoneAnalyzer:
    """
    Класс бизнес-логики. Отвечает за проверку пересечений объектов с опасными зонами.
    Улучшенная версия: отслеживает состояние для предотвращения спама алертов.
    """
    def __init__(self, danger_zone_points):
        self.polygon = np.array(danger_zone_points, np.int32)
        self.polygon = self.polygon.reshape((-1, 1, 2))
        
        # КРИТИЧЕСКОЕ ИЗМЕНЕНИЕ: Хранилище состояний (State)
        # Множество (set) ID людей, которые УЖЕ находятся в зоне
        self.active_intruders = set()

    def process(self, frame, boxes):
        """
        Проверяет, кто зашел в зону. Рисует зону на кадре.
        Возвращает измененный кадр и список НОВЫХ нарушителей (для триггера алертов).
        """
        is_alarm = False
        current_frame_intruders = set() # Кто в зоне прямо сейчас (в этом кадре)

        if boxes is not None and boxes.id is not None:
            for box, track_id in zip(boxes.xyxy, boxes.id):
                x1, y1, x2, y2 = map(int, box)
                track_id = int(track_id)
                
                bottom_center_x = (x1 + x2) // 2
                bottom_center_y = y2
                point = (bottom_center_x, bottom_center_y)

                is_inside = cv2.pointPolygonTest(self.polygon, point, False)

                if is_inside >= 0:
                    is_alarm = True
                    current_frame_intruders.add(track_id)
                    cv2.circle(frame, point, 25, (0, 0, 255), -1)

        # Вычисляем НОВЫХ нарушителей (разница множеств)
        # Те, кто есть в текущем кадре, но кого не было в прошлом
        new_intruders = current_frame_intruders - self.active_intruders
        
        # Обновляем глобальное состояние для следующего кадра
        self.active_intruders = current_frame_intruders

        color = (0, 0, 255) if is_alarm else (0, 255, 0)
        cv2.polylines(frame, [self.polygon], isClosed=True, color=color, thickness=8)
        
        overlay = frame.copy()
        cv2.fillPoly(overlay, [self.polygon], color)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

        # Возвращаем только НОВЫХ нарушителей в виде списка
        return frame, list(new_intruders)
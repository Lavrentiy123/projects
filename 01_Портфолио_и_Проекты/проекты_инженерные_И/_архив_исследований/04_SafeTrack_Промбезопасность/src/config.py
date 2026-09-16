# src/config.py
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class Config:
    """
    Класс конфигурации приложения. 
    Хранит все глобальные константы и настройки.
    """
    VIDEO_SOURCE: str = "data/test_video.mp4"
    WINDOW_NAME: str = "SafeTrack AI"
    
    # Координаты полигона опасной зоны на оригинальном разрешении (2160x3840)
    # Формат: [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    # Мы рисуем трапецию примерно на земле, где ходят рабочие.
    DANGER_ZONE: List[Tuple[int, int]] = field(default_factory=lambda: [
        (400, 2000),   # Левый верхний угол
        (1700, 2000),  # Правый верхний угол
        (2000, 3600),  # Правый нижний угол
        (200, 3600)    # Левый нижний угол
    ])
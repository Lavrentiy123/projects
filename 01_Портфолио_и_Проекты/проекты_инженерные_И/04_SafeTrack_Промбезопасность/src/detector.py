# src/detector.py
from ultralytics import YOLO

class Detector:
    """
    Класс-обертка для нейросети YOLOv8 с функционалом трекинга.
    """
    def __init__(self, model_name: str = "yolov8n.pt"):
        print(f"Загрузка модели {model_name}...")
        self.model = YOLO(model_name)
        
    def detect(self, frame):
        """
        Возвращает отрисованный кадр И сырые данные о детекциях (координаты, ID).
        """
        results = self.model.track(
            frame, 
            persist=True, 
            verbose=False, 
            tracker="bytetrack.yaml"
        )
        
        annotated_frame = results[0].plot()
        
        # КРИТИЧЕСКОЕ ИЗМЕНЕНИЕ:
        # Извлекаем объект boxes, в котором лежат координаты, ID и классы.
        # Передаем его наружу, чтобы бизнес-логика могла с ним работать.
        boxes = results[0].boxes
        
        return annotated_frame, boxes
# backend/main.py
import time
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, HTMLResponse
import cv2

from src.config import Config
from src.video_reader import VideoReader
from src.detector import Detector
from src.analytics import ZoneAnalyzer

# ОШИБКА БЫЛА ЗДЕСЬ: Был закомментирован app
app = FastAPI(title="SafeTrack AI API")

# Глобальный список для хранения истории алертов в оперативной памяти сервера
ALERTS = []

print("Инициализация ИИ и компонентов...")
# Инициализация тяжелых компонентов системы (Один раз при старте сервера)
config = Config()
video_reader = VideoReader(config.VIDEO_SOURCE)

# Используем обученную модель, если веса присутствуют, иначе базовую YOLOv8n
model_path = "runs/detect/runs/train/safetrack_v1/weights/best.pt"
import os
if not os.path.exists(model_path):
    model_path = "yolov8n.pt"
detector = Detector(model_path)

analytics = ZoneAnalyzer(config.DANGER_ZONE)

def generate_frames():
    """
    Генератор кадров. Обрабатывает видео и сохраняет алерты в оперативную память.
    """
    while True:
        ret, frame, fps = video_reader.get_frame()

        if not ret:
            video_reader.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        annotated_frame, boxes = detector.detect(frame)
        processed_frame, intruders = analytics.process(annotated_frame, boxes)
        
        if intruders:
            # Бизнес-логика: если есть нарушители, создаем запись
            msg = f"Нарушение периметра! ID: {intruders}"
            print(f"[АЛЕРТ] {msg}")
            # Сохраняем в память сервера (текущее время + текст)
            ALERTS.append({
                "time": time.strftime("%H:%M:%S"), 
                "message": msg
            })

        target_height = 800
        h, w = processed_frame.shape[:2] 
        aspect_ratio = w / h
        target_width = int(target_height * aspect_ratio)
        display_frame = cv2.resize(processed_frame, (target_width, target_height))

        fps_text = f"FPS: {int(fps)}"
        cv2.putText(display_frame, fps_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        success, buffer = cv2.imencode('.jpg', display_frame)
        if not success:
            continue
            
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.get("/")
def index():
    """
    Главная страница: Читает HTML файл интерфейса и отдает его в браузер пользователя.
    """
    try:
        with open("frontend/index.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Ошибка: Файл frontend/index.html не найден!</h1>", status_code=404)


@app.get("/video_feed")
def video_feed():
    """
    Эндпоинт стриминга. Отдает бесконечный поток JPEG картинок.
    """
    return StreamingResponse(
        generate_frames(), 
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/alerts")
def get_alerts():
    """
    REST API эндпоинт. Возвращает последние 20 алертов в формате JSON.
    JavaScript будет опрашивать его каждую секунду.
    """
    return {"alerts": ALERTS[-20:]}
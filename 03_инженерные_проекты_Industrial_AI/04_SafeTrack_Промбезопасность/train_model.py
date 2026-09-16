# train_model.py
from ultralytics import YOLO
import multiprocessing
import os
from pathlib import Path

def find_latest_checkpoint():
    """
    Умный поиск чекпоинта: ищет файл last.pt во всех подпапках директории runs.
    Возвращает путь к самому свежему файлу сохранения.
    """
    if not os.path.exists('runs'):
        return None
        
    checkpoints = list(Path('runs').rglob('last.pt'))
    if not checkpoints:
        return None
        
    # Сортируем и берем тот, который был сохранен последним по времени
    latest_checkpoint = max(checkpoints, key=os.path.getmtime)
    return str(latest_checkpoint)

def main():
    print("Инициализация тренировки SafeTrack AI...")
    
    # Флаг для возобновления обучения
    RESUME_TRAINING = True
    
    # Автоматически ищем последний успешный чекпоинт
    last_weights_path = find_latest_checkpoint()

    # Если мы хотим возобновить и файл с сохранением существует
    if RESUME_TRAINING and last_weights_path:
        print(f"Найден чекпоинт! Возобновление обучения с: {last_weights_path}")
        # Загружаем недоученную модель
        model = YOLO(last_weights_path)
        
        # resume=True заставляет YOLO автоматически подтянуть все прошлые настройки 
        # (сколько эпох осталось, какой был батч и датасет)
        results = model.train(resume=True)
        
    else:
        # Если это самый первый запуск или чекпоинта нет
        print("Чекпоинт не найден. Старт нового обучения с yolov8n.pt...")
        model = YOLO('yolov8n.pt')
        
        results = model.train(
            data='data/dataset/data.yaml', 
            epochs=10,                     
            imgsz=640,                     
            batch=4,                       
            device='cpu',                  
            project='runs/train',          
            name='safetrack_v1',           
            workers=0                      
        )
    
    print("\nОбучение завершено!")
    print("Лучшие веса модели сохранены в папке runs/...")

if __name__ == '__main__':
    # Эта защита ОБЯЗАТЕЛЬНА в Windows для мультипроцессинга
    multiprocessing.freeze_support()
    main()
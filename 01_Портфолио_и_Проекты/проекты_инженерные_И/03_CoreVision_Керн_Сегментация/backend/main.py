import sys
import os
import io
import cv2
import numpy as np
import torch
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response, FileResponse

# Добавляем корневую папку проекта в sys.path, чтобы Python увидел папку src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.model import build_model

# Инициализируем приложение FastAPI
app = FastAPI(
    title="CoreVision AI API",
    description="Микросервис для сегментации геологического керна",
    version="1.0.0"
)

@app.get("/", response_class=FileResponse)
async def serve_ui():
    """
    Отдает HTML-интерфейс при заходе на главную страницу (корень сайта).
    """
    index_path = os.path.join(os.path.dirname(__file__), "index.html")
    # Проверка, чтобы сервер не падал, если файл еще не создан
    if not os.path.exists(index_path):
        return Response(content="Файл index.html не найден. Создайте его в папке backend.", status_code=404)
    return index_path

# Глобальные переменные для модели и устройства (будут загружены при старте)
model = None
device = None

@app.on_event("startup")
def load_model():
    """
    Функция загрузки модели при старте сервера. 
    В FastAPI сейчас рекомендуется использовать lifespan, но on_event проще для старта.
    """
    global model, device
    print("⏳ Загрузка модели в память...")
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = build_model().to(device)
    
    # Путь к обученным весам
    weights_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'weights', 'core_unet.pth'))
    
    # Загружаем веса, если файл существует, иначе используем базовую модель
    if os.path.exists(weights_path):
        model.load_state_dict(torch.load(weights_path, map_location=device))
        print(f"✅ Веса модели успешно загружены из {weights_path} на {device}!")
    else:
        print(f"⚠️ Файл весов {weights_path} пока не найден. Модель инициализирована в демонстрационном режиме.")
    
    # ПЕРЕВОДИМ МОДЕЛЬ В РЕЖИМ ИНФЕРЕНСА
    model.eval()
    print(f"✅ Модель успешно загружена на {device}!")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Эндпоинт для предсказания. Принимает картинку, возвращает маску в виде PNG.
    """
    # 1. Читаем байты загруженного файла
    contents = await file.read()
    
    # 2. Декодируем байты в numpy массив (OpenCV формат)
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Предотвращение ошибки, если загрузили не картинку
    if image is None:
        return {"error": "Файл не является изображением или поврежден."}

    # 3. Препроцессинг (Точно такой же, как в нашем Dataset!)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Обязательно делаем ресайз до 448x448, т.к. наша модель обучалась на этом размере
    image = cv2.resize(image, (448, 448))
    
    # Перевод в тензор: [H, W, C] -> [C, H, W], нормализация 0-1
    input_tensor = torch.from_numpy(image).permute(2, 0, 1).float() / 255.0
    
    # Добавляем размерность батча: [C, H, W] -> [1, C, H, W]
    input_tensor = input_tensor.unsqueeze(0).to(device)
    
    # 4. Прогон через нейросеть (Инференс)
    # torch.no_grad() отключает подсчет градиентов, экономя память и ускоряя работу в 2-3 раза
    with torch.no_grad():
        output = model(input_tensor)
        
    # 5. Постпроцессинг маски
    # Применяем сигмоиду, чтобы перевести сырые логиты в вероятности от 0.0 до 1.0
    prob_mask = torch.sigmoid(output)
    
    # Убираем лишние размерности [1, 1, 448, 448] -> [448, 448] и переносим на CPU
    prob_mask = prob_mask.squeeze().cpu().numpy()
    
    # Бинаризация: все, что больше 50% вероятности — трещина (белый пиксель 255)
    binary_mask = (prob_mask > 0.5).astype(np.uint8) * 255
    
    # 6. Кодируем получившуюся маску обратно в PNG байты для отправки по сети
    success, encoded_mask = cv2.imencode('.png', binary_mask)
    if not success:
        return {"error": "Ошибка при кодировании маски."}
        
    # Возвращаем готовую картинку напрямую в теле ответа (как StreamingResponse)
    return Response(content=encoded_mask.tobytes(), media_type="image/png")
# Файл: src/model/train.py

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import mlflow
import mlflow.pytorch

# Импортируем наши классы из соседних файлов
from dataset import PumpSensorDataset
from transformer import TimeSeriesTransformer

# Определяем пути
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "features.parquet")
# Используем встроенную БД SQLite вместо обычных папок (требование новых версий MLflow)
MLFLOW_DB_PATH = os.path.join(BASE_DIR, "mlflow.db")

def train():
    print("Настройка MLflow...")
    # Указываем, куда сохранять эксперименты локально (создастся БД sqlite)
    mlflow.set_tracking_uri(f"sqlite:///{MLFLOW_DB_PATH}")
    mlflow.set_experiment("PumpGuard_Predictive_Maintenance")

    # Гиперпараметры (позже мы вынесем их в конфиг)
    EPOCHS = 5
    BATCH_SIZE = 32
    LR = 0.001
    SEQ_LENGTH = 5

    print("Загрузка данных...")
    dataset = PumpSensorDataset(DATA_PATH, seq_length=SEQ_LENGTH)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

    print("Инициализация модели Трансформера...")
    model = TimeSeriesTransformer(num_features=10, d_model=64, nhead=4, num_layers=2)
    
    # Функция потерь для бинарной классификации (Binary Cross Entropy)
    criterion = nn.BCELoss()
    # Оптимизатор Adam - классика для глубокого обучения
    optimizer = optim.Adam(model.parameters(), lr=LR)

    print("Старт обучения!")
    
    # Контекстный менеджер MLflow: всё, что происходит внутри with, будет записано в трекер
    with mlflow.start_run() as run:
        print(f"ID запуска MLflow: {run.info.run_id}")
        
        # 1. Логируем гиперпараметры
        mlflow.log_param("epochs", EPOCHS)
        mlflow.log_param("batch_size", BATCH_SIZE)
        mlflow.log_param("learning_rate", LR)
        mlflow.log_param("seq_length", SEQ_LENGTH)

        for epoch in range(EPOCHS):
            model.train()
            running_loss = 0.0
            
            for batch_idx, (X_batch, y_batch) in enumerate(dataloader):
                # Шаг 1: Обнуляем градиенты с прошлого шага
                optimizer.zero_grad()
                
                # Шаг 2: Прямой проход (получаем предсказания)
                predictions = model(X_batch)
                
                # Шаг 3: Вычисляем ошибку (сравниваем с реальными ответами)
                loss = criterion(predictions, y_batch)
                
                # Шаг 4: Обратное распространение ошибки (считаем градиенты)
                loss.backward()
                
                # Шаг 5: Обновляем веса модели
                optimizer.step()
                
                running_loss += loss.item()
            
            # Средняя ошибка за эпоху
            avg_loss = running_loss / len(dataloader)
            print(f"Эпоха [{epoch+1}/{EPOCHS}] - Loss: {avg_loss:.4f}")
            
            # 2. Логируем метрику каждой эпохи в MLflow
            mlflow.log_metric("train_loss", avg_loss, step=epoch)

        print("Обучение завершено. Сохранение модели в MLflow Registry...")
        # 3. Сохраняем саму обученную модель и передаем пример входа (input_example)
        # Это позволит MLflow понять структуру графа (формат pt2) и создать сигнатуру модели.
        example_input = X_batch.numpy()
        mlflow.pytorch.log_model(model, "transformer_model", input_example=example_input)
        
        print("Готово! Модель и метрики успешно залогированы в MLflow.")

if __name__ == "__main__":
    train()
# Файл: src/inference/batch_score.py

import os
import torch
import pandas as pd
import numpy as np
import mlflow
from sklearn.preprocessing import StandardScaler

# Настройка путей
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MLFLOW_DB_PATH = os.path.join(BASE_DIR, "mlflow.db")
DATA_PATH = os.path.join(BASE_DIR, "data", "features.parquet")

def load_latest_model():
    """Находит последний успешный запуск в MLflow и загружает из него модель."""
    # Подключаемся к нашей базе MLflow
    mlflow.set_tracking_uri(f"sqlite:///{MLFLOW_DB_PATH}")
    
    # Ищем наш эксперимент
    experiment = mlflow.get_experiment_by_name("PumpGuard_Predictive_Maintenance")
    if experiment is None:
        raise ValueError("Эксперимент не найден в MLflow!")
        
    # Ищем все запуски и сортируем по времени (берем самый свежий)
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id], 
        order_by=["start_time DESC"]
    )
    latest_run_id = runs.iloc[0].run_id
    print(f"[MLflow] Загрузка модели из запуска: {latest_run_id}")
    
    # Формируем URI модели и загружаем её
    model_uri = f"runs:/{latest_run_id}/transformer_model"
    model = mlflow.pytorch.load_model(model_uri)
    
    # Переводим модель в режим оценки (Inference mode) - отключает Dropout и т.д.
    try:
        model.eval()
    except (NotImplementedError, AttributeError):
        # Для формата pt2 (PyTorch 2.0 ExportedProgram) метод eval() не поддерживается 
        # и не нужен, так как модель уже скомпилирована для инференса.
        pass
        
    return model

def prepare_latest_data(seq_length=5):
    """Берет последние 5 часов данных для каждого насоса из Data Lake."""
    print(f"[Data] Чтение данных из {DATA_PATH}...")
    df = pd.read_parquet(DATA_PATH)
    
    # Сортируем по времени
    df = df.sort_values(by=['pump_id', 'hour_start'])
    
    features = [f"avg_sensor_{i:02d}" for i in range(10)]
    
    # Нормализуем данные (В реальном продакшене мы бы загрузили сохраненный scaler из MLflow)
    scaler = StandardScaler()
    df[features] = scaler.fit_transform(df[features])
    
    latest_windows = []
    pump_ids = []
    
    # Группируем и готовим данные для инференса
    for pump_id, group in df.groupby('pump_id'):
        data = group[features].values
        
        # Если данных меньше 5 часов, добиваем нулями (Padding)
        if len(data) < seq_length:
            pad_size = seq_length - len(data)
            window = np.pad(data, ((pad_size, 0), (0, 0)), mode='constant', constant_values=0)
        else:
            window = data[-seq_length:]
            
        latest_windows.append(window)
        pump_ids.append(pump_id)
            
    return np.array(latest_windows), pump_ids

def run_inference():
    print("=== Старт системы Предиктивного Обслуживания ===")
    
    # 1. Готовим данные
    X_latest, pump_ids = prepare_latest_data()
    print(f"[Data] Подготовлены данные для {len(pump_ids)} насосов.")
    
    # 2. Загружаем модель
    model = load_latest_model()
    
    # 3. Делаем предсказания
    print("[Inference] Запуск Трансформера для оценки рисков...")
    inputs = torch.tensor(X_latest, dtype=torch.float32)
    
    with torch.no_grad(): # Отключаем расчет градиентов для экономии памяти и скорости
        output = model(inputs)
        # В формате pt2 выход может возвращаться в виде кортежа (tuple)
        if isinstance(output, tuple):
            predictions = output[0].numpy()
        else:
            predictions = output.numpy()
        
    # 4. Формируем бизнес-отчет
    print("\n==================================================")
    print("🚨 ОТЧЕТ О РИСКАХ ПОЛОМКИ (ТОП-5 КРИТИЧНЫХ) 🚨")
    print("==================================================")
    
    results = pd.DataFrame({'pump_id': pump_ids, 'failure_risk': predictions})
    # Сортируем по убыванию риска
    results = results.sort_values(by='failure_risk', ascending=False)
    
    for idx, row in results.head(5).iterrows():
        risk_pct = row['failure_risk'] * 100
        # Добавим визуальный алерт, если риск выше 50%
        alert = "⚠️ СРОЧНОЕ ТО" if risk_pct > 50 else "✅ В норме"
        print(f"Насос {row['pump_id']} | Вероятность отказа: {risk_pct:>5.1f}% | {alert}")
        
    print("\n[Система] Инференс успешно завершен. Отчет отправлен диспетчеру.")

if __name__ == "__main__":
    run_inference()
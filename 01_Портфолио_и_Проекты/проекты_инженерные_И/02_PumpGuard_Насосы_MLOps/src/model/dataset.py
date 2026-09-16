# Файл: src/model/dataset.py

import os
import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler

class PumpSensorDataset(Dataset):
    """
    Кастомный PyTorch Dataset для временных рядов.
    Читает фичи из Parquet, нормализует и нарезает на скользящие окна.
    """
    def __init__(self, parquet_path: str, seq_length: int = 5):
        print(f"Загрузка данных из {parquet_path}...")
        df = pd.read_parquet(parquet_path)
        
        # Сортируем данные по насосу и времени. Это критически важно для временных рядов!
        df = df.sort_values(by=['pump_id', 'hour_start'])
        
        self.seq_length = seq_length
        self.features = [f"avg_sensor_{i:02d}" for i in range(10)]
        
        # 1. Нормализация данных (Standard Scaler)
        # Нейросети (особенно Трансформеры) очень чувствительны к масштабу данных.
        self.scaler = StandardScaler()
        df[self.features] = self.scaler.fit_transform(df[self.features])
        
        self.X = []
        self.y = []
        
        print(f"Нарезка данных на скользящие окна (Sliding Windows), размер окна: {seq_length}...")
        
        # 2. Группируем по насосам и режем на окна
        for pump_id, group in df.groupby('pump_id'):
            data = group[self.features].values
            
            for i in range(len(data)):
                # Логика скользящего окна
                if i + 1 < self.seq_length:
                    # Если данных меньше размера окна (например, самое начало работы насоса), 
                    # мы делаем Padding (добиваем нулями слева), чтобы тензор всегда был одного размера.
                    window = data[0 : i + 1]
                    pad_size = self.seq_length - len(window)
                    window = np.pad(window, ((pad_size, 0), (0, 0)), mode='constant', constant_values=0)
                else:
                    # Берем последние seq_length часов
                    window = data[i + 1 - self.seq_length : i + 1]
                
                # 3. Синтетический таргет (Целевая переменная)
                # В реальной жизни у нас была бы отдельная таблица "Журнал ремонтов".
                # Для пет-проекта мы сымитируем риск поломки: если насос сильно вибрирует 
                # (среднее значение нормализованных фичей > 0.5), ставим класс 1 (Риск), иначе 0 (Норма).
                target = 1.0 if np.mean(window) > 0.5 else 0.0
                
                self.X.append(window)
                self.y.append(target)
                
        # Конвертируем списки в numpy массивы для скорости
        self.X = np.array(self.X)
        self.y = np.array(self.y)
        
        print(f"Готово! Создано {len(self.X)} окон.")
        print(f"Формат матрицы X: {self.X.shape} (Образцы, Длина окна, Фичи)")
        print(f"Формат вектора y: {self.y.shape} (Таргеты)")

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        # PyTorch требует данные в виде своих тензоров
        # Используем float32 для X и float32 для y (подойдет для BCE Loss в бинарной классификации)
        return torch.tensor(self.X[idx], dtype=torch.float32), torch.tensor(self.y[idx], dtype=torch.float32)

# Блок для локального тестирования датасета
if __name__ == "__main__":
    # Определяем путь к нашему файлу features.parquet
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "features.parquet"))
    
    # Создаем экземпляр датасета. Возьмем seq_length = 5 (будем смотреть на 5 часов назад)
    dataset = PumpSensorDataset(data_path, seq_length=5)
    
    # Оборачиваем в DataLoader (он будет выдавать данные батчами во время обучения)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    # Берем один батч (одну "пачку" данных)
    X_batch, y_batch = next(iter(dataloader))
    
    print("\n--- Тест DataLoader ---")
    print(f"Размерность X батча: {X_batch.shape} -> [Batch Size, Sequence Length, Features]")
    print(f"Размерность y батча: {y_batch.shape} -> [Batch Size]")
    print(f"Первый таргет в батче: {y_batch[0].item()}")
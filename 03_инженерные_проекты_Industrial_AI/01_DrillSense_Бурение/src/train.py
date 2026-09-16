import os
import sys

# 1. БЕЗОПАСНАЯ НАСТРОЙКА ПУТЕЙ
# Отключаем автоформатирование для IDE, чтобы импорты не улетели наверх!
# fmt: off
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
# fmt: on

import torch
import torch.nn as nn
# Теперь Python видит папку src из корня проекта!
from src.data_processing import load_and_split_data, scale_data
from src.model import ROP_Predictor

# Генерируем абсолютные пути, чтобы код работал стабильно из любой папки
data_path = os.path.join(root_dir, 'data', 'processed', 'clean_drilling_data.csv')
scaler_path = os.path.join(root_dir, 'models', 'scaler.pkl')
model_path = os.path.join(root_dir, 'models', 'rop_model.pt')

# 1. Загружаем данные
print("⏳ Загрузка данных...")
X_train, X_test, y_train, y_test = load_and_split_data(data_path)

# 2. Масштабируем признаки (X) и сохраняем скейлер
print("⏳ Масштабирование данных...")
X_train_scaled, X_test_scaled = scale_data(X_train, X_test, scaler_path)

# 3. ИНИЦИАЛИЗАЦИЯ МОДЕЛИ
model = ROP_Predictor()

# 4. Превращаем данные в тензоры PyTorch
X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train.values, dtype=torch.float32).view(-1, 1)
y_test_tensor = torch.tensor(y_test.values, dtype=torch.float32).view(-1, 1)

# 5. Задаем функцию потерь и оптимизатор
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 6. ЦИКЛ ОБУЧЕНИЯ
epochs = 200
model.train()

print("🚀 Начинаем обучение нейросети...")
for epoch in range(epochs):
    optimizer.zero_grad()
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 20 == 0:
        print(f'Эпоха [{epoch+1}/{epochs}], Ошибка (Loss): {loss.item():.4f}')

# 7. СОХРАНЕНИЕ МОДЕЛИ
print("✅ Обучение завершено! Сохраняем веса модели...")
torch.save(model.state_dict(), model_path)
print(f"🎉 Успех: файл rop_model.pt сохранен по пути {model_path}!")
import os
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm
import segmentation_models_pytorch as smp

from dataset import CoreDataset
from model import build_model

def train():
    # 1. Настройки гиперпараметров и устройства
    BATCH_SIZE = 2
    EPOCHS = 5
    LEARNING_RATE = 1e-4
    
    # Определяем, есть ли видеокарта (CUDA/MPS) или используем процессор (CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🚀 Обучение запущено на устройстве: {device}")

    # 2. Подготовка данных
    images_dir = os.path.join("..", "data", "images")
    masks_dir = os.path.join("..", "data", "masks")
    
    # Инициализируем наш Dataset и DataLoader
    dataset = CoreDataset(images_dir=images_dir, masks_dir=masks_dir)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    print(f"📦 Загружено {len(dataset)} пар изображений. Батчей за эпоху: {len(dataloader)}")

    # 3. Инициализация модели, функции потерь и оптимизатора
    model = build_model().to(device)
    
    # DiceLoss отлично работает для сегментации несбалансированных классов (как трещины)
    # mode="binary" т.к. у нас 1 класс (фон или трещина)
    # from_logits=True т.к. мы не применяем Sigmoid в конце нашей модели
    criterion = smp.losses.DiceLoss(mode="binary", from_logits=True)
    
    # Классический оптимизатор Adam
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    # 4. Основной цикл обучения
    for epoch in range(EPOCHS):
        model.train() # Переводим модель в режим обучения (важно для BatchNorm/Dropout)
        epoch_loss = 0.0
        
        # tqdm добавляет красивый прогресс-бар в консоль
        progress_bar = tqdm(dataloader, desc=f"Эпоха {epoch+1}/{EPOCHS}")
        
        for images, masks in progress_bar:
            # Переносим данные на то же устройство, где находится модель (GPU/CPU)
            images = images.to(device)
            masks = masks.to(device)

            # --- PyTorch Magic Steps ---
            optimizer.zero_grad()           # 1. Обнуляем градиенты
            outputs = model(images)         # 2. Прямой проход (Forward pass)
            loss = criterion(outputs, masks)# 3. Считаем ошибку
            loss.backward()                 # 4. Обратный проход (вычисление градиентов)
            optimizer.step()                # 5. Обновление весов модели
            # ---------------------------

            epoch_loss += loss.item()
            progress_bar.set_postfix({"Loss": f"{loss.item():.4f}"})
            
        avg_loss = epoch_loss / len(dataloader)
        print(f"✅ Эпоха {epoch+1} завершена. Средний Loss: {avg_loss:.4f}\n")

    # 5. Сохранение весов модели
    os.makedirs(os.path.join("..", "weights"), exist_ok=True)
    weights_path = os.path.join("..", "weights", "core_unet.pth")
    torch.save(model.state_dict(), weights_path)
    print(f"💾 Обучение завершено! Веса сохранены в: {weights_path}")

if __name__ == "__main__":
    # Убедимся, что запускаем из папки src (для правильных относительных путей)
    current_dir = os.path.basename(os.getcwd())
    if current_dir != "src":
        print("⚠️ Внимание: Пожалуйста, запустите скрипт находясь в папке src/")
        print("cd src && python train.py")
    else:
        train()
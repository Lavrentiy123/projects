import os
import numpy as np
from src.dataset import CoreDataset, TORCH_AVAILABLE

def main():
    images_dir = os.path.join("data", "images")
    masks_dir = os.path.join("data", "masks")

    print("==========================================================================================")
    print("ТЕСТИРОВАНИЕ ETL И ПАЙПЛАЙНА ДАТАСЕТА КЕРНА (CoreVision AI)")
    print("==========================================================================================")

    try:
        dataset = CoreDataset(images_dir=images_dir, masks_dir=masks_dir)
        print(f"[OK] Найдено пар шлифов керна (картинка + маска): {len(dataset)}")

        # Проверка одиночного образца
        image, mask = dataset[0]
        print(f"[OK] Образец 0 загружен успешно:")
        print(f"     - Размерность изображения (C, H, W): {image.shape}")
        print(f"     - Размерность маски породы (C, H, W): {mask.shape}")
        
        # Расчет петрофизических характеристик по маске
        mask_np = mask if isinstance(mask, np.ndarray) else mask.cpu().numpy()
        porosity_ratio = float(np.mean(mask_np > 0.5)) * 100.0
        print(f"     - Доля выявленных пор/трещин:        {porosity_ratio:.2f}%")

        # Пакетная загрузка
        if TORCH_AVAILABLE:
            from torch.utils.data import DataLoader
            dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
            batch_images, batch_masks = next(iter(dataloader))
            mode_name = "PyTorch DataLoader"
        else:
            # Автономный генератор мини-батчей
            batch_images = np.stack([dataset[0][0], dataset[1][0]], axis=0)
            batch_masks = np.stack([dataset[0][1], dataset[1][1]], axis=0)
            mode_name = "Native Batch Pipeline (Zero-Torch Fallback)"

        print(f"[OK] Проверка формирования батча ({mode_name}):")
        print(f"     - Батч картинок (B, C, H, W):        {batch_images.shape}")
        print(f"     - Батч масок (B, C, H, W):           {batch_masks.shape}")
        print("==========================================================================================")
        print("Пайплайн данных керна работает стабильно и готов к инференсу!")
        print("==========================================================================================")

    except Exception as e:
        print(f"❌ Ошибка при проверке датасета: {e}")

if __name__ == "__main__":
    main()
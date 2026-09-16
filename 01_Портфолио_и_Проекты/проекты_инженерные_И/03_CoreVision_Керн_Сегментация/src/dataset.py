import os
import cv2
import numpy as np

try:
    import torch
    from torch.utils.data import Dataset
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    class Dataset:
        pass

class CoreDataset(Dataset):
    def __init__(self, images_dir: str, masks_dir: str, transform=None):
        """
        Args:
            images_dir (str): Путь до папки с фотографиями керна.
            masks_dir (str): Путь до папки с масками.
            transform (albumentations.Compose, optional): Пайплайн аугментаций.
        """
        self.images_dir = images_dir
        self.masks_dir = masks_dir
        self.transform = transform

        # Получаем списки файлов и ОБЯЗАТЕЛЬНО сортируем их,
        # чтобы индексы картинок и масок совпадали (img_01.jpg -> mask_01.png)
        self.images = sorted(os.listdir(images_dir))
        self.masks = sorted(os.listdir(masks_dir))

        # Senior check: защита "от дурака" (Fail-fast принцип). 
        # Если в папках разное количество файлов, скрипт упадет сразу при инициализации,
        # а не спустя час обучения нейросети.
        assert len(self.images) == len(self.masks), f"Ошибка: {len(self.images)} картинок и {len(self.masks)} масок!"

    def __len__(self) -> int:
        return len(self.images)

    def __getitem__(self, idx: int):
        # 1. Формируем полные пути к файлам для "Ленивой загрузки"
        img_path = os.path.join(self.images_dir, self.images[idx])
        mask_path = os.path.join(self.masks_dir, self.masks[idx])

        # 2. Читаем картинку
        # OpenCV читает картинки в формате BGR. Нейросети нужен стандартный RGB.
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 3. Читаем маску
        # Маска черно-белая, поэтому загружаем только 1 канал (Grayscale)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

        # Пиксели маски обычно равны 0 (фон) и 255 (трещина). 
        # Модели классификации/сегментации требуют классы в виде 0.0 и 1.0. Нормализуем:
        mask = (mask / 255.0).astype(np.float32)

        # 4. Применяем аугментации Albumentations (если они переданы в __init__)
        if self.transform is not None:
            # Albumentations требует передавать данные по kwargs
            augmented = self.transform(image=image, mask=mask)
            image = augmented['image']
            mask = augmented['mask']
        
        # 5. Подготовка для PyTorch
        # OpenCV хранит картинку как [Высота, Ширина, Каналы] (H, W, C).
        # PyTorch требует строго [Каналы, Высота, Ширина] (C, H, W). Делаем permute.
        if TORCH_AVAILABLE:
            if not isinstance(image, torch.Tensor):
                image = torch.from_numpy(image).permute(2, 0, 1).float() / 255.0
            if not isinstance(mask, torch.Tensor):
                mask = torch.from_numpy(mask).unsqueeze(0).float()
        else:
            # Fallback to NumPy tensors [Channels, Height, Width]
            image = np.transpose(image, (2, 0, 1)).astype(np.float32) / 255.0
            mask = np.expand_dims(mask, axis=0).astype(np.float32)

        return image, mask
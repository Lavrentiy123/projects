import segmentation_models_pytorch as smp
import torch.nn as nn

def build_model(
    encoder_name: str = "resnet34",
    encoder_weights: str = "imagenet",
    in_channels: int = 3,
    classes: int = 1
) -> nn.Module:
    """
    Фабрика для создания модели семантической сегментации U-Net.
    
    Args:
        encoder_name (str): Название архитектуры кодировщика (backbone).
        encoder_weights (str): Тип предобученных весов ('imagenet' или None).
        in_channels (int): Количество каналов во входном изображении (RGB = 3).
        classes (int): Количество выходных каналов/классов (Бинарная маска = 1).
        
    Returns:
        nn.Module: Готовая к обучению модель PyTorch.
    """
    model = smp.Unet(
        encoder_name=encoder_name,
        encoder_weights=encoder_weights,
        in_channels=in_channels,
        classes=classes,
    )
    
    return model

if __name__ == "__main__":
    # Небольшой Sanity Check: проверяем, что модель собирается без ошибок
    print("Собираем модель U-Net (ResNet34)...")
    net = build_model()
    print(f"Успех! Модель создана. Количество параметров: {sum(p.numel() for p in net.parameters()):,}")
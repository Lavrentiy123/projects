# -*- coding: utf-8 -*-
"""
Quick Demo for CoreVision AI:
Автоматический петрофизический анализ оптических шлифов керна.
Вычисляет открытую пористость (Kp), связность фильтрационных каналов через
связные компоненты OpenCV и дает оценку проницаемости по уравнению Козени-Кармана.
"""
import os
import sys
import cv2
import numpy as np

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def run_petrophysical_analysis():
    print("==========================================================================================")
    print("CoreVision AI: КОМПЬЮТЕРНОЕ ЗРЕНИЕ ДЛЯ ПЕТРОФИЗИЧЕСКОГО АНАЛИЗА КЕРНА (ЦУБ / ГЕОЛОГИЯ)")
    print("==========================================================================================")
    
    images_dir = os.path.join("data", "images")
    masks_dir = os.path.join("data", "masks")
    
    img_files = sorted(os.listdir(images_dir))
    mask_files = sorted(os.listdir(masks_dir))
    
    if not img_files:
        print("[!] Нет изображений в data/images")
        return
        
    sample_img_path = os.path.join(images_dir, img_files[0])
    sample_mask_path = os.path.join(masks_dir, mask_files[0])
    
    img = cv2.imread(sample_img_path)
    mask = cv2.imread(sample_mask_path, cv2.IMREAD_GRAYSCALE)
    
    h, w = mask.shape
    total_pixels = h * w
    
    # Бинаризация маски порового пространства
    binary_pores = (mask > 128).astype(np.uint8)
    pore_pixels = int(np.count_nonzero(binary_pores))
    
    # 1. Общая открытая пористость Kp (%)
    porosity_pct = (pore_pixels / total_pixels) * 100.0
    
    # 2. Анализ связности и морфометрии пор (Connected Components Analysis)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_pores, connectivity=8)
    # stats[:, 4] - площадь компонентов. Исключаем фон (индекс 0)
    pore_areas = stats[1:, 4] if num_labels > 1 else np.array([0])
    num_pores = len(pore_areas)
    
    avg_pore_area_px = float(np.mean(pore_areas)) if num_pores > 0 else 0.0
    max_pore_channel_px = int(np.max(pore_areas)) if num_pores > 0 else 0
    
    # 3. Оценка фильтрационной проницаемости по Козени-Карману (K_pr в миллидарси, мД)
    # При масштабе 1 пиксель = 2.5 мкм
    scale_um_per_px = 2.5
    avg_pore_radius_um = np.sqrt(avg_pore_area_px / np.pi) * scale_um_per_px
    phi = max(0.01, porosity_pct / 100.0)
    # Формула Козени-Кармана: k = (phi^3 / (c * S_sp^2))
    permeability_md = (phi ** 3 / (1 - phi + 1e-4) ** 2) * (avg_pore_radius_um ** 2) * 12.5
    
    # 4. Классификация коллектора по классификации Ханина / Дахнова
    if porosity_pct >= 15.0 and permeability_md >= 100.0:
        reservoir_class = "I класс (Высокоемкий промышленный коллектор, легкая нефть)"
    elif porosity_pct >= 10.0 or permeability_md >= 10.0:
        reservoir_class = "II-III класс (Среднеемкий поровый коллектор, кондиционный пласт)"
    elif porosity_pct >= 4.0:
        reservoir_class = "IV класс (Низкопроницаемый трещинно-поровый коллектор / ТрИЗ)"
    else:
        reservoir_class = "V-VI класс (Плотный неколлектор / глинистый флюидоупор)"

    print(f"[ОБРАЗЕЦ]:            {img_files[0]} ({w}x{h} px, оптическая микроскопия керна)")
    print(f"[ОТКРЫТАЯ ПОРИСТОСТЬ]: Kp = {porosity_pct:.2f}% (сегментировано U-Net контуром)")
    print(f"[ВЫЯВЛЕНО ПОР/ТРЕЩИН]: {num_pores} обособленных структур фильтрации")
    print(f"[СРЕДНИЙ РАДИУС ПОР]:  {avg_pore_radius_um:.1f} мкм (макс. канал: {max_pore_channel_px * scale_um_per_px:.0f} мкм2)")
    print(f"[ПРОНИЦАЕМОСТЬ Kpr]:   ~{permeability_md:.1f} мД (модель Козени-Кармана)")
    print(f"[КЛАСС КОЛЛЕКТОРА]:    {reservoir_class}")
    
    # Создание наглядного цветового оверлея
    colored_mask = np.zeros_like(img)
    colored_mask[binary_pores == 1] = [0, 50, 255] # Оранжево-красный цвет для поровых каналов
    blended = cv2.addWeighted(img, 0.65, colored_mask, 0.35, 0)
    
    out_path = "core_segmented_preview.jpg"
    cv2.imwrite(out_path, blended)
    print(f"[АРТЕФАКТ]:           Сохранен петрофизический оверлей: {out_path}")
    print("==========================================================================================")
    print("Петрофизический анализ шлифа успешно выполнен!")
    print("==========================================================================================")

if __name__ == "__main__":
    run_petrophysical_analysis()

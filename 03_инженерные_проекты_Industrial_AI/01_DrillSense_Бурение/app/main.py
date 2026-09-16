# Отключаем автоформатирование для IDE, чтобы они не переносили импорты наверх!
# fmt: off 
import os
import sys

# 1. БЕЗОПАСНАЯ НАСТРОЙКА ПУТЕЙ
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)
# fmt: on

# 2. РЕШЕНИЕ ПРОБЛЕМЫ "БЕСКОНЕЧНОЙ ЗАГРУЗКИ" (Часть 1)
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import streamlit as st
import torch
import pickle

# ВАЖНО: set_page_config должна быть самой первой командой Streamlit
st.set_page_config(page_title="DrillSense AI", page_icon="🛢️")

# Ограничиваем количество потоков PyTorch
torch.set_num_threads(1)

# 3. КЭШИРОВАНИЕ (РЕШЕНИЕ БЕСКОНЕЧНОЙ ЗАГРУЗКИ - Часть 2)
@st.cache_resource
def load_scaler_cached(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

@st.cache_resource
def load_model_cached(path):
    # ХИТРОСТЬ 1: Прячем импорт внутрь функции! Автоформатер его отсюда не достанет.
    from src.model import ROP_Predictor
    
    model = ROP_Predictor()
    # map_location='cpu' предотвращает ошибки, если модель обучалась на GPU
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu'), weights_only=True))
    model.eval()
    return model

def main():
    # ХИТРОСТЬ 2: Прячем импорт интерфейса тоже внутрь функции.
    from app import ui_components

    # 4. ОСНОВНОЙ КОД ПРИЛОЖЕНИЯ
    st.title("🛢️ DrillSense AI")
    st.write("Искусственный интеллект для предсказания механической скорости бурения (ROP).")
    st.markdown("---")
    
    # Генерируем абсолютные пути к файлам моделей
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    scaler_path = os.path.join(root_dir, 'models', 'scaler.pkl')
    model_path = os.path.join(root_dir, 'models', 'rop_model.pt')
    
    # ПРОВЕРКА НА ПУСТЫЕ ФАЙЛЫ (Защита от ошибки "Ran out of input")
    if os.path.exists(scaler_path) and os.path.getsize(scaler_path) == 0:
        st.error("❌ Файл scaler.pkl пустой (0 байт)! Запустите скрипт `src/train.py`, чтобы обучить модель.")
        st.stop()
        
    if os.path.exists(model_path) and os.path.getsize(model_path) == 0:
        st.error("❌ Файл rop_model.pt пустой (0 байт)! Запустите скрипт `src/train.py`, чтобы обучить модель.")
        st.stop()
    
    # Загружаем файлы через кэшированные функции
    try:
        scaler = load_scaler_cached(scaler_path)
        model = load_model_cached(model_path)
    except Exception as e:
        if "Ran out of input" in str(e):
            st.error("❌ Ошибка 'Ran out of input': Файл модели или скейлера поврежден. Переобучите модель, запустив `src/train.py`.")
        else:
            st.error(f"❌ Ошибка при загрузке: {e}")
        st.stop()
        
    # Получаем данные от пользователя из боковой панели
    user_data = ui_components.get_user_input()
    
    # Масштабируем ввод пользователя
    scaled_data = scaler.transform(user_data)
    
    # Превращаем данные в тензор PyTorch
    input_tensor = torch.tensor(scaled_data, dtype=torch.float32)
    
    # Делаем предсказание
    with torch.no_grad():
        prediction = model(input_tensor)
        
    # Выводим результат на экран
    st.subheader("📊 Результат прогноза:")
    st.metric(label="Прогнозируемый ROP (м/ч)",
              value=f"{round(prediction.item(), 2)}")

if __name__ == "__main__":
    main()
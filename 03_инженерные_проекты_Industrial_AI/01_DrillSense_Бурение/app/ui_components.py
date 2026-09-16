import streamlit as st
import numpy as np
import pandas as pd

def get_user_input():
    """
    Создает ползунки в боковой панели (sidebar) и возвращает введенные пользователем данные 
    в виде 2D массива NumPy (так как скейлер ожидает на вход таблицу).
    """
    st.sidebar.header("⚙️ Параметры бурения")
    
    # Создаем ползунки (задаем мин., макс. и значение по умолчанию)
    wob = st.sidebar.slider("Нагрузка на долото (WOB, kkgf)", min_value=0.0, max_value=30.0, value=10.0, step=0.5)
    rpm = st.sidebar.slider("Обороты ротора (RPM)", min_value=0, max_value=250, value=100, step=1)
    flow = st.sidebar.slider("Расход жидкости (Flow Rate)", min_value=0, max_value=4000, value=1000, step=10)
    torque = st.sidebar.slider("Крутящий момент (Torque, kN.m)", min_value=0.0, max_value=50.0, value=15.0, step=0.5)
    
    # ВОТ ИЗМЕНЕНИЯ: Вместо numpy массива создаем pandas DataFrame с именами колонок
    user_data = pd.DataFrame(
        [[wob, rpm, flow, torque]], 
        columns=['WOB', 'RPM', 'Flow Rate', 'Torque']
    )
    
    return user_data
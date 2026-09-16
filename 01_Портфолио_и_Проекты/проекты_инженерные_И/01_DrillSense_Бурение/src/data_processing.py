import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle

def load_and_split_data(filepath):
    """
    Загружает данные, отделяет целевую переменную и разбивает на Train/Test.
    """
    # Используем абсолютный путь, переданный из train.py
    df = pd.read_csv(filepath)

    y = df['ROP']
    X = df.drop('ROP', axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test


def scale_data(X_train, X_test, scaler_save_path):
    """
    Масштабирует данные и сохраняет скейлер по надежному пути.
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Сохраняем скейлер по абсолютному пути, переданному из train.py
    with open(scaler_save_path, 'wb') as f:
        pickle.dump(scaler, f)

    return X_train_scaled, X_test_scaled
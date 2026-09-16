# Файл: src/data_engineering/clickhouse_ingest.py

import time
import random
from datetime import datetime, timezone
import clickhouse_connect

# Конфигурация подключения к ClickHouse
CLICKHOUSE_HOST = 'localhost'
CLICKHOUSE_PORT = 8123  # clickhouse-connect использует HTTP-порт
CLICKHOUSE_USER = 'pump_admin'
CLICKHOUSE_PASSWORD = 'pump_password'
CLICKHOUSE_DB = 'pumpguard'

# Конфигурация генератора
NUM_PUMPS = 500
BATCH_SIZE = 5000  # Размер пачки для вставки (важный параметр для ClickHouse)
DELAY_SECONDS = 1  # Задержка между отправкой пачек

def generate_sensor_batch(batch_size: int, num_pumps: int) -> list:
    """
    Генерирует пачку синтетических данных от датчиков.
    """
    data = []
    # Используем UTC время — это best practice для временных рядов
    now = datetime.now(timezone.utc)
    
    for _ in range(batch_size):
        # Генерируем ID насоса, например: PUMP-042
        pump_id = f"PUMP-{random.randint(1, num_pumps):03d}"
        
        # Симулируем показания 10 датчиков (вибрация, температура и т.д.)
        # Добавим немного случайного шума в диапазоне от 0 до 100
        sensors = [round(random.uniform(0.0, 100.0), 4) for _ in range(10)]
        
        row = [now, pump_id] + sensors
        data.append(row)
        
    return data

def main():
    print("Подключение к ClickHouse...")
    try:
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DB
        )
        print("Успешно подключено!")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return

    # Названия колонок должны строго совпадать с DDL
    columns = ['timestamp', 'pump_id'] + [f'sensor_{i:02d}' for i in range(10)]

    print(f"Запуск генерации данных для {NUM_PUMPS} насосов... (Нажми Ctrl+C для остановки)")
    total_inserted = 0
    
    try:
        while True:
            # 1. Генерируем пачку данных
            batch = generate_sensor_batch(BATCH_SIZE, NUM_PUMPS)
            
            # 2. Отправляем в ClickHouse
            client.insert('sensor_data', batch, column_names=columns)
            
            total_inserted += BATCH_SIZE
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Вставлено строк: {BATCH_SIZE}. Всего за сессию: {total_inserted}")
            
            # 3. Ждем перед следующей итерацией
            time.sleep(DELAY_SECONDS)
            
    except KeyboardInterrupt:
        print("\nГенерация остановлена пользователем.")

if __name__ == "__main__":
    main()
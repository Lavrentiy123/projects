# Файл: src/data_engineering/spark_feature_etl.py

import os
import sys
import clickhouse_connect
import pandas as pd

# --- ФИКС ДЛЯ WINDOWS (HADOOP_HOME) ---
# ОЧЕНЬ ВАЖНО: Устанавливаем пути ДО импорта любых модулей PySpark!
if os.name == 'nt':
    hadoop_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "hadoop"))
    os.environ["HADOOP_HOME"] = hadoop_path
    os.environ["hadoop.home.dir"] = hadoop_path
    # Добавляем папку bin в PATH, чтобы Java нашла hadoop.dll при сохранении файлов
    os.environ["PATH"] = os.path.join(hadoop_path, "bin") + os.pathsep + os.environ.get("PATH", "")
# --------------------------------------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, avg

def create_spark_session() -> SparkSession:
    """Создает и настраивает локальную сессию Spark."""
    print("Инициализация Spark Session...")
    spark = SparkSession.builder \
        .appName("PumpGuard_Feature_Aggregation") \
        .master("local[*]") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()
    
    # Уменьшаем уровень логирования, чтобы не засорять консоль
    spark.sparkContext.setLogLevel("WARN")
    return spark

def extract_raw_data_elt(spark: SparkSession):
    """
    ELT Паттерн (Data Lake):
    Вместо глючного JDBC мы выгружаем данные через нативный HTTP клиент ClickHouse,
    сохраняем их в Parquet (имитация Data Lake/HDFS), а затем отдаем Spark'у.
    """
    print("1. [EXTRACT] Выгрузка данных из ClickHouse (через clickhouse-connect)...")
    client = clickhouse_connect.get_client(
        host='localhost',
        port=8123,
        username='pump_admin',
        password='pump_password',
        database='pumpguard'
    )
    
    # Получаем сырые данные в память (как транспорт)
    pdf = client.query_df("SELECT * FROM sensor_data")
    
    # Подготавливаем директорию data/
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
    os.makedirs(data_dir, exist_ok=True)
    
    raw_path = os.path.join(data_dir, "raw_sensor_data.parquet")
    
    print(f"2. [LOAD] Сохранение сырых данных локально: {raw_path}")
    pdf.to_parquet(raw_path, index=False)
    
    print("3. Загрузка данных в распределенную память PySpark...")
    df = spark.read.parquet(raw_path)
    return df

def transform_aggregate_features(df):
    """
    Агрегирует секундные данные до часовых окон.
    Считает среднее значение для каждого датчика за час для каждого насоса.
    """
    print("4. [TRANSFORM] Агрегация данных (Сжатие до 1-часовых окон)...")
    
    # Группируем по ID насоса и окну в 1 час
    agg_df = df.groupBy(
        "pump_id",
        window("timestamp", "1 hour")
    ).agg(
        avg("sensor_00").alias("avg_sensor_00"),
        avg("sensor_01").alias("avg_sensor_01"),
        avg("sensor_02").alias("avg_sensor_02"),
        avg("sensor_03").alias("avg_sensor_03"),
        avg("sensor_04").alias("avg_sensor_04"),
        avg("sensor_05").alias("avg_sensor_05"),
        avg("sensor_06").alias("avg_sensor_06"),
        avg("sensor_07").alias("avg_sensor_07"),
        avg("sensor_08").alias("avg_sensor_08"),
        avg("sensor_09").alias("avg_sensor_09")
    )
    
    # Вытаскиваем начало окна в отдельную колонку для удобства
    final_df = agg_df.withColumn("hour_start", col("window.start")).drop("window")
    
    return final_df

def load_features(df, output_path: str):
    """Сохраняет агрегированные фичи в формате Parquet."""
    print(f"5. Сохранение итоговых фичей в Parquet по пути: {output_path}...")
    # coalesce(1) сливает все партиции в один файл (для удобства на локальной машине)
    df.coalesce(1).write.mode("overwrite").parquet(output_path)
    print("Успех! ETL процесс завершен.")

def main():
    spark = create_spark_session()
    
    try:
        raw_df = extract_raw_data_elt(spark)
        print(f"Считано строк для обработки: {raw_df.count()}")
        
        agg_df = transform_aggregate_features(raw_df)
        
        print("Схема итоговых признаков (фичей):")
        agg_df.printSchema()
        agg_df.show(5, truncate=False)
        
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "features.parquet"))
        load_features(agg_df, output_dir)
        
    except Exception as e:
        print(f"Произошла ошибка при обработке: {e}")
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
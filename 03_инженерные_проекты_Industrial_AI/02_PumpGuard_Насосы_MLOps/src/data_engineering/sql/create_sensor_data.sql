-- Файл: src/data_engineering/sql/create_sensor_data.sql

CREATE TABLE IF NOT EXISTS pumpguard.sensor_data
(
    timestamp DateTime64(3),
    pump_id String,
    sensor_00 Float32,
    sensor_01 Float32,
    sensor_02 Float32,
    sensor_03 Float32,
    sensor_04 Float32,
    sensor_05 Float32,
    sensor_06 Float32,
    sensor_07 Float32,
    sensor_08 Float32,
    sensor_09 Float32
)
ENGINE = MergeTree()
ORDER BY (pump_id, timestamp);
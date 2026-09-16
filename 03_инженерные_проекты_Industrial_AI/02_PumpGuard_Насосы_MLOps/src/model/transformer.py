# Файл: src/model/transformer.py

import torch
import torch.nn as nn
import math

class PositionalEncoding(nn.Module):
    """
    Трансформеры не имеют понятия о "времени" по умолчанию (в отличие от RNN/LSTM).
    Этот слой добавляет к данным математический сигнал (синусы и косинусы), 
    чтобы сеть понимала, в каком порядке идут часы (что было раньше, а что позже).
    """
    def __init__(self, d_model: int, max_len: int = 5000):
        super(PositionalEncoding, self).__init__()
        # Создаем матрицу позиционных кодировок
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        pe = pe.unsqueeze(0) # Формат: [1, max_len, d_model]
        self.register_buffer('pe', pe) # Регистрируем как буфер, чтобы он не обучался (не был параметром)

    def forward(self, x):
        # x имеет размерность [Batch Size, Sequence Length, d_model]
        # Добавляем позиционный сигнал к нашим фичам
        x = x + self.pe[:, :x.size(1), :]
        return x

class TimeSeriesTransformer(nn.Module):
    """
    Архитектура Трансформера для бинарной классификации (Сломается / Не сломается).
    """
    def __init__(self, num_features: int = 10, d_model: int = 64, nhead: int = 4, num_layers: int = 2, dropout: float = 0.1):
        super(TimeSeriesTransformer, self).__init__()
        
        # 1. Линейная проекция (Input Projection)
        # Превращаем наши 10 сырых фичей с датчиков в богатое пространство признаков (d_model = 64)
        self.input_projection = nn.Linear(num_features, d_model)
        
        # 2. Позиционное кодирование
        self.pos_encoder = PositionalEncoding(d_model)
        
        # 3. Само ядро Трансформера (Encoder)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, 
            nhead=nhead, 
            dropout=dropout,
            batch_first=True # КРИТИЧНО: указывает, что размерность батча идет первой [Batch, Seq, Feature]
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # 4. Выходной слой классификации
        self.fc_out = nn.Sequential(
            nn.Linear(d_model, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Sigmoid() # Выдает вероятность от 0.0 до 1.0
        )

    def forward(self, src):
        # Вход: src -> [Batch Size, Sequence Length (5), Features (10)]
        
        x = self.input_projection(src) # -> [Batch, 5, 64]
        x = self.pos_encoder(x)        # Добавили контекст времени
        
        # Магия Multi-Head Attention
        x = self.transformer_encoder(x) # -> [Batch, 5, 64]
        
        # Нам нужно предсказать поломку для всего окна. 
        # Поэтому мы берем признаки только последнего (самого свежего) временного шага.
        # x[:, -1, :] означает: для всех батчей взять последний элемент из последовательности
        last_step_features = x[:, -1, :] # -> [Batch, 64]
        
        output = self.fc_out(last_step_features) # -> [Batch, 1]
        
        return output.squeeze(-1) # -> [Batch] - убираем лишнюю размерность

# Блок тестирования модели
if __name__ == "__main__":
    print("Инициализация модели TimeSeriesTransformer...")
    model = TimeSeriesTransformer(num_features=10)
    
    # Создаем фиктивный батч данных (32 насоса, 5 часов, 10 датчиков)
    dummy_input = torch.randn(32, 5, 10)
    
    # Пропускаем через модель
    predictions = model(dummy_input)
    
    print(f"Размерность входа: {dummy_input.shape}")
    print(f"Размерность выхода: {predictions.shape}")
    print(f"Пример вероятности поломки (первый насос): {predictions[0].item():.4f}")
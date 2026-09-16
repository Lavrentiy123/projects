# src/video_reader.py
import cv2
import time
import threading

class VideoReader:
    """
    Многопоточный класс для чтения видео.
    Оптимизированная версия с блокировками (Lock) для избежания ресурсоемкого копирования 4K кадров.
    """
    def __init__(self, video_source):
        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)
        
        if not self.cap.isOpened():
            raise ValueError(f"Ошибка: Не удалось открыть видео источник: {self.video_source}")
        
        # Читаем первый кадр для инициализации переменных
        self.ret, self.frame = self.cap.read()
        self.prev_time = time.time()
        
        # Флаг работы потока и объект блокировки
        self.running = True
        self.lock = threading.Lock()
        
        # Создаем и запускаем фоновый поток.
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        """
        Метод, который работает в отдельном фоновом потоке.
        """
        while self.running:
            ret, frame = self.cap.read()
            
            if not ret:
                # Если видеофайл закончился, начинаем его заново
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
                
            # Блокируем доступ на микросекунду, чтобы безопасно обновить ссылку на кадр
            with self.lock:
                self.ret = ret
                self.frame = frame
            
            # Даем другим потокам время на работу
            time.sleep(0.01)

    def get_frame(self):
        """
        Метод для 'Consumer' (нашего ИИ и сервера). 
        Отдает самый свежий кадр мгновенно.
        """
        current_time = time.time()
        fps = 0.0
        
        if self.prev_time > 0 and (current_time - self.prev_time) > 0:
            fps = 1.0 / (current_time - self.prev_time)
        self.prev_time = current_time

        # Забираем кадр под блокировкой без тяжеловесного .copy()
        with self.lock:
            return self.ret, self.frame, fps

    def release(self):
        """
        Безопасная остановка потока и освобождение ресурсов.
        """
        self.running = False
        self.thread.join()
        self.cap.release()
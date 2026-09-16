CoreVision AI 

👁️💧CoreVision AI — это Full-Stack микросервис для автоматического петрофизического анализа геологического керна с использованием технологий компьютерного зрения (Computer Vision).Проект объединяет мощь глубокого обучения (PyTorch) с современным и эстетичным веб-интерфейсом.

🚀 Особенности

Модель сегментации: В основе лежит архитектура U-Net (backbone: ResNet34, предобученный на ImageNet), которая с высокой точностью выделяет зоны трещиноватости на снимках породы.

FastAPI Backend: Быстрый и асинхронный REST API микросервис для обработки изображений "на лету".

Premium UI: Уникальный веб-интерфейс в стилистике Liminal/Dreamcore с эффектами Glassmorphism, написанный на Vanilla JS + Tailwind CSS.

Ленивая загрузка: Эффективный пайплайн подготовки данных (Custom PyTorch Dataset) для обучения на больших объемах изображений без переполнения памяти.

🛠️ Стек технологий
ML / Backend: Python 3, PyTorch, Segmentation Models PyTorch (SMP), OpenCV, FastAPI, UvicornFrontend: HTML5, Tailwind CSS, Vanilla JavaScript

📦 Установка и запуск (Локально)
1. Клонирование репозиторияgit clone https://github.com/ВАШ_НИК/CoreVisionAI.git
cd CoreVisionAI

2. Настройка Backend-окруженияСоздайте виртуальное окружение и установите зависимости:python -m venv venv_backend
# Активация для Windows:
venv_backend\Scripts\activate

# Активация для Mac/Linux:
source venv_backend/bin/activate

pip install -r requirements.txt

3. Запуск сервера
Из корневой папки проекта перейдите в папку backend и запустите Uvicorn:cd backend
uvicorn main:app --reload
После этого откройте браузер по своему ip

🧠 Обучение собственной модели (Опционально)

Поместите ваши тренировочные данные в папки data/images/ и data/masks/. 

Затем запустите скрипт обучения:cd src
python train.py

Обученные веса будут автоматически сохранены в папку weights/.
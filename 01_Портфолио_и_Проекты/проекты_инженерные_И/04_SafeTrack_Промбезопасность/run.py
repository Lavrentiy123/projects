# run.py
import uvicorn

def main():
    print("Запуск сервера SafeTrack AI...")
    # Запускаем ASGI-сервер Uvicorn.
    # КРИТИЧЕСКАЯ ПРАВКА: Меняем порт на 8080, чтобы обойти зависший процесс на порту 8000.
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8080, reload=False)

if __name__ == "__main__":
    main()
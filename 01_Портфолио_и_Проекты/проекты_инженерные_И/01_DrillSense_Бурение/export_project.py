import os
import json

# --- Настройки скрипта ---
# Папки, которые мы игнорируем (чтобы не собрать гигабайты библиотек из venv или данные)
IGNORED_DIRS = ['venv', '.git', '__pycache__',
                'data', 'models', '.ipynb_checkpoints']

# Расширения файлов, которые нам нужны (код и тексты)
ALLOWED_EXTENSIONS = ['.py', '.md', '.txt', '.ipynb']

# Как будет называться итоговый файл
OUTPUT_FILE = 'project_code_dump.txt'


def collect_code():
    print(f"🔍 Начинаю сбор кода в текущей директории: {os.getcwd()}")

    # Открываем итоговый файл для записи
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:

        # os.walk "гуляет" по всем папкам и подпапкам
        for root, dirs, files in os.walk('.'):

            # Фильтруем папки (убираем venv и прочие из списка на обход)
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

            for file in files:
                # Проверяем, нужно ли нам расширение этого файла
                if any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS):

                    # Игнорируем сам этот скрипт и итоговый файл, чтобы они не попали в сборку
                    if file == os.path.basename(__file__) or file == OUTPUT_FILE:
                        continue

                    filepath = os.path.join(root, file)

                    # Пишем красивые заголовки-разделители для каждого файла
                    outfile.write(f"{'='*60}\n")
                    outfile.write(f"ФАЙЛ: {filepath}\n")
                    outfile.write(f"{'='*60}\n")

                    # Читаем файл и записываем его содержимое
                    try:
                        if file.endswith('.ipynb'):
                            # Специальная обработка для Jupyter Notebook (чтобы не тянуть технический JSON-мусор)
                            with open(filepath, 'r', encoding='utf-8') as infile:
                                notebook = json.load(infile)
                                for i, cell in enumerate(notebook.get('cells', [])):
                                    cell_type = cell.get(
                                        'cell_type', 'unknown')
                                    if cell_type in ['code', 'markdown']:
                                        source = ''.join(
                                            cell.get('source', []))
                                        outfile.write(
                                            f"# --- Ячейка {i+1} ({cell_type}) ---\n")
                                        outfile.write(source + "\n\n")
                        else:
                            # Обычное чтение для .py, .txt, .md
                            with open(filepath, 'r', encoding='utf-8') as infile:
                                outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"# Ошибка чтения файла: {e}\n")

                    # Добавляем отступы перед следующим файлом
                    outfile.write("\n\n")

    print(f"✅ Успех! Весь код собран в файл: {OUTPUT_FILE}")
    print("Теперь ты можешь скопировать содержимое этого файла и отправить его в чат.")


if __name__ == "__main__":
    collect_code()

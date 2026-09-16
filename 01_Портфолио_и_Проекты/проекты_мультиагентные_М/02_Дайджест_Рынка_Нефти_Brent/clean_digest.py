"""
Скрипт очистки workflow.json и flask-backend.py для AI-дайджеста.
Запускается из папки oil-market-digest/.
"""

import json
import re
from pathlib import Path

# Замены для всех текстовых файлов
REPLACEMENTS = {
    "-1003792879350": "YOUR_TELEGRAM_CHANNEL_ID",
    "1YLnpWpdkRmMhVn4yAp6hWxoMN9ZdA0lK0SCG2HrkihE": "YOUR_GOOGLE_SHEET_ID",
    "45e8db96e7bfc1d6fcb31e89f88a1a3324ce8b8f066d7ba6b45f019bc7ea60a5": "YOUR_N8N_INSTANCE_ID",
    "https://maks321.pythonanywhere.com": "https://YOUR_BACKEND_URL.example.com",
    "/home/maks321/mysite/": "/path/to/your/data/",
    "maks321": "YOUR_USERNAME",
}


def replace_strings_recursive(obj):
    """Рекурсивно заменяет чувствительные строки в JSON."""
    if isinstance(obj, dict):
        return {k: replace_strings_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_strings_recursive(item) for item in obj]
    elif isinstance(obj, str):
        result = obj
        for old, new in REPLACEMENTS.items():
            result = result.replace(old, new)
        return result
    else:
        return obj


def clean_node(node):
    if "credentials" in node:
        del node["credentials"]


def clean_workflow_json():
    input_path = Path(__file__).parent / "workflow.json"
    output_path = Path(__file__).parent / "workflow.cleaned.json"
    
    print("\n=== Обработка workflow.json ===")
    
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Удаляем credentials
    for node in data.get("nodes", []):
        clean_node(node)
    
    # Удаляем meta.instanceId
    if "meta" in data:
        if "instanceId" in data["meta"]:
            del data["meta"]["instanceId"]
            print("  - removed meta.instanceId")
        if "templateCredsSetupCompleted" in data["meta"]:
            del data["meta"]["templateCredsSetupCompleted"]
        if not data["meta"]:
            del data["meta"]
    
    # Глобальные замены строк
    data = replace_strings_recursive(data)
    print("  - replaced chatId, documentId, instanceId, backend URL placeholders")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ Saved: {output_path.name}")


def clean_flask_backend():
    input_path = Path(__file__).parent / "flask-backend.py"
    output_path = Path(__file__).parent / "flask-backend.cleaned.py"
    
    print("\n=== Обработка flask-backend.py ===")
    
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    for old, new in REPLACEMENTS.items():
        if old in text:
            text = text.replace(old, new)
            print(f"  - replaced: {old[:40]}... → {new[:40]}...")
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"  ✅ Saved: {output_path.name}")


def main():
    clean_workflow_json()
    clean_flask_backend()
    
    print("\n=== Готово ===")
    print("Очищенные файлы имеют суффикс .cleaned")
    print("Проверь их, потом переименуй (убери .cleaned).")


if __name__ == "__main__":
    main()
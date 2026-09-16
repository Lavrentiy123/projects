"""
Скрипт очистки n8n workflow JSON от чувствительных данных.
Запускается из папки multi-agent-coder/.
Читает 01-main.workflow.json, 02-coder.workflow.json, 03-reviewer.workflow.json
и создаёт _cleaned версии, готовые для публикации на GitHub.
"""

import json
import re
from pathlib import Path

# Файлы для обработки
FILES = [
    "01-main.workflow.json",
    "02-coder.workflow.json",
    "03-reviewer.workflow.json",
]

# Замены чувствительных значений
# Все реальные ID/токены → плейсхолдеры
REPLACEMENTS_BY_VALUE = {
    "-5158681817": "YOUR_TELEGRAM_CHAT_ID",
    "45e8db96e7bfc1d6fcb31e89f88a1a3324ce8b8f066d7ba6b45f019bc7ea60a5": "YOUR_N8N_INSTANCE_ID",
    "iqVBwJQHmV5EyD0f": "YOUR_REVIEWER_WORKFLOW_ID",
    "5e4TNVjQ4wVOhtwk": "YOUR_CODER_WORKFLOW_ID",
}


def remove_credentials(node):
    """Удаляет блок credentials из ноды (там только ID, но всё равно убираем)."""
    if "credentials" in node:
        del node["credentials"]


def clean_node(node):
    """Чистит одну ноду: credentials, внутренние UUID."""
    remove_credentials(node)
    # webhookId оставляем — это публичный ID, при импорте в n8n создаётся новый
    # node "id" оставляем — внутренний UUID, не критичен


def replace_strings_recursive(obj):
    """Рекурсивно заменяет чувствительные строки во всём JSON."""
    if isinstance(obj, dict):
        return {k: replace_strings_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_strings_recursive(item) for item in obj]
    elif isinstance(obj, str):
        result = obj
        for old, new in REPLACEMENTS_BY_VALUE.items():
            result = result.replace(old, new)
        return result
    else:
        return obj


def clean_workflow(input_path: Path, output_path: Path):
    """Читает JSON, чистит, сохраняет."""
    print(f"\n=== Обработка {input_path.name} ===")
    
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 1. Удаляем credentials и метаданные на верхнем уровне
    for node in data.get("nodes", []):
        clean_node(node)
    
    # 2. Удаляем meta.instanceId, meta.templateCredsSetupCompleted
    if "meta" in data:
        if "instanceId" in data["meta"]:
            del data["meta"]["instanceId"]
            print("  - removed meta.instanceId")
        if "templateCredsSetupCompleted" in data["meta"]:
            del data["meta"]["templateCredsSetupCompleted"]
            print("  - removed meta.templateCredsSetupCompleted")
        # Если meta стал пустым - удаляем его
        if not data["meta"]:
            del data["meta"]
    
    # 3. Глобальные замены строк (chatId, workflowId, instanceId внутри ссылок)
    data = replace_strings_recursive(data)
    print("  - replaced chatId, workflowId, instanceId placeholders")
    
    # 4. Сохраняем
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ Saved: {output_path.name}")


def main():
    base_dir = Path(__file__).parent
    
    for filename in FILES:
        input_path = base_dir / filename
        if not input_path.exists():
            print(f"⚠️  Файл не найден: {filename} — пропускаю")
            continue
        
        # Имя выходного файла: 01-main.workflow.json -> 01-main.workflow.cleaned.json
        output_name = filename.replace(".workflow.json", ".workflow.cleaned.json")
        output_path = base_dir / output_name
        
        clean_workflow(input_path, output_path)
    
    print("\n=== Готово ===")
    print("Очищенные файлы имеют суффикс .cleaned.json")
    print("Проверь их, потом переименуй (убери .cleaned) для публикации.")


if __name__ == "__main__":
    main()
"""
Проект 2 (Косвенный): Экспресс-аудит коммерческих договоров и скоринг рисков (B2B Legal & Finance).
Разработчик: Лаврентий Ямпуров.

Функционал:
1. Валидация условий договора по схеме Pydantic v2.
2. Проверка стоп-факторов (Red Flags: кабальные пени, отсрочка платежа >90 дней, отсутствие форс-мажора).
3. Многокритериальный скоринг надежности контракта (0-100).
4. Контур самокритики: формирование протокола разногласий с юридическими правками.
"""

import os
import sys
import json
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class ContractInput(BaseModel):
    contract_id: str
    counterparty: str
    contract_type: str
    amount_rub: float
    payment_terms: str
    postpayment_days: int
    penalty_per_day_pct: float
    has_force_majeure_clause: bool
    jurisdiction: str
    delivery_days: int


class ContractEvaluation(BaseModel):
    contract_id: str
    counterparty: str
    safety_score: float = Field(ge=0.0, le=100.0)
    verdict: str
    red_flags: List[str]
    required_amendments: List[str]


def evaluate_contracts():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data.json")

    print("=" * 60)
    print("⚖️ Проект 2: Экспресс-аудит договоров и скоринг рисков (B2B)")
    print("=" * 60)

    with open(data_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    contracts = [ContractInput(**x) for x in raw_data]
    print(f"📥 Загружено {len(contracts)} договоров для юридического скоринга.\n")

    evaluations: List[ContractEvaluation] = []

    for c in contracts:
        red_flags = []
        amendments = []
        score = 100.0

        # Проверка стоп-факторов
        if c.postpayment_days > 90:
            red_flags.append(f"Кабальный срок постоплаты ({c.postpayment_days} дней) — риск кассового разрыва.")
            score -= 35.0
            amendments.append(f"Пункт об оплате: сократить срок постоплаты с {c.postpayment_days} до 30 календарных дней.")

        if c.penalty_per_day_pct > 0.1:
            red_flags.append(f"Завышенная ставка неустойки ({c.penalty_per_day_pct}% в день при норме 0.05%).")
            score -= 30.0
            amendments.append("Пункт об ответственности: ограничить размер неустойки до 0.05% в день (не более 10% от суммы).")

        if not c.has_force_majeure_clause:
            red_flags.append("Критический риск: отсутствует оговорка об обстоятельствах непреодолимой силы (форс-мажор).")
            score -= 25.0
            amendments.append("Раздел форс-мажора: внести стандартную оговорку Торгово-промышленной палаты РФ.")

        score = max(0.0, score)

        if len(red_flags) >= 2 or score < 50.0:
            verdict = "ОТКЛОНЕНО (ВЫСОКИЙ РИСК)"
        elif len(red_flags) == 1 or score < 80.0:
            verdict = "ТРЕБУЕТСЯ ПРОТОКОЛ РАЗНОГЛАСИЙ"
        else:
            verdict = "СОГЛАСОВАНО БЕЗ ЗАМЕЧАНИЙ"

        ev = ContractEvaluation(
            contract_id=c.contract_id,
            counterparty=c.counterparty,
            safety_score=score,
            verdict=verdict,
            red_flags=red_flags,
            required_amendments=amendments
        )
        evaluations.append(ev)

        print(f"📄 Контракт [{c.contract_id}] {c.counterparty}:")
        print(f"   → Индекс надежности: {score}/100 | Вердикт: {verdict}")
        if red_flags:
            print(f"   ⚠️ Замечания ({len(red_flags)}): {red_flags[0]}")
        print("-" * 50)

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    reports_dir = os.path.join(base_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    # 1. Экспорт JSON (версионированный + ссылка LATEST)
    versioned_json_path = os.path.join(reports_dir, f"contract_audit_{timestamp_str}.json")
    with open(versioned_json_path, "w", encoding="utf-8") as f:
        f.write(json.dumps([e.model_dump() for e in evaluations], ensure_ascii=False, indent=2))
    print(f"\n💾 1. Версионированный JSON аудита: reports/contract_audit_{timestamp_str}.json")

    latest_json_path = os.path.join(base_dir, "contract_audit.json")
    try:
        with open(latest_json_path, "w", encoding="utf-8") as f:
            f.write(json.dumps([e.model_dump() for e in evaluations], ensure_ascii=False, indent=2))
        print("🔗 Ссылка LATEST (в корне) обновлена: contract_audit.json")
    except Exception as e:
        print(f"ℹ️  LATEST JSON занят: {e}")

    # 2. Формирование сводного протокола разногласий (Markdown)
    full_md_content = f"# 📋 Протокол разногласий и сводный юридический аудит договоров\n"
    full_md_content += f"**Снимок аудита:** `{timestamp_str}` | **Дата:** {datetime.now().strftime('%Y-%m-%d %H:%M')} | **Эксперт:** Лаврентий Ямпуров\n\n"
    for ev in evaluations:
        full_md_content += f"## [{ev.verdict}] Договор {ev.contract_id} — {ev.counterparty}\n"
        full_md_content += f"- **Индекс правовой безопасности:** `{ev.safety_score} / 100`\n"
        if ev.red_flags:
            full_md_content += "- **Выявленные юридические риски (Red Flags):**\n"
            for rf in ev.red_flags:
                full_md_content += f"  * ⚠️ {rf}\n"
        if ev.required_amendments:
            full_md_content += "- **Требуемые формулировки для протокола разногласий:**\n"
            for am in ev.required_amendments:
                full_md_content += f"  * ✍️ {am}\n"
        else:
            full_md_content += "- **Статус:** Договор типовой, критических замечаний к условиям не выявлено.\n"
        full_md_content += "\n---\n\n"

    versioned_md_path = os.path.join(reports_dir, f"protocol_of_disagreements_{timestamp_str}.md")
    with open(versioned_md_path, "w", encoding="utf-8") as f:
        f.write(full_md_content)
    print(f"📝 2. Сводный версионированный протокол: reports/protocol_of_disagreements_{timestamp_str}.md")

    latest_md_path = os.path.join(base_dir, "protocol_of_disagreements.md")
    try:
        with open(latest_md_path, "w", encoding="utf-8") as f:
            f.write(full_md_content)
        print("🔗 Ссылка LATEST (в корне) обновлена: protocol_of_disagreements.md")
    except Exception as e:
        print(f"ℹ️  LATEST Markdown занят: {e}")

    # 3. Формирование индивидуальных целевых протоколов для рискованных контрактов
    flagged = [ev for ev in evaluations if ev.required_amendments]
    for ev in flagged:
        clean_cp = "".join([c if c.isalnum() else "_" for c in ev.counterparty])
        single_md_path = os.path.join(reports_dir, f"protocol_{ev.contract_id}_{clean_cp}_{timestamp_str}.md")
        with open(single_md_path, "w", encoding="utf-8") as f:
            f.write(f"# Протокол разногласий к Договору {ev.contract_id}\n\n")
            f.write(f"- **Контрагент:** {ev.counterparty}\n")
            f.write(f"- **Индекс безопасности:** {ev.safety_score}/100 ({ev.verdict})\n")
            f.write(f"- **Дата формирования:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write("### Выявленные несоответствия корпоративным стандартам:\n")
            for rf in ev.red_flags:
                f.write(f"- ⚠️ {rf}\n")
            f.write("\n### Редакция спорных пунктов (Позиция компании):\n")
            for am in ev.required_amendments:
                f.write(f"- ✍️ **Предлагаемая редакция:** {am}\n")
        print(f"   📑 Индивидуальный протокол сформирован: reports/{os.path.basename(single_md_path)}")

    print("✅ Проект 2 успешно выполнен!\n")


if __name__ == "__main__":
    evaluate_contracts()

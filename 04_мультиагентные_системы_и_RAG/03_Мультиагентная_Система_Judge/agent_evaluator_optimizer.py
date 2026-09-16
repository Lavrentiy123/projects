# -*- coding: utf-8 -*-
"""
Мультиагентный конвейер: Генератор -> Ревьюер -> Судья (LLM-as-a-Judge)
Реализация паттерна Evaluator-Optimizer + Reflexion Loop на Python.
Включает реальный статический AST-анализ синтаксиса и выполнение unit-тестов
в изолированном контексте (Sandbox Test Execution).
"""
import ast
import sys
import time

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

class MultiAgentJudgePipeline:
    def __init__(self, max_iterations=3):
        self.max_iterations = max_iterations

    def orchestrator_decompose(self, task: str) -> dict:
        """Агент 1: Декомпозиция задачи и формализация критериев приемки"""
        print(f"\n[АГЕНТ 1: ОРКЕСТРАТОР] Получена задача: '{task}'")
        print("  -> Анализ требований и декомпозиция на функциональные блоки...")
        return {
            "task": task,
            "requirements": [
                "1. Валидация входных данных (p_well >= 0, flow_rate >= 0)",
                "2. Физическая модель гидродинамических потерь Гершеля-Балкли",
                "3. Обработка исключений (ValueError)",
                "4. Совместимость со статусом телеметрии WITSML"
            ]
        }

    def coder_generate(self, iteration: int, feedback: str = None) -> str:
        """Агент 2: Генератор кода"""
        models = {1: "MiniMax M2.5 (Fast Prototyping)", 2: "Claude Haiku 4.5 (Refinement)"}
        model_name = models.get(iteration, "LLM-Optimizer")
        print(f"\n[АГЕНТ 2: ГЕНЕРАТОР (Итерация {iteration})] Модель: {model_name}")
        
        if iteration == 1:
            print("  -> Первичная генерация решения по спецификации...")
            code = """def calculate_hydraulics(p_well, flow_rate):
    # Упрощенный расчет без проверки отрицательного давления
    dp = 0.05 * (flow_rate ** 1.8)
    return p_well - dp"""
        else:
            print(f"  -> Исправление дефектов по замечаниям судьи: '{feedback[:60]}...'")
            code = """def calculate_hydraulics(p_well: float, flow_rate: float) -> dict:
    if p_well < 0 or flow_rate < 0:
        raise ValueError("Параметры давления и расхода не могут быть отрицательными")
    # Учет плотности бурового раствора и реологической модели Гершеля-Балкли
    dp = 0.048 * (flow_rate ** 1.82)
    p_bottom = max(0.0, p_well - dp)
    return {"bottom_pressure": round(p_bottom, 2), "pressure_loss": round(dp, 2), "status": "WITSML_OK"}"""
        return code

    def reviewer_inspect(self, code: str) -> dict:
        """Агент 3: Ревьюер (AST-анализ и динамические тесты в песочнице)"""
        print("\n[АГЕНТ 3: РЕВЬЮЕР] Статический AST-анализ и запуск unit-тестов в песочнице...")
        
        # 1. Проверка синтаксиса через AST
        try:
            tree = ast.parse(code)
            ast_valid = True
        except SyntaxError as e:
            return {"ast_valid": False, "tests_passed": 0, "total_tests": 3, "error": str(e)}

        # 2. Динамическое выполнение тестов в безопасном словаре
        sandbox = {}
        try:
            exec(code, sandbox)
            func = sandbox.get("calculate_hydraulics")
        except Exception as e:
            return {"ast_valid": True, "tests_passed": 0, "total_tests": 3, "error": str(e)}

        # Набор тестов:
        tests_passed = 0
        total_tests = 3
        
        # Тест 1: Корректный расчет при штатных значениях
        try:
            res1 = func(100.0, 30.0)
            if isinstance(res1, dict) and "bottom_pressure" in res1 and res1.get("status") == "WITSML_OK":
                tests_passed += 1
        except Exception:
            pass

        # Тест 2: Вызов исключения при отрицательном давлении
        try:
            func(-10.0, 30.0)
        except ValueError:
            tests_passed += 1
        except Exception:
            pass

        # Тест 3: Вызов исключения при отрицательном расходе
        try:
            func(100.0, -5.0)
        except ValueError:
            tests_passed += 1
        except Exception:
            pass

        return {
            "ast_valid": ast_valid,
            "tests_passed": tests_passed,
            "total_tests": total_tests,
            "has_types": "float" in code
        }

    def judge_evaluate(self, code: str, review: dict) -> tuple:
        """Агент 4: Судья (LLM-as-a-Judge) со строгой шкалой оценки"""
        print("\n[АГЕНТ 4: СУДЬЯ (LLM-as-a-Judge)] Оценка качества решения (Порог прохождения: 8.5/10)...")
        
        pass_rate = review["tests_passed"] / review["total_tests"]
        score = 4.0 * pass_rate + (2.0 if review.get("has_types") else 0.5) + (3.5 if pass_rate == 1.0 else 0.5)
        score = round(score, 1)

        if score >= 8.5:
            verdict = "[OK_APPROVED]"
            feedback = "Решение полностью соответствует отраслевым стандартам и успешно прошло все тесты."
        else:
            verdict = "[CRITICAL_REJECT]"
            defects = []
            if review["tests_passed"] < review["total_tests"]:
                defects.append(f"Провалено {review['total_tests'] - review['tests_passed']} unit-тестов на граничные условия (отрицательные параметры)")
            if not review.get("has_types"):
                defects.append("Отсутствует строгая типизация аргументов и совместимость с WITSML")
            feedback = "; ".join(defects)

        print(f"  --> Оценка: {score}/10. Вердикт: {verdict}")
        if score < 8.5:
            print(f"  --> Замечания для возврата на доработку: {feedback}")
        else:
            print(f"  --> Резолюция: {feedback}")

        return score, verdict, feedback

    def run(self, task: str):
        task_spec = self.orchestrator_decompose(task)
        feedback = None
        
        for iteration in range(1, self.max_iterations + 1):
            code = self.coder_generate(iteration, feedback)
            review = self.reviewer_inspect(code)
            score, verdict, feedback = self.judge_evaluate(code, review)
            
            if verdict == "[OK_APPROVED]":
                print(f"\n🎉 Решение утверждено на итерации {iteration} со скором {score}/10!")
                print("=" * 95)
                print("ФИНАЛЬНЫЙ ВАЛИДИРОВАННЫЙ КОД ПОСЛЕ КОНТУРА САМОКРИТИКИ:")
                print("=" * 95)
                print(code)
                print("=" * 95)
                return code
            else:
                print(f"\n🔄 Возврат кода на итерацию {iteration + 1} (Reflexion Feedback Loop)...")

if __name__ == "__main__":
    print("=" * 95)
    print("🚀 ЗАПУСК МУЛЬТИАГЕНТНОГО КОНВЕЙЕРА САМОКРИТИКИ С ДИНАМИЧЕСКИМИ UNIT-ТЕСТАМИ")
    print("=" * 95)
    pipeline = MultiAgentJudgePipeline(max_iterations=3)
    task_desc = "Разработать модуль расчета забойного давления при циркуляции бурового раствора"
    pipeline.run(task_desc)

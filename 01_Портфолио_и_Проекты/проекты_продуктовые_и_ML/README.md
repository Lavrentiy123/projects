# 📊 Продуктовые сервисы, машинное обучение и бизнес-аналитика

В данной папке представлены исходные коды и аналитические модули по продуктовым решениям, предиктивным моделям и BI-дашбордам Лаврентия Ямпурова:

| № | Проект | Направление | Стек технологий | Исходный код | Запуск | Ключевой результат / Метрики |
|---|---|---|---|---|---|---|
| **01** | [**Telecom Churn Prediction**](./01_telecom_churn_prediction/) | Предиктивный отток клиентов | Python, Scikit-learn, XGBoost, Pandas | [`run_churn_model.py`](./01_telecom_churn_prediction/run_churn_model.py) | `python run_churn_model.py` | **AUC-ROC = 0.8425**, Accuracy = 0.8034, выявление ключевых факторов риска оттока |
| **02** | [**StockFlow**](./02_stockflow_demand_forecast/) | ИИ-агент прогнозирования спроса | Time-Series ML, BPMN 2.0, User Stories | [`run_stockflow_forecast.py`](./02_stockflow_demand_forecast/run_stockflow_forecast.py) | `python run_stockflow_forecast.py` | Прогноз на 14 дней, расчет точки дозаказа, дефицит полок -15%, кросс-функциональная команда 7 чел. |
| **03** | [**DetailLab**](./03_detaillab_content_bot/) | LLM-генератор отраслевого контента | Claude API, ChatGPT, Telegram Bot API | [`run_detaillab_engine.py`](./03_detaillab_content_bot/run_detaillab_engine.py) | `python run_detaillab_engine.py` | CustDev 50+ предпринимателей, 78% сгенерированного контента принимается без правок |
| **04** | [**Health Assistant**](./04_health_assistant_llm/) | Диалоговый LLM-ассистент | OpenAI API, Replit, Safety Guardrails | [`run_health_assistant.py`](./04_health_assistant_llm/run_health_assistant.py) | `python run_health_assistant.py` | Сценарии диалогов, строгая медицинская этика, отсечение опасных рекомендаций |
| **05** | [**Bank Marketing Analytics**](./05_bank_marketing_datalens/) | Аналитический BI-дашборд | Yandex DataLens, SQL, Excel | [`run_bank_marketing_analysis.py`](./05_bank_marketing_datalens/run_bank_marketing_analysis.py) | `python run_bank_marketing_analysis.py` | Когортный анализ 41 188 записей, сегментация конверсий по длительности звонков |

---

## 🚀 Быстрый запуск всех модулей раздела
Каждый проект полностью автономен и снабжен скриптом демонстрации:
```bash
# Тест прогноза оттока (XGBoost vs LogReg)
python 01_telecom_churn_prediction/run_churn_model.py

# Тест прогнозирования спроса StockFlow
python 02_stockflow_demand_forecast/run_stockflow_forecast.py

# Генератор контента DetailLab
python 03_detaillab_content_bot/run_detaillab_engine.py

# Диалоговый ассистент Health Assistant с этическим фильтром
python 04_health_assistant_llm/run_health_assistant.py

# Когортный анализ банковских депозитов
python 05_bank_marketing_datalens/run_bank_marketing_analysis.py
```

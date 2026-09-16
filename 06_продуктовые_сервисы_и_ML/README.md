# 📊 Продуктовые сервисы, машинное обучение и бизнес-аналитика

В данном разделе представлены законченные продуктовые кейсы, аналитические исследования и ML-модели Лаврентия Ямпурова. Каждый проект снабжен **воспроизводимым кодом**, **локальными файлами презентаций/отчётов в репозитории** и **прямыми ссылками на внешние онлайн-артефакты**:

> 📥 **Скачать единый обзорный документ с проектами:**  
> • 📄 [**ПОРТФОЛИО_ПРОЕКТОВ_Лаврентий_Ямпуров.pdf**](./ПОРТФОЛИО_ПРОЕКТОВ_Лаврентий_Ямпуров.pdf) (интерактивный PDF со всеми ссылками)  
> • 📝 [**ПОРТФОЛИО_ПРОЕКТОВ_Лаврентий_Ямпуров.docx**](./ПОРТФОЛИО_ПРОЕКТОВ_Лаврентий_Ямпуров.docx) (редактируемый документ Word)  

| № | Проект | Роль и Стек | Исходный код | Локальные файлы в Git | Внешние онлайн-ссылки | Ключевые результаты / Метрики |
|---|---|---|---|---|---|---|
| **01** | [**Telecom Churn Prediction**](./01_telecom_churn_prediction/) | ML-инженер<br>Python, Scikit-learn, XGBoost | [`run_churn_model.py`](./01_telecom_churn_prediction/run_churn_model.py) | [📊 Telecom_Churn_Presentation.pptx](./01_telecom_churn_prediction/Telecom_Churn_Presentation.pptx) | [Google Slides](https://docs.google.com/presentation/d/1F-zmeWsoK9N36dUIy9wTz1WhveyvmVYG/edit?usp=sharing) | **AUC-ROC = 0.8425**, Accuracy = 0.8034. Топ-5 факторов оттока абонентов, retention-стратегия |
| **02** | [**StockFlow**](./02_stockflow_demand_forecast/) | Системный инженер<br>BPMN 2.0, Time-Series ML, Jira | [`run_stockflow_forecast.py`](./02_stockflow_demand_forecast/run_stockflow_forecast.py) | [📊 StockFlow_Презентация.pptx](./02_stockflow_demand_forecast/StockFlow_ИИ_Агент_Прогнозирования_Спроса.pptx) | [Google Slides](https://docs.google.com/presentation/d/15nC8xzPXrTYodyBwwZRlJSDey06OYHEKwI0ocs4V1ic/edit?usp=sharing) | Прогноз спроса на 14 дней, расчет точки заказа (EOQ + Safety Stock), дефицит полок -15% |
| **03** | [**DetailLab**](./03_detaillab_content_bot/) | Product Manager<br>Claude, ChatGPT, Telegram API | [`run_detaillab_engine.py`](./03_detaillab_content_bot/run_detaillab_engine.py) | [📊 DetailLab_Презентация_25_слайдов.pptx](./03_detaillab_content_bot/DetailLab_Презентация_Проекта.pptx) | [Google Drive](https://drive.google.com/file/d/1ZUo6grfGG3CICfcq6VdOpUBxEY0lESfD/view) | CustDev 50+ студий, 78% контента без правок, сокращение времени подготовки с 45 мин до 30 сек |
| **04** | [**Health Assistant**](./04_health_assistant_llm/) | Product Owner<br>OpenAI API, Replit, Safety Guardrails | [`run_health_assistant.py`](./04_health_assistant_llm/run_health_assistant.py) | [📄 Health_Assistant_Docs.pdf](./04_health_assistant_llm/Health_Assistant_Docs.pdf)<br>[📄 Health_Assistant_Docs.docx](./04_health_assistant_llm/Health_Assistant_Docs.docx) | [Google Docs](https://docs.google.com/document/d/1WbgyNOEuXo-2ZqzovYGxsWLp8RNBdFQx/edit)<br>[Код на Replit](https://replit.com/join/itilxzqftj-kinolavrik)<br>[Видео-демо](https://drive.google.com/file/d/1tCSXsKdtzVwht1ZrK_8EATxUVeI0D3YO/view) | Прототип персонального ассистента с веб-UI, жесткие этические дисклеймеры, обработка симптомов |
| **05** | [**Bank Marketing Analytics**](./05_bank_marketing_datalens/) | Бизнес-аналитик / Data Analyst<br>Yandex DataLens, SQL | [`run_bank_marketing_analysis.py`](./05_bank_marketing_datalens/run_bank_marketing_analysis.py) | [📄 Bank_Marketing_Report.pdf](./05_bank_marketing_datalens/Bank_Marketing_Report.pdf)<br>[📄 Bank_Marketing_Report.docx](./05_bank_marketing_datalens/Bank_Marketing_Report.docx)<br>[🖥️ bank_marketing_dashboard.html](./05_bank_marketing_datalens/bank_marketing_dashboard.html) | [Дашборд DataLens](https://datalens.yandex/s4usvxxpcueoc)<br>[Зеркало DataLens](https://datalens.yandex/9krm5z44271at)<br>[Google Docs Отчёт](https://docs.google.com/document/d/1xi71p8m69jWm-494B_mQWIvAQo0dMqf3/edit) | Анализ 41 188 обращений, CR 11.27%, когорты по времени разговора (5+ мин дают CR 34.2%) |

---

## 🚀 Быстрый запуск всех модулей раздела
Каждый проект полностью автономен и снабжен скриптом демонстрации:
```bash
# 1. Тест прогноза оттока (XGBoost vs LogReg, AUC-ROC 0.8425)
python 01_telecom_churn_prediction/run_churn_model.py

# 2. Тест прогнозирования спроса и автозакупок StockFlow
python 02_stockflow_demand_forecast/run_stockflow_forecast.py

# 3. Генератор контента DetailLab (эмуляция генерации постов)
python 03_detaillab_content_bot/run_detaillab_engine.py

# 4. Диалоговый ассистент Health Assistant с этическим фильтром
python 04_health_assistant_llm/run_health_assistant.py

# 5. Когортный анализ банковских депозитов (DataLens) и генерация локального HTML
python 05_bank_marketing_datalens/run_bank_marketing_analysis.py
```


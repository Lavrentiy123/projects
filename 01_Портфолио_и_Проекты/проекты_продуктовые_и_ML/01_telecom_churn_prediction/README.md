# 📱 Telecom Churn Prediction: Прогнозирование оттока клиентов

* **Роль:** Аналитик данных / ML-инженер (Лаврентий Ямпуров)
* **Стек:** Python 3.9+, Pandas, Scikit-learn, XGBoost, Matplotlib, Jupyter Notebook
* **Данные:** 7 043 клиента, 21 признак (демография, контракты, платежи, сервисы)
* **Презентация проекта:** [Google Slides](https://docs.google.com/presentation/d/1F-zmeWsoK9N36dUIy9wTz1WhveyvmVYG/edit?usp=sharing)

## 📊 Результаты моделирования
* **Лучшая модель:** Logistic Regression (L2) с **AUC-ROC = 0.8425**, **Accuracy = 0.8034**
* **Топ-факторы оттока:**
  1. Помесячный контракт (`Month-to-month`)
  2. Срок жизни абонента менее года (`tenure < 12`)
  3. Высокий чек (`MonthlyCharges > $75`)
  4. Оптоволоконный интернет (`Fiber Optic`)
  5. Оплата электронным чеком

## 🚀 Быстрый запуск
```bash
python run_churn_model.py
```
Скрипт выполняет валидацию, выводит сравнительную таблицу моделей и генерирует `churn_report.json`.

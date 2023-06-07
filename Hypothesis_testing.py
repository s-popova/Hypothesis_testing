import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
import seaborn as sns
alpha = 0.05

st.header("Попова Софья. Тестовое задание")
# Загрузка файла 
uploaded_file = st.file_uploader("Загрузите файл CSV", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    
    st.header("Файл Статистика")
    st.write(data)

    
    age_threshold = st.slider("Пороговый возраст", min_value=18, max_value=100, value=35, step=1)
    work_days_threshold = st.slider("Пороговое количество пропущенных дней", min_value=0, max_value=10, value=2, step=1)

 
    st.header("Графики распределений")

    # Распределение количества больничных дней по полу
    st.subheader("Распределение количества больничных дней по полу")
    fig, ax = plt.subplots()
    sns.histplot(data, x="Количество больничных дней", hue="Пол", multiple="stack", ax=ax)
    st.pyplot(fig)

    # Распределение количества больничных дней по возрасту
    st.subheader("Распределение количества больничных дней по возрасту")
    fig, ax = plt.subplots()
    sns.histplot(data, x="Количество больничных дней", hue="Возраст", multiple="stack", ax=ax)
    st.pyplot(fig)

    
    st.header("Гипотеза №1")
    st.write("Для проверки гипотезы 1 используется t-тест для независимых выборок.")
    st.subheader("Нулевая гипотеза")
    st.write("(H0): Мужчины и женщины пропускают одинаковое количество рабочих дней по болезни.")
    st.subheader("Альтернативная гипотеза")
    st.write(f"(H1): Мужчины пропускают более {work_days_threshold} рабочих дней по болезни чаще женщин.")

    
    men = data[data['Пол'] == '"М"']['Количество больничных дней']
    women = data[data['Пол'] == '"Ж"']['Количество больничных дней']
    men_above_threshold = men[men > work_days_threshold]
    women_above_threshold = women[women > work_days_threshold]
    
    # Выполнение двухвыборочного t-теста
    t_statistic, p_value = ttest_ind(men_above_threshold, women_above_threshold)

    st.header("Результаты проверки гипотезы №1")
    st.write(f"Гипотеза: Мужчины пропускают в течение года более {work_days_threshold} рабочих дней по болезни чаще женщин")
    st.write(f"Уровень значимости (alpha): {alpha}")
    st.write(f"t-статистика: {t_statistic}")
    st.write(f"p-значение: {p_value}")

    if p_value < alpha:
        st.write(f"Результат: Гипотеза 1 отвергается. Мужчины пропускают в течение года более {work_days_threshold} рабочих дней по болезни значимо чаще женщин.")
    else:
        st.write(f"Результат: Гипотеза 1 не отвергается. Нет статистически значимой разницы в пропущенных рабочих днях по болезни между мужчинами и женщинами.")

    st.header("Гипотеза №2")
    st.write("Для проверки гипотезы 2 используется t-тест для независимых выборок.")
    st.subheader("Нулевая гипотеза")
    st.write(f"(H0): Сотрудники старше {age_threshold} лет и молодые сотрудники пропускают одинаковое количество рабочих дней по болезни.")
    st.subheader("Альтернативная гипотеза")
    st.write(f"(H1): Сотрудники старше {age_threshold} лет пропускают более {work_days_threshold} рабочих дней по болезни чаще, чем молодые сотрудники.")
    
    young_employees_data = data[data['Возраст'] <= age_threshold]
    older_employees_data = data[data['Возраст'] > age_threshold]
    young_employees = young_employees_data[young_employees_data['Количество больничных дней'] > work_days_threshold]
    older_employees = older_employees_data[older_employees_data['Количество больничных дней'] > work_days_threshold]
    
    # Проверка гипотезы: Сотрудники старше 35 лет пропускают более 2 рабочих дней по болезни чаще, чем молодые сотрудники
    t_statistic_age, p_value_age = ttest_ind(older_employees['Количество больничных дней'], young_employees['Количество больничных дней'])

    st.header("Результаты проверки гипотезы №2")
    st.write(f"Гипотеза: Сотрудники старше {age_threshold} лет пропускают в течение года более {work_days_threshold} рабочих дней по болезни чаще, чем молодые сотрудники")
    st.write(f"Уровень значимости (alpha): {alpha}")
    st.write(f"t-статистика: {t_statistic_age}")
    st.write(f"p-значение: {p_value_age}")

    if p_value_age < alpha:
        st.write(f"Результат: Гипотеза 2 отвергается. Сотрудники старше  {age_threshold} лет пропускают в течение года более {work_days_threshold} рабочих дней по болезни значимо чаще, чем молодые сотрудники.")
    else:
        st.write(f"Результат: Гипотеза 2 не отвергается. Нет статистически значимой разницы в пропущенных рабочих днях по болезни между сотрудниками старше  {age_threshold} лет и молодыми сотрудниками.")

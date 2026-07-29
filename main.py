import streamlit as st
import pandas as pd
from database import get_universities_data
from articles import render_articles_page
from ai_bot import render_ai_bot_page

# Настройка страницы
st.set_page_config(page_title="Абитуриент 2026", page_icon="🎓", layout="wide")

# Загружаем базу данных
df = get_universities_data()

# Навигация
st.sidebar.title("📍 Навигация")
page = st.sidebar.radio("Перейти к разделу:", [
    "🎯 Калькулятор & Подбор Вуза",
    "📖 База знаний (Статьи 🖋️)",
    "💬 Помощник Абитуриента"
])

# 1. РАЗДЕЛ: КАЛЬКУЛЯТОР
if page == "🎯 Калькулятор & Подбор Вуза":
    st.title("🎓 Ассистент Абитуриента 2026")
    st.caption("Подбор программ на основе баллов ЕГЭ и дополнительных опций")

    with st.sidebar:
        st.divider()
        st.header("📊 Ваши предметы и баллы ЕГЭ")

        # Обязательные предметы
        rus = st.number_input("Русский язык", 0, 100, 80)
        math = st.number_input("Математика (профиль)", 0, 100, 75)

        user_subjects = {"Русский язык": rus, "Математика": math}

        # Дополнительные предметы на выбор
        st.subheader("Выберите доп. предметы:")
        if st.checkbox("Информатика", value=True):
            user_subjects["Информатика"] = st.number_input("Балл по Информатике", 0, 100, 85)
        if st.checkbox("Физика"):
            user_subjects["Физика"] = st.number_input("Балл по Физике", 0, 100, 60)
        if st.checkbox("Обществознание"):
            user_subjects["Обществознание"] = st.number_input("Балл по Обществознанию", 0, 100, 70)
        if st.checkbox("Химия"):
            user_subjects["Химия"] = st.number_input("Балл по Химии", 0, 100, 70)
        if st.checkbox("Биология"):
            user_subjects["Биология"] = st.number_input("Балл по Биологии", 0, 100, 70)
        if st.checkbox("История"):
            user_subjects["История"] = st.number_input("Балл по Истории", 0, 100, 70)
        if st.checkbox("Иностранный язык"):
            user_subjects["Иностранный язык"] = st.number_input("Балл по Иностр. языку", 0, 100, 70)
        if st.checkbox("Литература"):
            user_subjects["Литература"] = st.number_input("Балл по Литературе", 0, 100, 70)
        if st.checkbox("География"):
            user_subjects["География"] = st.number_input("Балл по Географии", 0, 100, 70)

        achievements = st.number_input("Индивидуальные достижения (ИД)", 0, 10, 3)

        st.divider()
        st.header("⚙️ Фильтры")
        only_suitable = st.checkbox("Показывать только подходящие по предметам", value=False)
        only_dorm = st.checkbox("Только с общежитием", False)
        only_military = st.checkbox("Наличие Военного центра (ВУЦ)", False)
        only_double = st.checkbox("Программы двойного диплома 🌐", False)
        max_price = st.slider("Макс. стоимость (руб/год)", 80000, 400000, 400000, 10000)

    filtered_df = df.copy()

    # Фильтрация по чекбоксам
    if only_dorm:
        filtered_df = filtered_df[filtered_df['dormitory'] == True]
    if only_military:
        filtered_df = filtered_df[filtered_df['military'] == True]
    if only_double:
        filtered_df = filtered_df[filtered_df['double_degree'] == True]

    # Корректная фильтрация цены
    filtered_df = filtered_df[
        (filtered_df['price'] <= max_price) | (filtered_df['price'] == 0) | (filtered_df['price'].isna())]

    # Считаем совпадение по предметам
    results = []
    for idx, row in filtered_df.iterrows():
        req_subjects = row['subjects']

        if isinstance(req_subjects, str):
            req_subjects = [s.strip() for s in req_subjects.split(',')]

        user_score = 0
        has_all_subjects = True

        for subj in req_subjects:
            if subj in user_subjects:
                user_score += user_subjects[subj]
            else:
                has_all_subjects = False

        user_score += achievements

        if not only_suitable or has_all_subjects:
            results.append((row, user_score, has_all_subjects))

    st.subheader(f"🔍 Найдено направлений: {len(results)}")

    for row, user_score, has_all_subjects in results:
        pass_score = float(row['pass_score']) if pd.notnull(row['pass_score']) else 0.0
        budget = int(row['budget_places']) if pd.notnull(row['budget_places']) else 0
        price = int(row['price']) if pd.notnull(row['price']) else 0

        if not has_all_subjects:
            chance_badge = ":gray[Не выбраны все предметы ⚠️]"
            score_text = "Не совпадает набор ЕГЭ"
        elif pass_score > 0:
            diff = user_score - pass_score
            if diff >= 10:
                chance_badge = ":green[Высокий шанс 🟢]"
            elif diff >= -15:
                chance_badge = ":orange[Средний шанс 🟡]"
            else:
                chance_badge = ":red[Низкий шанс 🔴]"
            score_text = f"{user_score} / {int(pass_score)}"
        else:
            chance_badge = ":blue[Конкурс платных мест 🔵]"
            score_text = f"{user_score} (Проходной не указан)"

        req_subjects = row['subjects']
        if isinstance(req_subjects, list):
            req_subjects_str = ', '.join(req_subjects)
        else:
            req_subjects_str = str(req_subjects)

        # Выводим карточку направления
        with st.expander(f"{row['university']} ({row['faculty']}) — {row['program']} ({row['code']}) | {chance_badge}"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Ваш балл / Проходной", score_text)
            c2.metric("Бюджетных мест", f"{budget}" if budget > 0 else "Нет бюджета")
            c3.metric("Стоимость", f"{price:,} ₽/год".replace(',', ' ') if price > 0 else "По запросу")

            st.write(f"**Город:** {row['city']}")
            st.write(f"**Необходимые предметы:** {req_subjects_str}")

            tags = []
            if row['dormitory']: tags.append("🏠 Общежитие")
            if row['military']: tags.append("🪖 Военный центр")
            if row['double_degree']: tags.append("🌐 Двойной диплом")
            if pd.notnull(row['target_places']) and row['target_places'] > 0:
                tags.append(f"🎯 Целевые места: {int(row['target_places'])}")

            st.success(" | ".join(tags))

# 2. РАЗДЕЛ: БАЗА ЗНАНИЙ
elif page == "📖 База знаний (Статьи 🖋️)":
    render_articles_page()

# 3. РАЗДЕЛ: ПОМОЩНИК
elif page == "💬 Помощник Абитуриента":
    render_ai_bot_page()
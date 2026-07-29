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
    st.caption("Подбор программ на основе ваших предметов и баллов ЕГЭ")

    with st.sidebar:
        st.divider()
        st.header("📊 Ваши предметы и баллы ЕГЭ")

        # Список всех возможных предметов
        all_subjects_list = [
            "Русский язык", "Математика", "Информатика", "Физика",
            "Обществознание", "Химия", "Биология", "История",
            "Иностранный язык", "Литература", "География"
        ]

        selected_subjects = st.multiselect(
            "Выберите сданные предметы ЕГЭ:",
            options=all_subjects_list,
            default=["Русский язык", "Математика", "Информатика"]
        )

        user_subjects = {}
        if selected_subjects:
            st.subheader("Введите баллы по предметам:")
            for subj in selected_subjects:
                user_subjects[subj] = st.number_input(f"{subj}", 0, 100, 75, key=f"score_{subj}")

        achievements = st.number_input("Индивидуальные достижения (ИД)", 0, 10, 3)

        st.divider()
        st.header("⚙️ Фильтры")
        # По умолчанию скрываем подходящие частично
        only_suitable = st.checkbox("Показывать ТОЛЬКО с полным совпадением предметов", value=True)
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

    # Корректная фильтрация стоимости
    filtered_df = filtered_df[
        (filtered_df['price'] <= max_price) | (filtered_df['price'] == 0) | (filtered_df['price'].isna())]

    # Проверка совпадения по предметам
    results = []
    for idx, row in filtered_df.iterrows():
        req_subjects = row['subjects']

        if isinstance(req_subjects, str):
            req_subjects = [s.strip() for s in req_subjects.split(',')]

        user_score = 0
        has_all_subjects = True

        # Проверяем, есть ли ВСЕ требуемые предметы у пользователя
        for subj in req_subjects:
            if subj in user_subjects:
                user_score += user_subjects[subj]
            else:
                has_all_subjects = False

        user_score += achievements

        # Строго добавляем только если предметы совпадают на 100% (или если снят флаг filtering)
        if has_all_subjects or not only_suitable:
            results.append((row, user_score, has_all_subjects))

    st.subheader(f"🔍 Найдено подпадающих направлений: {len(results)}")

    if not results:
        st.warning(
            "⚠️ По выбранным предметам не найдено ни одного направления. Попробуйте выбрать дополнительные предметы ЕГЭ в боковой панели!")

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
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
            default=[]
        )

        user_subjects = {}
        if selected_subjects:
            st.subheader("Введите баллы по предметам:")
            for subj in selected_subjects:
                user_subjects[subj] = st.number_input(f"{subj}", 0, 100, 75, key=f"score_{subj}")

        achievements = st.number_input("Индивидуальные достижения (ИД)", 0, 10, 3)

        st.divider()
        st.header("⚙️ Фильтры")

        # Фильтр по вузам
        all_unis = sorted(df['university'].dropna().unique().tolist())
        selected_uni_filter = st.selectbox("Выбрать конкретный вуз:", ["Все вузы"] + all_unis)

        only_suitable = st.checkbox("Показывать ТОЛЬКО с полным совпадением предметов", value=True)
        only_dorm = st.checkbox("Только с общежитием", False)
        only_military = st.checkbox("Наличие Военного центра (ВУЦ)", False)
        only_double = st.checkbox("Программы двойного диплома 🌐", False)

        # Увеличили макс. порог стоимости, чтобы топовые вузы (НИУ ВШЭ, МГУ) не скрывались
        max_price = st.slider("Макс. стоимость (руб/год)", 50000, 1200000, 1200000, 50000)

    filtered_df = df.copy()

    # Фильтр по выбору конкретного вуза
    if selected_uni_filter != "Все вузы":
        filtered_df = filtered_df[filtered_df['university'] == selected_uni_filter]

    # Фильтрация по чекбоксам
    if only_dorm:
        filtered_df = filtered_df[filtered_df['dormitory'] == True]
    if only_military:
        filtered_df = filtered_df[filtered_df['military'] == True]
    if only_double:
        filtered_df = filtered_df[filtered_df['double_degree'] == True]

    # Корректная фильтрация стоимости (включая программы, где цена 0 или не указана)
    filtered_df = filtered_df[
        (filtered_df['price'] <= max_price) | (filtered_df['price'] == 0) | (filtered_df['price'].isna())
        ]

    # Проверка совпадения по предметам
    results = []
    for idx, row in filtered_df.iterrows():
        req_subjects_raw = row['subjects']

        # Надежная проверка на пустые/незаполненные данные
        if not req_subjects_raw or pd.isnull(req_subjects_raw) is True or str(req_subjects_raw) == 'nan':
            continue

        # Разбиваем строку предметов по запятым
        req_groups = [s.strip() for s in str(req_subjects_raw).split(',')]

        user_score = 0
        has_all_subjects = True

        for group in req_groups:
            # Если написано "Физика или Информатика" — проверяем альтернативы
            options = [opt.strip() for opt in group.split(' или ')]

            # Находим максимальный балл среди выбранных пользователем альтернатив
            matched_scores = [user_subjects[opt] for opt in options if opt in user_subjects]

            if matched_scores:
                user_score += max(matched_scores)
            else:
                has_all_subjects = False

        user_score += achievements

        if has_all_subjects or not only_suitable:
            results.append((row, user_score, has_all_subjects))

    st.subheader(f"🔍 Найдено подпадающих направлений: {len(results)}")

    if not results:
        st.warning(
            "⚠️ По выбранным предметам и фильтрам не найдено направлений. Попробуйте увеличить максимальную стоимость или выбрать больше предметов!")

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

        faculty_str = f" ({row['faculty']})" if pd.notnull(row['faculty']) else ""

        # Выводим карточку направления
        with st.expander(f"{row['university']}{faculty_str} — {row['program']} ({row['code']}) | {chance_badge}"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Ваш балл / Проходной", score_text)
            c2.metric("Бюджетных мест", f"{budget}" if budget > 0 else "Нет бюджета")
            c3.metric("Стоимость", f"{price:,} ₽/год".replace(',', ' ') if price > 0 else "По запросу")

            st.write(f"**Город:** {row['city']}")
            st.write(f"**Необходимые предметы:** {row['subjects']}")

            tags = []
            if row['dormitory'] == True: tags.append("🏠 Общежитие")
            if row['military'] == True: tags.append("🪖 Военный центр")
            if row['double_degree'] == True: tags.append("🌐 Двойной диплом")
            if pd.notnull(row['target_places']) and row['target_places'] > 0:
                tags.append(f"🎯 Целевые места: {int(row['target_places'])}")

            if tags:
                st.success(" | ".join(tags))

# 2. РАЗДЕЛ: БАЗА ЗНАНИЙ
elif page == "📖 База знаний (Статьи 🖋️)":
    render_articles_page()

# 3. РАЗДЕЛ: ПОМОЩНИК
elif page == "💬 Помощник Абитуриента":
    render_ai_bot_page()
import streamlit as st
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

        # Список всех возможных предметов из базы
        rus = st.number_input("Русский язык", 0, 100, 80)
        math = st.number_input("Математика (профиль)", 0, 100, 75)

        # Дополнительные предметы на выбор
        st.subheader("Выберите доп. предметы:")
        user_subjects = {"Русский язык": rus, "Математика": math}

        if st.checkbox("Информатика"):
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
        st.header("⚙️ Дополнительные опции")
        only_dorm = st.checkbox("Только с общежитием", False)
        only_military = st.checkbox("Наличие Военного центра (ВУЦ)", False)
        only_double = st.checkbox("Программы двойного диплома 🌐", False)
        max_price = st.slider("Макс. стоимость (руб/год)", 80000, 400000, 350000, 10000)

    filtered_df = df.copy()

    # Фильтрация по чекбоксам
    if only_dorm:
        filtered_df = filtered_df[filtered_df['dormitory'] == True]
    if only_military:
        filtered_df = filtered_df[filtered_df['military'] == True]
    if only_double:
        filtered_df = filtered_df[filtered_df['double_degree'] == True]

    # Фильтр по стоимости (пропускаем 0 — это если цена не указана)
    filtered_df = filtered_df[(filtered_df['price'] <= max_price) | (filtered_df['price'] == 0)]

    st.subheader(f"🔍 Найдено направлений в базе: {len(filtered_df)}")

    for idx, row in filtered_df.iterrows():
        req_subjects = row['subjects']

        # Считаем сумму баллов абитуриента по предметам, необходимым для этого направления
        user_score = 0
        has_all_subjects = True

        for subj in req_subjects:
            if subj in user_subjects:
                user_score += user_subjects[subj]
            else:
                # Если абитуриент не сдавал этот предмет
                has_all_subjects = False

        user_score += achievements

        # Рассчитываем шансы, если указан проходной балл
        pass_score = row['pass_score']
        if pass_score > 0:
            diff = user_score - pass_score
            if diff >= 10:
                chance_badge = ":green[Высокий шанс 🟢]"
            elif diff >= -15:
                chance_badge = ":orange[Средний шанс 🟡]"
            else:
                chance_badge = ":red[Низкий шанс 🔴]"
            score_text = f"{user_score} / {int(pass_score)}"
        else:
            chance_badge = ":blue[Конкурс платных мест / Подача документов 🔵]"
            score_text = f"{user_score} (Проходной не указан)"

        # Выводим карточку направления
        with st.expander(f"{row['university']} ({row['faculty']}) — {row['program']} ({row['code']}) | {chance_badge}"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Ваш балл / Проходной", score_text)
            c2.metric("Бюджетных мест", f"{int(row['budget_places'])}" if row['budget_places'] > 0 else "Нет бюджета")
            c3.metric("Стоимость",
                      f"{int(row['price']):,} ₽/год".replace(',', ' ') if row['price'] > 0 else "По запросу")

            st.write(f"**Город:** {row['city']}")
            st.write(f"**Необходимые предметы:** {', '.join(req_subjects)}")

            tags = []
            if row['dormitory']: tags.append("🏠 Общежитие")
            if row['military']: tags.append("🪖 Военный центр")
            if row['double_degree']: tags.append("🌐 Двойной диплом")
            if row['target_places'] > 0: tags.append(f"🎯 Целевые места: {int(row['target_places'])}")

            st.success(" | ".join(tags))

# 2. РАЗДЕЛ: БАЗА ЗНАНИЙ
elif page == "📖 База знаний (Статьи 🖋️)":
    render_articles_page()

# 3. РАЗДЕЛ: ПОМОЩНИК
elif page == "💬 Помощник Абитуриента":
    render_ai_bot_page()
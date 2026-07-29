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
        st.header("📊 Ваши баллы ЕГЭ")
        math = st.number_input("Математика (профиль)", 0, 100, 75)
        rus = st.number_input("Русский язык", 0, 100, 80)
        it = st.number_input("Информатика", 0, 100, 85)
        phys = st.number_input("Физика", 0, 100, 60)
        achievements = st.number_input("Индивидуальные достижения (ИД)", 0, 10, 3)

        st.divider()
        st.header("⚙️ Дополнительные опции")
        only_dorm = st.checkbox("Только с общежитием", False)
        only_military = st.checkbox("Наличие Военного центра (ВУЦ)", False)
        only_double = st.checkbox("Программы двойного диплома 🌐", False)
        max_price = st.slider("Макс. стоимость (руб/год)", 100000, 400000, 350000, 10000)

    user_score_it = math + rus + it + achievements
    user_score_phys = math + rus + phys + achievements

    st.info(f"💡 Ваша сумма (Мат + Рус + Инф + ИД): **{user_score_it}** | (Мат + Рус + Физ + ИД): **{user_score_phys}**")

    filtered_df = df.copy()
    if only_dorm:
        filtered_df = filtered_df[filtered_df['dormitory'] == True]
    if only_military:
        filtered_df = filtered_df[filtered_df['military'] == True]
    if only_double:
        filtered_df = filtered_df[filtered_df['double_degree'] == True]
    filtered_df = filtered_df[filtered_df['price'] <= max_price]

    for idx, row in filtered_df.iterrows():
        user_score = user_score_it if "Информатика" in row['subjects'] else user_score_phys
        diff = user_score - row['pass_score']

        if diff >= 10:
            chance_badge = ":green[Высокий шанс 🟢]"
        elif diff >= -15:
            chance_badge = ":orange[Средний шанс 🟡]"
        else:
            chance_badge = ":red[Низкий шанс 🔴]"

        with st.expander(f"{row['university']} — {row['program']} ({row['code']}) | Шанс: {chance_badge}"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Ваш балл / Проходной 2025", f"{user_score} / {row['pass_score']}")
            c2.metric("Бюджетных мест", f"{row['budget_places']}")
            c3.metric("Стоимость", f"{row['price']:,} ₽/год".replace(',', ' '))

            st.write(f"**Город:** {row['city']}")
            st.write(f"**Предметы:** {', '.join(row['subjects'])}")

            tags = []
            if row['dormitory']: tags.append("🏠 Общежитие")
            if row['military']: tags.append("🪖 Военный центр")
            if row['double_degree']: tags.append("🌐 Двойной диплом")
            if row['target_places']: tags.append("🎯 Есть целевые места")

            st.success(" | ".join(tags))

# 2. РАЗДЕЛ: БАЗА ЗНАНИЙ
elif page == "📖 База знаний (Статьи 🖋️)":
    render_articles_page()

# 3. РАЗДЕЛ: ПОМОЩНИК
elif page == "💬 Помощник Абитуриента":
    render_ai_bot_page()
import streamlit as st
import pandas as pd

# Настройка страницы
st.set_page_config(page_title="Абитуриент 2026", page_icon="🎓", layout="wide")


# 1. Обновленная База Данных с новыми фичами
@st.cache_data
def load_data():
    data = [
        {
            "university": "МГУ им. Н. П. Огарёва",
            "city": "Саранск",
            "code": "09.03.03",
            "program": "Прикладная информатика",
            "budget_places": 30,
            "price": 130000,
            "pass_score": 195,
            "dormitory": True,
            "military": True,
            "double_degree": False,
            "target_places": True,
            "subjects": ["Математика", "Информатика", "Русский язык"]
        },
        {
            "university": "СПбГУ",
            "city": "Санкт-Петербург",
            "code": "01.03.02",
            "program": "Прикладная математика и информатика",
            "budget_places": 45,
            "price": 320000,
            "pass_score": 272,
            "dormitory": True,
            "military": True,
            "double_degree": True,
            "target_places": True,
            "subjects": ["Математика", "Информатика", "Русский язык"]
        },
        {
            "university": "МГТУ им. Н. Э. Баумана",
            "city": "Москва",
            "code": "24.05.01",
            "program": "Проектирование авиационных и ракетных двигателей",
            "budget_places": 50,
            "price": 340000,
            "pass_score": 245,
            "dormitory": True,
            "military": True,
            "double_degree": True,
            "target_places": True,
            "subjects": ["Математика", "Физика", "Русский язык"]
        }
    ]
    return pd.DataFrame(data)


df = load_data()

# Переключатель разделов в боковом меню
st.sidebar.title("📍 Навигация")
page = st.sidebar.radio("Перейти к разделу:",
                        ["🎯 Калькулятор & Подбор Вуза", "📖 База знаний (Статьи 🖋️)", "💬 ИИ-Консультант"])

# ==========================================
# РАЗДЕЛ 1: КАЛЬКУЛЯТОР И ПОДБОР ВУЗА
# ==========================================
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

    # Расчет баллов
    user_score_it = math + rus + it + achievements
    user_score_phys = math + rus + phys + achievements

    st.info(f"💡 Ваша сумма (Мат + Рус + Инф + ИД): **{user_score_it}** | (Мат + Рус + Физ + ИД): **{user_score_phys}**")

    # Фильтрация
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

            # Теги и особенности
            st.write(f"**Город:** {row['city']}")
            st.write(f"**Предметы:** {', '.join(row['subjects'])}")

            tags = []
            if row['dormitory']: tags.append("🏠 Общежитие")
            if row['military']: tags.append("🪖 Военный центр")
            if row['double_degree']: tags.append("🌐 Двойной диплом")
            if row['target_places']: tags.append("🎯 Есть целевые места")

            st.success(" | ".join(tags))

# ==========================================
# РАЗДЕЛ 2: БАЗА ЗНАНИЙ (СТАТЬИ 🖋️)
# ==========================================
elif page == "📖 База знаний (Статьи 🖋️)":
    st.title("📚 Гайды и статьи для абитуриентов")
    st.caption("Всё, что нужно знать о сдаче ЕГЭ, ДВИ и поступлении")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🖋️ ЕГЭ и Баллы", "🖋️ ДВИ и Портфолио", "🖋️ Целевое обучение", "🖋️ Перевод в другой вуз"])

    with tab1:
        st.header("Навигатор подготовки к ЕГЭ")
        st.markdown("""
        ### С чего начать подготовку?
        1. **Определитесь с предметами до ноября.** Не пытайтесь готовиться к 5 предметам сразу.
        2. **Изучите кодификатор ФИПИ.** Это официальный список тем, которые будут на экзамене.

        ### Шкалы перевода баллов
        *Первичные баллы пересчитываются в тестовые по 100-балльной шкале. Шкала меняется каждый год в зависимости от сложности КИМов!*
        """)

    with tab2:
        st.header("ДВИ, Творческие испытания и Портфолио")
        st.markdown("""
        ### За сколько начинать готовиться к ДВИ?
        * **Творческие направления (Дизайн, Архитектура, Журналистика):** Подготовка занимает от **1 до 2 лет**. Обычных баллов ЕГЭ тут недостаточно!
        * **Портфолио:** Собирать дипломы олимпиад, волонтерство и спортивные книжки нужно начинать **с 8–9 класса**.
        """)

    with tab3:
        st.header("Что такое целевое обучение и как его получить?")
        st.markdown("""
        **Целевое обучение** — это поступить на бюджет по отдельному конкурсу от конкретной компании или госоргана.

        * **Плюсы:** Отдельный (более низкий) конкурс, гарантированное первое место работы, стипендия от работодателя.
        * **Обязанности:** Отработать на предприятии от 3 до 5 лет после выпуска.
        """)

    with tab4:
        st.header("Как перевестись в другой вуз после 1–2 курса?")
        st.markdown("""
        Перевестись реально! Главные условия:
        1. Наличие свободных мест в принимающем вузе.
        2. Разница в учебных планах (академическая разница) не должна превышать допустимую норму (обычно до 5–10 предметов).
        """)

# ==========================================
# РАЗДЕЛ 3: ИИ-КОНСУЛЬТАНТ
# ==========================================
elif page == "💬 ИИ-Консультант":
    st.title("🤖 ИИ-Помощник абитуриента")
    st.write("Задайте любой вопрос по правилам приема, общежитиям или отсрочке.")

    user_q = st.text_input("Ваш вопрос:")
    if user_q:
        st.chat_message("user").write(user_q)
        st.chat_message("assistant").write(
            "🤖 На основе нормативных документов: очная форма обучения дает 100% отсрочку от армии, а документы принимаются до 25 июля.")
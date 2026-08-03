import streamlit as st
import pandas as pd
from database import get_universities_data
from articles import render_articles_page
from ai_bot import render_ai_bot_page

# Настройка страницы
st.set_page_config(page_title="Абитуриент 2026", page_icon="🎓", layout="wide")

# Загружаем базу данных
df = get_universities_data()

# Инициализируем хранилище для сравнения в session_state
if "compare_list" not in st.session_state:
    st.session_state.compare_list = []

# Навигация
st.sidebar.title("📍 Навигация")
page = st.sidebar.radio("Перейти к разделу:", [
    "🎯 Калькулятор & Подбор Вуза",
    "⚖️ Сравнение выбранных (" + str(len(st.session_state.compare_list)) + ")",
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

        all_cities = sorted(df['city'].dropna().unique().tolist())
        selected_city_filter = st.selectbox("🏙️ Город:", ["Все города"] + all_cities)

        if selected_city_filter != "Все города":
            available_unis = sorted(df[df['city'] == selected_city_filter]['university'].dropna().unique().tolist())
        else:
            available_unis = sorted(df['university'].dropna().unique().tolist())

        selected_uni_filter = st.selectbox("🏫 Выбрать конкретный вуз:", ["Все вузы"] + available_unis)

        only_suitable = st.checkbox("Показывать ТОЛЬКО с полным совпадением предметов", value=True)
        only_dorm = st.checkbox("Только с общежитием 🏠", False)
        only_military = st.checkbox("Наличие Военного центра (ВУЦ) 🪖", False)
        only_double = st.checkbox("Программы двойного диплома 🌐", False)

        max_price = st.slider("Макс. стоимость (руб/год)", 50000, 1200000, 1200000, 50000)

    # ------------------ ФИЛЬТРАЦИЯ ------------------
    filtered_df = df.copy()

    if selected_city_filter != "Все города":
        filtered_df = filtered_df[filtered_df['city'] == selected_city_filter]

    if selected_uni_filter != "Все вузы":
        filtered_df = filtered_df[filtered_df['university'] == selected_uni_filter]

    if only_dorm:
        filtered_df = filtered_df[filtered_df['dormitory'] == True]
    if only_military:
        filtered_df = filtered_df[filtered_df['military'] == True]
    if only_double:
        filtered_df = filtered_df[filtered_df['double_degree'] == True]

    filtered_df = filtered_df[
        (filtered_df['price'] <= max_price) | (filtered_df['price'] == 0) | (filtered_df['price'].isna())
        ]

    results = []
    for idx, row in filtered_df.iterrows():
        subj_val = row['subjects']

        # Проверяем, заполнено ли поле предметов в Excel
        is_empty_subjects = (subj_val != subj_val) or (subj_val is None) or str(subj_val).strip() in ['', 'nan', 'None']

        if is_empty_subjects:
            req_subjects_raw = ""
            has_all_subjects = False
            user_score = achievements
        else:
            req_subjects_raw = str(subj_val).strip()
            req_groups = [s.strip() for s in req_subjects_raw.split(',')]

            user_score = 0
            has_all_subjects = True

            for group in req_groups:
                options = [opt.strip() for opt in group.split(' или ')]
                matched_scores = [user_subjects[opt] for opt in options if opt in user_subjects]

                if matched_scores:
                    user_score += max(matched_scores)
                else:
                    has_all_subjects = False

            user_score += achievements

        # Если стоит галочка "Только совпадение" — исключаем записи без предметов или с неполным совпадением
        if only_suitable:
            if not is_empty_subjects and has_all_subjects:
                results.append((row, user_score, has_all_subjects, is_empty_subjects))
        else:
            results.append((row, user_score, has_all_subjects, is_empty_subjects))

    # --- БЛОК СОРТИРОВКИ ---
    col_title, col_sort = st.columns([2, 1])
    with col_title:
        st.subheader(f"🔍 Найдено подпадающих направлений: {len(results)}")

    with col_sort:
        sort_option = st.selectbox(
            "Сортировать по:",
            [
                "По умолчанию",
                "Проходному баллу (по возрастанию)",
                "Проходному баллу (по убыванию)",
                "Количеству бюджетных мест (по убыванию)",
                "Стоимости (сначала дешевые)",
                "Стоимости (сначала дорогие)"
            ]
        )


    def get_sort_key(item, key_type):
        row = item[0]
        val = row.get(key_type)
        if pd.isna(val) or val is None:
            return -1 if 'desc' in sort_option or 'убыва' in sort_option else 999999
        return float(val)


    if sort_option == "Проходному баллу (по возрастанию)":
        results.sort(key=lambda x: get_sort_key(x, 'pass_score'))
    elif sort_option == "Проходному баллу (по убыванию)":
        results.sort(key=lambda x: get_sort_key(x, 'pass_score'), reverse=True)
    elif sort_option == "Количеству бюджетных мест (по убыванию)":
        results.sort(key=lambda x: get_sort_key(x, 'budget_places'), reverse=True)
    elif sort_option == "Стоимости (сначала дешевые)":
        results.sort(key=lambda x: get_sort_key(x, 'price'))
    elif sort_option == "Стоимости (сначала дорогие)":
        results.sort(key=lambda x: get_sort_key(x, 'price'), reverse=True)

    if not results:
        st.warning("⚠️ По выбранным критериям не найдено направлений. Попробуйте изменить фильтры!")

    # Отрисовка результатов
    for idx, (row, user_score, has_all_subjects, is_empty_subjects) in enumerate(results):
        pass_score = float(row['pass_score']) if pd.notnull(row['pass_score']) else 0.0
        budget = int(row['budget_places']) if pd.notnull(row['budget_places']) else 0
        price = int(row['price']) if pd.notnull(row['price']) else 0

        if is_empty_subjects:
            chance_badge = ":gray[Предметы уточняются ℹ️]"
            score_text = "Не заполнен набор предметов"
        elif not has_all_subjects:
            chance_badge = ":orange[Не выбраны все предметы ⚠️]"
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
        card_id = f"{row['university']}_{row['code']}_{row['program']}_{idx}"

        with st.expander(f"{row['university']}{faculty_str} — {row['program']} ({row['code']}) | {chance_badge}"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Ваш балл / Проходной", score_text)
            c2.metric("Бюджетных мест", f"{budget}" if budget > 0 else "Нет бюджета")
            c3.metric("Стоимость", f"{price:,} ₽/год".replace(',', ' ') if price > 0 else "По запросу")

            st.write(f"📍 **Город:** {row['city']}")
            st.write(f"📚 **Необходимые предметы:** {row['subjects'] if not is_empty_subjects else 'Уточняются'}")

            tags = []
            if row['dormitory'] == True: tags.append("🏠 Общежитие")
            if row['military'] == True: tags.append("🪖 Военный центр")
            if row['double_degree'] == True: tags.append("🌐 Двойной диплом")
            if pd.notnull(row['target_places']) and row['target_places'] > 0:
                tags.append(f"🎯 Целевые места: {int(row['target_places'])}")

            if tags:
                st.success(" | ".join(tags))

            # --- ЧЕКБОКС ДОБАВЛЕНИЯ К СРАВНЕНИЮ ---
            is_in_compare = any(item['card_id'] == card_id for item in st.session_state.compare_list)

            if st.checkbox("⚖️ Добавить к сравнению", value=is_in_compare, key=f"chk_{card_id}"):
                if not is_in_compare:
                    st.session_state.compare_list.append({
                        "card_id": card_id,
                        "university": row['university'],
                        "faculty": row['faculty'] if pd.notnull(row['faculty']) else "—",
                        "program": row['program'],
                        "code": row['code'],
                        "city": row['city'],
                        "pass_score": int(pass_score) if pass_score > 0 else "—",
                        "budget": budget if budget > 0 else "Нет",
                        "price": f"{price:,} ₽/год".replace(',', ' ') if price > 0 else "По запросу",
                        "dorm": "Да 🏠" if row['dormitory'] == True else "Нет",
                        "military": "Да 🪖" if row['military'] == True else "Нет"
                    })
                    st.rerun()
            else:
                if is_in_compare:
                    st.session_state.compare_list = [item for item in st.session_state.compare_list if
                                                     item['card_id'] != card_id]
                    st.rerun()

# 2. РАЗДЕЛ: СРАВНЕНИЕ
elif page.startswith("⚖️ Сравнение"):
    st.title("⚖️ Сравнение выбранных программ")
    st.caption("Наглядная таблица для сопоставления вузов бок о бок")

    if not st.session_state.compare_list:
        st.info(
            "💡 Вы пока не добавили ни одного направления к сравнению. Вернитесь в раздел Калькулятора и отметьте галочкой «⚖️ Добавить к сравнению» в карточке вуза!")
    else:
        if st.button("🗑️ Очистить список сравнения"):
            st.session_state.compare_list = []
            st.rerun()

        compare_df = pd.DataFrame(st.session_state.compare_list)

        compare_df = compare_df.rename(columns={
            "university": "Университет",
            "faculty": "Факультет",
            "program": "Направление",
            "code": "Код",
            "city": "Город",
            "pass_score": "Проходной балл",
            "budget": "Бюджетные места",
            "price": "Стоимость",
            "dorm": "Общежитие",
            "military": "Военная кафедра"
        }).drop(columns=["card_id"])

        st.dataframe(compare_df.T, use_container_width=True)

# 3. РАЗДЕЛ: БАЗА ЗНАНИЙ
elif page == "📖 База знаний (Статьи 🖋️)":
    render_articles_page()

# 4. РАЗДЕЛ: ПОМОЩНИК
elif page == "💬 Помощник Абитуриента":
    render_ai_bot_page()
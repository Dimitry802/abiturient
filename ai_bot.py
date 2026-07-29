import streamlit as st

def render_ai_bot_page():
    st.title("🤖 Помощник Абитуриента")
    st.write("Задайте любой вопрос по правилам приема, общежитиям, целевому обучению или отсрочке.")

    # Инициализация истории чата в сессии Streamlit
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Отображение предыдущих сообщений
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Поле ввода нового вопроса
    if prompt := st.chat_input("Напишите ваш вопрос..."):
        # Сохраняем вопрос пользователя
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Простая база правил для ответа (в будущем подключим умную RAG-систему!)
        query = prompt.lower()
        if "арми" in query or "отсроч" in query or "вуц" in query or "воен" in query:
            response = "🪖 **Ответ:** Очная форма обучения по аккредитованным программам бакалавриата и специалитета дает 100% отсрочку от призыва на весь период обучения."
        elif "целевой" in query or "целев" in query:
            response = "🎯 **Ответ:** Подача документов на целевое обучение проходит через Единую платформу «Работа в России». Конкурс на целевые места отдельный и обычно ниже общего."
        elif "общежит" in query or "комнат" in query:
            response = "🏠 **Ответ:** Общежитие предоставляется иногородним студентам очной формы. Приоритет отдается льготным категориям и абитуриентам с высокими баллами."
        elif "документ" in query or "срок" in query or "справк" in query:
            response = "📄 **Ответ:** Прием документов на бюджет обычно завершается 25 июля (или 20 июля, если нужно сдавать ДВИ). Нужны: паспорт, аттестат, СНИЛС и фото."
        else:
            response = "🤖 Я пока учусь и собираю базу знаний по вузам! Обязательно уточню этот вопрос в официальных правилах приема 2026 года."

        # Сохраняем ответ ассистента
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
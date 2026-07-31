import streamlit as st
import google.generativeai as genai


def render_ai_bot_page():
    st.title("💬 Помощник Абитуриента 2026 (AI)")
    st.caption("Умный консультант на базе нейросети Google Gemini")

    # Безопасно считываем ключ из Streamlit Secrets
    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        st.error("⚠️ API ключ не найден в Secrets! Проверьте настройки приложения.")
        return

    # Настраиваем Gemini
    genai.configure(api_key=api_key)

    # Используем актуальное имя модели
    model = genai.GenerativeModel('gemini-2.0-flash')

    # Инициализация истории чата
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant",
             "content": "Привет! Я твой ИИ-консультант по поступлению в 2026 году. Задай любой вопрос о вузах, баллах, льготах или документах!"}
        ]

    # Отображение истории переписки
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Чат-ввод
    if user_input := st.chat_input("Спросите о поступлении..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Нейросеть печатает ответ..."):
                try:
                    system_prompt = (
                        "Ты — экспертный и дружелюбный консультант приёмной комиссии вузов России 2026 года. "
                        "Отвечай вежливо, понятным языком, структурировано (используй списки) и по делу. "
                        f"Вопрос абитуриента: {user_input}"
                    )

                    response = model.generate_content(system_prompt)
                    bot_reply = response.text
                except Exception as e:
                    bot_reply = f"⚠️ Произошла ошибка при обращении к AI: {e}"

                st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
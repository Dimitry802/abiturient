import pandas as pd
import streamlit as st


@st.cache_data
def get_universities_data():
    """Считывает полную базу данных из Excel-файла data.xlsx"""
    try:
        # Читаем наш файлик с 137 направлениями
        df = pd.read_excel('data.xlsx')

        # Защита от пустых значений, чтобы калькулятор не выдавал ошибок
        df['budget_places'] = df['budget_places'].fillna(0)
        df['pass_score'] = df['pass_score'].fillna(0)
        df['price'] = df['price'].fillna(0)
        df['subjects'] = df['subjects'].fillna('')

        # Превращаем строку с предметами в удобный список для фильтра
        df['subjects'] = df['subjects'].apply(
            lambda x: [s.strip() for s in str(x).split(',')] if x else []
        )
        return df
    except Exception as e:
        st.error(f"⚠️ Ошибка чтения файла data.xlsx: {e}")
        return pd.DataFrame()
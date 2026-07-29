import pandas as pd
import streamlit as st


@st.cache_data
def get_universities_data():
    """Считывает полную базу данных из Excel-файла data.xlsx"""
    cols = ['university', 'city', 'code', 'program', 'faculty', 'budget_places',
            'price', 'pass_score', 'dormitory', 'military', 'double_degree', 'target_places', 'subjects']

    try:
        df = pd.read_excel('data.xlsx')

        # Заполняем пустые значения
        df['budget_places'] = df['budget_places'].fillna(0)
        df['pass_score'] = df['pass_score'].fillna(0)
        df['price'] = df['price'].fillna(0)
        df['target_places'] = df['target_places'].fillna(0)
        df['subjects'] = df['subjects'].fillna('')

        # Превращаем строку с предметами в список
        df['subjects'] = df['subjects'].apply(
            lambda x: [s.strip() for s in str(x).split(',')] if x else []
        )
        return df
    except Exception as e:
        st.error(f"⚠️ Ошибка чтения файла data.xlsx: {e}")
        # Возвращаем пустую структуру с нужными колонками, чтобы сайт не падал
        return pd.DataFrame(columns=cols)
import pandas as pd
import streamlit as st

@st.cache_data
def get_universities_data():
    """Возвращает базу данных по вузам"""
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
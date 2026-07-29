import pandas as pd
import streamlit as st

@st.cache_data
def get_universities_data():
    """Возвращает полную базу данных по вузам и их направлениям"""
    data = [
        # ==========================================
        # МГУ им. Н. П. Огарёва (г. Саранск)
        # ==========================================
        {
            "university": "МГУ им. Н. П. Огарёва",
            "city": "Саранск",
            "code": "09.03.03",
            "program": "Прикладная информатика (в экономике)",
            "faculty": "Институт электроники и светотехники",
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
            "university": "МГУ им. Н. П. Огарёва",
            "city": "Саранск",
            "code": "09.03.01",
            "program": "Информатика и вычислительная техника",
            "faculty": "Факультет математики и информационных технологий",
            "budget_places": 40,
            "price": 130000,
            "pass_score": 188,
            "dormitory": True,
            "military": True,
            "double_degree": False,
            "target_places": True,
            "subjects": ["Математика", "Информатика", "Русский язык"]
        },
        {
            "university": "МГУ им. Н. П. Огарёва",
            "city": "Саранск",
            "code": "38.03.01",
            "program": "Экономика и бизнес-аналитика",
            "faculty": "Экономический институт",
            "budget_places": 15,
            "price": 125000,
            "pass_score": 210,
            "dormitory": True,
            "military": True,
            "double_degree": False,
            "target_places": True,
            "subjects": ["Математика", "Обществознание", "Русский язык"]
        },
        {
            "university": "МГУ им. Н. П. Огарёва",
            "city": "Саранск",
            "code": "13.03.02",
            "program": "Электроэнергетика и электротехника",
            "faculty": "Институт электроники и светотехники",
            "budget_places": 45,
            "price": 130000,
            "pass_score": 165,
            "dormitory": True,
            "military": True,
            "double_degree": False,
            "target_places": True,
            "subjects": ["Математика", "Физика", "Русский язык"]
        },

        # ==========================================
        # СПбГУ (г. Санкт-Петербург)
        # ==========================================
        {
            "university": "СПбГУ",
            "city": "Санкт-Петербург",
            "code": "01.03.02",
            "program": "Прикладная математика и информатика",
            "faculty": "ПМ-ПУ",
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
            "university": "СПбГУ",
            "city": "Санкт-Петербург",
            "code": "09.03.04",
            "program": "Программная инженерия",
            "faculty": "Математико-механический факультет",
            "budget_places": 35,
            "price": 340000,
            "pass_score": 285,
            "dormitory": True,
            "military": True,
            "double_degree": True,
            "target_places": False,
            "subjects": ["Математика", "Информатика", "Русский язык"]
        },
        {
            "university": "СПбГУ",
            "city": "Санкт-Петербург",
            "code": "38.03.02",
            "program": "Менеджмент (International Management)",
            "faculty": "Высшая школа менеджмента (ВШМ)",
            "budget_places": 20,
            "price": 450000,
            "pass_score": 290,
            "dormitory": True,
            "military": True,
            "double_degree": True,
            "target_places": False,
            "subjects": ["Математика", "Обществознание", "Русский язык"]
        },

        # ==========================================
        # МГТУ им. Н. Э. Баумана (г. Москва)
        # ==========================================
        {
            "university": "МГТУ им. Н. Э. Баумана",
            "city": "Москва",
            "code": "24.05.01",
            "program": "Проектирование авиационных и ракетных двигателей",
            "faculty": "Специальное машиностроение",
            "budget_places": 50,
            "price": 340000,
            "pass_score": 245,
            "dormitory": True,
            "military": True,
            "double_degree": True,
            "target_places": True,
            "subjects": ["Математика", "Физика", "Русский язык"]
        },
        {
            "university": "МГТУ им. Н. Э. Баумана",
            "city": "Москва",
            "code": "09.03.01",
            "program": "Компьютерные системы и сети (ИУ6)",
            "faculty": "Информатика и системы управления",
            "budget_places": 60,
            "price": 370000,
            "pass_score": 280,
            "dormitory": True,
            "military": True,
            "double_degree": False,
            "target_places": True,
            "subjects": ["Математика", "Информатика", "Русский язык"]
        },
        {
            "university": "МГТУ им. Н. Э. Баумана",
            "city": "Москва",
            "code": "15.03.04",
            "program": "Автоматизация технологических процессов",
            "faculty": "Робототехника и комплексная автоматизация",
            "budget_places": 40,
            "price": 330000,
            "pass_score": 230,
            "dormitory": True,
            "military": True,
            "double_degree": False,
            "target_places": True,
            "subjects": ["Математика", "Физика", "Русский язык"]
        }
    ]
    return pd.DataFrame(data)
# ແອັບຄະນິດສາດວິສະວະກຳ (ຮັນໄດ້ດ້ວຍຕົວເອງ)   ຮັນ: python -m streamlit run app.py
import streamlit as st

from eng_pages import SECTIONS, apply_nav_style

st.set_page_config(page_title="ຄະນິດສາດວິສະວະກຳ", page_icon="🧮", layout="wide")
apply_nav_style()
home = st.Page("views_eng/home.py", title="ໜ້າຫຼັກ", icon="🏠", default=True, url_path="eng_home")
st.navigation({"ເລີ່ມຕົ້ນ": [home], **SECTIONS}).run()

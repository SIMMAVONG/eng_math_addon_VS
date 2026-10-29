"""ລາຍຊື່ໜ້າຄະນິດສາດວິສະວະກຳ — ນຳໄປໃສ່ໃນ st.navigation ຂອງແອັບຫຼັກ

ໃຊ້ໃນ app.py ຂອງ math_app:
    from eng_pages import SECTIONS as ENG_SECTIONS
    st.navigation({"ຄະນິດສາດພື້ນຖານ": [...ໜ້າເກົ່າ...], **ENG_SECTIONS}).run()
"""
import streamlit as st


def _p(file, title, icon):
    return st.Page(f"views_eng/{file}.py", title=title, icon=icon, url_path=f"eng_{file}")


SECTIONS = {
    "ວິສະວະກຳ: ເລກ & ພີຊະຄະນິດ": [
        _p("arithmetic_page", "ເລກຄະນິດ (ບວກ ລົບ ຄູນ ຫານ)", "➕"),
        _p("logic_page", "Logic (ຕາຕະລາງຄວາມຈິງ)", "💡"),
        _p("fractions_percent", "ເສດສ່ວນ & ເປີເຊັນ", "🍰"),
        _p("indices", "ເລກຍົກກຳລັງ", "⬆️"),
        _p("number_systems", "ລະບົບເລກ (Binary/Hex)", "💻"),
        _p("partial_fractions", "ເສດສ່ວນຍ່ອຍ", "🧩"),
        _p("logarithms", "ລອກາລິດ", "🔢"),
        _p("sequences", "ລຳດັບ & ການລວມ", "🎲"),
        _p("matrix_ops", "Matrix", "🧮"),
        _p("determinants", "Determinant & Cramer", "🔑"),
        _p("parabola_page", "Parabola", "🌈"),
        _p("ellipse_page", "Ellipse", "🥚"),
    ],
    "ວິສະວະກຳ: ເລຂາຄະນິດ & ຕຣີໂກນ": [
        _p("areas", "ພື້ນທີ່ຮູບຮາບພຽງ", "🔷"),
        _p("volumes", "ປະລິມານຮູບທົງ 3D", "📦"),
        _p("trigonometry", "ຕຣີໂກນົມມິຕິ", "📐"),
        _p("straight_lines", "ເສັ້ນຊື່ & ສົມຜົນພ້ອມກັນ", "📏"),
    ],
    "ວິສະວະກຳ: ແຄວຄຸລັດ": [
        _p("differentiation", "ການອະນຸພັນ", "📈"),
        _p("integration", "ການອິນທີເກຣດ", "🌊"),
    ],
    "ວິສະວະກຳ: ແບບຝຶກຫັດ": [
        _p("quiz", "ແບບຝຶກຫັດ (ທີລະຂໍ້ / Quiz 10 ຂໍ້)", "📝"),
    ],
}


def apply_nav_style():
    """ເຮັດໃຫ້ຊື່ກຸ່ມເມນູດ້ານຊ້າຍ (ເຊັ່ນ 'ວິສະວະກຳ: ແຄວຄຸລັດ') ເປັນຕົວໜາ ແລະ ໃຫຍ່ຂຶ້ນ"""
    st.markdown(
        """
        <style>
        [data-testid="stNavSectionHeader"],
        [data-testid="stNavSectionHeader"] * {
            font-size: 1.1rem !important;   /* ປັບຂະໜາດທີ່ນີ້ (ປົກກະຕິ ≈ 0.875rem) */
            font-weight: 700 !important;    /* 700 = ໜາ */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

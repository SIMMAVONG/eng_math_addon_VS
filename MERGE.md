# ວິທີລວມເຂົ້າ math_app

1. ກ໊ອບປີ້ ໂຟນເດີ `views_eng/`, `mathcore/` ແລະ ໄຟລ໌ `eng_utils.py`, `eng_pages.py` ໄປວາງໃນໂຟນເດີ math_app (ຢູ່ຂ້າງ app.py ຫຼັກ)
   (`mathcore/` ແມ່ນ common/matrix/determinant/parabola/ellipse ຂອງ math_app ເດີມ — ຖ້າ math_app ມີແພັກເກັດນີ້ຢູ່ແລ້ວ ແລະ ຊື່ຕ່າງ ໃຫ້ແກ້ `from mathcore...` ໃນ views_eng/ ໃຫ້ຊື້ກົງກັນ)
2. ໃນ app.py ຂອງ math_app ເພີ່ມ:

       from eng_pages import SECTIONS as ENG_SECTIONS, apply_nav_style
       apply_nav_style()   # ຕົວໜັງສືກຸ່ມເມນູ ໜາ ແລະ ໃຫຍ່ຂຶ້ນ (ບໍ່ໃສ່ກໍໄດ້)

   ແລ້ວປ່ຽນ st.navigation ໃຫ້ເປັນແບບແບ່ງກຸ່ມ:

       st.navigation({"ຄະນິດສາດພື້ນຖານ": [ ...ໜ້າເກົ່າຂອງ math_app... ], **ENG_SECTIONS}).run()

3. ຕິດຕັ້ງ: python -m pip install -r requirements.txt   (ຕ້ອງມີ sympy, plotly)
4. ຮັນ: python -m streamlit run app.py

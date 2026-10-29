import streamlit as st

st.title("🧮 ຄະນິດສາດວິສະວະກຳ")
st.write("ສື່ການສອນແບບໂຕ້ຕອບ: ປັບຄ່າ ແລ້ວເຫັນຜົນ ແລະ ຂັ້ນຕອນທັນທີ ເໝາະສຳລັບສາທິດໃນຫ້ອງຮຽນ.")
topics = [
    ("➕ ເລກຄະນິດ", "ບວກ ລົບ ຄູນ ຫານ ເສດສ່ວນ, ຄຸນສົມບັດ, (a ± b)²"),
    ("💡 Logic", "ຕາຕະລາງຄວາມຈິງ, If-Then, Converse/Inverse/Contrapositive"),
    ("🍰 ເສດສ່ວນ & ເປີເຊັນ", "ເສດສ່ວນ, ທົດສະນິຍົມ, ອັດຕາສ່ວນ, ເປີເຊັນ"),
    ("⬆️ ເລກຍົກກຳລັງ", "ກົດຂອງ indices, ຫຍໍ້ນິພົດ, surd"),
    ("💻 ລະບົບເລກ", "Binary · Octal · Decimal · Hex"),
    ("🧩 ເສດສ່ວນຍ່ອຍ", "Partial fractions ແບບ cover-up"),
    ("🔢 ລອກາລິດ", "ກົດ log, ສົມຜົນ, ກຣາຟ"),
    ("🎲 ລຳດັບ & ການລວມ", "AP, GP, nPr, nCr, binomial"),
    ("🧮 Matrix", "ບວກ ລົບ ຄູນ, Transpose, Inverse ພ້ອມຂັ້ນຕອນ"),
    ("🔑 Determinant & Cramer", "Determinant 2×2 / 3×3, ແກ້ລະບົບສົມຜົນ"),
    ("🌈 Parabola", "ຈຸດຍອດ, ຮາກ, Focus, Directrix ແລະ ກຣາຟ"),
    ("🥚 Ellipse", "ໂຟກັສ, ຄວາມເບີ້ຍ, PF₁ + PF₂ = 2a, ກວດຕຳແໜ່ງຈຸດ"),
    ("🔷 ພື້ນທີ່", "ຮູບຮາບພຽງ 9 ຊະນິດ"),
    ("📦 ປະລິມານ", "ຮູບທົງ 3 ມິຕິ ໝຸນເບິ່ງໄດ້"),
    ("📐 ຕຣີໂກນົມມິຕິ", "ສາມຫຼ່ຽມ, ກຣາຟ, ກົດ sin/cos"),
    ("📏 ເສັ້ນຊື່", "y = mx + c, ສອງຈຸດ, ສົມຜົນພ້ອມກັນ"),
    ("📈 ການອະນຸພັນ", "f′(x), ເສັ້ນຖືກ, max/min"),
    ("🌊 ການອິນທີເກຣດ", "ອິນທີເກຣດ, ພື້ນທີ່ໃຕ້ເສັ້ນໂຄ້ງ, Riemann"),
    ("📝 ແບບຝຶກຫັດ", "ຝຶກຫັດທີລະຂໍ້ · Quiz 10 ຂໍ້ (20 ຫົວຂໍ້)"),
]
cols = st.columns(3)
for i, (n, d) in enumerate(topics):
    with cols[i % 3]:
        with st.container(border=True):
            st.subheader(n)
            st.caption(d)

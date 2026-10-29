import pandas as pd
import streamlit as st

from eng_utils import render_steps
from mathcore import arithmetic
from mathcore.common import dec, parse_fr, tex, txt

st.title("➕ ເລກຄະນິດ: ບວກ ລົບ ຄູນ ຫານ")
st.caption("ປ້ອນຕົວເລກເຕັມ, ທົດສະນິຍົມ ຫຼື ເສດສ່ວນ (ເຊັ່ນ 3, -2, 0.75, 3/5) — ຄິດແບບແນ່ນອນ ແລະ ສະແດງຂັ້ນຕອນ")
tab1, tab2, tab3 = st.tabs(["ບວກ ລົບ ຄູນ ຫານ", "ຄຸນສົມບັດຂອງຈຳນວນ", "ເອກະລັກ (a ± b)²"])

with tab1:
    c1, c2, c3 = st.columns([3, 2, 3])
    a_t = c1.text_input("ຈຳນວນ a", "1/2", key="ar_a")
    op = c2.radio("ເຄື່ອງໝາຍ", ["+", "-", "×", "÷"], horizontal=True, key="ar_op")
    b_t = c3.text_input("ຈຳນວນ b", "3/4", key="ar_b")
    try:
        a, b = parse_fr(a_t), parse_fr(b_t)
        out = arithmetic.operate(a, b, op)
    except ValueError as e:
        st.error(str(e)); st.stop()
    st.latex(out["equation"])
    m1, m2 = st.columns(2)
    m1.metric("ຄຳຕອບ (ເສດສ່ວນ)", txt(out["result"]))
    m2.metric("ທົດສະນິຍົມ", dec(out["result"], 6))
    with st.expander("ເບິ່ງຂັ້ນຕອນ", expanded=True):
        render_steps(out["steps"])

with tab2:
    st.write("ກວດຄຸນສົມບັດຂອງການບວກ ແລະ ການຄູນ ດ້ວຍຄ່າ a, b, c ທີ່ເລືອກ")
    c = st.columns(3)
    try:
        a = parse_fr(c[0].text_input("a", "2", key="pr_a"))
        b = parse_fr(c[1].text_input("b", "3", key="pr_b"))
        cc = parse_fr(c[2].text_input("c", "5", key="pr_c"))
    except ValueError as e:
        st.error(str(e)); st.stop()
    rows = arithmetic.properties(a, b, cc)
    df = pd.DataFrame([{"ຄຸນສົມບັດ": r["name"], "ຊ້າຍ": f"{r['lhs']} = {txt(r['lv'])}",
                        "ຂວາ": f"{r['rhs']} = {txt(r['rv'])}", "ເທົ່າກັນ": "✅" if r["ok"] else "❌"} for r in rows])
    st.dataframe(df, hide_index=True, width="stretch")
    st.caption("ການລົບ ແລະ ການຫານ ບໍ່ມີຄຸນສົມບັດສະຫຼັບ ແລະ ຈັດກຸ່ມ (ເຊັ່ນ 5 − 3 ≠ 3 − 5)")

with tab3:
    c = st.columns(2)
    try:
        a2 = parse_fr(c[0].text_input("a", "5", key="id_a"))
        b2 = parse_fr(c[1].text_input("b", "2", key="id_b"))
    except ValueError as e:
        st.error(str(e)); st.stop()
    for r in arithmetic.identities(a2, b2):
        st.latex(rf"{r['lhs']} = {r['rhs']}")
        st.write(f"ຊ້າຍ = {txt(r['lv'])}  ·  ຂວາ = {txt(r['rv'])}  {'✅' if r['ok'] else '❌'}")

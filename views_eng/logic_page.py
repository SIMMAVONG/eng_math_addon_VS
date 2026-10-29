import pandas as pd
import streamlit as st

from mathcore import logic

st.title("💡 Logic: ຕາຕະລາງຄວາມຈິງ")
tab1, tab2 = st.tabs(["ຕາຕະລາງຄວາມຈິງ", "If-Then: Converse · Inverse · Contrapositive"])


def color(v):
    return "background-color: #d4edda; color: #155724" if v == "T" else (
        "background-color: #f8d7da; color: #721c24" if v == "F" else "")


def show(headers, rows):
    df = pd.DataFrame(rows, columns=headers)
    styler = df.style
    styler = styler.map(color) if hasattr(styler, "map") else styler.applymap(color)
    st.dataframe(styler, hide_index=True, width="stretch")


with tab1:
    st.write("ໃຊ້ຕົວແປຕົວອັກສອນດຽວ (p, q, r, s — ສູງສຸດ 4 ຕົວ). ເຄື່ອງໝາຍ:")
    st.markdown("`&` ຫຼື `and` = ∧ (ແລະ) · `|` ຫຼື `or` = ∨ (ຫຼື) · `~` ຫຼື `not` = ¬ (ບໍ່) · `->` = → (ຖ້າ…ແລ້ວ) · `<->` = ↔ (ກໍຕໍ່ເມື່ອ)")
    examples = {
        "p → q": "p -> q",
        "(p ∧ q) → p": "(p & q) -> p",
        "p ∨ ¬p": "p | ~p",
        "p ∧ ¬p": "p & ~p",
        "De Morgan: ¬(p ∧ q) ↔ (¬p ∨ ¬q)": "~(p & q) <-> (~p | ~q)",
        "ກົດ Syllogism": "((p -> q) & (q -> r)) -> (p -> r)",
        "ພິມເອງ": "",
    }
    ex = st.selectbox("ຕົວຢ່າງ", list(examples))
    expr = st.text_input("ສູດ", value=examples[ex] or "p -> q", key=f"lg_{ex}")
    try:
        tt = logic.truth_table(expr)
    except ValueError as e:
        st.error(str(e)); st.stop()
    st.latex(tt["expr"].replace("∧", r"\land").replace("∨", r"\lor").replace("¬", r"\lnot ")
             .replace("→", r"\rightarrow ").replace("↔", r"\leftrightarrow "))
    show(tt["headers"], tt["rows"])
    if tt["kind"] == "tautology":
        st.success("Tautology — ຈິງສະເໝີ ທຸກກໍລະນີ ✅")
    elif tt["kind"] == "contradiction":
        st.error("Contradiction — ຜິດສະເໝີ ທຸກກໍລະນີ")
    else:
        st.info("Contingent — ບາງກໍລະນີຈິງ ບາງກໍລະນີຜິດ")
    st.caption("ຖັນສຸດທ້າຍແມ່ນຜົນຂອງສູດທັງໝົດ. T = ຈິງ, F = ຜິດ")

with tab2:
    fam = logic.implication_family()
    st.write("ຈາກປະໂຫຍກ **ຖ້າ p ແລ້ວ q** ສ້າງໄດ້ 3 ຮູບແບບ:")
    st.markdown("- **Converse**: ຖ້າ q ແລ້ວ p\n- **Inverse**: ຖ້າບໍ່ p ແລ້ວບໍ່ q\n- **Contrapositive**: ຖ້າບໍ່ q ແລ້ວບໍ່ p")
    show(fam["headers"], fam["rows"])
    (st.success if fam["contrapositive_equiv"] else st.error)(
        "p → q ເທົ່າກັບ Contrapositive (¬q → ¬p) ທຸກກໍລະນີ ✅" if fam["contrapositive_equiv"] else "ບໍ່ເທົ່າກັນ")
    if fam["converse_equiv_inverse"]:
        st.success("Converse ເທົ່າກັບ Inverse ✅")
    if not fam["converse_equiv_original"]:
        st.warning("p → q ບໍ່ເທົ່າກັບ Converse (q → p) — ຢ່າສັບສົນ!")

import math
from fractions import Fraction

import streamlit as st

st.title("🍰 ເສດສ່ວນ, ອັດຕາສ່ວນ, ທົດສະນິຍົມ & ເປີເຊັນ")


def fl(fr: Fraction) -> str:
    if fr.denominator == 1:
        return str(fr.numerator)
    sign = "-" if fr < 0 else ""
    return rf"{sign}\frac{{{abs(fr.numerator)}}}{{{fr.denominator}}}"


def mixed(fr: Fraction) -> str:
    if fr.denominator == 1 or abs(fr.numerator) < fr.denominator:
        return ""
    w, r = divmod(abs(fr.numerator), fr.denominator)
    sign = "-" if fr < 0 else ""
    return rf"{sign}{w}\frac{{{r}}}{{{fr.denominator}}}"


def decimal_expansion(fr: Fraction, maxd=40) -> str:
    """ເຊັ່ນ 1/3 -> 0.(3)  ,  1/4 -> 0.25"""
    n, d = abs(fr.numerator), fr.denominator
    ip, rem = divmod(n, d)
    digits, seen = [], {}
    while rem and rem not in seen and len(digits) < maxd:
        seen[rem] = len(digits)
        rem *= 10
        digits.append(str(rem // d))
        rem %= d
    sign = "-" if fr < 0 else ""
    if not rem:
        return f"{sign}{ip}" + ("." + "".join(digits) if digits else "")
    if rem in seen:
        i = seen[rem]
        return f"{sign}{ip}." + "".join(digits[:i]) + "(" + "".join(digits[i:]) + ")"
    return f"{sign}{ip}." + "".join(digits) + "…"


tab1, tab2, tab3, tab4 = st.tabs(["ຄິດເລກເສດສ່ວນ", "ເສດສ່ວນ ↔ ທົດສະນິຍົມ ↔ %", "ອັດຕາສ່ວນ & ສັດສ່ວນ", "ເປີເຊັນ"])

with tab1:
    c = st.columns([2, 2, 1, 2, 2])
    a = c[0].number_input("ເສດ 1: ຕົວຕັ້ງ", value=1, step=1, key="fa")
    b = c[0].number_input("ເສດ 1: ຕົວຫານ", value=2, step=1, min_value=1, key="fb")
    op = c[2].selectbox("ເຄື່ອງໝາຍ", ["+", "−", "×", "÷"])
    cc = c[3].number_input("ເສດ 2: ຕົວຕັ້ງ", value=3, step=1, key="fc")
    d = c[3].number_input("ເສດ 2: ຕົວຫານ", value=4, step=1, min_value=1, key="fd")
    f1, f2 = Fraction(int(a), int(b)), Fraction(int(cc), int(d))
    if op == "÷" and f2 == 0:
        st.error("ຫານດ້ວຍສູນບໍ່ໄດ້"); st.stop()
    res = {"+": f1 + f2, "−": f1 - f2, "×": f1 * f2, "÷": f1 / f2}[op]
    sym = {"+": "+", "−": "-", "×": r"\times", "÷": r"\div"}[op]
    st.latex(rf"\frac{{{a}}}{{{b}}} {sym} \frac{{{cc}}}{{{d}}} = {fl(res)}")
    if op in "+−":
        L = math.lcm(int(b), int(d))
        n1, n2 = int(a) * (L // int(b)), int(cc) * (L // int(d))
        st.write(f"ຂັ້ນຕອນ: ຕົວຫານຮ່ວມນ້ອຍສຸດ (LCM) = {L}")
        st.latex(rf"= \frac{{{n1}}}{{{L}}} {sym} \frac{{{n2}}}{{{L}}} = \frac{{{n1 + n2 if op == '+' else n1 - n2}}}{{{L}}} = {fl(res)}")
    elif op == "×":
        st.latex(rf"= \frac{{{a} \times {cc}}}{{{b} \times {d}}} = \frac{{{int(a) * int(cc)}}}{{{int(b) * int(d)}}} = {fl(res)}")
    else:
        st.write("ຫານ = ຄູນດ້ວຍສ່ວນກັບກັນ")
        st.latex(rf"= \frac{{{a}}}{{{b}}} \times \frac{{{d}}}{{{cc}}} = {fl(res)}")
    if mixed(res):
        st.write("ເປັນຈຳນວນປະສົມ:")
        st.latex(mixed(res))
    st.write(f"ທົດສະນິຍົມ = **{decimal_expansion(res)}**  ·  ເປີເຊັນ = **{float(res) * 100:.6g} %**")

with tab2:
    kind = st.radio("ປ້ອນຄ່າເປັນ", ["ທົດສະນິຍົມ", "ເສດສ່ວນ", "ເປີເຊັນ"], horizontal=True)
    try:
        if kind == "ທົດສະນິຍົມ":
            v = Fraction(st.text_input("ທົດສະນິຍົມ (ເຊັ່ນ 0.375)", "0.375").strip())
        elif kind == "ເສດສ່ວນ":
            cx, cy = st.columns(2)
            v = Fraction(int(cx.number_input("ຕົວຕັ້ງ", value=3, step=1, key="t2n")),
                         int(cy.number_input("ຕົວຫານ", value=8, step=1, min_value=1, key="t2d")))
        else:
            v = Fraction(st.text_input("ເປີເຊັນ (ເຊັ່ນ 37.5)", "37.5").strip()) / 100
    except (ValueError, ZeroDivisionError):
        st.error("ປ້ອນຕົວເລກໃຫ້ຖືກຮູບແບບ ເຊັ່ນ 0.375"); st.stop()
    m1, m2, m3 = st.columns(3)
    m1.metric("ທົດສະນິຍົມ", decimal_expansion(v))
    m2.metric("ເປີເຊັນ", f"{float(v) * 100:.6g} %")
    m3.metric("ເສດສ່ວນ (ຫຍໍ້ແລ້ວ)", f"{v.numerator}/{v.denominator}")
    st.latex(fl(v))
    st.caption("0.(3) ໝາຍເຖິງ 0.333… (ເລກໃນວົງເລັບຊ້ຳກັນ)")

with tab3:
    st.markdown("##### ແບ່ງຕາມອັດຕາສ່ວນ")
    c1, c2 = st.columns(2)
    total = c1.number_input("ຈຳນວນລວມ", value=1000.0, min_value=0.0)
    txt = c2.text_input("ອັດຕາສ່ວນ (ຄັ່ນດ້ວຍ :)", "2:3:5")
    try:
        parts = [int(p) for p in txt.replace(" ", "").split(":") if p]
        if len(parts) < 2 or min(parts) <= 0:
            raise ValueError
    except ValueError:
        st.error("ໃສ່ອັດຕາສ່ວນເປັນຈຳນວນເຕັມບວກ ເຊັ່ນ 2:3:5"); st.stop()
    s = sum(parts)
    rows = [{"ສ່ວນ": i + 1, "ອັດຕາ": p, "ເສດສ່ວນ": f"{p}/{s}", "ໄດ້ຮັບ": round(total * p / s, 4)} for i, p in enumerate(parts)]
    st.dataframe(rows, hide_index=True, width="stretch")
    st.write(f"ຜົນລວມອັດຕາ = {s} → ແຕ່ລະສ່ວນ = ຈຳນວນລວມ × (ອັດຕາ ÷ {s})")
    st.markdown("##### ສັດສ່ວນ (proportion)")
    mode = st.radio("ຊະນິດ", ["ສັດສ່ວນໂດຍກົງ (y ເພີ່ມ ເມື່ອ x ເພີ່ມ)", "ສັດສ່ວນຜັນກັບ (y ຫຼຸດ ເມື່ອ x ເພີ່ມ)"])
    k1, k2, k3 = st.columns(3)
    x1 = k1.number_input("x ເດີມ", value=4.0, min_value=0.0001)
    y1 = k2.number_input("y ເດີມ", value=12.0)
    x2 = k3.number_input("x ໃໝ່", value=10.0, min_value=0.0001)
    if mode.startswith("ສັດສ່ວນໂດຍກົງ"):
        st.success(f"y ໃໝ່ = y ເດີມ × x ໃໝ່ ÷ x ເດີມ = {y1 * x2 / x1:.6g}")
    else:
        st.success(f"y ໃໝ່ = (x ເດີມ × y ເດີມ) ÷ x ໃໝ່ = {x1 * y1 / x2:.6g}")

with tab4:
    kind = st.selectbox("ຄິດຫຍັງ?", ["x % ຂອງ N", "A ເປັນຈັກ % ຂອງ N", "ປ່ຽນແປງຈາກຄ່າເກົ່າເປັນຄ່າໃໝ່ (% ເພີ່ມ/ຫຼຸດ)",
                                      "ຫາຄ່າເດີມ ເມື່ອຮູ້ຄ່າຫຼັງເພີ່ມ/ຫຼຸດ %"])
    if kind == "x % ຂອງ N":
        p = st.number_input("x (%)", value=15.0); n = st.number_input("N", value=240.0)
        st.success(f"{p:g}% ຂອງ {n:g} = {p / 100 * n:.6g}")
    elif kind.startswith("A ເປັນ"):
        A = st.number_input("A", value=45.0); n = st.number_input("N", value=180.0, min_value=0.0001)
        st.success(f"{A:g} ເປັນ {A / n * 100:.6g} % ຂອງ {n:g}")
    elif kind.startswith("ປ່ຽນແປງ"):
        old = st.number_input("ຄ່າເກົ່າ", value=80.0, min_value=0.0001); new = st.number_input("ຄ່າໃໝ່", value=100.0)
        ch = (new - old) / old * 100
        st.success(f"{'ເພີ່ມຂຶ້ນ' if ch >= 0 else 'ຫຼຸດລົງ'} {abs(ch):.6g} %")
        st.latex(r"\%\text{ປ່ຽນແປງ} = \frac{\text{ໃໝ່} - \text{ເກົ່າ}}{\text{ເກົ່າ}} \times 100")
    else:
        new = st.number_input("ຄ່າຫຼັງປ່ຽນ", value=115.0)
        p = st.number_input("ເພີ່ມຂຶ້ນ (+) ຫຼື ຫຼຸດລົງ (−) ຈັກ %", value=15.0)
        if 1 + p / 100 == 0:
            st.error("ຫຼຸດ 100% ຫາຄ່າເດີມບໍ່ໄດ້")
        else:
            st.success(f"ຄ່າເດີມ = {new / (1 + p / 100):.6g}")

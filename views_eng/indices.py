import sympy as sp
import streamlit as st

from eng_utils import X, parse_math

st.title("⬆️ ເລກຍົກກຳລັງ (Indices)")
tab1, tab2, tab3 = st.tabs(["ກົດເລກຍົກກຳລັງ", "ຫຍໍ້ນິພົດ", "ຮາກ & ຮູບ surd"])


def base(a):
    return f"({a})" if a < 0 else str(a)


with tab1:
    laws = ["aᵐ × aⁿ = aᵐ⁺ⁿ", "aᵐ ÷ aⁿ = aᵐ⁻ⁿ", "(aᵐ)ⁿ = aᵐⁿ", "a⁰ = 1", "a⁻ⁿ = 1 / aⁿ (ສ່ວນກັບ)",
            "a^(m/n) = ⁿ√(aᵐ)", "(ab)ⁿ = aⁿ bⁿ"]
    law = st.selectbox("ເລືອກກົດ", laws)
    c = st.columns(4)
    a = c[0].number_input("a", value=2, step=1)
    m = c[1].number_input("m", value=3, step=1)
    n = c[2].number_input("n", value=4, step=1)
    bb = c[3].number_input("b (ສຳລັບ (ab)ⁿ)", value=3, step=1)
    a, m, n, bb = int(a), int(m), int(n), int(bb)
    A, B = sp.Integer(a), sp.Integer(bb)
    if a == 0 and law[0] != "a" or (a == 0 and "⁻" in law):
        st.warning("a ≠ 0"); st.stop()
    try:
        if law.startswith("aᵐ ×"):
            L, R = A**m * A**n, A**(m + n)
            st.latex(rf"{base(a)}^{{{m}}} \times {base(a)}^{{{n}}} = {base(a)}^{{{m}+{n}}} = {base(a)}^{{{m + n}}}")
        elif law.startswith("aᵐ ÷"):
            L, R = A**m / A**n, A**(m - n)
            st.latex(rf"{base(a)}^{{{m}}} \div {base(a)}^{{{n}}} = {base(a)}^{{{m}-({n})}} = {base(a)}^{{{m - n}}}")
        elif law.startswith("(aᵐ)"):
            L, R = (A**m)**n, A**(m * n)
            st.latex(rf"\left({base(a)}^{{{m}}}\right)^{{{n}}} = {base(a)}^{{{m} \times {n}}} = {base(a)}^{{{m * n}}}")
        elif law.startswith("a⁰"):
            L, R = A**0, sp.Integer(1)
            st.latex(rf"{base(a)}^{{0}} = 1")
        elif law.startswith("a⁻ⁿ"):
            L, R = A**(-n), 1 / A**n
            st.latex(rf"{base(a)}^{{-{n}}} = \frac{{1}}{{{base(a)}^{{{n}}}}}")
        elif law.startswith("a^(m/n)"):
            if n == 0:
                st.warning("n ≠ 0"); st.stop()
            L = A ** sp.Rational(m, n)
            R = sp.root(A**m, n) if n > 0 else sp.root(A**m, n)
            st.latex(rf"{base(a)}^{{\frac{{{m}}}{{{n}}}}} = \sqrt[{n}]{{{base(a)}^{{{m}}}}}")
        else:
            L, R = (A * B)**n, A**n * B**n
            st.latex(rf"({base(a)} \times {base(bb)})^{{{n}}} = {base(a)}^{{{n}}} \times {base(bb)}^{{{n}}}")
    except Exception:
        st.error("ຄິດບໍ່ໄດ້ (ກວດ a, m, n — ເຊັ່ນ ຮາກຄູ່ຂອງຈຳນວນລົບ)"); st.stop()
    L, R = sp.nsimplify(L), sp.nsimplify(R)
    c1, c2, c3 = st.columns(3)
    c1.metric("ຊ້າຍ", sp.sstr(L))
    c2.metric("ຂວາ", sp.sstr(R))
    c3.metric("ເທົ່າກັນ?", "✅" if sp.simplify(L - R) == 0 else "❌")

with tab2:
    expr_txt = st.text_input("ປ້ອນນິພົດ ເຊັ່ນ (x^3*x^4)/x^2 ຫຼື (2x^2)^3 ຫຼື x^(-2)*x^5", "(x^3*x^4)/x^2")
    try:
        e = parse_math(expr_txt)
    except ValueError as err:
        st.error(str(err)); st.stop()
    st.latex(rf"{sp.latex(e)} = {sp.latex(sp.simplify(e))}")
    st.caption("ກົດທີ່ໃຊ້ບ່ອຍ: ຄູນ → ບວກກຳລັງ · ຫານ → ລົບກຳລັງ · ກຳລັງຂອງກຳລັງ → ຄູນກຳລັງ")

with tab3:
    N = st.number_input("ຈຳນວນເຕັມ N ເພື່ອຖອດຮາກທີ່ສອງ √N", value=72, min_value=1, step=1)
    k = st.number_input("ດັດຊະນີຮາກ (2 = ຮາກທີ່ສອງ, 3 = ຮາກທີ່ສາມ)", value=2, min_value=2, max_value=6, step=1)
    N, k = int(N), int(k)
    fac = sp.factorint(N)
    outside = 1
    inside = 1
    for p, ex in fac.items():
        outside *= p ** (ex // k)
        inside *= p ** (ex % k)
    fs = r" \cdot ".join(f"{p}^{{{ex}}}" for p, ex in fac.items()) if N > 1 else "1"
    root_sym = r"\sqrt" if k == 2 else rf"\sqrt[{k}]"
    st.latex(rf"{root_sym}{{{N}}} = {root_sym}{{{fs}}}")
    st.latex(rf"= {outside if outside != 1 else ''}{root_sym}{{{inside}}}" if inside != 1 else rf"= {outside}")
    st.write(f"ຄ່າປະມານ = {N ** (1 / k):.6g}")

import math

import plotly.graph_objects as go
import sympy as sp
import streamlit as st

st.title("🎲 ລຳດັບ, ຜົນບວກ & ການລວມ (AP · GP · nPr · nCr)")
tab1, tab2, tab3, tab4 = st.tabs(["ລຳດັບເລກຄະນິດ (AP)", "ລຳດັບເລຂາຄະນິດ (GP)", "ວິທີລຽງ & ວິທີເລືອກ", "ທິດສະດີບົດ binomial"])

with tab1:
    c = st.columns(3)
    a = c[0].number_input("ພົດທຳອິດ a", value=3.0, key="ap_a")
    d = c[1].number_input("ຜົນຕ່າງຮ່ວມ d", value=4.0, key="ap_d")
    n = int(c[2].number_input("ຈຳນວນພົດ n", value=10, min_value=1, max_value=200, step=1, key="ap_n"))
    Tn = a + (n - 1) * d
    Sn = n / 2 * (2 * a + (n - 1) * d)
    st.latex(rf"T_n = a + (n-1)d = {a:g} + ({n}-1)({d:g}) = {Tn:g}")
    st.latex(rf"S_n = \frac{{n}}{{2}}\left[2a + (n-1)d\right] = \frac{{{n}}}{{2}}\left[{2 * a:g} + {(n - 1) * d:g}\right] = {Sn:g}")
    terms = [a + i * d for i in range(n)]
    st.write("ພົດຕ່າງໆ: " + ", ".join(f"{t:g}" for t in terms[:15]) + (" …" if n > 15 else ""))
    fig = go.Figure(go.Scatter(x=list(range(1, n + 1)), y=terms, mode="lines+markers"))
    fig.update_layout(height=320, xaxis_title="n", yaxis_title="Tₙ", margin=dict(t=20))
    st.plotly_chart(fig, width="stretch")
    st.markdown("**ຫາ n ເມື່ອຮູ້ຄ່າຂອງພົດ**")
    target = st.number_input("ຄ່າພົດທີ່ຕ້ອງການ", value=43.0, key="ap_t")
    if d == 0:
        st.info("d = 0: ທຸກພົດເທົ່າ a")
    else:
        nn = (target - a) / d + 1
        st.write(f"n = (T − a)/d + 1 = {nn:.6g} " + ("✅ ເປັນພົດທີ " + str(int(round(nn))) if nn > 0 and abs(nn - round(nn)) < 1e-9 else "→ ບໍ່ແມ່ນພົດຂອງລຳດັບນີ້"))

with tab2:
    c = st.columns(3)
    a2 = c[0].number_input("ພົດທຳອິດ a", value=2.0, key="gp_a")
    r = c[1].number_input("ອັດຕາສ່ວນຮ່ວມ r", value=3.0, key="gp_r")
    n2 = int(c[2].number_input("ຈຳນວນພົດ n", value=8, min_value=1, max_value=60, step=1, key="gp_n"))
    Tn2 = a2 * r ** (n2 - 1)
    st.latex(rf"T_n = a r^{{n-1}} = {a2:g} \times {r:g}^{{{n2 - 1}}} = {Tn2:.6g}")
    if r == 1:
        Sn2 = a2 * n2
        st.latex(rf"r = 1 \Rightarrow S_n = na = {Sn2:g}")
    else:
        Sn2 = a2 * (1 - r ** n2) / (1 - r)
        st.latex(rf"S_n = \frac{{a(1-r^n)}}{{1-r}} = \frac{{{a2:g}(1-{r:g}^{{{n2}}})}}{{1-{r:g}}} = {Sn2:.6g}")
    if abs(r) < 1:
        st.success(f"|r| < 1 → ຜົນບວກຮອດອະນັນ S∞ = a/(1−r) = {a2 / (1 - r):.6g}")
    else:
        st.info("|r| ≥ 1 → ຜົນບວກຮອດອະນັນບໍ່ລວມ (diverges)")
    terms2 = [a2 * r ** i for i in range(n2)]
    st.write("ພົດຕ່າງໆ: " + ", ".join(f"{t:.5g}" for t in terms2[:12]) + (" …" if n2 > 12 else ""))
    fig = go.Figure(go.Scatter(x=list(range(1, n2 + 1)), y=terms2, mode="lines+markers"))
    fig.update_layout(height=320, xaxis_title="n", yaxis_title="Tₙ", margin=dict(t=20))
    st.plotly_chart(fig, width="stretch")

with tab3:
    c = st.columns(2)
    n3 = int(c[0].number_input("n", value=7, min_value=0, max_value=100, step=1, key="pc_n"))
    r3 = int(c[1].number_input("r", value=3, min_value=0, max_value=100, step=1, key="pc_r"))
    if r3 > n3:
        st.error("r ຕ້ອງບໍ່ເກີນ n"); st.stop()
    st.latex(rf"{n3}! = {math.factorial(n3)}")
    st.latex(rf"{{}}^{{{n3}}}P_{{{r3}}} = \frac{{{n3}!}}{{({n3}-{r3})!}} = {math.perm(n3, r3)}")
    st.latex(rf"{{}}^{{{n3}}}C_{{{r3}}} = \frac{{{n3}!}}{{{r3}!\,({n3}-{r3})!}} = {math.comb(n3, r3)}")
    st.caption("ວິທີລຽງ (permutation): ລຳດັບສຳຄັນ · ວິທີເລືອກ (combination): ລຳດັບບໍ່ສຳຄັນ  ·  nPr = nCr × r!")

with tab4:
    c = st.columns(3)
    pa = c[0].text_input("ພົດທຳອິດ", "x", key="bn_a")
    pb = c[1].text_input("ພົດທີສອງ", "2", key="bn_b")
    pn = int(c[2].number_input("ກຳລັງ n", value=5, min_value=0, max_value=12, step=1, key="bn_n"))
    from eng_utils import parse_math
    try:
        A, B = parse_math(pa), parse_math(pb)
    except ValueError as e:
        st.error(str(e)); st.stop()
    st.latex(rf"({sp.latex(A)} + {sp.latex(B)})^{{{pn}}} = {sp.latex(sp.expand((A + B) ** pn))}")
    st.write("ສຳປະສິດ (ແຖວ n ຂອງສາມຫຼ່ຽມ Pascal): " + ", ".join(str(math.comb(pn, k)) for k in range(pn + 1)))

import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.title("🔢 ລອກາລິດ (Logarithms)")
tab1, tab2, tab3, tab4 = st.tabs(["ຄິດ log", "ເລກຍົກກຳລັງ ↔ log", "ກົດ log", "ສົມຜົນ & ກຣາຟ"])


def ok_base(b):
    return b > 0 and b != 1


with tab1:
    c1, c2 = st.columns(2)
    b = c1.number_input("ຖານ b (b > 0, b ≠ 1)", value=2.0, min_value=0.0001, key="l_b")
    x = c2.number_input("ຄ່າ x (x > 0)", value=32.0, min_value=0.0000001, key="l_x")
    if not ok_base(b):
        st.error("ຖານຕ້ອງບໍ່ເທົ່າກັບ 1"); st.stop()
    y = math.log(x) / math.log(b)
    st.latex(rf"\log_{{{b:g}}} {x:g} = {y:.6g} \quad\Longleftrightarrow\quad {b:g}^{{{y:.6g}}} = {x:g}")
    m1, m2, m3 = st.columns(3)
    m1.metric(f"log_{b:g}({x:g})", f"{y:.6g}")
    m2.metric("log₁₀ (ທົ່ວໄປ)", f"{math.log10(x):.6g}")
    m3.metric("ln (ທຳມະຊາດ, ຖານ e)", f"{math.log(x):.6g}")
    st.latex(rf"\log_b x = \frac{{\log x}}{{\log b}} = \frac{{{math.log10(x):.5g}}}{{{math.log10(b):.5g}}} = {y:.6g}")

with tab2:
    find = st.radio("ຕ້ອງການຫາ", ["N (ຄ່າ)", "y (ເລກຍົກກຳລັງ)", "b (ຖານ)"], horizontal=True)
    c = st.columns(3)
    if find.startswith("N"):
        b2 = c[0].number_input("b", value=2.0, min_value=0.0001, key="t2b")
        y2 = c[1].number_input("y", value=5.0, key="t2y")
        if not ok_base(b2):
            st.error("b ≠ 1"); st.stop()
        N = b2 ** y2
        st.latex(rf"{b2:g}^{{{y2:g}}} = {N:.6g} \Longleftrightarrow \log_{{{b2:g}}} {N:.6g} = {y2:g}")
    elif find.startswith("y"):
        b2 = c[0].number_input("b", value=3.0, min_value=0.0001, key="t2b2")
        N = c[1].number_input("N", value=81.0, min_value=0.0000001, key="t2N")
        if not ok_base(b2):
            st.error("b ≠ 1"); st.stop()
        y2 = math.log(N) / math.log(b2)
        st.latex(rf"\log_{{{b2:g}}} {N:g} = {y2:.6g} \Longleftrightarrow {b2:g}^{{{y2:.6g}}} = {N:g}")
    else:
        y2 = c[0].number_input("y", value=4.0, key="t2y3")
        N = c[1].number_input("N", value=81.0, min_value=0.0000001, key="t2N3")
        if y2 == 0:
            st.error("y ≠ 0"); st.stop()
        b2 = N ** (1 / y2)
        st.latex(rf"b^{{{y2:g}}} = {N:g} \Rightarrow b = {N:g}^{{1/{y2:g}}} = {b2:.6g}")

with tab3:
    law = st.selectbox("ກົດ", ["ຜະລິດຕະພັນ: log(MN) = log M + log N", "ຜົນຫານ: log(M/N) = log M − log N",
                               "ກຳລັງ: log(Mᵏ) = k·log M", "ປ່ຽນຖານ: log_b N = log_c N / log_c b"])
    c = st.columns(4)
    b3 = c[0].number_input("ຖານ b", value=10.0, min_value=0.0001, key="l3b")
    M = c[1].number_input("M", value=8.0, min_value=0.0001, key="l3M")
    N3 = c[2].number_input("N", value=5.0, min_value=0.0001, key="l3N")
    k = c[3].number_input("k (ຫຼື ຖານ c)", value=3.0, min_value=0.0001, key="l3k")
    if not ok_base(b3) or (law.startswith("ປ່ຽນ") and not ok_base(k)):
        st.error("ຖານຕ້ອງ > 0 ແລະ ≠ 1"); st.stop()
    lg = lambda v, base=b3: math.log(v) / math.log(base)
    if law.startswith("ຜະລິດ"):
        L, R = lg(M * N3), lg(M) + lg(N3)
        st.latex(rf"\log_{{{b3:g}}}({M:g}\times{N3:g}) = \log {M:g} + \log {N3:g}")
    elif law.startswith("ຜົນຫານ"):
        L, R = lg(M / N3), lg(M) - lg(N3)
        st.latex(rf"\log_{{{b3:g}}}\frac{{{M:g}}}{{{N3:g}}} = \log {M:g} - \log {N3:g}")
    elif law.startswith("ກຳລັງ"):
        L, R = lg(M ** k), k * lg(M)
        st.latex(rf"\log_{{{b3:g}}}({M:g}^{{{k:g}}}) = {k:g}\log {M:g}")
    else:
        L, R = lg(M), lg(M, k) / lg(b3, k)
        st.latex(rf"\log_{{{b3:g}}} {M:g} = \frac{{\log_{{{k:g}}} {M:g}}}{{\log_{{{k:g}}} {b3:g}}}")
    a, b_, c_ = st.columns(3)
    a.metric("ຊ້າຍ", f"{L:.6g}"); b_.metric("ຂວາ", f"{R:.6g}"); c_.metric("ເທົ່າກັນ?", "✅" if math.isclose(L, R, rel_tol=1e-9, abs_tol=1e-12) else "❌")

with tab4:
    st.markdown("##### ແກ້ສົມຜົນ  bˣ = c")
    c = st.columns(2)
    bb = c[0].number_input("b", value=3.0, min_value=0.0001, key="l4b")
    cc = c[1].number_input("c (c > 0)", value=50.0, min_value=0.0000001, key="l4c")
    if not ok_base(bb):
        st.error("b ≠ 1"); st.stop()
    xs = math.log(cc) / math.log(bb)
    st.latex(rf"{bb:g}^x = {cc:g} \Rightarrow x = \frac{{\log {cc:g}}}{{\log {bb:g}}} = {xs:.6g}")
    gb = st.slider("ຖານ b ສຳລັບກຣາຟ", 0.2, 10.0, 2.0, 0.1, key="gb")
    if abs(gb - 1) < 1e-9:
        st.warning("b = 1 ບໍ່ໄດ້"); st.stop()
    x1 = np.linspace(-4, 4, 400)
    x2 = np.linspace(0.02, 8, 400)
    fig = go.Figure()
    fig.add_scatter(x=x1, y=gb ** x1, mode="lines", name=f"y = {gb:g}ˣ", line=dict(width=3))
    fig.add_scatter(x=x2, y=np.log(x2) / np.log(gb), mode="lines", name=f"y = log_{gb:g} x", line=dict(width=3))
    fig.add_scatter(x=[-4, 8], y=[-4, 8], mode="lines", name="y = x", line=dict(dash="dot", color="gray"))
    fig.update_layout(xaxis_range=[-4, 8], yaxis_range=[-4, 8], height=480, margin=dict(t=20))
    fig.update_yaxes(scaleanchor="x")
    st.plotly_chart(fig, width="stretch")
    st.caption("ກຣາຟຂອງ bˣ ແລະ log_b x ເປັນພາບສະທ້ອນຂອງກັນ ຜ່ານເສັ້ນ y = x (ເປັນຟັງຊັນຜັນກັນ). ທັງສອງຜ່ານຈຸດ (0,1) ແລະ (1,0).")

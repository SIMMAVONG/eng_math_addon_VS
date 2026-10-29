import math
from fractions import Fraction

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.title("📏 ເສັ້ນຊື່ & ລະບົບສົມຜົນເສັ້ນຊື່")
tab1, tab2, tab3 = st.tabs(["y = mx + c", "ເສັ້ນຜ່ານສອງຈຸດ", "ສົມຜົນພ້ອມກັນ (ຈຸດຕັດ)"])


def base_fig(rng=10):
    fig = go.Figure()
    fig.add_hline(y=0, line_color="gray", line_width=1)
    fig.add_vline(x=0, line_color="gray", line_width=1)
    fig.update_layout(height=450, margin=dict(t=10), xaxis_range=[-rng, rng], yaxis_range=[-rng, rng])
    fig.update_yaxes(scaleanchor="x")
    return fig


def fr(v):
    return Fraction(str(v)).limit_denominator(10000)


with tab1:
    c1, c2 = st.columns(2)
    m = c1.slider("ຄວາມຊັນ m (gradient)", -5.0, 5.0, 2.0, 0.1)
    c = c2.slider("ຈຸດຕັດແກນ y (c)", -8.0, 8.0, 1.0, 0.5)
    x = np.array([-10, 10])
    fig = base_fig()
    fig.add_scatter(x=x, y=m * x + c, mode="lines", line=dict(width=3), name="y = mx + c")
    fig.add_scatter(x=[0], y=[c], mode="markers", marker=dict(size=11, color="red"), name="ຈຸດຕັດ y")
    if m != 0:
        fig.add_scatter(x=[-c / m], y=[0], mode="markers", marker=dict(size=11, color="green"), name="ຈຸດຕັດ x")
    st.plotly_chart(fig, width="stretch")
    st.latex(rf"y = {m:g}x {'+' if c >= 0 else '-'} {abs(c):g}")
    k = st.columns(3)
    k[0].metric("ຈຸດຕັດແກນ y", f"(0, {c:g})")
    k[1].metric("ຈຸດຕັດແກນ x", f"({-c / m:.4g}, 0)" if m != 0 else ("ບໍ່ມີ (ຂະໜານແກນ x)" if c != 0 else "ທັບແກນ x"))
    k[2].metric("ມຸມກັບແກນ x", f"{math.degrees(math.atan(m)):.2f}°")
    st.caption("m > 0 ເສັ້ນຂຶ້ນ · m < 0 ເສັ້ນລົງ · m = 0 ເສັ້ນຮາບພຽງ. ສອງເສັ້ນຂະໜານກັນ ເມື່ອ m ເທົ່າກັນ; ຕັ້ງສາກກັນ ເມື່ອ m₁·m₂ = −1")

with tab2:
    c = st.columns(4)
    x1 = c[0].number_input("x₁", value=1.0); y1 = c[1].number_input("y₁", value=2.0)
    x2 = c[2].number_input("x₂", value=5.0); y2 = c[3].number_input("y₂", value=10.0)
    if (x1, y1) == (x2, y2):
        st.error("ສອງຈຸດຕ້ອງຕ່າງກັນ"); st.stop()
    dist = math.hypot(x2 - x1, y2 - y1)
    mid = ((x1 + x2) / 2, (y1 + y2) / 2)
    fig = base_fig()
    if x1 == x2:
        st.latex(rf"x = {x1:g}\ (\text{{ເສັ້ນຕັ້ງ, ຄວາມຊັນບໍ່ມີຄ່າ}})")
        fig.add_scatter(x=[x1, x1], y=[-10, 10], mode="lines", line=dict(width=3), name="ເສັ້ນ")
    else:
        m = (y2 - y1) / (x2 - x1)
        cc = y1 - m * x1
        st.latex(rf"m = \frac{{y_2 - y_1}}{{x_2 - x_1}} = \frac{{{y2:g} - {y1:g}}}{{{x2:g} - {x1:g}}} = {m:.6g}")
        st.latex(rf"y - y_1 = m(x - x_1) \Rightarrow y = {m:.6g}x {'+' if cc >= 0 else '-'} {abs(cc):.6g}")
        xs = np.array([-10, 10])
        fig.add_scatter(x=xs, y=m * xs + cc, mode="lines", line=dict(width=3), name="ເສັ້ນ")
    fig.add_scatter(x=[x1, x2], y=[y1, y2], mode="markers+text", text=["P₁", "P₂"], textposition="top center",
                    marker=dict(size=11, color="red"), name="ຈຸດ")
    fig.add_scatter(x=[mid[0]], y=[mid[1]], mode="markers", marker=dict(size=10, color="green", symbol="diamond"), name="ຈຸດກາງ")
    st.plotly_chart(fig, width="stretch")
    k = st.columns(2)
    k[0].metric("ໄລຍະຫ່າງ P₁P₂", f"{dist:.6g}")
    k[1].metric("ຈຸດກາງ", f"({mid[0]:.4g}, {mid[1]:.4g})")
    st.latex(rf"d = \sqrt{{(x_2-x_1)^2 + (y_2-y_1)^2}} = {dist:.6g}")

with tab3:
    st.latex(r"a_1 x + b_1 y = c_1 \qquad a_2 x + b_2 y = c_2")
    c = st.columns(3)
    a1 = c[0].number_input("a₁", value=1.0); b1 = c[1].number_input("b₁", value=1.0); c1v = c[2].number_input("c₁", value=5.0)
    c = st.columns(3)
    a2 = c[0].number_input("a₂", value=1.0); b2 = c[1].number_input("b₂", value=-1.0); c2v = c[2].number_input("c₂", value=1.0)
    if (a1 == 0 and b1 == 0) or (a2 == 0 and b2 == 0):
        st.error("ແຕ່ລະສົມຜົນຕ້ອງມີ x ຫຼື y"); st.stop()
    A1, B1, C1, A2, B2, C2 = map(fr, (a1, b1, c1v, a2, b2, c2v))
    det = A1 * B2 - A2 * B1
    fig = base_fig()
    for (a_, b_, c_, nm) in [(a1, b1, c1v, "ເສັ້ນ 1"), (a2, b2, c2v, "ເສັ້ນ 2")]:
        if b_ != 0:
            xs = np.array([-10, 10])
            fig.add_scatter(x=xs, y=(c_ - a_ * xs) / b_, mode="lines", line=dict(width=3), name=nm)
        else:
            fig.add_scatter(x=[c_ / a_] * 2, y=[-10, 10], mode="lines", line=dict(width=3), name=nm)
    if det != 0:
        xs_ = (C1 * B2 - C2 * B1) / det
        ys_ = (A1 * C2 - A2 * C1) / det
        fig.add_scatter(x=[float(xs_)], y=[float(ys_)], mode="markers+text", text=[f"({float(xs_):.3g}, {float(ys_):.3g})"],
                        textposition="top right", marker=dict(size=13, color="red"), name="ຈຸດຕັດ")
        st.success(f"ຄຳຕອບ: x = {xs_} , y = {ys_}   (≈ {float(xs_):.5g}, {float(ys_):.5g})")
        st.latex(rf"D = a_1 b_2 - a_2 b_1 = {det},\quad x = \frac{{c_1 b_2 - c_2 b_1}}{{D}},\quad y = \frac{{a_1 c_2 - a_2 c_1}}{{D}}")
        st.write(f"ກວດ: ສົມຜົນ 1 → {a1:g}({float(xs_):.5g}) + {b1:g}({float(ys_):.5g}) = {a1 * float(xs_) + b1 * float(ys_):.5g} ✅")
    else:
        if (A1 * C2 - A2 * C1 == 0) and (C1 * B2 - C2 * B1 == 0):
            st.info("ສອງເສັ້ນທັບກັນ → ມີຄຳຕອບເປັນອະນັນ")
        else:
            st.warning("ສອງເສັ້ນຂະໜານກັນ → ບໍ່ມີຄຳຕອບ")
    st.plotly_chart(fig, width="stretch")

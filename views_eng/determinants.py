import numpy as np
import plotly.graph_objects as go
import streamlit as st

from eng_utils import matrix_input, render_steps
from mathcore import determinant
from mathcore.common import mat_tex, tex, txt

st.title("🔑 Determinant & Cramer's Rule")
tab1, tab2 = st.tabs(["Determinant 2×2 / 3×3", "Cramer's Rule (ແກ້ລະບົບສົມຜົນ)"])

with tab1:
    n = st.radio("ຂະໜາດ", [2, 3], horizontal=True, format_func=lambda v: f"{v}×{v}", key="dt_n")
    base = [[2, 1, 3], [0, 4, 1], [5, 2, 1]]
    try:
        M = matrix_input("a", n, n, f"dt{n}", lambda i, j: str(base[i][j]))
    except ValueError as e:
        st.error(str(e)); st.stop()
    out = determinant.det2(M) if n == 2 else determinant.det3(M)
    st.latex(rf"\det A = {mat_tex(M, 'v')} = {tex(out['value'])}")
    st.success(f"det A = {txt(out['value'])}")
    if out["value"] == 0:
        st.info("det = 0 → Matrix ນີ້ບໍ່ມີ Inverse (singular)")
    with st.expander("ເບິ່ງຂັ້ນຕອນ", expanded=True):
        render_steps(out["steps"])

with tab2:
    n2 = st.radio("ຈຳນວນຕົວແປ", [2, 3], horizontal=True, format_func=lambda v: f"{v} ຕົວແປ", key="cr_n")
    names = ["x", "y", "z"][:n2]
    A0 = [[2, 1, -1], [1, 3, 2], [1, 0, 1]]
    b0 = [1, 13, 4]
    st.caption("ຮູບແບບ: a₁x + b₁y (+ c₁z) = ຄ່າຄົງທີ່  — ປ້ອນສຳປະສິດ (ຊ້າຍ) ແລະ ຄ່າຄົງທີ່ (ຂວາ)")
    left, right = st.columns([3, 1])
    try:
        with left:
            st.markdown("**ສຳປະສິດ A**")
            A = matrix_input("a", n2, n2, f"crA{n2}", lambda i, j: str(A0[i][j]))
        with right:
            st.markdown("**ຄ່າຄົງທີ່ b**")
            bcol = matrix_input("b", n2, 1, f"crb{n2}", lambda i, j: str(b0[i]))
    except ValueError as e:
        st.error(str(e)); st.stop()
    b = [row[0] for row in bcol]
    res = determinant.cramer(A, b)
    if res["unique"]:
        st.success("ຄຳຕອບ:  " + ",   ".join(f"{nm} = {txt(s)}" for nm, s in zip(names, res["solution"])))
    else:
        st.warning("D = 0 → ບໍ່ມີຄຳຕອບດຽວ (ໃຊ້ Cramer's Rule ບໍ່ໄດ້)")
    with st.expander("ເບິ່ງຂັ້ນຕອນ", expanded=True):
        render_steps(res["steps"])
    if n2 == 2:
        fig = go.Figure()
        xs = np.array([-10.0, 10.0])
        for (a1, b1), c1, nm in zip(A, b, ["ສົມຜົນ 1", "ສົມຜົນ 2"]):
            a1, b1, c1 = float(a1), float(b1), float(c1)
            if b1 != 0:
                fig.add_scatter(x=xs, y=(c1 - a1 * xs) / b1, mode="lines", line=dict(width=3), name=nm)
            elif a1 != 0:
                fig.add_scatter(x=[c1 / a1] * 2, y=[-10, 10], mode="lines", line=dict(width=3), name=nm)
        if res["unique"]:
            sx, sy = float(res["solution"][0]), float(res["solution"][1])
            fig.add_scatter(x=[sx], y=[sy], mode="markers+text", text=[f"({sx:.3g}, {sy:.3g})"], textposition="top right",
                            marker=dict(size=13, color="red"), name="ຈຸດຕັດ")
        fig.add_hline(y=0, line_color="gray", line_width=1)
        fig.add_vline(x=0, line_color="gray", line_width=1)
        fig.update_layout(height=420, margin=dict(t=10), xaxis_range=[-10, 10], yaxis_range=[-10, 10])
        fig.update_yaxes(scaleanchor="x")
        st.plotly_chart(fig, width="stretch")

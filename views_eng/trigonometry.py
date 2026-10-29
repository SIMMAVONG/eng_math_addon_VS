import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.title("📐 ຕຣີໂກນົມມິຕິ (Trigonometry)")
tab1, tab2, tab3 = st.tabs(["ສາມຫຼ່ຽມມຸມສາກ", "ກຣາຟ sin · cos · tan", "ສາມຫຼ່ຽມທົ່ວໄປ (ກົດ sin / cos)"])
D2R = math.pi / 180


def draw_tri(A_pt, B_pt, C_pt, labels=("A", "B", "C")):
    xs = [A_pt[0], B_pt[0], C_pt[0], A_pt[0]]
    ys = [A_pt[1], B_pt[1], C_pt[1], A_pt[1]]
    fig = go.Figure(go.Scatter(x=xs, y=ys, fill="toself", mode="lines+markers+text", line=dict(width=3),
                               text=list(labels) + [""], textposition="top center"))
    fig.update_yaxes(scaleanchor="x")
    fig.update_layout(height=340, margin=dict(t=10), showlegend=False)
    return fig


with tab1:
    mode = st.radio("ຮູ້ຂໍ້ມູນ", ["ສອງຂາ (a, b)", "ຂາຍາວສຸດ c ແລະ ມຸມ A", "ຂາ a ແລະ ມຸມ A"], horizontal=True)
    st.caption("ມຸມສາກຢູ່ C · a ກົງຂ້າມມຸມ A · b ກົງຂ້າມມຸມ B · c = hypotenuse")
    c = st.columns(2)
    if mode.startswith("ສອງຂາ"):
        a = c[0].number_input("a", min_value=0.01, value=3.0, key="r_a")
        b = c[1].number_input("b", min_value=0.01, value=4.0, key="r_b")
        cc = math.hypot(a, b)
        A = math.degrees(math.atan2(a, b))
        st.latex(rf"c = \sqrt{{a^2 + b^2}} = \sqrt{{{a:g}^2 + {b:g}^2}} = {cc:.6g}")
        st.latex(rf"A = \tan^{{-1}}\frac{{a}}{{b}} = {A:.4f}^\circ")
    elif mode.startswith("ຂາຍາວ"):
        cc = c[0].number_input("c (hypotenuse)", min_value=0.01, value=10.0, key="r_c")
        A = c[1].number_input("ມຸມ A (ອົງສາ, 0–90)", min_value=0.1, max_value=89.9, value=30.0, key="r_A")
        a, b = cc * math.sin(A * D2R), cc * math.cos(A * D2R)
        st.latex(rf"a = c\sin A = {a:.6g},\qquad b = c\cos A = {b:.6g}")
    else:
        a = c[0].number_input("a", min_value=0.01, value=5.0, key="r_a2")
        A = c[1].number_input("ມຸມ A (ອົງສາ, 0–90)", min_value=0.1, max_value=89.9, value=40.0, key="r_A2")
        cc, b = a / math.sin(A * D2R), a / math.tan(A * D2R)
        st.latex(rf"c = \frac{{a}}{{\sin A}} = {cc:.6g},\qquad b = \frac{{a}}{{\tan A}} = {b:.6g}")
    B = 90 - A
    m = st.columns(5)
    m[0].metric("a", f"{a:.5g}"); m[1].metric("b", f"{b:.5g}"); m[2].metric("c", f"{cc:.5g}")
    m[3].metric("A", f"{A:.4g}°"); m[4].metric("B", f"{B:.4g}°")
    st.latex(rf"\sin A = \frac{{a}}{{c}} = {a / cc:.4f},\quad \cos A = \frac{{b}}{{c}} = {b / cc:.4f},\quad \tan A = \frac{{a}}{{b}} = {a / b:.4f}")
    st.plotly_chart(draw_tri((0, b), (a, 0), (0, 0), ("A", "B", "C")), width="stretch")
    with st.expander("ຄ່າມຸມພິເສດ"):
        st.markdown("""
| ມຸມ | sin | cos | tan |
|---|---|---|---|
| 0° | 0 | 1 | 0 |
| 30° | 1/2 | √3/2 | 1/√3 |
| 45° | √2/2 | √2/2 | 1 |
| 60° | √3/2 | 1/2 | √3 |
| 90° | 1 | 0 | ບໍ່ມີຄ່າ |
""")

with tab2:
    fn = st.radio("ຟັງຊັນ", ["sin", "cos", "tan"], horizontal=True)
    st.latex(rf"y = A\,\{fn}(Bx + C) + D")
    c = st.columns(4)
    Aa = c[0].slider("A (amplitude)", -5.0, 5.0, 1.0, 0.1)
    Bb = c[1].slider("B (ຄວາມຖີ່)", 0.25, 5.0, 1.0, 0.25)
    Cc = c[2].slider("C (ເຟສ, ອົງສາ)", -180, 180, 0, 5)
    Dd = c[3].slider("D (ເລື່ອນຂຶ້ນ/ລົງ)", -5.0, 5.0, 0.0, 0.1)
    x = np.linspace(0, 720, 2000)
    arg = np.radians(Bb * x + Cc)
    with np.errstate(all="ignore"):
        y = Aa * {"sin": np.sin, "cos": np.cos, "tan": np.tan}[fn](arg) + Dd
    if fn == "tan":
        y = np.where(np.abs(y) > 10, np.nan, y)
    fig = go.Figure(go.Scatter(x=x, y=y, mode="lines", line=dict(width=3), connectgaps=False))
    fig.add_hline(y=Dd, line_dash="dot", line_color="gray")
    fig.update_xaxes(tickvals=list(range(0, 721, 90)), title="x (ອົງສາ)")
    fig.update_layout(height=400, margin=dict(t=10))
    if fn == "tan":
        fig.update_yaxes(range=[-6, 6])
    st.plotly_chart(fig, width="stretch")
    period = (180 if fn == "tan" else 360) / Bb
    m = st.columns(3)
    m[0].metric("Amplitude" if fn != "tan" else "ປັດໄຈຂະຫຍາຍ", f"{abs(Aa):g}" if fn != "tan" else "ບໍ່ມີ (tan ບໍ່ມີຂອບ)")
    m[1].metric("ຄາບ (period)", f"{period:g}°")
    m[2].metric("ເລື່ອນເຟສ", f"{-Cc / Bb:g}°")

with tab3:
    st.caption("ສາມຫຼ່ຽມທົ່ວໄປ: ດ້ານ a, b, c ກົງຂ້າມມຸມ A, B, C ຕາມລຳດັບ")
    case = st.selectbox("ຮູ້ຂໍ້ມູນ", ["SSS (ສາມດ້ານ)", "SAS (ສອງດ້ານ ແລະ ມຸມລະຫວ່າງ)", "AAS/ASA (ສອງມຸມ ແລະ ໜຶ່ງດ້ານ)",
                                      "SSA (ສອງດ້ານ ແລະ ມຸມທີ່ບໍ່ຢູ່ລະຫວ່າງ — ອາດມີ 2 ຄຳຕອບ)"])
    c = st.columns(3)
    sols = []
    try:
        if case.startswith("SSS"):
            a = c[0].number_input("a", min_value=0.01, value=7.0, key="g_a")
            b = c[1].number_input("b", min_value=0.01, value=8.0, key="g_b")
            cc = c[2].number_input("c", min_value=0.01, value=9.0, key="g_c")
            if a + b <= cc or a + cc <= b or b + cc <= a:
                raise ValueError("ສາມດ້ານນີ້ບໍ່ປະກອບເປັນສາມຫຼ່ຽມ")
            A = math.degrees(math.acos((b * b + cc * cc - a * a) / (2 * b * cc)))
            B = math.degrees(math.acos((a * a + cc * cc - b * b) / (2 * a * cc)))
            sols.append((a, b, cc, A, B, 180 - A - B))
            st.latex(r"\cos A = \frac{b^2 + c^2 - a^2}{2bc}")
        elif case.startswith("SAS"):
            a = c[0].number_input("a", min_value=0.01, value=7.0, key="g_a2")
            b = c[1].number_input("b", min_value=0.01, value=10.0, key="g_b2")
            C = c[2].number_input("ມຸມ C (ອົງສາ)", min_value=0.1, max_value=179.9, value=50.0, key="g_C2")
            cc = math.sqrt(a * a + b * b - 2 * a * b * math.cos(C * D2R))
            A = math.degrees(math.acos((b * b + cc * cc - a * a) / (2 * b * cc)))
            sols.append((a, b, cc, A, 180 - A - C, C))
            st.latex(r"c^2 = a^2 + b^2 - 2ab\cos C")
        elif case.startswith("AAS"):
            A = c[0].number_input("ມຸມ A", min_value=0.1, max_value=179.0, value=40.0, key="g_A3")
            B = c[1].number_input("ມຸມ B", min_value=0.1, max_value=179.0, value=60.0, key="g_B3")
            a = c[2].number_input("ດ້ານ a (ກົງຂ້າມ A)", min_value=0.01, value=8.0, key="g_a3")
            if A + B >= 180:
                raise ValueError("ຜົນບວກສອງມຸມຕ້ອງໜ້ອຍກວ່າ 180°")
            C = 180 - A - B
            sols.append((a, a * math.sin(B * D2R) / math.sin(A * D2R), a * math.sin(C * D2R) / math.sin(A * D2R), A, B, C))
            st.latex(r"\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C}")
        else:
            a = c[0].number_input("a", min_value=0.01, value=6.0, key="g_a4")
            b = c[1].number_input("b", min_value=0.01, value=8.0, key="g_b4")
            A = c[2].number_input("ມຸມ A (ກົງຂ້າມ a)", min_value=0.1, max_value=179.0, value=35.0, key="g_A4")
            s = b * math.sin(A * D2R) / a
            if s > 1:
                raise ValueError("ບໍ່ມີສາມຫຼ່ຽມທີ່ເປັນໄປໄດ້ (sin B > 1)")
            B1 = math.degrees(math.asin(s))
            for B in sorted({B1, 180 - B1}):
                if A + B < 180 - 1e-9:
                    C = 180 - A - B
                    sols.append((a, b, a * math.sin(C * D2R) / math.sin(A * D2R), A, B, C))
            st.latex(r"\sin B = \frac{b\sin A}{a}")
    except ValueError as e:
        st.error(str(e)); st.stop()

    if len(sols) == 2:
        st.warning("ກໍລະນີກຳກວມ (ambiguous case): ມີ 2 ສາມຫຼ່ຽມທີ່ເປັນໄປໄດ້")
    for i, (a, b, cc, A, B, C) in enumerate(sols):
        area = 0.5 * a * b * math.sin(C * D2R)
        if len(sols) > 1:
            st.markdown(f"**ຄຳຕອບທີ {i + 1}**")
        m = st.columns(7)
        for col, (lab, v) in zip(m, [("a", a), ("b", b), ("c", cc), ("A", A), ("B", B), ("C", C)]):
            col.metric(lab, f"{v:.4g}" + ("°" if lab in "ABC" else ""))
        m[6].metric("ພື້ນທີ່", f"{area:.4g}")
        Ap, Bp = (0, 0), (cc, 0)
        Cp = (b * math.cos(A * D2R), b * math.sin(A * D2R))
        st.plotly_chart(draw_tri(Ap, Bp, Cp), width="stretch", key=f"tri{i}")
    st.caption("ພື້ນທີ່ = ½ ab sin C")

import numpy as np
import plotly.graph_objects as go
import sympy as sp
import streamlit as st

from eng_utils import X, parse_math, to_func

st.title("🌊 ການອິນທີເກຣດ (Integration)")
st.caption("ພິມຟັງຊັນຂອງ x ເຊັ່ນ 3x^2 + 2x + 1, sin(x), e^x, 1/x, sqrt(x)  ·  ln(x) ແລະ log(x) ແມ່ນ logarithm ທຳມະຊາດ")

tab1, tab2, tab3 = st.tabs(["ອິນທີເກຣດບໍ່ກຳນົດ", "ອິນທີເກຣດກຳນົດ & ພື້ນທີ່", "ຜົນບວກ Riemann"])

with tab1:
    text = st.text_input("f(x) =", value="3x^2 + 2x + 1", key="i_f")
    try:
        f = parse_math(text)
    except ValueError as e:
        st.error(str(e)); st.stop()
    F = sp.integrate(f, X)
    if F.has(sp.Integral):
        st.warning("ຫາອິນທີເກຣດແບບປິດບໍ່ໄດ້ສຳລັບຟັງຊັນນີ້ — ລອງຟັງຊັນງ່າຍກວ່າ")
    else:
        st.latex(rf"\int \left({sp.latex(f)}\right) dx = {sp.latex(F)} + C")
        terms = sp.Add.make_args(sp.expand(f))
        if len(terms) > 1:
            with st.expander("ຂັ້ນຕອນ: ອິນທີເກຣດທີລະພົດ"):
                st.write("∫ xⁿ dx = xⁿ⁺¹/(n+1) + C (n ≠ −1)  ·  ∫ (u + v) dx = ∫u dx + ∫v dx")
                for t in terms:
                    st.latex(rf"\int {sp.latex(t)}\, dx = {sp.latex(sp.integrate(t, X))}")
        ok = sp.simplify(sp.diff(F, X) - f) == 0
        st.success("ກວດຄືນ: d/dx (ຄຳຕອບ) = f(x) ✅" if ok else "ກວດຄືນດ້ວຍການອະນຸພັນ — ກະລຸນາກວດ")

with tab2:
    text2 = st.text_input("f(x) =", value="x^2", key="i_f2")
    c1, c2 = st.columns(2)
    a = c1.number_input("ຂອບເຂດລຸ່ມ a", value=0.0)
    b = c2.number_input("ຂອບເຂດເທິງ b", value=3.0)
    try:
        g = parse_math(text2)
    except ValueError as e:
        st.error(str(e)); st.stop()
    if b <= a:
        st.error("b ຕ້ອງຫຼາຍກວ່າ a"); st.stop()
    exact = sp.integrate(g, (X, sp.nsimplify(a), sp.nsimplify(b)))
    xs = np.linspace(a, b, 800)
    ys = to_func(g)(xs)
    if exact.has(sp.Integral) or not exact.is_real:
        if np.isnan(ys).any():
            st.error("ຟັງຊັນບໍ່ມີຄ່າໃນຊ່ວງນີ້ (ຫຼື ບໍ່ຕໍ່ເນື່ອງ) — ປ່ຽນຂອບເຂດ"); st.stop()
        val = float(np.sum((ys[1:] + ys[:-1]) / 2 * np.diff(xs)))
        st.metric("ຄ່າປະມານ (ວິທີ trapezoid)", f"{val:.6g}")
    else:
        val = float(exact)
        st.latex(rf"\int_{{{a:g}}}^{{{b:g}}} \left({sp.latex(g)}\right) dx = {sp.latex(exact)} \approx {val:.6g}")
        F = sp.integrate(g, X)
        if not F.has(sp.Integral):
            st.latex(rf"= \left[{sp.latex(F)}\right]_{{{a:g}}}^{{{b:g}}} = F({b:g}) - F({a:g})")
    fig = go.Figure()
    fig.add_scatter(x=xs, y=ys, mode="lines", fill="tozeroy", name="f(x)", line=dict(width=3))
    fig.add_hline(y=0, line_color="gray", line_width=1)
    fig.update_layout(height=400, margin=dict(t=20), xaxis_title="x", yaxis_title="y")
    st.plotly_chart(fig, width="stretch")
    if np.isfinite(ys).all() and (ys < 0).any():
        area = float(np.sum((np.abs(ys[1:]) + np.abs(ys[:-1])) / 2 * np.diff(xs)))
        st.warning(f"ມີສ່ວນທີ່ຢູ່ຕ່ຳກວ່າແກນ x: ອິນທີເກຣດ = ພື້ນທີ່ເທິງ − ພື້ນທີ່ລຸ່ມ. ພື້ນທີ່ຈິງ (ບວກທັງໝົດ) ≈ {area:.6g}")

with tab3:
    st.caption("ປະມານພື້ນທີ່ໃຕ້ເສັ້ນໂຄ້ງດ້ວຍສີ່ຫຼ່ຽມ ແລ້ວເບິ່ງວ່າ n ຫຼາຍຂຶ້ນ ຄຳຕອບໃກ້ຄ່າແທ້ຂຶ້ນແນວໃດ")
    text3 = st.text_input("f(x) =", value="x^2", key="i_f3")
    c1, c2, c3 = st.columns(3)
    a3 = c1.number_input("a", value=0.0, key="ra")
    b3 = c2.number_input("b", value=3.0, key="rb")
    method = c3.selectbox("ວິທີ", ["ຊ້າຍ (left)", "ຂວາ (right)", "ກາງ (midpoint)", "Trapezoid"])
    n = st.slider("ຈຳນວນແຖບ n", 1, 100, 6)
    try:
        h = parse_math(text3)
    except ValueError as e:
        st.error(str(e)); st.stop()
    if b3 <= a3:
        st.error("b ຕ້ອງຫຼາຍກວ່າ a"); st.stop()
    fn = to_func(h)
    edges = np.linspace(a3, b3, n + 1)
    dx = (b3 - a3) / n
    if method.startswith("ຊ້າຍ"): hts = fn(edges[:-1])
    elif method.startswith("ຂວາ"): hts = fn(edges[1:])
    elif method.startswith("ກາງ"): hts = fn((edges[:-1] + edges[1:]) / 2)
    else: hts = None
    if hts is not None:
        approx = float(np.sum(hts) * dx)
    else:
        approx = float(np.sum((fn(edges[:-1]) + fn(edges[1:])) / 2) * dx)
    if not np.isfinite(approx):
        st.error("ຟັງຊັນບໍ່ມີຄ່າໃນຊ່ວງນີ້"); st.stop()
    ex = sp.integrate(h, (X, sp.nsimplify(a3), sp.nsimplify(b3)))
    xs = np.linspace(a3, b3, 600)
    fig = go.Figure()
    if hts is not None:
        lefts = edges[:-1]
        fig.add_bar(x=lefts, y=hts, width=dx, offset=0, opacity=0.4, marker_line_width=1, name="ສີ່ຫຼ່ຽມ")
    else:
        px, py = [], []
        for i in range(n):
            px += [edges[i], edges[i], edges[i + 1], edges[i + 1], None]
            py += [0, float(fn(edges[i])), float(fn(edges[i + 1])), 0, None]
        fig.add_scatter(x=px, y=py, fill="toself", mode="lines", opacity=0.5, name="trapezoid")
    fig.add_scatter(x=xs, y=fn(xs), mode="lines", line=dict(width=3, color="black"), name="f(x)")
    fig.update_layout(height=400, margin=dict(t=20), xaxis_title="x")
    st.plotly_chart(fig, width="stretch")
    m1, m2, m3 = st.columns(3)
    m1.metric("ຄ່າປະມານ", f"{approx:.6g}")
    if ex.has(sp.Integral) or not ex.is_real:
        m2.metric("ຄ່າແທ້", "—")
    else:
        m2.metric("ຄ່າແທ້", f"{float(ex):.6g}")
        m3.metric("ຄວາມຄາດເຄື່ອນ", f"{abs(approx - float(ex)):.3g}")

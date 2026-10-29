import numpy as np
import plotly.graph_objects as go
import sympy as sp
import streamlit as st

from eng_utils import X, parse_math, to_func

st.title("📈 ການອະນຸພັນ (Differentiation)")
st.caption("ພິມຟັງຊັນຂອງ x ເຊັ່ນ x^3 - 6x^2 + 9x + 1, sin(x), e^(2x), ln(x), sqrt(x), (x^2+1)/(x-1)  ·  ln(x) ແລະ log(x) ແມ່ນ logarithm ທຳມະຊາດ")

tab1, tab2, tab3 = st.tabs(["ຫາ f′(x) & ເສັ້ນຖືກ", "ຈຸດວິກິດ (max / min)", "ກົດການອະນຸພັນ"])

with tab1:
    text = st.text_input("f(x) =", value="x^3 - 6x^2 + 9x + 1", key="d_f")
    try:
        f = parse_math(text)
    except ValueError as e:
        st.error(str(e))
        st.stop()
    f1 = sp.diff(f, X)
    f2 = sp.diff(f1, X)
    st.latex(rf"f(x) = {sp.latex(f)}")
    st.latex(rf"f'(x) = \frac{{d}}{{dx}}\left({sp.latex(f)}\right) = {sp.latex(f1)}")
    st.latex(rf"f''(x) = {sp.latex(f2)}")
    st.caption(f"ແບບຫຍໍ້ (simplified): f′(x) = {sp.simplify(f1)}")

    terms = sp.Add.make_args(f)
    if len(terms) > 1:
        with st.expander("ຂັ້ນຕອນ: ອະນຸພັນທີລະພົດ (ກົດຜົນບວກ)"):
            st.write("d/dx (u + v) = u′ + v′ ແລະ d/dx (a·xⁿ) = a·n·xⁿ⁻¹")
            for t in terms:
                st.latex(rf"\frac{{d}}{{dx}}\left({sp.latex(t)}\right) = {sp.latex(sp.diff(t, X))}")

    st.markdown("##### ເສັ້ນຖືກ (tangent) ທີ່ຈຸດ x = x₀")
    c1, c2, c3 = st.columns(3)
    x0 = c1.number_input("x₀", value=1.0, step=0.5)
    xmin = c2.number_input("x ຕ່ຳສຸດ", value=-2.0)
    xmax = c3.number_input("x ສູງສຸດ", value=5.0)
    if xmax <= xmin:
        st.error("x ສູງສຸດ ຕ້ອງຫຼາຍກວ່າ x ຕ່ຳສຸດ")
        st.stop()
    y0 = f.subs(X, x0)
    m = f1.subs(X, x0)
    if not (y0.is_real and m.is_real and y0.is_finite and m.is_finite):
        st.warning("f(x) ຫຼື f′(x) ບໍ່ມີຄ່າທີ່ x₀ ນີ້ (ນອກໂດເມນ ຫຼື ບໍ່ຕໍ່ເນື່ອງ)")
    else:
        y0f, mf = float(y0), float(m)
        a, b, c = st.columns(3)
        a.metric("f(x₀)", f"{y0f:.4g}")
        b.metric("ຄວາມຊັນ f′(x₀)", f"{mf:.4g}")
        c.metric("ເສັ້ນຖືກ", f"y = {mf:.4g}x + {y0f - mf * x0:.4g}")
        xs = np.linspace(xmin, xmax, 600)
        fig = go.Figure()
        fig.add_scatter(x=xs, y=to_func(f)(xs), mode="lines", name="f(x)", line=dict(width=3))
        fig.add_scatter(x=xs, y=mf * (xs - x0) + y0f, mode="lines", name="ເສັ້ນຖືກ", line=dict(dash="dash"))
        fig.add_scatter(x=[x0], y=[y0f], mode="markers", marker=dict(size=12, color="red"), name="ຈຸດ (x₀, f(x₀))")
        ys = to_func(f)(xs)
        if np.isfinite(ys).any():
            lo, hi = np.nanpercentile(ys, 2), np.nanpercentile(ys, 98)
            pad = (hi - lo) * 0.3 + 1e-9
            fig.update_yaxes(range=[lo - pad, hi + pad])
        fig.update_layout(height=430, margin=dict(t=20), xaxis_title="x", yaxis_title="y")
        st.plotly_chart(fig, width="stretch")

with tab2:
    text2 = st.text_input("f(x) =", value="x^3 - 6x^2 + 9x + 1", key="d_f2")
    try:
        g = parse_math(text2)
    except ValueError as e:
        st.error(str(e))
        st.stop()
    g1, g2 = sp.diff(g, X), sp.diff(sp.diff(g, X), X)
    st.latex(rf"f'(x) = {sp.latex(sp.simplify(g1))} = 0")
    sols = sp.solveset(g1, X, domain=sp.S.Reals)
    if sols == sp.S.EmptySet:
        st.info("ບໍ່ມີຈຸດວິກິດ (f′(x) = 0 ບໍ່ມີຄຳຕອບຈິງ)")
    elif not isinstance(sols, sp.FiniteSet):
        st.warning("f′(x) = 0 ມີຄຳຕອບຫຼາຍແບບ/ອະນັນ (ເຊັ່ນ sin, cos ທີ່ເປັນຄາບ ຫຼື ຄ່າຄົງທີ່) ຫຼື ຫາຍາກ — ລອງຟັງຊັນພະຫຸນາມ ຫຼື ຈຳກັດໂດເມນ")
    else:
        rows = []
        pts = []
        for s in sorted(sols, key=lambda v: float(v)):
            val = g.subs(X, s)
            try:
                d2v = float(g2.subs(X, s))
            except (TypeError, ValueError):
                d2v = None
            if d2v is None: kind = "f″ ບໍ່ມີຄ່າ (ອາດເປັນຈຸດແຫຼມ ເຊັ່ນ |x|) — ກວດເຄື່ອງໝາຍ f′ ຂ້າງຊ້າຍ-ຂວາ"
            elif d2v > 0: kind = "ຄ່າຕ່ຳສຸດທ້ອງຖິ່ນ (min)"
            elif d2v < 0: kind = "ຄ່າສູງສຸດທ້ອງຖິ່ນ (max)"
            else: kind = "ບໍ່ສາມາດສະຫຼຸບດ້ວຍ f″ (ກວດເຄື່ອງໝາຍ f′ ຂ້າງຊ້າຍ-ຂວາ)"
            rows.append({"x": str(sp.nsimplify(s)), "f(x)": f"{float(val):.4g}",
                         "f″(x)": f"{d2v:.4g}" if d2v is not None else "—", "ຊະນິດ": kind})
            pts.append((float(s), float(val), kind))
        st.dataframe(rows, hide_index=True, width="stretch")
        xs0 = [p[0] for p in pts]
        xs = np.linspace(min(xs0) - 3, max(xs0) + 3, 600)
        fig = go.Figure()
        fig.add_scatter(x=xs, y=to_func(g)(xs), mode="lines", name="f(x)", line=dict(width=3))
        fig.add_scatter(x=xs, y=to_func(g1)(xs), mode="lines", name="f′(x)", line=dict(dash="dot"))
        fig.add_scatter(x=[p[0] for p in pts], y=[p[1] for p in pts], mode="markers+text",
                        text=["max" if "max" in p[2] else ("min" if "min" in p[2] else "?") for p in pts],
                        textposition="top center", marker=dict(size=12, color="red"), name="ຈຸດວິກິດ")
        fig.add_hline(y=0, line_color="gray", line_width=1)
        ys = to_func(g)(xs)
        lo, hi = np.nanpercentile(ys, 3), np.nanpercentile(ys, 97)
        pad = (hi - lo) * 0.4 + 1e-9
        fig.update_yaxes(range=[lo - pad, hi + pad])
        fig.update_layout(height=430, margin=dict(t=20), xaxis_title="x")
        st.plotly_chart(fig, width="stretch")
        st.info("f′(x) = 0 → ຄວາມຊັນເປັນສູນ (ເສັ້ນຖືກຮາບພຽງ). ຖ້າ f″ > 0 ເປັນ min, f″ < 0 ເປັນ max.")

with tab3:
    st.markdown("##### ຕາຕະລາງອະນຸພັນມາດຕະຖານ")
    st.markdown("""
| f(x) | f′(x) |
|---|---|
| a (ຄ່າຄົງທີ່) | 0 |
| a·xⁿ | a·n·xⁿ⁻¹ |
| eˣ | eˣ |
| ln x | 1/x |
| sin x | cos x |
| cos x | − sin x |
| tan x | sec² x |
""")
    rule = st.radio("ສາທິດກົດ", ["ຜະລິດຕະພັນ (u·v)", "ຜົນຫານ (u/v)", "ລູກໂສ້ (f(g(x)))"], horizontal=True)
    if rule.startswith("ຜະລິດ"):
        cu, cv = st.columns(2)
        try:
            u = parse_math(cu.text_input("u(x) =", "x^2", key="ru"))
            v = parse_math(cv.text_input("v(x) =", "sin(x)", key="rv"))
        except ValueError as e:
            st.error(str(e)); st.stop()
        st.latex(r"(uv)' = u'v + uv'")
        st.latex(rf"= ({sp.latex(sp.diff(u, X))})({sp.latex(v)}) + ({sp.latex(u)})({sp.latex(sp.diff(v, X))})")
        st.latex(rf"= {sp.latex(sp.simplify(sp.diff(u * v, X)))}")
    elif rule.startswith("ຜົນຫານ"):
        cu, cv = st.columns(2)
        try:
            u = parse_math(cu.text_input("u(x) =", "x^2 + 1", key="qu"))
            v = parse_math(cv.text_input("v(x) =", "x - 1", key="qv"))
        except ValueError as e:
            st.error(str(e)); st.stop()
        st.latex(r"\left(\frac{u}{v}\right)' = \frac{u'v - uv'}{v^2}")
        st.latex(rf"= \frac{{({sp.latex(sp.diff(u, X))})({sp.latex(v)}) - ({sp.latex(u)})({sp.latex(sp.diff(v, X))})}}{{({sp.latex(v)})^2}}")
        st.latex(rf"= {sp.latex(sp.simplify(sp.diff(u / v, X)))}")
    else:
        co, ci = st.columns(2)
        try:
            outer = parse_math(co.text_input("ຟັງຊັນນອກ f(u) =", "u^5", key="co"), symbols=("u",))
            inner = parse_math(ci.text_input("ຟັງຊັນໃນ u = g(x) =", "3x^2 + 1", key="ci"))
        except ValueError as e:
            st.error(str(e)); st.stop()
        U = sp.Symbol("u", real=True)
        st.latex(r"\frac{d}{dx} f(g(x)) = f'(g(x)) \cdot g'(x)")
        st.latex(rf"f'(u) = {sp.latex(sp.diff(outer, U))},\qquad g'(x) = {sp.latex(sp.diff(inner, X))}")
        st.latex(rf"= \left({sp.latex(sp.diff(outer, U).subs(U, inner))}\right)\cdot\left({sp.latex(sp.diff(inner, X))}\right)")
        st.latex(rf"= {sp.latex(sp.simplify(sp.diff(outer.subs(U, inner), X)))}")

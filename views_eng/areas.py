import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.title("🔷 ພື້ນທີ່ & ເສັ້ນຮອບຮູບຂອງຮູບຮາບພຽງ")


def poly(pts):
    return [p[0] for p in pts], [p[1] for p in pts]


def rect(v):
    l, w = v
    return l * w, 2 * (l + w), r"A = l \times w", rf"A = {l:g} \times {w:g}", poly([(0, 0), (l, 0), (l, w), (0, w), (0, 0)])


def square(v):
    a, = v
    return a * a, 4 * a, r"A = a^2", rf"A = {a:g}^2", poly([(0, 0), (a, 0), (a, a), (0, a), (0, 0)])


def tri_bh(v):
    b, h = v
    return b * h / 2, None, r"A = \frac{1}{2} b h", rf"A = \frac{{1}}{{2}} \times {b:g} \times {h:g}", poly([(0, 0), (b, 0), (b / 2, h), (0, 0)])


def tri_heron(v):
    a, b, c = v
    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError("ສາມດ້ານນີ້ບໍ່ປະກອບເປັນສາມຫຼ່ຽມ (ຜົນບວກສອງດ້ານຕ້ອງຫຼາຍກວ່າດ້ານທີສາມ)")
    s = (a + b + c) / 2
    A = math.sqrt(s * (s - a) * (s - b) * (s - c))
    x = (a * a + c * c - b * b) / (2 * c)
    y = math.sqrt(max(a * a - x * x, 0))
    return A, a + b + c, r"A = \sqrt{s(s-a)(s-b)(s-c)},\ s = \frac{a+b+c}{2}", rf"s = {s:g},\ A = \sqrt{{{s:g}({s - a:g})({s - b:g})({s - c:g})}}", poly([(0, 0), (c, 0), (x, y), (0, 0)])


def para(v):
    b, h, s = v
    if s < h:
        raise ValueError("ດ້ານຂ້າງ (s) ຕ້ອງບໍ່ສັ້ນກວ່າຄວາມສູງ (h)")
    dx = math.sqrt(s * s - h * h)
    return b * h, 2 * (b + s), r"A = b \times h", rf"A = {b:g} \times {h:g}", poly([(0, 0), (b, 0), (b + dx, h), (dx, h), (0, 0)])


def trap(v):
    a, b, h = v
    return (a + b) * h / 2, None, r"A = \frac{1}{2}(a+b)h", rf"A = \frac{{1}}{{2}}({a:g}+{b:g})\times{h:g}", poly([(0, 0), (a, 0), (a / 2 + b / 2, h), (a / 2 - b / 2, h), (0, 0)])


def rhombus(v):
    d1, d2 = v
    side = math.hypot(d1 / 2, d2 / 2)
    return d1 * d2 / 2, 4 * side, r"A = \frac{1}{2} d_1 d_2", rf"A = \frac{{1}}{{2}} \times {d1:g} \times {d2:g}", poly([(d1 / 2, 0), (d1, d2 / 2), (d1 / 2, d2), (0, d2 / 2), (d1 / 2, 0)])


def circle(v):
    r, = v
    t = np.linspace(0, 2 * math.pi, 120)
    return math.pi * r * r, 2 * math.pi * r, r"A = \pi r^2,\quad C = 2\pi r", rf"A = \pi \times {r:g}^2", (list(r * np.cos(t)), list(r * np.sin(t)))


def sector(v):
    r, th = v
    t = np.linspace(0, math.radians(th), 100)
    xs = [0] + list(r * np.cos(t)) + [0]
    ys = [0] + list(r * np.sin(t)) + [0]
    arc = r * math.radians(th)
    return th / 360 * math.pi * r * r, arc + 2 * r, r"A = \frac{\theta}{360^\circ}\pi r^2,\quad \ell = r\theta", rf"A = \frac{{{th:g}}}{{360}} \times \pi \times {r:g}^2", (xs, ys)


SHAPES = {
    "ສີ່ຫຼ່ຽມມຸມສາກ": (["ຍາວ l", "ກວ້າງ w"], [8.0, 5.0], rect),
    "ສີ່ຫຼ່ຽມຈັດຕຸລັດ": (["ດ້ານ a"], [6.0], square),
    "ສາມຫຼ່ຽມ (ຖານ & ສູງ)": (["ຖານ b", "ສູງ h"], [8.0, 5.0], tri_bh),
    "ສາມຫຼ່ຽມ (ຮູ້ 3 ດ້ານ, Heron)": (["ດ້ານ a", "ດ້ານ b", "ດ້ານ c"], [7.0, 8.0, 9.0], tri_heron),
    "ສີ່ຫຼ່ຽມຂະໜານ": (["ຖານ b", "ສູງ h", "ດ້ານຂ້າງ s"], [9.0, 4.0, 5.0], para),
    "ສີ່ຫຼ່ຽມຄາງໝູ": (["ດ້ານຂະໜານ a", "ດ້ານຂະໜານ b", "ສູງ h"], [10.0, 6.0, 4.0], trap),
    "ສີ່ຫຼ່ຽມຂ້າວຫຼາມຕັດ (rhombus)": (["ເສັ້ນຂວາງ d₁", "ເສັ້ນຂວາງ d₂"], [8.0, 6.0], rhombus),
    "ວົງມົນ": (["ລັດສະໝີ r"], [5.0], circle),
    "ຮູບພັດ (sector)": (["ລັດສະໝີ r", "ມຸມ θ (ອົງສາ)"], [6.0, 75.0], sector),
}

name = st.selectbox("ເລືອກຮູບ", list(SHAPES))
labels, defaults, fn = SHAPES[name]
unit = st.text_input("ຫົວໜ່ວຍຄວາມຍາວ", "cm")
cols = st.columns(len(labels))
vals = [col.number_input(lb, min_value=0.01, value=df, key=f"{name}{i}") for i, (col, lb, df) in enumerate(zip(cols, labels, defaults))]
try:
    A, P, formula, step, (xs, ys) = fn(vals)
except ValueError as e:
    st.error(str(e)); st.stop()

st.latex(formula)
st.latex(step + rf" = {A:.6g}\ \text{{{unit}}}^2")
m1, m2 = st.columns(2)
m1.metric(f"ພື້ນທີ່ ({unit}²)", f"{A:.6g}")
m2.metric(f"ເສັ້ນຮອບຮູບ ({unit})", f"{P:.6g}" if P is not None else "ຕ້ອງຮູ້ດ້ານຂ້າງ")
fig = go.Figure(go.Scatter(x=xs, y=ys, fill="toself", mode="lines", line=dict(width=3)))
fig.update_yaxes(scaleanchor="x")
fig.update_layout(height=380, margin=dict(t=10), showlegend=False)
st.plotly_chart(fig, width="stretch")

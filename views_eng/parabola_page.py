import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from eng_utils import render_steps, render_summary
from mathcore import parabola
from mathcore.common import parse_fr

st.title("🌈 Parabola  y = ax² + bx + c")
c1, c2, c3 = st.columns(3)
try:
    a = parse_fr(c1.text_input("a", "1", key="pb_a"))
    b = parse_fr(c2.text_input("b", "-4", key="pb_b"))
    c = parse_fr(c3.text_input("c", "3", key="pb_c"))
    res = parabola.analyze(a, b, c)
except ValueError as e:
    st.error(str(e)); st.stop()

render_summary(res["summary"])

h, k, p, af = float(res["h"]), float(res["k"]), float(res["p"]), float(res["a"])
fx, fy = float(res["focus"][0]), float(res["focus"][1])
dy = float(res["directrix"])
roots = res["roots_f"]
half = max(4.0, 1.6 * max([abs(r - h) for r in roots], default=0.0) + 0.5)
x0 = st.slider("ເລື່ອນຈຸດ P ເທິງ parabola (ເບິ່ງ PF = Pd)", float(round(h - half, 1)), float(round(h + half, 1)),
               float(round(h + half / 2, 1)), 0.1)
y0 = af * (x0 - h) ** 2 + k
PF, Pd = math.hypot(x0 - fx, y0 - fy), abs(y0 - dy)

xs = np.linspace(h - half, h + half, 400)
ys = af * (xs - h) ** 2 + k
fig = go.Figure()
fig.add_scatter(x=xs, y=ys, mode="lines", line=dict(width=3), name="Parabola")
fig.add_scatter(x=[xs[0], xs[-1]], y=[dy, dy], mode="lines", line=dict(dash="dash", color="gray"), name="Directrix")
top, bot = float(max(ys.max(), fy, dy)), float(min(ys.min(), fy, dy))
fig.add_scatter(x=[h, h], y=[bot, top], mode="lines", line=dict(dash="dot", color="lightgray"), name="ແກນສົມມາດ")
fig.add_scatter(x=[h], y=[k], mode="markers+text", text=["V"], textposition="bottom center", marker=dict(size=11, color="red"), name="Vertex")
fig.add_scatter(x=[fx], y=[fy], mode="markers+text", text=["F"], textposition="top center", marker=dict(size=11, color="green"), name="Focus")
if roots:
    fig.add_scatter(x=roots, y=[0] * len(roots), mode="markers", marker=dict(size=10, color="orange"), name="ຮາກ")
fig.add_scatter(x=[0], y=[float(res["c"])], mode="markers", marker=dict(size=9, color="purple", symbol="diamond"), name="ຕັດແກນ y")
fig.add_scatter(x=[x0, fx], y=[y0, fy], mode="lines+markers", line=dict(color="green"), name="PF")
fig.add_scatter(x=[x0, x0], y=[y0, dy], mode="lines+markers", line=dict(color="crimson"), name="Pd")
fig.update_layout(height=520, margin=dict(t=10))
st.plotly_chart(fig, width="stretch")
m1, m2 = st.columns(2)
m1.metric("PF (ໄລຍະຈາກ P ຫາ Focus)", f"{PF:.4f}")
m2.metric("Pd (ໄລຍະຈາກ P ຫາ Directrix)", f"{Pd:.4f}")
st.caption("ທຸກຈຸດເທິງ parabola ມີ PF = Pd ສະເໝີ")

with st.expander("ເບິ່ງຂັ້ນຕອນທັງໝົດ", expanded=False):
    render_steps(res["steps"])

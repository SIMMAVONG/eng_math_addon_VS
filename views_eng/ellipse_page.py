import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from eng_utils import render_steps, render_summary
from mathcore import ellipse
from mathcore.common import parse_fr

st.title("🥚 Ellipse  (x−h)²/a² + (y−k)²/b² = 1")
c = st.columns(4)
try:
    a = parse_fr(c[0].text_input("a (ແກນເຄິ່ງແນວ x)", "5", key="el_a"))
    b = parse_fr(c[1].text_input("b (ແກນເຄິ່ງແນວ y)", "3", key="el_b"))
    h = parse_fr(c[2].text_input("h (ສູນກາງ x)", "0", key="el_h"))
    k = parse_fr(c[3].text_input("k (ສູນກາງ y)", "0", key="el_k"))
    res = ellipse.analyze(a, b, h, k)
except ValueError as e:
    st.error(str(e)); st.stop()

render_summary(res["summary"])

hf, kf, af, bf = float(h), float(k), float(a), float(b)
(f1x, f1y), (f2x, f2y) = res["foci_f"]
th = st.slider("ເລື່ອນຈຸດ P ອ້ອມຮູບໄຂ່ (ມຸມ, ອົງສາ)", 0, 360, 40, 5)
px, py = hf + af * math.cos(math.radians(th)), kf + bf * math.sin(math.radians(th))
d1, d2 = math.hypot(px - f1x, py - f1y), math.hypot(px - f2x, py - f2y)

t = np.linspace(0, 2 * math.pi, 400)
fig = go.Figure()
fig.add_scatter(x=hf + af * np.cos(t), y=kf + bf * np.sin(t), mode="lines", line=dict(width=3), name="Ellipse")
fig.add_scatter(x=[hf], y=[kf], mode="markers+text", text=["C"], textposition="bottom center", marker=dict(size=9, color="black"), name="ສູນກາງ")
fig.add_scatter(x=[f1x, f2x], y=[f1y, f2y], mode="markers+text", text=["F₁", "F₂"], textposition="top center", marker=dict(size=11, color="green"), name="Foci")
fig.add_scatter(x=[v[0] for v in res["vertices_f"]], y=[v[1] for v in res["vertices_f"]], mode="markers", marker=dict(size=9, color="red"), name="ຈຸດຍອດ (ແກນໃຫຍ່)")
fig.add_scatter(x=[v[0] for v in res["cov_f"]], y=[v[1] for v in res["cov_f"]], mode="markers", marker=dict(size=9, color="orange"), name="ປາຍແກນນ້ອຍ")
fig.add_scatter(x=[f1x, px, f2x], y=[f1y, py, f2y], mode="lines+markers", line=dict(color="crimson"), name="PF₁ + PF₂")
fig.update_yaxes(scaleanchor="x")
fig.update_layout(height=520, margin=dict(t=10))
st.plotly_chart(fig, width="stretch")
m1, m2, m3 = st.columns(3)
m1.metric("PF₁", f"{d1:.4f}")
m2.metric("PF₂", f"{d2:.4f}")
m3.metric("PF₁ + PF₂", f"{d1 + d2:.4f}", delta=f"2a = {2 * float(res['major']):g}", delta_color="off")

st.markdown("##### ກວດຕຳແໜ່ງຈຸດ")
q1, q2 = st.columns(2)
try:
    qx = parse_fr(q1.text_input("x₀", "3", key="el_qx"))
    qy = parse_fr(q2.text_input("y₀", "2", key="el_qy"))
    loc = ellipse.locate_point(res, qx, qy)
    label = {"on": "ຢູ່ເທິງຮູບໄຂ່ ✅", "inside": "ຢູ່ພາຍໃນຮູບໄຂ່", "outside": "ຢູ່ພາຍນອກຮູບໄຂ່"}[loc["status"]]
    st.info(f"ຈຸດ ({qx}, {qy}): ຄ່າ {float(loc['value']):.4f} → {label}  (ເທິງ = 1, ໃນ < 1, ນອກ > 1)")
except ValueError as e:
    st.error(str(e))

with st.expander("ເບິ່ງຂັ້ນຕອນທັງໝົດ", expanded=False):
    render_steps(res["steps"])

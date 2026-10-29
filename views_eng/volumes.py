import math

import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.title("📦 ປະລິມານ & ພື້ນທີ່ຜິວຂອງຮູບທົງ 3 ມິຕິ")
COLOR = "#4C78A8"


def mesh(verts, faces):
    """faces ເປັນລາຍການ ຂອງ ຈຸດຍອດ 3 ຫຼື 4 ຈຸດ (ສີ່ຈຸດຖືກແບ່ງເປັນສາມຫຼ່ຽມ)"""
    i, j, k = [], [], []
    for f in faces:
        tris = [(f[0], f[1], f[2])] + ([(f[0], f[2], f[3])] if len(f) == 4 else [])
        for a, b, c in tris:
            i.append(a); j.append(b); k.append(c)
    v = np.array(verts, dtype=float)
    return [go.Mesh3d(x=v[:, 0], y=v[:, 1], z=v[:, 2], i=i, j=j, k=k, color=COLOR, opacity=0.7, flatshading=True)]


def surf(X, Y, Z):
    return go.Surface(x=X, y=Y, z=Z, colorscale=[[0, COLOR], [1, COLOR]], showscale=False, opacity=0.8)


def cuboid(v):
    l, w, h = v
    V = l * w * h
    SA = 2 * (l * w + l * h + w * h)
    verts = [(0, 0, 0), (l, 0, 0), (l, w, 0), (0, w, 0), (0, 0, h), (l, 0, h), (l, w, h), (0, w, h)]
    faces = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return dict(V=V, SA=SA, vf=r"V = lwh", sf=r"S = 2(lw + lh + wh)", vs=rf"V = {l:g}\times{w:g}\times{h:g}",
                ss=rf"S = 2({l * w:g} + {l * h:g} + {w * h:g})", extra=None, traces=mesh(verts, faces))


def cylinder(v):
    r, h = v
    th, z = np.meshgrid(np.linspace(0, 2 * math.pi, 50), np.linspace(0, h, 2))
    return dict(V=math.pi * r * r * h, SA=2 * math.pi * r * (r + h), vf=r"V = \pi r^2 h", sf=r"S = 2\pi r(r+h)",
                vs=rf"V = \pi\times{r:g}^2\times{h:g}", ss=rf"S = 2\pi\times{r:g}({r:g}+{h:g})",
                extra=("ຜິວໂຄ້ງ 2πrh", 2 * math.pi * r * h), traces=[surf(r * np.cos(th), r * np.sin(th), z)])


def cone(v):
    r, h = v
    l = math.hypot(r, h)
    th, t = np.meshgrid(np.linspace(0, 2 * math.pi, 50), np.linspace(0, 1, 2))
    return dict(V=math.pi * r * r * h / 3, SA=math.pi * r * (r + l), vf=r"V = \frac{1}{3}\pi r^2 h", sf=r"S = \pi r(r+l),\ l=\sqrt{r^2+h^2}",
                vs=rf"V = \frac{{1}}{{3}}\pi\times{r:g}^2\times{h:g}", ss=rf"l = {l:.4g},\ S = \pi\times{r:g}({r:g}+{l:.4g})",
                extra=("ຜິວໂຄ້ງ πrl", math.pi * r * l), traces=[surf(r * (1 - t) * np.cos(th), r * (1 - t) * np.sin(th), h * t)])


def sphere(v):
    r, = v
    th, ph = np.meshgrid(np.linspace(0, 2 * math.pi, 50), np.linspace(0, math.pi, 30))
    return dict(V=4 / 3 * math.pi * r**3, SA=4 * math.pi * r * r, vf=r"V = \frac{4}{3}\pi r^3", sf=r"S = 4\pi r^2",
                vs=rf"V = \frac{{4}}{{3}}\pi\times{r:g}^3", ss=rf"S = 4\pi\times{r:g}^2", extra=None,
                traces=[surf(r * np.sin(ph) * np.cos(th), r * np.sin(ph) * np.sin(th), r * np.cos(ph))])


def hemisphere(v):
    r, = v
    th, ph = np.meshgrid(np.linspace(0, 2 * math.pi, 50), np.linspace(0, math.pi / 2, 20))
    return dict(V=2 / 3 * math.pi * r**3, SA=3 * math.pi * r * r, vf=r"V = \frac{2}{3}\pi r^3", sf=r"S = 3\pi r^2\ (\text{ລວມຖານ})",
                vs=rf"V = \frac{{2}}{{3}}\pi\times{r:g}^3", ss=rf"S = 3\pi\times{r:g}^2", extra=("ຜິວໂຄ້ງ 2πr²", 2 * math.pi * r * r),
                traces=[surf(r * np.sin(ph) * np.cos(th), r * np.sin(ph) * np.sin(th), r * np.cos(ph))])


def pyramid(v):
    a, h = v
    l = math.hypot(h, a / 2)
    verts = [(0, 0, 0), (a, 0, 0), (a, a, 0), (0, a, 0), (a / 2, a / 2, h)]
    faces = [(0, 1, 2, 3), (0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)]
    return dict(V=a * a * h / 3, SA=a * a + 2 * a * l, vf=r"V = \frac{1}{3} a^2 h", sf=r"S = a^2 + 2al,\ l = \sqrt{h^2 + (a/2)^2}",
                vs=rf"V = \frac{{1}}{{3}}\times{a:g}^2\times{h:g}", ss=rf"l = {l:.4g},\ S = {a:g}^2 + 2\times{a:g}\times{l:.4g}",
                extra=None, traces=mesh(verts, faces))


def tri_prism(v):
    p, q, L = v
    c = math.hypot(p, q)
    verts = [(0, 0, 0), (p, 0, 0), (0, q, 0), (0, 0, L), (p, 0, L), (0, q, L)]
    faces = [(0, 1, 2), (3, 4, 5), (0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)]
    return dict(V=p * q / 2 * L, SA=p * q + (p + q + c) * L, vf=r"V = (\text{ພື້ນທີ່ຖານ}) \times L = \frac{1}{2}pqL",
                sf=r"S = pq + (p+q+c)L,\ c=\sqrt{p^2+q^2}", vs=rf"V = \frac{{1}}{{2}}\times{p:g}\times{q:g}\times{L:g}",
                ss=rf"c = {c:.4g},\ S = {p * q:g} + ({p:g}+{q:g}+{c:.4g})\times{L:g}", extra=None, traces=mesh(verts, faces))


SOLIDS = {
    "ກ່ອງສີ່ຫຼ່ຽມ (cuboid)": (["ຍາວ l", "ກວ້າງ w", "ສູງ h"], [6.0, 4.0, 3.0], cuboid),
    "ກະບອກ (cylinder)": (["ລັດສະໝີ r", "ສູງ h"], [3.0, 7.0], cylinder),
    "ກວຍ (cone)": (["ລັດສະໝີ r", "ສູງ h"], [3.0, 6.0], cone),
    "ທົງກົມ (sphere)": (["ລັດສະໝີ r"], [4.0], sphere),
    "ເຄິ່ງທົງກົມ (hemisphere)": (["ລັດສະໝີ r"], [4.0], hemisphere),
    "ປິຣາມິດຖານສີ່ຫຼ່ຽມຈັດຕຸລັດ": (["ດ້ານຖານ a", "ສູງ h"], [6.0, 8.0], pyramid),
    "ແທ່ງປິຣຶສຖານສາມຫຼ່ຽມມຸມສາກ": (["ຂາ p", "ຂາ q", "ຍາວ L"], [3.0, 4.0, 8.0], tri_prism),
}

name = st.selectbox("ເລືອກຮູບທົງ", list(SOLIDS))
labels, defaults, fn = SOLIDS[name]
unit = st.text_input("ຫົວໜ່ວຍຄວາມຍາວ", "cm")
cols = st.columns(len(labels))
vals = [col.number_input(lb, min_value=0.01, value=df, key=f"v{name}{i}") for i, (col, lb, df) in enumerate(zip(cols, labels, defaults))]
r = fn(vals)

a, b = st.columns(2)
with a:
    st.latex(r["vf"]); st.latex(r["vs"] + rf" = {r['V']:.6g}\ \text{{{unit}}}^3")
with b:
    st.latex(r["sf"]); st.latex(r["ss"] + rf" = {r['SA']:.6g}\ \text{{{unit}}}^2")
m1, m2, m3 = st.columns(3)
m1.metric(f"ປະລິມານ ({unit}³)", f"{r['V']:.6g}")
m2.metric(f"ພື້ນທີ່ຜິວທັງໝົດ ({unit}²)", f"{r['SA']:.6g}")
if r["extra"]:
    m3.metric(f"{r['extra'][0]} ({unit}²)", f"{r['extra'][1]:.6g}")
fig = go.Figure(r["traces"])
fig.update_layout(scene=dict(aspectmode="data", xaxis_visible=False, yaxis_visible=False, zaxis_visible=False),
                  height=480, margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig, width="stretch")
st.caption("ໃຊ້ເມົ້າໝຸນຮູບເບິ່ງໄດ້")

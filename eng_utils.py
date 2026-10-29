"""ຟັງຊັນຊ່ວຍສຳລັບໜ້າຄະນິດສາດວິສະວະກຳ"""
import re

import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication_application,
                                        parse_expr, standard_transformations)

X = sp.Symbol("x", real=True)
_FUNCS = {"sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "sec": sp.sec, "csc": sp.csc, "cot": sp.cot,
          "exp": sp.exp, "ln": sp.log, "log": sp.log, "sqrt": sp.sqrt, "asin": sp.asin,
          "acos": sp.acos, "atan": sp.atan, "abs": sp.Abs, "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh}
_CONST = {"pi": sp.pi, "e": sp.E}
_TRANS = standard_transformations + (implicit_multiplication_application, convert_xor)


def parse_math(text, symbols=("x",)):
    """ອ່ານສົມຜົນຈາກຂໍ້ຄວາມຢ່າງປອດໄພ (ອະນຸຍາດສະເພາະຕົວແປ ແລະ ຟັງຊັນທີ່ກຳນົດ)"""
    t = (text or "").strip()
    if not t:
        raise ValueError("ຍັງບໍ່ໄດ້ປ້ອນສົມຜົນ")
    if len(t) > 120:
        raise ValueError("ສົມຜົນຍາວເກີນໄປ")
    if not re.fullmatch(r"[0-9A-Za-z_+\-*/^().,\s]*", t):
        raise ValueError("ມີຕົວອັກສອນທີ່ບໍ່ຮອງຮັບ (ໃຊ້ໄດ້: ຕົວເລກ, x, + − * / ^ ( ) ແລະ ຟັງຊັນ sin cos tan exp ln sqrt)")
    local = {**_FUNCS, **_CONST}
    for s in symbols:
        local[s] = X if s == "x" else sp.Symbol(s, real=True)
    for name in re.findall(r"[A-Za-z_]+", t):
        if name not in local:
            raise ValueError(f"ບໍ່ຮູ້ຈັກ '{name}' — ຖ້າເປັນຟັງຊັນໃຫ້ໃສ່ວົງເລັບ ເຊັ່ນ sin(x), ແລະ ໃຊ້ * ລະຫວ່າງຕົວແປ")
    try:
        return parse_expr(t, local_dict=local, transformations=_TRANS)
    except Exception:
        raise ValueError("ອ່ານສົມຜົນບໍ່ໄດ້ — ກວດວົງເລັບ ແລະ ເຄື່ອງໝາຍ")


def to_func(expr, var=X):
    """ແປງ sympy → ຟັງຊັນ numpy (ຄ່າທີ່ບໍ່ມີຄວາມໝາຍ → nan)"""
    f = sp.lambdify(var, expr, "numpy")

    def g(x):
        x = np.asarray(x, dtype=float)
        with np.errstate(all="ignore"):
            y = np.asarray(f(x.astype(complex)), dtype=complex)
        y = np.broadcast_to(y, x.shape)
        out = np.where(np.abs(y.imag) < 1e-9, y.real, np.nan)
        return np.where(np.isfinite(out), out, np.nan)
    return g


def fmt(x, nd=6):
    """ຈັດຮູບຕົວເລກໃຫ້ອ່ານງ່າຍ"""
    if isinstance(x, (int,)) or (isinstance(x, float) and x == int(x) and abs(x) < 1e12):
        return str(int(x))
    return f"{x:.{nd}g}"


# ------------------------------------------------------------------ UI ຊ່ວຍ (ໃຊ້ກັບ mathcore)
def render_steps(steps):
    """ສະແດງຂັ້ນຕອນຈາກ mathcore: [{'title','text'?,'latex'?[...]}]"""
    import streamlit as st
    for i, s in enumerate(steps, 1):
        st.markdown(f"**ຂັ້ນຕອນທີ {i}: {s['title']}**")
        if s.get("text"):
            st.markdown(s["text"])
        for line in s.get("latex", []):
            st.latex(line)


def render_summary(rows):
    """ຕາຕະລາງສະຫຼຸບ [(ຫົວຂໍ້, ຄ່າ, is_latex)]"""
    import streamlit as st
    with st.container(border=True):
        for label, val, is_tex in rows:
            c1, c2 = st.columns([2, 3])
            c1.markdown(f"**{label}**")
            if is_tex:
                c2.latex(val)
            else:
                c2.write(val)


def matrix_input(name, rows, cols, key, default=None):
    """ຊ່ອງປ້ອນ matrix ເປັນ Fraction (ປ້ອນ 3, -2, 0.75 ຫຼື 3/5 ໄດ້). ຖ້າຜິດຮູບແບບ → ValueError"""
    import streamlit as st
    from mathcore.common import parse_fr
    default = default or (lambda i, j: "0")
    data, bad = [], None
    for i in range(rows):
        cs = st.columns(cols)
        row = []
        for j in range(cols):
            t = cs[j].text_input(f"{name}{i + 1}{j + 1}", value=default(i, j), key=f"{key}_{i}_{j}",
                                 label_visibility="collapsed", placeholder=f"{name}{i + 1}{j + 1}")
            try:
                row.append(parse_fr(t))
            except ValueError as e:
                bad = bad or f"ຊ່ອງ {name}{i + 1}{j + 1}: {e}"
                row.append(0)
        data.append(row)
    if bad:
        raise ValueError(bad)
    return data

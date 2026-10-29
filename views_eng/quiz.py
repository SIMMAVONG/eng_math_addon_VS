import math
import random
from fractions import Fraction

import sympy as sp
import streamlit as st

from eng_utils import X, parse_math
from mathcore.common import mat_tex, poly_tex
from mathcore.determinant import det as det_fn
from mathcore.ellipse import analyze as ellipse_analyze
from mathcore.parabola import analyze as parabola_analyze

st.title("📝 ແບບຝຶກຫັດ")
st.caption("ເລືອກຫົວຂໍ້ ແລ້ວຕອບ. ຕົວເລກຕອບໄດ້ເປັນທົດສະນິຍົມ ຫຼື ເສດສ່ວນ (ເຊັ່ນ 7/12). ຄຳຕອບທົດສະນິຍົມຍອມຮັບຄວາມຄາດເຄື່ອນນ້ອຍໆ.")


def frac_tex(f: Fraction) -> str:
    return str(f.numerator) if f.denominator == 1 else rf"\frac{{{f.numerator}}}{{{f.denominator}}}"


# ---- ຕົວສ້າງຄຳຖາມ: ຄືນ dict(text, kind, answer, why) ----
def g_frac(r):
    a, b, c, d = r.randint(1, 7), r.randint(2, 9), r.randint(1, 7), r.randint(2, 9)
    op = r.choice(["+", "-"])
    ans = Fraction(a, b) + Fraction(c, d) if op == "+" else Fraction(a, b) - Fraction(c, d)
    return dict(text=rf"ຄິດ $\frac{{{a}}}{{{b}}} {op} \frac{{{c}}}{{{d}}}$ (ຕອບເປັນເສດສ່ວນຫຍໍ້ ຫຼື ທົດສະນິຍົມ)",
                kind="frac", answer=ans, why=rf"ໃຊ້ຕົວຫານຮ່ວມ {math.lcm(b, d)} → ${frac_tex(ans)}$")


def g_percent(r):
    p, n = r.choice([5, 10, 12, 15, 20, 25, 30, 35, 40]), r.choice([80, 120, 150, 240, 360, 500])
    return dict(text=rf"${p}\%$ ຂອງ ${n}$ ເປັນເທົ່າໃດ?", kind="num", answer=p / 100 * n,
                why=rf"${p}/100 \times {n} = {p / 100 * n:g}$")


def g_index(r):
    a = r.choice([2, 3, 5])
    m, n = r.randint(2, 6), r.randint(2, 5)
    p = r.randint(1, m + n + 1)
    ans = Fraction(a) ** (m + n - p)
    return dict(text=rf"ຄິດຄ່າ ${a}^{{{m}}} \times {a}^{{{n}}} \div {a}^{{{p}}}$", kind="frac", answer=ans,
                why=rf"ບວກກຳລັງ ລົບກຳລັງ: ${a}^{{{m}+{n}-{p}}} = {a}^{{{m + n - p}}} = {frac_tex(ans)}$")


def g_binary(r):
    n = r.randint(5, 120)
    return dict(text=rf"ແປງເລກຖານສິບ ${n}$ ເປັນເລກຖານສອງ (ພິມສະເພາະ 0 ແລະ 1)", kind="text", answer=format(n, "b"),
                why=f"ຫານ 2 ຊ້ຳໆ ແລ້ວອ່ານເສດຈາກລຸ່ມຂຶ້ນເທິງ → {format(n, 'b')}")


def g_hex(r):
    n = r.randint(30, 255)
    return dict(text=rf"ແປງເລກຖານສິບ ${n}$ ເປັນເລກຖານສິບຫົກ (Hex, ໃຊ້ A–F)", kind="text", answer=format(n, "X"),
                why=f"ຫານ 16 ຊ້ຳໆ ແລ້ວອ່ານເສດຈາກລຸ່ມຂຶ້ນເທິງ → {format(n, 'X')}")


def g_log(r):
    b = r.choice([2, 3, 5, 10])
    i, j = r.randint(1, 3), r.randint(1, 3)
    if r.random() < 0.5:
        return dict(text=rf"ຄິດ $\log_{{{b}}} {b ** (i + j)}$", kind="num", answer=i + j,
                    why=rf"${b}^{{{i + j}}} = {b ** (i + j)}$ ດັ່ງນັ້ນ log = {i + j}")
    return dict(text=rf"ຄິດ $\log_{{{b}}} {b ** i} + \log_{{{b}}} {b ** j}$", kind="num", answer=i + j,
                why=rf"$\log_{{{b}}}({b ** i}\times{b ** j}) = \log_{{{b}}}{b ** (i + j)} = {i + j}$")


def g_ap(r):
    a, d, n = r.randint(2, 10), r.randint(2, 7), r.randint(8, 20)
    if r.random() < 0.5:
        return dict(text=rf"ລຳດັບເລກຄະນິດ: $a={a},\ d={d}$ ຫາ $T_{{{n}}}$", kind="num", answer=a + (n - 1) * d,
                    why=rf"$T_n = a + (n-1)d = {a} + {n - 1}\times{d} = {a + (n - 1) * d}$")
    s = n * (2 * a + (n - 1) * d) // 2
    return dict(text=rf"ລຳດັບເລກຄະນິດ: $a={a},\ d={d}$ ຫາຜົນບວກ $S_{{{n}}}$", kind="num", answer=s,
                why=rf"$S_n = \frac{{n}}{{2}}[2a + (n-1)d] = {s}$")


def g_gp(r):
    a, rr, n = r.randint(1, 5), r.choice([2, 3]), r.randint(4, 7)
    s = a * (rr ** n - 1) // (rr - 1)
    return dict(text=rf"ລຳດັບເລຂາຄະນິດ: $a={a},\ r={rr}$ ຫາຜົນບວກ $S_{{{n}}}$", kind="num", answer=s,
                why=rf"$S_n = \frac{{a(r^n-1)}}{{r-1}} = \frac{{{a}({rr}^{{{n}}}-1)}}{{{rr - 1}}} = {s}$")


def g_comb(r):
    n, k = r.randint(5, 10), r.randint(2, 4)
    if r.random() < 0.5:
        return dict(text=rf"ຄິດ ${{}}^{{{n}}}C_{{{k}}}$", kind="num", answer=math.comb(n, k),
                    why=rf"$\frac{{{n}!}}{{{k}!({n}-{k})!}} = {math.comb(n, k)}$")
    return dict(text=rf"ຄິດ ${{}}^{{{n}}}P_{{{k}}}$", kind="num", answer=math.perm(n, k),
                why=rf"$\frac{{{n}!}}{{({n}-{k})!}} = {math.perm(n, k)}$")


def g_area(r):
    t = r.choice(["circle", "tri", "trap"])
    if t == "circle":
        rad = r.randint(3, 12)
        return dict(text=rf"ພື້ນທີ່ວົງມົນລັດສະໝີ ${rad}$ cm (ໃຊ້ π ຈາກເຄື່ອງຄິດເລກ, ຕອບທົດສະນິຍົມ 2 ຕຳແໜ່ງ)", kind="num",
                    answer=math.pi * rad ** 2, why=rf"$\pi r^2 = \pi\times{rad}^2 = {math.pi * rad ** 2:.2f}$")
    if t == "tri":
        b, h = r.randint(4, 15), r.randint(3, 12)
        return dict(text=rf"ພື້ນທີ່ສາມຫຼ່ຽມ ຖານ ${b}$ cm ສູງ ${h}$ cm", kind="num", answer=b * h / 2,
                    why=rf"$\frac{{1}}{{2}}bh = \frac{{1}}{{2}}\times{b}\times{h} = {b * h / 2:g}$")
    a, b, h = r.randint(4, 12), r.randint(2, 9), r.randint(3, 10)
    return dict(text=rf"ພື້ນທີ່ສີ່ຫຼ່ຽມຄາງໝູ ດ້ານຂະໜານ ${a}$ ແລະ ${b}$ cm ສູງ ${h}$ cm", kind="num", answer=(a + b) * h / 2,
                why=rf"$\frac{{1}}{{2}}(a+b)h = \frac{{1}}{{2}}({a}+{b})\times{h} = {(a + b) * h / 2:g}$")


def g_volume(r):
    t = r.choice(["cyl", "cone", "sph"])
    if t == "cyl":
        rad, h = r.randint(2, 8), r.randint(3, 12)
        return dict(text=rf"ປະລິມານກະບອກ ລັດສະໝີ ${rad}$ cm ສູງ ${h}$ cm (ຕອບທົດສະນິຍົມ 2 ຕຳແໜ່ງ)", kind="num",
                    answer=math.pi * rad ** 2 * h, why=rf"$\pi r^2 h = {math.pi * rad ** 2 * h:.2f}$")
    if t == "cone":
        rad, h = r.randint(2, 8), r.randint(3, 12)
        return dict(text=rf"ປະລິມານກວຍ ລັດສະໝີ ${rad}$ cm ສູງ ${h}$ cm (ຕອບທົດສະນິຍົມ 2 ຕຳແໜ່ງ)", kind="num",
                    answer=math.pi * rad ** 2 * h / 3, why=rf"$\frac{{1}}{{3}}\pi r^2 h = {math.pi * rad ** 2 * h / 3:.2f}$")
    rad = r.randint(2, 9)
    return dict(text=rf"ປະລິມານທົງກົມ ລັດສະໝີ ${rad}$ cm (ຕອບທົດສະນິຍົມ 2 ຕຳແໜ່ງ)", kind="num",
                answer=4 / 3 * math.pi * rad ** 3, why=rf"$\frac{{4}}{{3}}\pi r^3 = {4 / 3 * math.pi * rad ** 3:.2f}$")


def g_trig(r):
    c, ang = r.randint(5, 20), r.choice([20, 25, 30, 35, 40, 45, 50, 55, 60, 65])
    if r.random() < 0.5:
        return dict(text=rf"ສາມຫຼ່ຽມມຸມສາກ: hypotenuse $c={c}$, ມຸມ $A={ang}^\circ$. ຫາ $a$ (ຂ້າງກົງຂ້າມ A) ທົດສະນິຍົມ 2 ຕຳແໜ່ງ",
                    kind="num", answer=c * math.sin(math.radians(ang)), why=rf"$a = c\sin A = {c}\sin {ang}^\circ = {c * math.sin(math.radians(ang)):.2f}$")
    return dict(text=rf"ສາມຫຼ່ຽມມຸມສາກ: hypotenuse $c={c}$, ມຸມ $A={ang}^\circ$. ຫາ $b$ (ຂ້າງຕິດ A) ທົດສະນິຍົມ 2 ຕຳແໜ່ງ",
                kind="num", answer=c * math.cos(math.radians(ang)), why=rf"$b = c\cos A = {c}\cos {ang}^\circ = {c * math.cos(math.radians(ang)):.2f}$")


def g_line(r):
    while True:
        x1, y1, x2, y2 = (r.randint(-5, 5) for _ in range(4))
        if x1 != x2:
            break
    m = Fraction(y2 - y1, x2 - x1)
    return dict(text=rf"ຫາຄວາມຊັນຂອງເສັ້ນຊື່ຜ່ານຈຸດ $({x1},{y1})$ ແລະ $({x2},{y2})$", kind="frac", answer=m,
                why=rf"$m = \frac{{{y2}-({y1})}}{{{x2}-({x1})}} = {frac_tex(m)}$")


def g_simul(r):
    while True:
        x, y = r.randint(-4, 6), r.randint(-4, 6)
        a1, b1, a2, b2 = (r.choice([1, 2, 3, 4, -1, -2]) for _ in range(4))
        if a1 * b2 - a2 * b1 != 0:
            break
    c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
    return dict(text=rf"ແກ້ລະບົບ ${a1}x + ({b1})y = {c1}$ ແລະ ${a2}x + ({b2})y = {c2}$. ຫາຄ່າ $x + y$", kind="num", answer=x + y,
                why=rf"ຄຳຕອບ $x={x},\ y={y}$ ດັ່ງນັ້ນ $x+y={x + y}$")


def g_diff(r):
    a, b, c, d = r.randint(1, 5), r.randint(-6, 6), r.randint(-8, 8), r.randint(-9, 9)
    f = a * X**3 + b * X**2 + c * X + d
    if r.random() < 0.6:
        return dict(text=rf"ຫາ $\frac{{d}}{{dx}}\left({sp.latex(f)}\right)$ (ພິມເຊັ່ນ 3x^2 - 4x + 1)", kind="expr", answer=sp.diff(f, X),
                    why=rf"ກົດຍົກກຳລັງ → ${sp.latex(sp.diff(f, X))}$")
    k = r.randint(2, 5)
    g = sp.sin(k * X) * X
    return dict(text=rf"ຫາ $\frac{{d}}{{dx}}\left({sp.latex(g)}\right)$ (ໃຊ້ sin(), cos(), x)", kind="expr", answer=sp.diff(g, X),
                why=rf"ກົດຜະລິດຕະພັນ → ${sp.latex(sp.diff(g, X))}$")


def g_int(r):
    a, b, c = r.choice([3, 6, 9]), r.choice([2, 4, 6]), r.randint(1, 9)
    f = a * X**2 + b * X + c
    return dict(text=rf"ຫາ $\int \left({sp.latex(f)}\right) dx$ (ບໍ່ຕ້ອງໃສ່ + C; ພິມ ເຊັ່ນ x^3 + 2x^2 + 5x)", kind="antideriv", answer=f,
                why=rf"${sp.latex(sp.integrate(f, X))} + C$")


def g_det(r):
    n = r.choice([2, 3])
    lo, hi = (-5, 9) if n == 2 else (-3, 5)
    M = [[r.randint(lo, hi) for _ in range(n)] for _ in range(n)]
    val = det_fn(M)
    if n == 2:
        why = rf"$ad - bc = ({M[0][0]})({M[1][1]}) - ({M[0][1]})({M[1][0]}) = {val}$"
    else:
        why = rf"ກະຈາຍຕາມແຖວທີ 1 (cofactor) → $\det A = {val}$"
    return dict(text=rf"ຫາ Determinant ${mat_tex(M, 'v')}$", kind="num", answer=val, why=why)


def g_matmul(r):
    A = [[r.randint(0, 5) for _ in range(2)] for _ in range(2)]
    B = [[r.randint(0, 5) for _ in range(2)] for _ in range(2)]
    i, j = r.randint(0, 1), r.randint(0, 1)
    val = A[i][0] * B[0][j] + A[i][1] * B[1][j]
    return dict(text=rf"$A = {mat_tex(A)},\ B = {mat_tex(B)}$ ຫາຕຳແໜ່ງ $c_{{{i + 1}{j + 1}}}$ ຂອງ $AB$",
                kind="num", answer=val,
                why=rf"$c_{{{i + 1}{j + 1}}} = {A[i][0]}\cdot{B[0][j]} + {A[i][1]}\cdot{B[1][j]} = {val}$")


def g_parabola(r):
    a = r.choice([1, 2, 3, -1, -2])
    h, k = r.randint(-4, 4), r.randint(-6, 6)
    b, c = -2 * a * h, a * h * h + k
    res = parabola_analyze(a, b, c)
    pol = poly_tex(a, b, c)
    ask = r.choice(["h", "k", "D"])
    if ask == "h":
        return dict(text=rf"Parabola $y = {pol}$ ຫາຄ່າ $x$ ຂອງຈຸດຍອດ (Vertex)", kind="num", answer=float(res["h"]),
                    why=rf"$h = -\frac{{b}}{{2a}} = -\frac{{{b}}}{{2({a})}} = {h}$")
    if ask == "k":
        return dict(text=rf"Parabola $y = {pol}$ ຫາຄ່າ $y$ ຂອງຈຸດຍອດ (Vertex)", kind="num", answer=float(res["k"]),
                    why=rf"ແທນ $x = {h}$ ໃນສົມຜົນ → $k = {k}$")
    return dict(text=rf"Parabola $y = {pol}$ ຫາຕົວຈຳແນກ $D = b^2 - 4ac$", kind="num", answer=float(res["D"]),
                why=rf"$D = ({b})^2 - 4({a})({c}) = {float(res['D']):g}$")


def g_ellipse(r):
    A, B = r.choice([(5, 4), (5, 3), (10, 6), (10, 8), (13, 12), (13, 5), (17, 15), (17, 8)])
    if r.random() < 0.5:
        A, B = B, A
    res = ellipse_analyze(A, B)
    major, c = int(res["major"]), int(round(res["c_f"]))
    eq = rf"\frac{{x^2}}{{{A * A}}} + \frac{{y^2}}{{{B * B}}} = 1"
    if r.random() < 0.5:
        return dict(text=rf"ຮູບໄຂ່ ${eq}$ ຫາໄລຍະ $c$ ຈາກສູນກາງຫາໂຟກັສ", kind="num", answer=c,
                    why=rf"$c^2 = {major}^2 - {int(res['minor'])}^2 = {c * c}$ → $c = {c}$")
    return dict(text=rf"ຮູບໄຂ່ ${eq}$ ຫາຄວາມເບີ້ຍ $e = c / a_{{\max}}$ (ຕອບເປັນເສດສ່ວນ ຫຼື ທົດສະນິຍົມ)", kind="frac",
                answer=Fraction(c, major), why=rf"$e = \frac{{{c}}}{{{major}}}$")


GENS = {
    "ເສດສ່ວນ": g_frac, "ເປີເຊັນ": g_percent, "ເລກຍົກກຳລັງ": g_index, "ເລກຖານສອງ": g_binary, "ເລກຖານສິບຫົກ": g_hex,
    "ລອກາລິດ": g_log, "ລຳດັບ AP": g_ap, "ລຳດັບ GP": g_gp, "ວິທີລຽງ/ເລືອກ": g_comb, "ພື້ນທີ່": g_area,
    "ປະລິມານ": g_volume, "ຕຣີໂກນ": g_trig, "ເສັ້ນຊື່": g_line, "ສົມຜົນພ້ອມກັນ": g_simul,
    "ການອະນຸພັນ": g_diff, "ການອິນທີເກຣດ": g_int,
    "Determinant": g_det, "Matrix": g_matmul, "Parabola": g_parabola, "Ellipse": g_ellipse,
}


def check(q, user):
    """True / False ຫຼື None (ຮູບແບບຄຳຕອບບໍ່ຖືກ)"""
    u = (user or "").strip()
    if not u:
        return None
    try:
        if q["kind"] == "num":
            v = float(Fraction(u))
            return math.isclose(v, q["answer"], rel_tol=0.005, abs_tol=0.011)
        if q["kind"] == "frac":
            return Fraction(u) == q["answer"]
        if q["kind"] == "text":
            return u.upper().replace(" ", "") == q["answer"].upper()
        e = parse_math(u)
        diff = sp.diff(e, X) if q["kind"] == "antideriv" else e
        return sp.simplify(diff - q["answer"]) == 0
    except Exception:
        return None


def correct_text(q):
    k = q["kind"]
    if k in ("expr", "antideriv"):
        return sp.sstr(q["answer"]) + (" + C" if k == "antideriv" else "")
    if k == "num":
        return str(round(q["answer"], 4))
    return str(q["answer"])


S = st.session_state
S.setdefault("qz_correct", 0)
S.setdefault("qz_total", 0)
S.setdefault("q10", None)
S.setdefault("q10_result", None)
S.setdefault("q10_id", 0)

topics = st.multiselect("ເລືອກຫົວຂໍ້", list(GENS), default=list(GENS))
if not topics:
    st.info("ເລືອກຢ່າງໜ້ອຍ 1 ຫົວຂໍ້"); st.stop()
mode = st.radio("ໂໝດ", ["ຝຶກຫັດທີລະຂໍ້", "Quiz 10 ຂໍ້"], horizontal=True)
st.divider()

if mode == "ຝຶກຫັດທີລະຂໍ້":
    def new_question():
        S.qz_seed = random.randrange(10**9)
        S.qz_topic = random.choice(topics)
        S.qz_done = False
        S.qz_ok = None

    if "qz_seed" not in S or S.qz_topic not in topics:
        new_question()

    q = GENS[S.qz_topic](random.Random(S.qz_seed))
    st.markdown(f"**ຫົວຂໍ້: {S.qz_topic}**")
    st.markdown(q["text"])
    ans = st.text_input("ຄຳຕອບ", key=f"qz_ans_{S.qz_seed}", disabled=S.qz_done)
    b1, b2, b3 = st.columns([1, 1, 3])
    if b1.button("ກວດຄຳຕອບ", type="primary", disabled=S.qz_done):
        res = check(q, ans)
        if res is None:
            st.warning("ຮູບແບບຄຳຕອບບໍ່ຖືກ ຫຼື ຍັງບໍ່ໄດ້ພິມ — ລອງໃໝ່")
        else:
            S.qz_done, S.qz_ok = True, res
            S.qz_total += 1
            S.qz_correct += int(res)
            st.rerun()
    if b2.button("ຂ້າມ / ຄຳຖາມໃໝ່"):
        new_question()
        st.rerun()
    if S.qz_done:
        (st.success if S.qz_ok else st.error)("ຖືກຕ້ອງ ✅" if S.qz_ok else "ຍັງບໍ່ຖືກ ❌")
        st.markdown("**ວິທີຄິດ:** " + q["why"])
        if not S.qz_ok:
            st.caption("ຄຳຕອບທີ່ຖືກ: " + correct_text(q))
    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("ຖືກ", S.qz_correct)
    m2.metric("ທັງໝົດ", S.qz_total)
    m3.metric("ເປີເຊັນ", f"{S.qz_correct / S.qz_total * 100:.0f} %" if S.qz_total else "—")
    if st.button("ລ້າງຄະແນນ"):
        S.qz_correct = S.qz_total = 0
        st.rerun()

else:
    def new_quiz():
        S.q10 = [(random.choice(topics), random.randrange(10**9)) for _ in range(10)]
        S.q10_id = random.randrange(10**9)
        S.q10_result = None

    if S.q10 is None:
        st.write("ຄຳຖາມ 10 ຂໍ້ ສຸ່ມຈາກຫົວຂໍ້ທີ່ເລືອກ. ຕອບໃຫ້ຄົບ ແລ້ວກົດ **ສົ່ງຄຳຕອບ** ເພື່ອເບິ່ງຄະແນນ ແລະ ເຉລີຍ.")
        if st.button("ເລີ່ມ Quiz", type="primary"):
            new_quiz()
            st.rerun()
        st.stop()

    if S.q10_result is None:
        with st.form(f"q10form_{S.q10_id}"):
            answers = []
            for i, (t, seed) in enumerate(S.q10):
                qq = GENS[t](random.Random(seed))
                st.markdown(f"**ຂໍ້ {i + 1}.** · {t}")
                st.markdown(qq["text"])
                answers.append(st.text_input("ຄຳຕອບ", key=f"q10_{S.q10_id}_{i}", label_visibility="collapsed"))
            submitted = st.form_submit_button("ສົ່ງຄຳຕອບ", type="primary")
        if submitted:
            S.q10_result = [(a, check(GENS[t](random.Random(seed)), a) is True) for (t, seed), a in zip(S.q10, answers)]
            st.rerun()
        if st.button("ເລີ່ມ Quiz ໃໝ່"):
            new_quiz()
            st.rerun()
    else:
        score = sum(ok for _, ok in S.q10_result)
        c1, c2 = st.columns(2)
        c1.metric("ຄະແນນ", f"{score} / 10")
        c2.metric("ເປີເຊັນ", f"{score * 10} %")
        if score >= 9: st.success("ດີເລີດ! 🎉")
        elif score >= 7: st.success("ດີ — ເກືອບຄົບແລ້ວ")
        elif score >= 5: st.info("ພໍໃຊ້ — ທົບທວນເພີ່ມອີກໜ້ອຍ")
        else: st.warning("ຄວນທົບທວນເນື້ອຫາ ແລ້ວລອງໃໝ່")
        weak = sorted({t for (t, _), (_, ok) in zip(S.q10, S.q10_result) if not ok})
        if weak:
            st.write("ຫົວຂໍ້ທີ່ຄວນທົບທວນ: " + ", ".join(weak))
        st.markdown("##### ເຉລີຍ ແລະ ວິທີຄິດ")
        for i, ((t, seed), (a, ok)) in enumerate(zip(S.q10, S.q10_result)):
            qq = GENS[t](random.Random(seed))
            with st.expander(f"ຂໍ້ {i + 1}  {'✅' if ok else '❌'}  · {t}"):
                st.markdown(qq["text"])
                st.write(f"ຄຳຕອບຂອງເຈົ້າ: **{a if a.strip() else '(ບໍ່ໄດ້ຕອບ)'}**")
                st.write("ຄຳຕອບທີ່ຖືກ: **" + correct_text(qq) + "**")
                st.markdown("ວິທີຄິດ: " + qq["why"])
        if st.button("Quiz ໃໝ່", type="primary"):
            new_quiz()
            st.rerun()

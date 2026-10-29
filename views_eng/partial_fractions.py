import sympy as sp
import streamlit as st

from eng_utils import X, parse_math

st.title("🧩 ເສດສ່ວນຍ່ອຍ (Partial Fractions)")
st.caption("ແຍກ  N(x) / [(ປັດໄຈ 1)(ປັດໄຈ 2)…]  ເປັນຜົນບວກຂອງເສດສ່ວນທີ່ງ່າຍກວ່າ. ປັດໄຈຕ້ອງເປັນເສັ້ນຊື່ (ax + b).")

c1, c2 = st.columns(2)
num_txt = c1.text_input("ຕົວຕັ້ງ N(x)", "3x + 5")
fac_txt = c2.text_input("ປັດໄຈຂອງຕົວຫານ (ຄັ່ນດ້ວຍ ,)", "x - 1, x + 2")
try:
    N = sp.nsimplify(parse_math(num_txt))
    factors = [sp.nsimplify(parse_math(t)) for t in fac_txt.split(",") if t.strip()]
except ValueError as e:
    st.error(str(e)); st.stop()
if not factors:
    st.error("ໃສ່ປັດໄຈຂອງຕົວຫານຢ່າງໜ້ອຍ 1 ຕົວ"); st.stop()
for f in factors:
    if not f.is_polynomial(X) or sp.degree(f, X) != 1:
        st.error(f"ປັດໄຈ '{f}' ບໍ່ແມ່ນເສັ້ນຊື່ (ຕ້ອງເປັນຮູບ ax + b)"); st.stop()
if not N.is_polynomial(X):
    st.error("ຕົວຕັ້ງຕ້ອງເປັນພະຫຸນາມຂອງ x"); st.stop()


def P(e):
    """latex ພ້ອມວົງເລັບ"""
    return r"\left(" + sp.latex(e) + r"\right)"


D = sp.expand(sp.Mul(*factors))
orig = N / D
roots = [sp.solve(f, X)[0] for f in factors]
den_latex = "".join(P(f) for f in factors)
st.latex(rf"\frac{{{sp.latex(N)}}}{{{den_latex}}}")

q, r = sp.Integer(0), N
if sp.degree(N, X) >= len(factors):
    q, r = sp.div(N, D, X)
    st.info("ເປັນເສດສ່ວນບໍ່ແທ້ (ກຳລັງຕົວຕັ້ງ ≥ ກຳລັງຕົວຫານ) → ຫານພະຫຸນາມກ່ອນ")
    st.latex(rf"\text{{ຜົນຫານ}} = {sp.latex(q)},\qquad \text{{ເສດ}} = {sp.latex(r)}")

if len(set(roots)) == len(roots):
    letters = "ABCDEFGH"
    st.latex(" + ".join(rf"\frac{{{letters[i]}}}{{{sp.latex(f)}}}" for i, f in enumerate(factors)))
    st.write("**ວິທີປິດ (cover-up):** ແທນ x = ຮາກຂອງແຕ່ລະປັດໄຈ ໃນສ່ວນທີ່ເຫຼືອ")
    coefs = []
    for i, (f, rt) in enumerate(zip(factors, roots)):
        others = [g for j, g in enumerate(factors) if j != i]
        vals = [g.subs(X, rt) for g in others]
        den = sp.Mul(*vals)
        A = sp.nsimplify(r.subs(X, rt) / den)
        coefs.append(A)
        den_txt = r" \cdot ".join(P(v) for v in vals) if vals else "1"
        st.latex(rf"{letters[i]} = \frac{{N({sp.latex(rt)})}}{{{den_txt}}} = {sp.latex(A)}")
    def term(A, f):
        if A.is_Rational and A.q != 1:
            sign = "-" if A < 0 else ""
            return rf"{sign}\frac{{{abs(A.p)}}}{{{A.q}{P(f)}}}"
        return rf"\frac{{{sp.latex(A)}}}{{{sp.latex(f)}}}"
    terms = ([sp.latex(q)] if q != 0 else []) + [term(A, f) for A, f in zip(coefs, factors)]
    result = q + sum(A / f for A, f in zip(coefs, factors))
    final_latex = " + ".join(terms).replace("+ -", "- ")
else:
    st.warning("ມີປັດໄຈຊ້ຳກັນ → ຮູບແບບ A/(x−a) + B/(x−a)² + … (ແອັບໃຊ້ sympy ແຍກໃຫ້ໂດຍກົງ)")
    result = sp.apart(orig, X)
    final_latex = sp.latex(result)

st.success("ຜົນລັບ:")
st.latex(final_latex)
ok = sp.simplify(result - orig) == 0
st.write("ກວດຄືນ (ລວມເສດສ່ວນກັບຄືນ): " + ("✅ ຕົງກັບຕົ້ນສະບັບ" if ok else "❌ ບໍ່ຕົງ — ກວດຂໍ້ມູນ"))

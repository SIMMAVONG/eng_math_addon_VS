import streamlit as st

from eng_utils import matrix_input, render_steps
from mathcore import matrix
from mathcore.common import mat_tex, parse_fr

st.title("🧮 Matrix")
st.caption("ປ້ອນຄ່າເປັນຕົວເລກເຕັມ, ທົດສະນິຍົມ ຫຼື ເສດສ່ວນ (ເຊັ່ນ 3, -2, 0.75, 3/5) — ຄຳຕອບຄິດແບບແນ່ນອນ (ເສດສ່ວນ)")

OPS = ["A + B", "A − B", "k · A (ຄູນຄ່າຄົງທີ່)", "Aᵀ (Transpose)", "A × B", "A⁻¹ (Inverse)"]
op = st.selectbox("ການດຳເນີນການ", OPS, index=4)
needs_b = op in ("A + B", "A − B", "A × B")
same_size = op in ("A + B", "A − B")

st.markdown("##### Matrix A")
c1, c2 = st.columns(2)
ra = int(c1.number_input("ຈຳນວນແຖວ A", 1, 4, 2, key="mx_ra"))
ca = int(c2.number_input("ຈຳນວນຖັນ A", 1, 4, 2, key="mx_ca"))
try:
    A = matrix_input("A", ra, ca, "mxA", lambda i, j: str(i * ca + j + 1 + (2 if i == j else 0)))
    B = None
    if needs_b:
        st.markdown("##### Matrix B")
        if same_size:
            rb, cb = ra, ca
            st.caption("ບວກ/ລົບ: B ມີຂະໜາດເທົ່າ A")
        else:
            d1, d2 = st.columns(2)
            rb = int(d1.number_input("ຈຳນວນແຖວ B", 1, 4, ca, key="mx_rb"))
            cb = int(d2.number_input("ຈຳນວນຖັນ B", 1, 4, 2, key="mx_cb"))
        B = matrix_input("B", rb, cb, f"mxB{rb}x{cb}", lambda i, j: str((i + j) % 4 + 1))
    k = parse_fr(st.text_input("ຄ່າ k", "2", key="mx_k")) if op.startswith("k") else None
except ValueError as e:
    st.error(str(e)); st.stop()

try:
    if op == "A + B": out = matrix.add(A, B, 1)
    elif op == "A − B": out = matrix.add(A, B, -1)
    elif op.startswith("k"): out = matrix.scalar(k, A)
    elif op.startswith("Aᵀ"): out = matrix.transpose(A)
    elif op == "A × B": out = matrix.multiply(A, B)
    else: out = matrix.inverse(A)
except ValueError as e:
    st.error(str(e)); st.stop()

st.divider()
if out["result"] is None:
    st.warning("ບໍ່ມີ Inverse (det = 0, Singular matrix)")
else:
    st.success("ຜົນລັບ")
    st.latex(mat_tex(out["result"]))
with st.expander("ເບິ່ງຂັ້ນຕອນ", expanded=True):
    render_steps(out["steps"])

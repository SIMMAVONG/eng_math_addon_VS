import streamlit as st

st.title("💻 ລະບົບເລກ (Binary · Octal · Decimal · Hex)")
DIGITS = "0123456789ABCDEF"
BASES = {"ເລກຖານສອງ (Binary, 2)": 2, "ເລກຖານແປດ (Octal, 8)": 8, "ເລກຖານສິບ (Decimal, 10)": 10,
         "ເລກຖານສິບຫົກ (Hex, 16)": 16}


def to_base(n: int, b: int) -> str:
    if n == 0:
        return "0"
    sign, n = ("-" if n < 0 else ""), abs(n)
    out = []
    while n:
        n, r = divmod(n, b)
        out.append(DIGITS[r])
    return sign + "".join(reversed(out))


def parse(text: str, b: int) -> int:
    t = text.strip().upper().replace(" ", "")
    if not t:
        raise ValueError("ຍັງບໍ່ໄດ້ປ້ອນຕົວເລກ")
    neg = t.startswith("-")
    t = t.lstrip("-")
    if any(ch not in DIGITS[:b] for ch in t):
        raise ValueError(f"ເລກຖານ {b} ໃຊ້ໄດ້ສະເພາະ: {', '.join(DIGITS[:b])}")
    return -int(t, b) if neg else int(t, b)


tab1, tab2, tab3 = st.tabs(["ແປງລະບົບເລກ", "ບວກ ລົບ ຄູນ", "ຈັດກຸ່ມ Binary ↔ Octal/Hex"])

with tab1:
    c1, c2 = st.columns(2)
    src_name = c1.selectbox("ເລກທີ່ປ້ອນເປັນຖານ", list(BASES), index=2)
    src = BASES[src_name]
    text = c2.text_input("ຕົວເລກ", "156")
    try:
        val = parse(text, src)
    except ValueError as e:
        st.error(str(e)); st.stop()
    cols = st.columns(4)
    for col, (nm, b) in zip(cols, BASES.items()):
        col.metric(nm.split("(")[1].rstrip(")"), to_base(val, b))

    st.markdown("##### ຂັ້ນຕອນ")
    tgt_name = st.selectbox("ແປງໄປເປັນຖານ", list(BASES), index=0)
    tgt = BASES[tgt_name]
    if src != 10:
        digs = text.strip().upper().lstrip("-")
        L = len(digs)
        terms = " + ".join(f"{d}×{src}^{{{L - 1 - i}}}" for i, d in enumerate(digs))
        vals = " + ".join(str(DIGITS.index(d) * src ** (L - 1 - i)) for i, d in enumerate(digs))
        st.write(f"ແປງເປັນຖານສິບ (ຄູນຄ່າຫຼັກດ້ວຍ {src} ຍົກກຳລັງຕາມຕຳແໜ່ງ):")
        st.latex(rf"({digs})_{{{src}}} = {terms} = {vals} = {abs(val)}")
    if tgt != 10 and val != 0:
        n = abs(val)
        rows, q = [], n
        while q:
            rows.append({"ຫານ": f"{q} ÷ {tgt}", "ຜົນຫານ": q // tgt, "ເສດ": DIGITS[q % tgt]})
            q //= tgt
        st.write(f"ຫານດ້ວຍ {tgt} ຊ້ຳໆ ຈົນຜົນຫານເປັນ 0 ແລ້ວອ່ານເສດ **ຈາກລຸ່ມຂຶ້ນເທິງ**:")
        st.dataframe(rows, hide_index=True)
        st.success(f"({abs(val)})₁₀ = ({to_base(abs(val), tgt)})_{tgt}" + ("  (ຕິດລົບ)" if val < 0 else ""))

with tab2:
    c1, c2, c3, c4 = st.columns([2, 2, 1, 2])
    nm = c1.selectbox("ຖານ", list(BASES), index=0, key="arith_b")
    b = BASES[nm]
    x = c2.text_input("ເລກ 1", "1011", key="ax")
    op = c3.selectbox("ເຄື່ອງໝາຍ", ["+", "−", "×"])
    y = c4.text_input("ເລກ 2", "110", key="ay")
    try:
        xv, yv = parse(x, b), parse(y, b)
    except ValueError as e:
        st.error(str(e)); st.stop()
    r = {"+": xv + yv, "−": xv - yv, "×": xv * yv}[op]
    op_tex = {"+": "+", "−": "-", "×": r"\times"}[op]
    st.latex(rf"({x})_{{{b}}} {op_tex} ({y})_{{{b}}} = ({to_base(r, b)})_{{{b}}}")
    st.write(f"ກວດດ້ວຍຖານສິບ: {xv} {op} {yv} = {r}")
    cols = st.columns(4)
    for col, (nm2, bb) in zip(cols, BASES.items()):
        col.metric(nm2.split("(")[1].rstrip(")"), to_base(r, bb))

with tab3:
    bt = st.text_input("ເລກຖານສອງ", "110101110", key="grp")
    t = bt.strip().replace(" ", "")
    if not t or any(ch not in "01" for ch in t):
        st.error("ໃສ່ສະເພາະ 0 ແລະ 1"); st.stop()

    def group(s, k):
        s = s.zfill(-(-len(s) // k) * k)
        return [s[i:i + k] for i in range(0, len(s), k)]
    g3, g4 = group(t, 3), group(t, 4)
    st.write("**→ Octal** (ຈັດກຸ່ມ 3 ບິດຈາກຂວາ):")
    st.latex(r"\ ".join(g3) + " \\Rightarrow " + r"\ ".join(str(int(g, 2)) for g in g3))
    st.write("**→ Hex** (ຈັດກຸ່ມ 4 ບິດຈາກຂວາ):")
    st.latex(r"\ ".join(g4) + " \\Rightarrow " + r"\ ".join(DIGITS[int(g, 2)] for g in g4))
    st.caption("ເຕີມ 0 ທາງຊ້າຍໃຫ້ຄົບກຸ່ມ. ກົງກັນຂ້າມ: ແປງແຕ່ລະຫຼັກ Octal/Hex ເປັນ 3/4 ບິດ ແລ້ວຕໍ່ກັນ.")

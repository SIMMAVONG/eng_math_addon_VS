"""Determinant ແລະ Cramer's Rule"""
from .common import tex, tex_p, mat_tex, lin_tex


def minor(M, i, j):
    return [[M[r][c] for c in range(len(M)) if c != j] for r in range(len(M)) if r != i]


def det(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0] * M[1][1] - M[0][1] * M[1][0]
    return sum(((-1) ** j) * M[0][j] * det(minor(M, 0, j)) for j in range(n))


def det2(M):
    (a, b), (c, d) = M
    val = a * d - b * c
    steps = [
        {"title": "ສູດ Determinant 2×2",
         "latex": [r"\begin{vmatrix} a & b \\ c & d \end{vmatrix} = ad - bc"]},
        {"title": "ແທນຄ່າ",
         "latex": [rf"{mat_tex(M, 'v')} = {tex_p(a)}{tex_p(d)} - {tex_p(b)}{tex_p(c)}"
                   rf" = {tex(a * d)} - {tex_p(b * c)} = {tex(val)}"]},
    ]
    return {"value": val, "steps": steps}


def det3(M):
    (a, b, c), (d, e, f), (g, h, i) = M
    val = det(M)
    minors = [det(minor(M, 0, j)) for j in range(3)]
    steps = [
        {"title": "ກະຈາຍຕາມແຖວທີ 1 (Cofactor expansion)",
         "latex": [r"\det A = a_{11}M_{11} - a_{12}M_{12} + a_{13}M_{13}"]},
        {"title": "ຫາ Minor ແຕ່ລະຕົວ (ຕັດແຖວ ແລະ ຖັນຂອງຕົວນັ້ນອອກ)",
         "latex": [rf"M_{{1{j + 1}}} = {mat_tex(minor(M, 0, j), 'v')} = {tex(minors[j])}" for j in range(3)]},
        {"title": "ແທນຄ່າ",
         "text": "ເຄື່ອງໝາຍ + − + ສະຫຼັບກັນຕາມຕຳແໜ່ງ",
         "latex": [rf"\det A = {tex_p(a)}({tex(minors[0])}) - {tex_p(b)}({tex(minors[1])})"
                   rf" + {tex_p(c)}({tex(minors[2])}) = {tex(val)}"]},
    ]
    pos = a * e * i + b * f * g + c * d * h
    neg = c * e * g + a * f * h + b * d * i
    steps.append({"title": "ກວດດ້ວຍວິທີ Sarrus",
                  "text": "ຜົນບວກຂອງເສັ້ນຂວາງລົງ ລົບ ຜົນບວກຂອງເສັ້ນຂວາງຂຶ້ນ",
                  "latex": [r"(aei + bfg + cdh) - (ceg + afh + bdi)",
                            rf"= {tex(pos)} - {tex_p(neg)} = {tex(pos - neg)}"]})
    return {"value": val, "steps": steps}


def cramer(A, b):
    n = len(A)
    names = ["x", "y", "z"][:n]
    D = det(A)
    eqs = r" \\ ".join(f"{lin_tex(A[r], names)} = {tex(b[r])}" for r in range(n))
    steps = [
        {"title": "ຂຽນລະບົບສົມຜົນ", "latex": [rf"\begin{{cases}} {eqs} \end{{cases}}"]},
        {"title": "ຄິດໄລ່ D = det A (Determinant ຂອງສຳປະສິດ)",
         "latex": [rf"D = {mat_tex(A, 'v')} = {tex(D)}"]},
    ]
    if D == 0:
        steps.append({"title": "ສະຫຼຸບ",
                      "text": "D = 0 → ລະບົບ **ບໍ່ມີຄຳຕອບດຽວ** (ອາດບໍ່ມີຄຳຕອບ ຫຼື ມີຄຳຕອບຫຼາຍບໍ່ສິ້ນສຸດ) ຈຶ່ງໃຊ້ Cramer's Rule ບໍ່ໄດ້"})
        return {"unique": False, "solution": None, "steps": steps}
    sol, lat = [], []
    for j, nm in enumerate(names):
        Aj = [[(b[r] if cidx == j else A[r][cidx]) for cidx in range(n)] for r in range(n)]
        Dj = det(Aj)
        sol.append(Dj / D)
        lat.append(rf"D_{nm} = {mat_tex(Aj, 'v')} = {tex(Dj)}")
    steps.append({"title": "ແທນຖັນຂອງແຕ່ລະຕົວແປດ້ວຍຄ່າຄົງທີ່ (ຖັນ b)", "latex": lat})
    steps.append({"title": "ຫາຄຳຕອບ",
                  "latex": [rf"{nm} = \dfrac{{D_{nm}}}{{D}} = {tex(s)}" for nm, s in zip(names, sol)]})
    ok = all(sum(A[r][c] * sol[c] for c in range(n)) == b[r] for r in range(n))
    steps.append({"title": "ກວດຄຳຕອບ", "text": "ແທນຄືນໃນທຸກສົມຜົນ: " + ("✅ ຖືກຕ້ອງ" if ok else "❌ ບໍ່ຖືກ")})
    return {"unique": True, "solution": sol, "steps": steps}

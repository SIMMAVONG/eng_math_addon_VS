"""ການດຳເນີນການ Matrix (ລາຍການເປັນ list ຂອງ list ຂອງ Fraction)"""
from fractions import Fraction
from .common import tex, tex_p, mat_tex
from .determinant import det, minor


def shape(M):
    return len(M), len(M[0])


def _same(A, B):
    if shape(A) != shape(B):
        ra, ca = shape(A)
        rb, cb = shape(B)
        raise ValueError(f"ບວກ/ລົບບໍ່ໄດ້: A ມີຂະໜາດ {ra}×{ca} ແຕ່ B ມີຂະໜາດ {rb}×{cb} — ຂະໜາດຕ້ອງເທົ່າກັນ")


def add(A, B, sign=1):
    _same(A, B)
    sym = "+" if sign == 1 else "-"
    R = [[x + sign * y for x, y in zip(ra, rb)] for ra, rb in zip(A, B)]
    expr = [[f"{tex(x)} {sym} {tex_p(y)}" for x, y in zip(ra, rb)] for ra, rb in zip(A, B)]
    steps = [
        {"title": "ດຳເນີນການທີລະຕຳແໜ່ງທີ່ກົງກັນ",
         "latex": [rf"A {sym} B = {mat_tex(A)} {sym} {mat_tex(B)}", rf"= {mat_tex(expr)}"]},
        {"title": "ຜົນລັບ", "latex": [rf"= {mat_tex(R)}"]},
    ]
    return {"result": R, "steps": steps}


def scalar(k, A):
    R = [[k * x for x in row] for row in A]
    expr = [[f"{tex_p(k)}\\cdot{tex_p(x)}" for x in row] for row in A]
    return {"result": R, "steps": [
        {"title": "ຄູນທຸກຕຳແໜ່ງດ້ວຍຄ່າ k",
         "latex": [rf"kA = {mat_tex(expr)}", rf"= {mat_tex(R)}"]}]}


def transpose(A):
    R = [list(col) for col in zip(*A)]
    return {"result": R, "steps": [
        {"title": "ສະຫຼັບແຖວເປັນຖັນ", "text": "ແຖວທີ i ຂອງ A ກາຍເປັນຖັນທີ i ຂອງ Aᵀ",
         "latex": [rf"A^T = {mat_tex(R)}"]}]}


def multiply(A, B):
    ra, ca = shape(A)
    rb, cb = shape(B)
    if ca != rb:
        raise ValueError(f"ຄູນບໍ່ໄດ້: ຈຳນວນຖັນຂອງ A ({ca}) ຕ້ອງເທົ່າກັບຈຳນວນແຖວຂອງ B ({rb}). "
                         f"A ແມ່ນ {ra}×{ca}, B ແມ່ນ {rb}×{cb}")
    R = [[sum(A[i][t] * B[t][j] for t in range(ca)) for j in range(cb)] for i in range(ra)]
    lines = []
    for i in range(ra):
        for j in range(cb):
            terms = " + ".join(f"{tex_p(A[i][t])}{tex_p(B[t][j])}" for t in range(ca))
            lines.append(rf"c_{{{i + 1}{j + 1}}} = {terms} = {tex(R[i][j])}")
    steps = [
        {"title": "ກວດຂະໜາດ", "text": f"A ແມ່ນ {ra}×{ca}, B ແມ່ນ {rb}×{cb} → ຜົນລັບ AB ມີຂະໜາດ **{ra}×{cb}**"},
        {"title": "ຄິດໄລ່ແຕ່ລະຕຳແໜ່ງ", "text": "c_ij = (ແຖວ i ຂອງ A) ຄູນ (ຖັນ j ຂອງ B) ແລ້ວບວກກັນ",
         "latex": lines},
        {"title": "ຜົນລັບ", "latex": [rf"AB = {mat_tex(R)}"]},
    ]
    return {"result": R, "steps": steps}


def identity(n):
    return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]


def inverse(A):
    r, c = shape(A)
    if r != c:
        raise ValueError("ຫາ Inverse ໄດ້ສະເພາະ Matrix ສີ່ຫຼ່ຽມຈັດຕຸລັດ (ແຖວ = ຖັນ)")
    D = det(A)
    steps = [{"title": "ຄິດໄລ່ Determinant", "text": "Matrix ມີ inverse ກໍຕໍ່ເມື່ອ det ≠ 0",
              "latex": [rf"\det A = {mat_tex(A, 'v')} = {tex(D)}"]}]
    if D == 0:
        steps.append({"title": "ສະຫຼຸບ", "text": "det = 0 → **ບໍ່ມີ Inverse** (Singular matrix)"})
        return {"result": None, "steps": steps}
    n = r
    C = [[(-1) ** (i + j) * det(minor(A, i, j)) if n > 1 else Fraction(1) for j in range(n)] for i in range(n)]
    adj = [list(col) for col in zip(*C)]
    inv = [[x / D for x in row] for row in adj]
    steps += [
        {"title": "ຫາ Cofactor matrix", "text": r"$C_{ij} = (-1)^{i+j} M_{ij}$",
         "latex": [rf"C = {mat_tex(C)}"]},
        {"title": "ຫາ Adjugate (transpose ຂອງ Cofactor)", "latex": [rf"\operatorname{{adj}}A = C^T = {mat_tex(adj)}"]},
        {"title": "ຫານດ້ວຍ det", "latex": [rf"A^{{-1}} = \dfrac{{1}}{{\det A}}\operatorname{{adj}}A = \dfrac{{1}}{{{tex_p(D)}}}{mat_tex(adj)}",
                                         rf"= {mat_tex(inv)}"]},
    ]
    check = multiply(A, inv)["result"]
    steps.append({"title": "ກວດຄຳຕອບ", "text": "A · A⁻¹ ຕ້ອງເທົ່າກັບ Identity matrix I",
                  "latex": [rf"A A^{{-1}} = {mat_tex(check)}"]})
    return {"result": inv, "steps": steps}

"""ການບວກ ລົບ ຄູນ ຫານ ແລະ ຄຸນສົມບັດຂອງຈຳນວນ"""
from fractions import Fraction
from math import gcd
from .common import to_fr, tex, tex_p

_SYM = {"+": "+", "-": "-", "×": r"\times", "÷": r"\div"}


def _frac_t(n, d):
    return str(n) if d == 1 else rf"\frac{{{n}}}{{{d}}}"


def operate(a, b, op):
    a, b = to_fr(a), to_fr(b)
    if op not in _SYM:
        raise ValueError("ເຄື່ອງໝາຍບໍ່ຖືກຕ້ອງ")
    if op == "÷" and b == 0:
        raise ValueError("ຫານດ້ວຍສູນບໍ່ໄດ້ (ຕົວຫານຕ້ອງບໍ່ເທົ່າ 0)")
    sym = _SYM[op]
    steps = [{"title": "ຂຽນໂຈດ", "latex": [rf"{tex(a)} {sym} {tex_p(b)}"]}]
    m, n, r, s = a.numerator, a.denominator, b.numerator, b.denominator

    if op in "+-":
        sg = 1 if op == "+" else -1
        if n == 1 and s == 1:
            N, Dn = m + sg * r, 1
            steps.append({"title": "ຄິດໄລ່ຈຳນວນເຕັມ", "latex": [rf"{m} {op} {tex_p(r)} = {N}"]})
        else:
            L = n * s // gcd(n, s)
            n1, n2 = m * (L // n), r * (L // s)
            N, Dn = n1 + sg * n2, L
            steps.append({"title": f"ຫາຕົວຫານຮ່ວມ (ຕົວຄູນຮ່ວມນ້ອຍສຸດ = {L})",
                          "text": "ປ່ຽນເສດສ່ວນໃຫ້ມີຕົວຫານເທົ່າກັນກ່ອນ ຈຶ່ງບວກ/ລົບຕົວເສດໄດ້",
                          "latex": [rf"{_frac_t(m, n)} {op} {tex_p(b)} = \frac{{{m}\cdot{L // n}}}{{{L}}} {op} \frac{{{r}\cdot{L // s}}}{{{L}}}",
                                    rf"= \frac{{{n1}}}{{{L}}} {op} \frac{{{tex_p(n2) if n2 < 0 else n2}}}{{{L}}}"]})
            steps.append({"title": "ບວກ/ລົບຕົວເສດ (ຕົວຫານຄືເກົ່າ)",
                          "latex": [rf"= \frac{{{N}}}{{{L}}}"]})
    elif op == "×":
        N, Dn = m * r, n * s
        steps.append({"title": "ຄູນຕົວເສດກັບຕົວເສດ, ຕົວຫານກັບຕົວຫານ",
                      "latex": [rf"\frac{{{m}\cdot({r})}}{{{n}\cdot{s}}} = {_frac_t(N, Dn)}"]})
    else:
        inv = 1 / b
        steps.append({"title": "ຫານ = ຄູນດ້ວຍສ່ວນກັບ (reciprocal)",
                      "latex": [rf"{tex(a)} \div {tex_p(b)} = {tex(a)} \times {tex_p(inv)}"]})
        N, Dn = m * inv.numerator, n * inv.denominator
        steps.append({"title": "ຄູນເສດສ່ວນ", "latex": [rf"= {_frac_t(N, Dn)}"]})
    if Dn < 0:
        N, Dn = -N, -Dn
    res = Fraction(N, Dn)
    g = gcd(abs(N), Dn) if N else Dn
    if Dn != 1 and g > 1:
        steps.append({"title": f"ຍ່ອໃຫ້ເປັນເສດສ່ວນຢ່າງຕ່ຳ (ຫານດ້ວຍ {g})",
                      "latex": [rf"{_frac_t(N, Dn)} = {tex(res)}"]})
    steps.append({"title": "ຄຳຕອບ", "latex": [rf"{tex(a)} {sym} {tex_p(b)} = {tex(res)}"]})
    return {"result": res, "steps": steps, "equation": rf"{tex(a)} {sym} {tex_p(b)} = {tex(res)}"}


def properties(a, b, c):
    a, b, c = to_fr(a), to_fr(b), to_fr(c)
    rows = [
        ("ສະຫຼັບທີ່ການບວກ (Commutative)", "a + b", "b + a", a + b, b + a),
        ("ສະຫຼັບທີ່ການຄູນ (Commutative)", "ab", "ba", a * b, b * a),
        ("ຈັດກຸ່ມການບວກ (Associative)", "(a + b) + c", "a + (b + c)", (a + b) + c, a + (b + c)),
        ("ຈັດກຸ່ມການຄູນ (Associative)", "(ab)c", "a(bc)", (a * b) * c, a * (b * c)),
        ("ກະຈາຍ (Distributive)", "a(b + c)", "ab + ac", a * (b + c), a * b + a * c),
    ]
    return [{"name": n, "lhs": l, "rhs": r, "lv": lv, "rv": rv, "ok": lv == rv} for n, l, r, lv, rv in rows]


def identities(a, b):
    a, b = to_fr(a), to_fr(b)
    rows = [
        ("(a + b)²", "a² + 2ab + b²", (a + b) ** 2, a * a + 2 * a * b + b * b),
        ("(a − b)²", "a² − 2ab + b²", (a - b) ** 2, a * a - 2 * a * b + b * b),
        ("(a + b)(a − b)", "a² − b²", (a + b) * (a - b), a * a - b * b),
    ]
    return [{"lhs": l, "rhs": r, "lv": lv, "rv": rv, "ok": lv == rv} for l, r, lv, rv in rows]

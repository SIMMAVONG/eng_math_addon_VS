"""Ellipse  (x-h)^2/a^2 + (y-k)^2/b^2 = 1"""
import math
from .common import to_fr, tex, sqrt_fr, dec


def _sh(var, v):
    v = to_fr(v)
    return var if v == 0 else rf"\left({var} {'-' if v > 0 else '+'} {tex(abs(v))}\right)"


def analyze(a, b, h=0, k=0):
    a, b, h, k = to_fr(a), to_fr(b), to_fr(h), to_fr(k)
    if a <= 0 or b <= 0:
        raise ValueError("a ແລະ b ຕ້ອງເປັນຈຳນວນບວກ")
    horizontal = a >= b
    major, minor = (a, b) if horizontal else (b, a)
    c2 = major * major - minor * minor
    c_exact = sqrt_fr(c2)
    c_f = math.sqrt(float(c2))
    e_f = c_f / float(major)
    circle = a == b

    def shown(x0, sign):
        if c_exact is not None:
            return tex(x0 + sign * c_exact)
        return dec(float(x0) + sign * c_f)

    c_tex = tex(c_exact) if c_exact is not None else rf"\sqrt{{{tex(c2)}}} \approx {dec(c_f)}"
    hf, kf, af, bf = float(h), float(k), float(a), float(b)
    if horizontal:
        foci_f = [(hf - c_f, kf), (hf + c_f, kf)]
        vertices_f = [(hf - af, kf), (hf + af, kf)]
        cov_f = [(hf, kf - bf), (hf, kf + bf)]
        foci_t = [(shown(h, -1), tex(k)), (shown(h, 1), tex(k))]
    else:
        foci_f = [(hf, kf - c_f), (hf, kf + c_f)]
        vertices_f = [(hf, kf - bf), (hf, kf + bf)]
        cov_f = [(hf - af, kf), (hf + af, kf)]
        foci_t = [(tex(h), shown(k, -1)), (tex(h), shown(k, 1))]

    eq = rf"\dfrac{{{_sh('x', h)}^2}}{{{tex(a * a)}}} + \dfrac{{{_sh('y', k)}^2}}{{{tex(b * b)}}} = 1"
    if circle:
        orient = "ເປັນ **ວົງມົນ** (a = b) — ບໍ່ມີແກນໃຫຍ່ພິເສດ, c = 0"
    elif horizontal:
        orient = "ຕົວຫານທີ່ໃຫຍ່ກວ່າ ຢູ່ກັບ **x** → ແກນໃຫຍ່ຢູ່ແນວນອນ (ຂະໜານແກນ x)"
    else:
        orient = "ຕົວຫານທີ່ໃຫຍ່ກວ່າ ຢູ່ກັບ **y** → ແກນໃຫຍ່ຢູ່ແນວຕັ້ງ (ຂະໜານແກນ y)"
    steps = [
        {"title": "ອ່ານຄ່າຈາກສົມຜົນມາດຕະຖານ",
         "latex": [eq,
                   rf"a^2 = {tex(a * a)},\ b^2 = {tex(b * b)}\ \Rightarrow\ a = {tex(a)},\ b = {tex(b)}",
                   rf"C({tex(h)},\ {tex(k)})"]},
        {"title": "ກຳນົດທິດຂອງແກນໃຫຍ່", "text": orient,
         "latex": [rf"a_{{\max}} = {tex(major)},\qquad b_{{\min}} = {tex(minor)}"]},
        {"title": "ຫາໄລຍະ c ຈາກສູນກາງຫາໂຟກັສ",
         "latex": [r"c^2 = a_{\max}^2 - b_{\min}^2",
                   rf"c^2 = {tex(major * major)} - {tex(minor * minor)} = {tex(c2)}",
                   rf"c = {c_tex}"]},
        {"title": "ຈຸດໂຟກັສ (Foci)",
         "latex": [rf"F_1({foci_t[0][0]},\ {foci_t[0][1]}),\qquad F_2({foci_t[1][0]},\ {foci_t[1][1]})"]},
        {"title": "ຄວາມເບີ້ຍ (Eccentricity)",
         "text": "ຄ່າ e ຢູ່ລະຫວ່າງ 0 ຫາ 1 — ຍິ່ງໃກ້ 0 ຍິ່ງກົມ, ຍິ່ງໃກ້ 1 ຍິ່ງແປ້",
         "latex": [rf"e = \dfrac{{c}}{{a_{{\max}}}} = {dec(e_f)}"]},
        {"title": "ຄຸນສົມບັດສຳຄັນ",
         "text": "ຜົນບວກຂອງໄລຍະຈາກຈຸດໃດໆເທິງຮູບໄຂ່ ໄປຫາໂຟກັສທັງສອງ ເປັນຄ່າຄົງທີ່",
         "latex": [rf"PF_1 + PF_2 = 2a_{{\max}} = {tex(2 * major)}"]},
    ]
    summary = [
        ("ສົມຜົນ", eq, True),
        ("ຈຸດສູນກາງ", rf"C({tex(h)},\ {tex(k)})", True),
        ("ແກນໃຫຍ່", "ວົງມົນ (ບໍ່ມີ)" if circle else ("ແນວນອນ" if horizontal else "ແນວຕັ້ງ"), False),
        ("c", f"c = {c_tex}", True),
        ("ໂຟກັສ F₁, F₂", rf"({foci_t[0][0]},\ {foci_t[0][1]}),\ ({foci_t[1][0]},\ {foci_t[1][1]})", True),
        ("ຄວາມເບີ້ຍ e", f"e = {dec(e_f)}", True),
        ("ພື້ນທີ່ ( πab )", rf"A = \pi \cdot {tex(a * b)} \approx {dec(math.pi * float(a * b))}", True),
    ]
    return {"a": a, "b": b, "h": h, "k": k, "major": major, "minor": minor, "c_f": c_f,
            "e_f": e_f, "horizontal": horizontal, "circle": circle, "foci_f": foci_f,
            "vertices_f": vertices_f, "cov_f": cov_f, "summary": summary, "steps": steps}


def locate_point(res, x0, y0):
    """ກວດວ່າຈຸດຢູ່ເທິງ/ພາຍໃນ/ພາຍນອກ ຮູບໄຂ່"""
    x0, y0 = to_fr(x0), to_fr(y0)
    v = ((x0 - res["h"]) / res["a"]) ** 2 + ((y0 - res["k"]) / res["b"]) ** 2
    status = "on" if v == 1 else ("inside" if v < 1 else "outside")
    return {"value": v, "status": status}

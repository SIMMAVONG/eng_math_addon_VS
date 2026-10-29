"""Parabola  y = ax^2 + bx + c"""
import math
from .common import to_fr, tex, tex_p, sqrt_fr, dec, poly_tex


def _vertex_form(a, h, k):
    ac = "" if a == 1 else ("-" if a == -1 else tex(a))
    x = "x" if h == 0 else rf"\left(x {'-' if h > 0 else '+'} {tex(abs(h))}\right)"
    s = f"y = {ac}{x}^2"
    if k != 0:
        s += f" {'+' if k > 0 else '-'} {tex(abs(k))}"
    return s


def analyze(a, b, c):
    a, b, c = to_fr(a), to_fr(b), to_fr(c)
    if a == 0:
        raise ValueError("ຄ່າ a ຕ້ອງບໍ່ເທົ່າ 0 (ຖ້າ a = 0 ຈະເປັນເສັ້ນຊື່ ບໍ່ແມ່ນ parabola)")
    D = b * b - 4 * a * c
    h = -b / (2 * a)
    k = a * h * h + b * h + c
    p = 1 / (4 * a)
    focus = (h, k + p)
    directrix = k - p

    roots_exact, roots_f = None, []
    s = sqrt_fr(D) if D >= 0 else None
    if D > 0 and s is not None:
        roots_exact = sorted([(-b - s) / (2 * a), (-b + s) / (2 * a)])
        roots_f = [float(r) for r in roots_exact]
    elif D == 0:
        roots_exact = [h]
        roots_f = [float(h)]
    elif D > 0:
        sq = math.sqrt(float(D))
        roots_f = sorted([(-float(b) - sq) / (2 * float(a)), (-float(b) + sq) / (2 * float(a))])
    root_type = "two" if D > 0 else ("one" if D == 0 else "none")
    vform = _vertex_form(a, h, k)

    steps = [
        {"title": "ຂຽນສົມຜົນ ແລະ ລະບຸຄ່າ a, b, c",
         "text": "ຮູບແບບທົ່ວໄປຂອງ parabola: $y = ax^2 + bx + c$",
         "latex": [f"y = {poly_tex(a, b, c)}",
                   rf"a = {tex(a)},\quad b = {tex(b)},\quad c = {tex(c)}"]},
        {"title": "ຄິດໄລ່ຕົວຈຳແນກ (Discriminant)",
         "latex": [r"D = b^2 - 4ac",
                   rf"D = {tex_p(b)}^2 - 4({tex(a)})({tex(c)}) = {tex(D)}"]},
    ]
    if D > 0:
        text = "D > 0 → ມີ **2 ຮາກຈິງ** ທີ່ແຕກຕ່າງກັນ (ກຣາຟຕັດແກນ x ສອງຈຸດ)"
    elif D == 0:
        text = "D = 0 → ມີ **ຮາກດຽວ** (ກຣາຟແຕະແກນ x ທີ່ຈຸດຍອດ)"
    else:
        text = "D < 0 → **ບໍ່ມີຮາກຈິງ** (ກຣາຟບໍ່ຕັດແກນ x)"
    lat = [r"x = \dfrac{-b \pm \sqrt{D}}{2a}"]
    if D >= 0:
        lat.append(rf"x = \dfrac{{-({tex(b)}) \pm \sqrt{{{tex(D)}}}}}{{2({tex(a)})}}")
        if roots_exact is not None:
            lat.append(r",\quad ".join(f"x_{i + 1} = {tex(r)}" for i, r in enumerate(roots_exact)))
        else:
            lat.append(rf"x_1 \approx {dec(roots_f[0])},\quad x_2 \approx {dec(roots_f[1])}")
    steps.append({"title": "ຫາຮາກຂອງສົມຜົນ (ສູດ quadratic)", "text": text, "latex": lat})
    steps.append({
        "title": "ຫາຈຸດຍອດ (Vertex) ແລະ ແກນສົມມາດ",
        "text": f"ກຣາຟ **ເປີດ{'ຂຶ້ນ' if a > 0 else 'ລົງ'}** ເພາະ a {'> 0' if a > 0 else '< 0'}",
        "latex": [r"h = -\dfrac{b}{2a}",
                  rf"h = -\dfrac{{{tex(b)}}}{{2({tex(a)})}} = {tex(h)}",
                  rf"k = a h^2 + b h + c = {tex(k)}",
                  rf"V({tex(h)},\ {tex(k)}),\qquad x = {tex(h)}"]})
    steps.append({"title": "ຂຽນໃນຮູບແບບຈຸດຍອດ (Vertex form)",
                  "text": r"$y = a(x - h)^2 + k$", "latex": [vform]})
    steps.append({
        "title": "ຫາຈຸດໂຟກັສ (Focus) ແລະ ເສັ້ນຊີ້ທິດ (Directrix)",
        "text": "ທຸກຈຸດເທິງ parabola ຫ່າງຈາກໂຟກັສ ເທົ່າກັບທີ່ຫ່າງຈາກເສັ້ນຊີ້ທິດ",
        "latex": [r"p = \dfrac{1}{4a}" + rf" = {tex(p)}",
                  rf"F({tex(h)},\ {tex(k)} + {tex_p(p)}) = F({tex(focus[0])},\ {tex(focus[1])})",
                  rf"y = k - p = {tex(directrix)}"]})
    steps.append({"title": "ຈຸດຕັດແກນ y", "text": "ແທນ $x = 0$",
                  "latex": [rf"y = {tex(c)}\ \Rightarrow\ (0,\ {tex(c)})"]})

    if root_type == "none":
        roots_val, roots_is_tex = "ບໍ່ມີຮາກຈິງ (D < 0)", False
    elif roots_exact is not None:
        roots_val, roots_is_tex = r",\ ".join(f"x = {tex(r)}" for r in roots_exact), True
    else:
        roots_val, roots_is_tex = rf"x \approx {dec(roots_f[0])},\ x \approx {dec(roots_f[1])}", True

    summary = [
        ("ສົມຜົນ", f"y = {poly_tex(a, b, c)}", True),
        ("ຕົວຈຳແນກ D = b² − 4ac", f"D = {tex(D)}", True),
        ("ຈຸດຍອດ (Vertex)", rf"V({tex(h)},\ {tex(k)})", True),
        ("ແກນສົມມາດ", f"x = {tex(h)}", True),
        ("ຮູບແບບຈຸດຍອດ", vform, True),
        ("ທິດທາງ", "ເປີດຂຶ້ນ ↑ (a > 0)" if a > 0 else "ເປີດລົງ ↓ (a < 0)", False),
        ("ຈຸດໂຟກັສ (Focus)", rf"F({tex(focus[0])},\ {tex(focus[1])})", True),
        ("ເສັ້ນຊີ້ທິດ (Directrix)", f"y = {tex(directrix)}", True),
        ("ຈຸດຕັດແກນ y", rf"(0,\ {tex(c)})", True),
        ("ຮາກ / ຈຸດຕັດແກນ x", roots_val, roots_is_tex),
    ]
    return {"a": a, "b": b, "c": c, "D": D, "h": h, "k": k, "p": p, "focus": focus,
            "directrix": directrix, "roots_f": roots_f, "root_type": root_type,
            "opens_up": a > 0, "vertex_form": vform, "summary": summary, "steps": steps}

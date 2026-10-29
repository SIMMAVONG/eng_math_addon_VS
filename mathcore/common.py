"""ຟັງຊັນກາງ: ແປງຕົວເລກເປັນ Fraction (ຄິດໄລ່ແນ່ນອນ) ແລະ ສ້າງສູດ LaTeX"""
from fractions import Fraction
from math import isqrt


def to_fr(x):
    if isinstance(x, Fraction):
        return x
    if isinstance(x, bool):
        return Fraction(int(x))
    if isinstance(x, int):
        return Fraction(x)
    return Fraction(str(x)).limit_denominator(10**6)


def parse_fr(text):
    try:
        return Fraction(str(text).strip().replace(" ", ""))
    except (ValueError, ZeroDivisionError):
        raise ValueError("ປ້ອນຕົວເລກບໍ່ຖືກຮູບແບບ — ໃຊ້ເຊັ່ນ 3, -2, 0.75 ຫຼື 3/5")


def tex(x):
    x = to_fr(x)
    if x.denominator == 1:
        return str(x.numerator)
    sign = "-" if x < 0 else ""
    return rf"{sign}\frac{{{abs(x.numerator)}}}{{{x.denominator}}}"


def tex_p(x):
    """ໃສ່ວົງເລັບຖ້າເປັນຄ່າລົບ"""
    x = to_fr(x)
    return f"({tex(x)})" if x < 0 else tex(x)


def txt(x):
    x = to_fr(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def dec(x, nd=4):
    s = f"{float(x):.{nd}f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def sqrt_fr(x):
    """ຮາກທີ່ສອງຂອງ Fraction ຖ້າເປັນຄ່າພໍດີ, ບໍ່ດັ່ງນັ້ນ None"""
    x = to_fr(x)
    if x < 0:
        return None
    rn, rd = isqrt(x.numerator), isqrt(x.denominator)
    if rn * rn == x.numerator and rd * rd == x.denominator:
        return Fraction(rn, rd)
    return None


def _cell(x):
    return tex(x) if isinstance(x, (Fraction, int)) else str(x)


def mat_tex(M, kind="b"):
    env = {"b": "bmatrix", "v": "vmatrix", "p": "pmatrix"}[kind]
    body = r" \\ ".join(" & ".join(_cell(x) for x in row) for row in M)
    return rf"\begin{{{env}}} {body} \end{{{env}}}"


def lin_tex(coefs, names):
    parts = []
    for c, v in zip(coefs, names):
        c = to_fr(c)
        if c == 0:
            continue
        mag = abs(c)
        parts.append(("-" if c < 0 else "+", v if mag == 1 else f"{tex(mag)}{v}"))
    if not parts:
        return "0"
    s = ("-" if parts[0][0] == "-" else "") + parts[0][1]
    for sg, b in parts[1:]:
        s += f" {sg} {b}"
    return s


def poly_tex(a, b, c, var="x"):
    parts = []
    for coef, pw in ((a, 2), (b, 1), (c, 0)):
        coef = to_fr(coef)
        if coef == 0:
            continue
        mag = abs(coef)
        if pw == 0:
            body = tex(mag)
        else:
            cs = "" if mag == 1 else tex(mag)
            body = f"{cs}{var}^2" if pw == 2 else f"{cs}{var}"
        parts.append(("-" if coef < 0 else "+", body))
    if not parts:
        return "0"
    s = ("-" if parts[0][0] == "-" else "") + parts[0][1]
    for sg, b_ in parts[1:]:
        s += f" {sg} {b_}"
    return s

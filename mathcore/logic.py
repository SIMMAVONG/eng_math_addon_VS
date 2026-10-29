"""Logic: ຕາຕະລາງຄວາມຈິງ ແລະ ຄຸນສົມບັດຂອງປະໂຫຍກ If-Then"""
import re
import itertools

_TOK = re.compile(r"\s*(<->|->|[A-Za-z]+|[()&|~!])")
_SYM = {"and": "∧", "or": "∨", "imp": "→", "iff": "↔"}


def _tokenize(s):
    for a, b in (("∧", " & "), ("∨", " | "), ("¬", " ~ "), ("↔", " <-> "), ("⇔", " <-> "),
                 ("→", " -> "), ("⇒", " -> ")):
        s = s.replace(a, b)
    pos, out = 0, []
    while pos < len(s):
        if s[pos:].strip() == "":
            break
        m = _TOK.match(s, pos)
        if not m:
            raise ValueError(f"ພົບສັນຍາລັກທີ່ບໍ່ຮູ້ຈັກ: '{s[pos:].strip()[0]}'")
        t = m.group(1)
        pos = m.end()
        low = t.lower()
        if low == "and":
            t = "&"
        elif low == "or":
            t = "|"
        elif low == "not" or t == "!":
            t = "~"
        elif t.isalpha() and len(t) > 1:
            raise ValueError(f"ໃຊ້ຕົວອັກສອນດຽວເປັນຕົວແປ (p, q, r) — '{t}' ໃຊ້ບໍ່ໄດ້")
        out.append(t)
    return out


def parse(expr):
    toks = _tokenize(expr)
    if not toks:
        raise ValueError("ກະລຸນາປ້ອນສູດ ເຊັ່ນ p -> q")
    pos = 0

    def peek():
        return toks[pos] if pos < len(toks) else None

    def eat(t=None):
        nonlocal pos
        tok = peek()
        if tok is None or (t is not None and tok != t):
            raise ValueError("ສູດບໍ່ຖືກຕ້ອງ — ກວດວົງເລັບ ແລະ ເຄື່ອງໝາຍ")
        pos += 1
        return tok

    def p_iff():
        node = p_imp()
        while peek() == "<->":
            eat()
            node = ("iff", node, p_imp())
        return node

    def p_imp():
        node = p_or()
        if peek() == "->":
            eat()
            node = ("imp", node, p_imp())
        return node

    def p_or():
        node = p_and()
        while peek() == "|":
            eat()
            node = ("or", node, p_and())
        return node

    def p_and():
        node = p_not()
        while peek() == "&":
            eat()
            node = ("and", node, p_not())
        return node

    def p_not():
        if peek() == "~":
            eat()
            return ("not", p_not())
        return p_atom()

    def p_atom():
        tok = peek()
        if tok == "(":
            eat()
            node = p_iff()
            eat(")")
            return node
        if tok is not None and tok.isalpha():
            eat()
            return ("var", tok)
        raise ValueError("ສູດບໍ່ຖືກຕ້ອງ — ຄາດວ່າຈະມີຕົວແປ ຫຼື ວົງເລັບ")

    node = p_iff()
    if pos != len(toks):
        raise ValueError("ສູດບໍ່ຖືກຕ້ອງ — ມີສ່ວນເກີນ ຫຼື ຂາດເຄື່ອງໝາຍເຊື່ອມ")
    return node


def variables(n, acc=None):
    acc = [] if acc is None else acc
    if n[0] == "var":
        if n[1] not in acc:
            acc.append(n[1])
    else:
        for ch in n[1:]:
            variables(ch, acc)
    return sorted(acc)


def evaluate(n, env):
    k = n[0]
    if k == "var":
        return env[n[1]]
    if k == "not":
        return not evaluate(n[1], env)
    x, y = evaluate(n[1], env), evaluate(n[2], env)
    return {"and": x and y, "or": x or y, "imp": (not x) or y, "iff": x == y}[k]


def to_str(n, top=True):
    k = n[0]
    if k == "var":
        return n[1]
    if k == "not":
        return "¬" + to_str(n[1], False)
    s = f"{to_str(n[1], False)} {_SYM[k]} {to_str(n[2], False)}"
    return s if top else f"({s})"


def _subs(n, acc):
    if n[0] == "var":
        return
    for ch in n[1:]:
        _subs(ch, acc)
    if n not in acc:
        acc.append(n)


def _tf(b):
    return "T" if b else "F"


def truth_table(expr):
    tree = parse(expr)
    vs = variables(tree)
    if len(vs) > 4:
        raise ValueError("ໃຊ້ຕົວແປໄດ້ສູງສຸດ 4 ຕົວ (p, q, r, s)")
    subs = []
    _subs(tree, subs)
    headers = vs + [to_str(s, top=(s == tree)) for s in subs]
    rows, finals = [], []
    for vals in itertools.product([True, False], repeat=len(vs)):
        env = dict(zip(vs, vals))
        row = [_tf(v) for v in vals] + [_tf(evaluate(s, env)) for s in subs]
        rows.append(row)
        finals.append(evaluate(tree, env))
    kind = "tautology" if all(finals) else ("contradiction" if not any(finals) else "contingent")
    return {"headers": headers, "rows": rows, "kind": kind, "expr": to_str(tree)}


def implication_family():
    """If p then q  ກັບ converse / inverse / contrapositive"""
    forms = [("p → q", "p -> q"), ("q → p  (Converse)", "q -> p"),
             ("¬p → ¬q  (Inverse)", "~p -> ~q"), ("¬q → ¬p  (Contrapositive)", "~q -> ~p")]
    trees = [parse(f) for _, f in forms]
    rows, cols = [], [[] for _ in forms]
    for p, q in itertools.product([True, False], repeat=2):
        env = {"p": p, "q": q}
        vals = [evaluate(t, env) for t in trees]
        rows.append([_tf(p), _tf(q)] + [_tf(v) for v in vals])
        for i, v in enumerate(vals):
            cols[i].append(v)
    return {"headers": ["p", "q"] + [n for n, _ in forms], "rows": rows,
            "contrapositive_equiv": cols[0] == cols[3], "converse_equiv_inverse": cols[1] == cols[2],
            "converse_equiv_original": cols[0] == cols[1]}

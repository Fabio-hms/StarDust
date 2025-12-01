import json
from typing import Dict, List, Set, Tuple

def make_grammar():

    G = {
        "Program": [["FunctionDeclList"]],

        "FunctionDeclList": [["FunctionDecl", "FunctionDeclList"], []],
        "FunctionDecl": [["function", "IDENT", "(", "ParameterListOpt", ")", "Block"]],
        "ParameterListOpt": [["ParameterList"], []],
        "ParameterList": [["IDENT", "ParameterListTail"]],
        "ParameterListTail": [[",", "IDENT", "ParameterListTail"], []],

        "Block": [["{", "StatementList", "}"]],
        "StatementList": [["Statement", "StatementList"], []],

        "Statement": [
            ["IDENT", "StatementPrime"],
            ["if", "(", "Expression", ")", "Block", "ElsifPart", "ElsePart"],
            ["while", "(", "Expression", ")", "Block"],
            ["for", "(", "ExpressionOpt", ";", "ExpressionOpt", ";", "ExpressionOpt", ")", "Block"],
            ["return", "ExpressionOpt", ";"],
            ["{", "StatementList", "}"],
            [";"]
        ],

        "StatementPrime": [
            ["=", "Expression", ";"],
            ["ExpressionRest", ";"]
        ],

        "ElsifPart": [["elsif", "(", "Expression", ")", "Block", "ElsifPart"], []],
        "ElsePart": [["else", "Block"], []],
        "ExpressionOpt": [["Expression"], []],

        "Expression": [["AddExpr", "ExpressionRel"]],

        "ExpressionRel": [["RelationalOperator", "AddExpr"], []],

        "AddExpr": [["TermExpression", "AddExprPrime"]],
        "AddExprPrime": [["AdditiveOperator", "TermExpression", "AddExprPrime"], []],
        "AdditiveOperator": [["+"], ["-"], ["and"], ["or"]],

        "TermExpression": [["FactorExpression", "TermTail"]],
        "TermTail": [["MultiplicativeOperator", "FactorExpression", "TermTail"], []],
        "MultiplicativeOperator": [["*"], ["/"], ["//"], ["%"]],

        "FactorExpression": [
            ["IDENT"],
            ["NumberLiteral"],
            ["StringLiteral"],
            ["true"],
            ["false"],
            ["null"],
            ["(", "Expression", ")"],
            ["-", "FactorExpression"]
        ],

        "NumberLiteral": [["INT"], ["FLOAT"]],
        "StringLiteral": [["STRING"]],

        "RelationalOperator": [["=="], ["!="], [">"], [">="], ["<"], ["<="]],
    }

    return G


# ---------- FIRST / FOLLOW  ----------

def compute_first(G: Dict[str, List[List[str]]]) -> Dict[str, Set[str]]:
    FIRST = {A: set() for A in G}
    changed = True
    while changed:
        changed = False
        for A in G:
            for prod in G[A]:
                if prod == []:
                    if "ε" not in FIRST[A]:
                        FIRST[A].add("ε")
                        changed = True
                    continue
                for X in prod:
                    if X not in G:
                        if X not in FIRST[A]:
                            FIRST[A].add(X)
                            changed = True
                        break
                    else:
                        before = len(FIRST[A])
                        # add FIRST[X] \ {ε} to FIRST[A]
                        FIRST[A].update(x for x in FIRST[X] if x != "ε")
                        # if FIRST[X] contains ε, continue to next symbol; mark changed if new items added
                        if "ε" in FIRST[X]:
                            if len(FIRST[A]) != before:
                                changed = True
                            continue
                        # otherwise stop considering this production
                        if len(FIRST[A]) != before:
                            changed = True
                        break
                else:
                    # all symbols in prod derive ε
                    if "ε" not in FIRST[A]:
                        FIRST[A].add("ε")
                        changed = True
    return FIRST


def first_of_string(beta: List[str], G, FIRST) -> Set[str]:
    res = set()
    if beta == []:
        res.add("ε")
        return res
    for X in beta:
        if X not in G:
            res.add(X)
            return res
        res.update(x for x in FIRST[X] if x != "ε")
        if "ε" in FIRST[X]:
            continue
        return res
    res.add("ε")
    return res


def compute_follow(G, FIRST, start="Program"):
    FOLLOW = {A: set() for A in G}
    FOLLOW[start].add("$")
    changed = True
    while changed:
        changed = False
        for A in G:
            for prod in G[A]:
                for i, B in enumerate(prod):
                    if B in G:
                        beta = prod[i+1:]
                        first_beta = first_of_string(beta, G, FIRST)
                        before = len(FOLLOW[B])
                        FOLLOW[B].update(x for x in first_beta if x != "ε")
                        if "ε" in first_beta or beta == []:
                            FOLLOW[B].update(FOLLOW[A])
                        if len(FOLLOW[B]) != before:
                            changed = True
    return FOLLOW


def build_parsing_table(G, FIRST, FOLLOW):
    table = {}
    for A in G:
        for prod in G[A]:
            first_set = first_of_string(prod, G, FIRST)
            for t in (first_set - {"ε"}):
                key = (A, t)
                if key in table:
                    raise ValueError(f"LL(1) conflict for {key}: {table[key]} vs {prod}")
                table[key] = prod
            if "ε" in first_set:
                for t in FOLLOW[A]:
                    key = (A, t)
                    if key in table:
                        raise ValueError(f"LL(1) conflict for {key}: {table[key]} vs {prod}")
                    table[key] = prod
    return table


def generate(filename="stardust_ll1/ll1_table.json"):
    G = make_grammar()
    FIRST = compute_first(G)
    FOLLOW = compute_follow(G, FIRST)
    TABLE = build_parsing_table(G, FIRST, FOLLOW)
    data = {
        "G": G,
        "FIRST": {k: sorted(list(v)) for k, v in FIRST.items()},
        "FOLLOW": {k: sorted(list(v)) for k, v in FOLLOW.items()},
        "TABLE": {f"{A}|{t}": TABLE[(A,t)] for (A,t) in TABLE}
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return data

if __name__ == "__main__":
    generate()
    print("ll1_table.json created")

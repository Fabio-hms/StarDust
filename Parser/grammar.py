# stardust_ll1/grammar.py
import json
from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple, Any

# Grammar representation:
# dict from nonterminal -> list of productions (each prod is list of symbols (str), terminals are lowercase tokens or symbols)
# We'll use uppercase names for nonterminals and token strings like "IDENT", "INT", "+", "if", etc. as terminals.

def make_grammar():
    # This grammar is adapted to match the course slides (LL(1)-friendly).
    # Nonterminals are uppercase identifiers.
    G = {
        "Program": [["FunctionDeclarationList"]],
        "FunctionDeclarationList": [["FunctionDeclaration", "FunctionDeclarationList"], []],  # [] denotes epsilon
        "FunctionDeclaration": [["function", "IDENT", "(", "ParameterListOpt", ")", "Block"]],
        "ParameterListOpt": [["ParameterList"], []],
        "ParameterList": [["IDENT", "ParameterListTail"]],
        "ParameterListTail": [[",", "IDENT", "ParameterListTail"], []],
        "Block": [["{", "StatementList", "}"]],
        "StatementList": [["Statement", "StatementList"], []],
        "Statement": [
            ["AssignmentStatement"],
            ["ConditionalStatement"],
            ["LoopStatement"],
            ["ReturnStatement"],
            ["Block"],
            [";",],
            ["Expression", ";"]
        ],
        "AssignmentStatement": [["IDENT", "=", "Expression", ";"]],
        "ConditionalStatement": [["if", "(", "ConditionExpression", ")", "Block", "ElsifPart", "ElsePart"]],
        "ElsifPart": [["elsif", "(", "ConditionExpression", ")", "Block", "ElsifPart"], []],
        "ElsePart": [["else", "Block"], []],
        "LoopStatement": [["while", "(", "ConditionExpression", ")", "Block"],
                          ["for", "(", "ExpressionOpt", ";", "ExpressionOpt", ";", "ExpressionOpt", ")", "Block"]],
        "ReturnStatement": [["return", "ExpressionOpt", ";"]],
        "ExpressionOpt": [["Expression"], []],
        "ConditionExpression": [["Expression", "RelationalOperator", "Expression"], ["Expression"]],
        "RelationalOperator": [["=="], ["!="], [">"], [">="], ["<"], ["<="]],
        "Expression": [["TermExpression", "ExpressionTail"]],
        "ExpressionTail": [["AdditiveOperator", "TermExpression", "ExpressionTail"], []],
        "AdditiveOperator": [["+"], ["-"], ["and"], ["or"]],
        "TermExpression": [["FactorExpression", "TermTail"]],
        "TermTail": [["MultiplicativeOperator", "FactorExpression", "TermTail"], []],
        "MultiplicativeOperator": [["*"], ["/"], ["//"], ["%"]],
        "FactorExpression": [["IDENT"], ["NumberLiteral"], ["StringLiteral"], ["true"], ["false"], ["null"], ["(", "Expression", ")"], ["-", "FactorExpression"]],
        "NumberLiteral": [["INT"], ["FLOAT"]],
        "StringLiteral": [["STRING"]],
    }
    # Normalize empty production as explicit list []
    for A, prods in G.items():
        new = []
        for p in prods:
            if p == []:
                new.append([])
            else:
                new.append(p)
        G[A] = new
    return G

# Utilities to compute FIRST and FOLLOW sets
def compute_first(G):
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
                    if X not in G:  # X is terminal
                        if X not in FIRST[A]:
                            FIRST[A].add(X)
                            changed = True
                        break
                    else:
                        # add FIRST(X) \ {ε} to FIRST(A)
                        before = len(FIRST[A])
                        FIRST[A].update(x for x in FIRST[X] if x != "ε")
                        if "ε" in FIRST[X]:
                            # continue to next symbol
                            pass
                        else:
                            break
                        if len(FIRST[A]) != before:
                            changed = True
                else:
                    # all symbols had ε
                    if "ε" not in FIRST[A]:
                        FIRST[A].add("ε")
                        changed = True
    return FIRST

def first_of_string(symbols: List[str], G, FIRST) -> Set[str]:
    res = set()
    if symbols == []:
        res.add("ε")
        return res
    for X in symbols:
        if X not in G:
            res.add(X)
            return res
        res.update(x for x in FIRST[X] if x != "ε")
        if "ε" in FIRST[X]:
            continue
        else:
            return res
    res.add("ε")
    return res

def compute_follow(G, FIRST, start_symbol="Program"):
    FOLLOW = {A: set() for A in G}
    FOLLOW[start_symbol].add("$")
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
    table: Dict[Tuple[str,str], List[str]] = {}
    for A in G:
        for prod in G[A]:
            first_set = first_of_string(prod, G, FIRST)
            for terminal in (first_set - {"ε"}):
                key = (A, terminal)
                if key in table:
                    # conflict detected - ambiguous or not LL(1)
                    raise ValueError(f"LL(1) conflict for {key}: {table[key]} vs {prod}")
                table[key] = prod
            if "ε" in first_set:
                for terminal in FOLLOW[A]:
                    key = (A, terminal)
                    if key in table:
                        raise ValueError(f"LL(1) conflict for {key}: {table[key]} vs {prod}")
                    table[key] = prod  # epsilon production
    return table

def generate_and_save_table(filename="stardust_ll1/ll1_table.json"):
    G = make_grammar()
    FIRST = compute_first(G)
    FOLLOW = compute_follow(G, FIRST, "Program")
    table = build_parsing_table(G, FIRST, FOLLOW)
    # convert sets to lists for json
    data = {
        "G": G,
        "FIRST": {k: sorted(list(v)) for k,v in FIRST.items()},
        "FOLLOW": {k: sorted(list(v)) for k,v in FOLLOW.items()},
        "TABLE": {f"{A}|||{t}": prod for (A,t), prod in table.items()}
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return data

if __name__ == "__main__":
    data = generate_and_save_table()
    print("Wrote table and sets to ll1_table.json")

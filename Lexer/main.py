
from afn_to_afd import afn_to_afd
from afns_definicao import AFNS

def simulate_afd(afd, text, i):
    state = afd["start"]
    j = i
    last_final_pos = -1
    transitions = afd["transitions"]
    finals = set(afd["finals"])
    while j < len(text):
        ch = text[j]
        key = (state, ch)
        if key in transitions:
            state = transitions[key]
            if state in finals:
                last_final_pos = j+1
            j += 1
        else:
            break
    return last_final_pos - i if last_final_pos != -1 else 0

def tokenize(text):
    # Precompute AFDs
    afd_map = {name: afn_to_afd(afn) for name, afn in AFNS.items()}
    tokens = []
    i = 0
    while i < len(text):
        if text[i].isspace():
            i += 1
            continue
        best = (None, 0)
        for name, afd in afd_map.items():
            l = simulate_afd(afd, text, i)
            if l > best[1]:
                best = (name, l)
        if best[1] > 0:
            lex = text[i:i+best[1]]
            if best[0] != "COMENT":  # skip comments
                tokens.append((best[0], lex))
            i += best[1]
        else:
            tokens.append(("UNKNOWN", text[i]))
            i += 1
    return tokens

if __name__ == "__main__":
    sample = 'var x = 42; // exemplo\\nfunc f() { return x; }'
    print("Input:", sample)
    toks = tokenize(sample)
    print("Tokens:", toks)

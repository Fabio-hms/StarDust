from lexer.afn_to_afd import AFN, afn_to_afd
from lexer.lexer import Lexer

if __name__ == "__main__":
    afn = AFN(
        states=['q0', 'q1'],
        alphabet=list("abcdefghijklmnopqrstuvwxyz"),
        transitions={
            ('q0', 'a'): {'q1'},
            ('q1', 'a'): {'q1'},
            ('q1', 'b'): {'q1'}
        },
        start='q0',
        finals={'q1'}
    )

    afd = afn_to_afd(afn)
    token_map = {state: "IDENT" for state in afd['finals']}
    lexer = Lexer(afd, token_map)

    code = "aab aaabb"
    tokens = lexer.tokenize(code)
    print(tokens)

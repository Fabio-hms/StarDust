from afn_to_afd import AFN

digits = "0123456789"
letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
alnum = letters + digits + "_"

# IDENT
afn_ident = AFN(
    states=['q0','q1'],
    alphabet=list(alnum),
    transitions={
        ('q0','_'): {'q1'},
        **{('q0', c): {'q1'} for c in letters},
        **{('q1', c): {'q1'} for c in alnum},
    },
    start='q0',
    finals={'q1'}
)

# INT
afn_int = AFN(
    states=['q0','q1'],
    alphabet=list(digits),
    transitions={
        **{('q0', c): {'q1'} for c in digits},
        **{('q1', c): {'q1'} for c in digits},
    },
    start='q0',
    finals={'q1'}
)

# SIMPLE REAL
afn_real = AFN(
    states=['q0','q1','q2'],
    alphabet=list(digits + '.'),
    transitions={
        **{('q0', c): {'q1'} for c in digits},
        ('q1', '.'): {'q2'},
        **{('q2', c): {'q2'} for c in digits},
    },
    start='q0',
    finals={'q2'}
)

# STRING (simple)
afn_string = AFN(
    states=['q0','q1','q2'],
    alphabet=[chr(i) for i in range(32,127) if chr(i) != '"'],
    transitions={
        ('q0','"'): {'q1'},
        **{('q1', c): {'q1'} for c in [chr(i) for i in range(32,127) if chr(i) != '"']},
        ('q1','"'): {'q2'},
    },
    start='q0',
    finals={'q2'}
)

# Operators (single char)
ops = ['+', '-', '*', '/', '=', '<', '>', '!', '&', '|']
afn_ops = AFN(
    states=['q0','q1'],
    alphabet=ops,
    transitions={('q0', c): {'q1'} for c in ops},
    start='q0',
    finals={'q1'}
)

# Punctuation
puns = [';', ',', '(', ')', '{', '}', ':']
afn_pont = AFN(
    states=['q0','q1'],
    alphabet=puns,
    transitions={('q0', c): {'q1'} for c in puns},
    start='q0',
    finals={'q1'}
)

# Comments: // single-line
afn_comentario = AFN(
    states=['q0','q1','q2'],
    alphabet=['/'] + [chr(i) for i in range(32,127) if chr(i) != '/'],
    transitions={
        ('q0','/'): {'q1'},
        ('q1','/'): {'q2'},
        **{('q2', c): {'q2'} for c in [chr(i) for i in range(32,127) if chr(i) != '\n']},
    },
    start='q0',
    finals={'q2'}
)

AFNS = {
    "IDENT": afn_ident,
    "INT": afn_int,
    "REAL": afn_real,
    "STRING": afn_string,
    "OP": afn_ops,
    "PONT": afn_pont,
    "COMENT": afn_comentario
}

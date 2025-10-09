from lexer.afn_to_afd import AFN

# ===============================
# IDENTIFICADORES: [a-z_][a-zA-Z0-9_]*
# ===============================
afn_ident = AFN(
    states=['qa0', 'qa1'],
    alphabet=list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"),
    transitions={
        ('qa0', '_'): {'qa1'},
        **{('qa0', c): {'qa1'} for c in "abcdefghijklmnopqrstuvwxyz"},
        **{('qa1', c): {'qa1'} for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"},
    },
    start='qa0',
    finals={'qa1'}
)

# ===============================
# NÚMEROS INTEIROS: [+|-]?[0-9]+
# ===============================
afn_int = AFN(
    states=['qn0', 'qn1', 'qn2'],
    alphabet=list("0123456789+-"),
    transitions={
        ('qn0', '+'): {'qn1'},
        ('qn0', '-'): {'qn1'},
        **{('qn0', c): {'qn2'} for c in "0123456789"},
        **{('qn1', c): {'qn2'} for c in "0123456789"},
        **{('qn2', c): {'qn2'} for c in "0123456789"},
    },
    start='qn0',
    finals={'qn2'}
)

# ===============================
# NÚMEROS REAIS: [+|-]?[0-9]*.[0-9]+([eE][+|-]?[0-9]+)?
# ===============================
afn_real = AFN(
    states=['qo0','qo1','qo2','qo3','qo4','qo5','qo6','qo7','qo8'],
    alphabet=list("0123456789.+-eE"),
    transitions={
        ('qo0', '+'): {'qo1'},
        ('qo0', '-'): {'qo1'},
        **{('qo0', c): {'qo2'} for c in "0123456789"},
        **{('qo1', c): {'qo2'} for c in "0123456789"},
        **{('qo2', c): {'qo2'} for c in "0123456789"},
        ('qo2', '.'): {'qo4'},
        ('qo0', '.'): {'qo3'},
        ('qo1', '.'): {'qo3'},
        ('qo3', c): {'qo5'} for c in "0123456789",
        ('qo4', c): {'qo5'} for c in "0123456789",
        **{('qo5', c): {'qo5'} for c in "0123456789"},
        ('qo5', 'e'): {'qo6'},
        ('qo5', 'E'): {'qo6'},
        ('qo6', '+'): {'qo7'},
        ('qo6', '-'): {'qo7'},
        **{('qo6', c): {'qo8'} for c in "0123456789"},
        **{('qo7', c): {'qo8'} for c in "0123456789"},
        **{('qo8', c): {'qo8'} for c in "0123456789"},
    },
    start='qo0',
    finals={'qo5', 'qo8'}
)

# ===============================
# CHAR: 'c' ou com escape
# ===============================
afn_char = AFN(
    states=['qs0', 'qs1', 'qs2', 'qsf'],
    alphabet=[chr(i) for i in range(32,127)] + ['\\'],
    transitions={
        ('qs0', "'"): {'qs1'},
        **{('qs1', c): {'qsf'} for c in [chr(i) for i in range(32,127)] if c not in ["'", "\\"]},
        ('qs1', '\\'): {'qs2'},
        **{('qs2', c): {'qsf'} for c in [chr(i) for i in range(32,127)]},
        ('qsf', "'"): set(),
    },
    start='qs0',
    finals={'qsf'}
)

# ===============================
# STRING: "texto" ou com escapes
# ===============================
afn_string = AFN(
    states=['qss0', 'qss1', 'qss2', 'qssf'],
    alphabet=[chr(i) for i in range(32,127)] + ['\\'],
    transitions={
        ('qss0', '"'): {'qss1'},
        **{('qss1', c): {'qss1'} for c in [chr(i) for i in range(32,127)] if c not in ['"', '\\']},
        ('qss1', '\\'): {'qss2'},
        **{('qss2', c): {'qss1'} for c in [chr(i) for i in range(32,127)]},
        ('qss1', '"'): {'qssf'}
    },
    start='qss0',
    finals={'qssf'}
)

# ===============================
# OPERADORES: + - * / % = == != >= <=
# ===============================
ops = ['+', '-', '*', '/', '%', '=', '==', '!=', '>=', '<=']
afn_ops = AFN(
    states=['qop0','qop1','qop2'],
    alphabet=list("+-*/%=!><"),
    transitions={
        ('qop0', '+'): {'qop1'},
        ('qop0', '-'): {'qop1'},
        ('qop0', '*'): {'qop1'},
        ('qop0', '/'): {'qop1'},
        ('qop0', '%'): {'qop1'},
        ('qop0', '='): {'qop1'},
        ('qop0', '!'): {'qop1'},
        ('qop0', '>'): {'qop1'},
        ('qop0', '<'): {'qop1'},
        ('qop1', '='): {'qop2'}
    },
    start='qop0',
    finals={'qop1','qop2'}
)

# ===============================
# PONTUAÇÃO: ( ) { } ;
# ===============================
afn_pont = AFN(
    states=['qpt0','qpt1'],
    alphabet=list("(){};"),
    transitions={('qpt0', c): {'qpt1'} for c in "(){};"},
    start='qpt0',
    finals={'qpt1'}
)

# ===============================
# COMENTÁRIOS:
#   Linha: // até \n
#   Bloco: /* ... */
# ===============================
afn_comentario = AFN(
    states=['qsb0','qsb1','qsb2','qsb3','qsbf'],
    alphabet=[chr(i) for i in range(32,127)] + ['\n'],
    transitions={
        ('qsb0', '/'): {'qsb1'},
        ('qsb1', '/'): {'qsbf'},
        ('qsb1', '*'): {'qsb2'},
        **{('qsb2', c): {'qsb2'} for c in [chr(i) for i in range(32,127)] if c != '*'},
        ('qsb2', '*'): {'qsb3'},
        ('qsb3', '*'): {'qsb3'},
        ('qsb3', '/'): {'qsbf'}
    },
    start='qsb0',
    finals={'qsbf'}
)

# ===============================
# CONJUNTO GERAL
# ===============================
AFNS = {
    "IDENT": afn_ident,
    "INT": afn_int,
    "REAL": afn_real,
    "CHAR": afn_char,
    "STRING": afn_string,
    "OP": afn_ops,
    "PONT": afn_pont,
    "COMENT": afn_comentario
}

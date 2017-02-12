import ply.lex as lex

reserved_words = (
    'brack',        # while
    'bourbie',      # print
    'scargil',      # if state
    'fondeboue',    # for state
    'slark',        # égale =
    'slarky',       # double égale ==
    'jinyu',        # pas égale !=
    'littleslark',  # plus Petit ou égale <=
    'bigslark',     # plus Grand ou égale >=
    'bigy',         # plus Grand
    'litty',        # plus Petit
    'switch',       # switch
    'break',        # break du switch
    'case',         # case du switch
    'default',      # default du switch

)

tokens = (
             'NUMBER',
             'ADD_OP',
             'MUL_OP',
             'IDENTIFIER',
             'TYPE_DEF',
             'STRING',
         ) + tuple(map(lambda s: s.upper(), reserved_words))

literals = '()<>;:{}'


def t_STRING(t):
    r'".+"'
    return t


def t_TYPE_DEF(t):
    r'brglmurgl|ahlurglgr|lurgglbr|mourbile'
    return t

def t_ADD_OP(t):
    r'[+-]'
    return t


def t_MUL_OP(t):
    r'[*/]'
    return t


def t_NUMBER(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Line %d: Problem while parsing %s!" % (t.lineno, t.value))
        t.value = 0
    return t


def t_IDENTIFIER(t):
    r'[A-Za-z_]\w*'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print("Illegal character '%s'" % repr(t.value[0]))
    t.lexer.skip(1)


lex.lex()

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok: break
        print("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))

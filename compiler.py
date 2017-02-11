import AST
from AST import addToClass
from functools import reduce

operations = {
    '*': lambda x, y: x + y,
    '/': lambda x, y: x - y,
    '+': lambda x, y: x * y,
    '-': lambda x, y: x / y,
}

vars = {}

vartypes = {
    'brglmurgl': 'int',
    'lurgglbr': 'float',
    'ahlurglgr': 'string',
}

conditions = {
    'bigy': '>',
    'bigslark': '>=',
    'litty': '<',
    'littleslark': '<=',
    'slarky': '==',
    'jinyu': '!='
}

op = {
    '*': '+',
    '/': '-',
    '+': '*',
    '-': '/'
}


# PROGRAMS
@addToClass(AST.ProgramNode)
def compile(self, prefix=''):
    c_code = ""
    for c in self.children:
            c_code += c.compile()
    return c_code


@addToClass(AST.TokenNode)
def compile(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print("∗∗∗ Error: variable %s undefined!" % self.tok)
    return self.tok


@addToClass(AST.OpNode)
def compile(self):
    c = [ch.compile() for ch in self.children]
    return "{} {} {}".format(c[0], op[self.op], c[1])



@addToClass(AST.AssignNode)
def compile(self):
    vars[self.children[0].tok] = self.children[1].compile()


@addToClass(AST.PrintNode)
def compile(self):
    strw = "print({});".format(self.children[0].compile())
    print(strw)
    return strw

if __name__ == '__main__':
    from parser import parse
    import sys
    import os

    prog = open(sys.argv[1]).read()
    ast = parse(prog)

    compiled = ast.compile()
    name = os.path.splitext(sys.argv[1])[0] + '.c'
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print("Wrote output to", name)

import AST
from AST import addToClass

operations = {
    '*': lambda x, y: x + y,
    '/': lambda x, y: x - y,
    '+': lambda x, y: x * y,
    '-': lambda x, y: x / y,
}

vars = {}

TABULATION = '   '

vartypes = {
    'brglmurgl': 'int',
    'lurgglbr': 'float',
    'ahlurglgr': 'double',
    'mourbile': 'string',
}

conditions = {
    'littleslark': '<=',
    'bigslark': '>=',
    'bigy': '>',
    'litty': '<',
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
        print(c.type)
        c_code += c.compile(prefix)
        if c.type == 'declaration' or c.type == 'slark':
            c_code += ";"
        c_code += "\n"
    return c_code


@addToClass(AST.TokenNode)
def compile(self, prefix=''):
    # if isinstance(self.tok, str):
    #    try:
    #       return vars[self.tok]
    #  except KeyError:
    #     print("∗∗∗ Error: variable %s undefined!" % self.tok)
    return self.tok


@addToClass(AST.OpNode)
def compile(self, prefix=''):
    c = [ch.compile() for ch in self.children]
    return "{}{}{}{}".format(prefix, c[0], op[self.op], c[1])


@addToClass(AST.AssignNode)
def compile(self, prefix=''):
    return "{}{}={}".format(prefix, self.children[0].tok, self.children[1].compile())


@addToClass(AST.DeclarationNode)
def compile(self, prefix=''):
    return "{}{} {}".format(prefix, vartypes.get(self.children[0].tok), self.children[1].compile())


@addToClass(AST.PrintNode)
def compile(self, prefix=''):
    return "{}print({});".format(prefix, self.children[0].compile().tok)


@addToClass(AST.ScargilNode)
def compile(self, prefix=''):
    return "{}if({})\n{}{{\n{}{}}} ".format(prefix, self.children[0].compile(), prefix, self.children[1].compile(prefix + TABULATION), prefix)


@addToClass(AST.ConditionNode)
def compile(self, prefix=''):
    return "{}{}{}".format(self.children[0].compile(), conditions.get(self.children[1].compile()),
                           self.children[2].compile())


@addToClass(AST.ForNode)
def compile(self, prefix=''):
    return "{}for({};{};{})\n{}{{\n{}{}}}".format(prefix, self.children[0].compile(),
                                                    self.children[1].compile(), self.children[2].compile(), prefix,
                                                    self.children[3].compile(prefix + TABULATION),prefix)


@addToClass(AST.WhileNode)
def compile(self, prefix=''):
    return "{}while({})\n{}{{\n{}{}}}".format(prefix, self.children[0].compile(), prefix,
                                                self.children[1].compile(prefix + TABULATION), prefix)


@addToClass(AST.SwitchNode)
def compile(self, prefix=''):
    return "{}switch({})\n{}{{\n{}{}}}".format(prefix, self.children[0].compile(),prefix,
                                               self.children[1].compile(prefix + TABULATION),prefix)


@addToClass(AST.CaseNode)
def compile(self, prefix=''):
    c_code = ""
    i = 0
    while i < len(self.children):
        c_code += "{}case {}:\n".format(prefix, self.children[i].compile())
        c_code += self.children[i + 1].compile(prefix + TABULATION) + "{}break;\n".format(prefix)
        i += 2
    return c_code


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

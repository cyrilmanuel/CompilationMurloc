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
suffix = "   "
vartypes = {
    'brglmurgl': 'int',
    'lurgglbr': 'float',
    'ahlurglgr': 'double',
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
def compile(self):
    c_code = ""
    for c in self.children:
        c_code += c.compile() + "\n"
    return c_code


@addToClass(AST.TokenNode)
def compile(self):
   # if isinstance(self.tok, str):
    #    try:
     #       return vars[self.tok]
      #  except KeyError:
       #     print("∗∗∗ Error: variable %s undefined!" % self.tok)
    return self.tok


@addToClass(AST.OpNode)
def compile(self):
    c = [ch.compile() for ch in self.children]
    return "{}{}{}".format(c[0], op[self.op], c[1])


@addToClass(AST.AssignNode)
def compile(self):
    return "{}={}".format(self.children[0].tok, self.children[1].compile())


@addToClass(AST.DeclarationNode)
def compile(self):
    return "{} {}".format(vartypes.get(self.children[0].tok), self.children[1].compile())

@addToClass(AST.PrintNode)
def compile(self):
    return "print({});".format(self.children[0].compile().tok)

@addToClass(AST.ScargilNode)
def compile(self):
    return "if({}) \n {{ \n   {} }} ".format(self.children[0].compile(), self.children[1].compile())

@addToClass(AST.ConditionNode)
def compile(self):
    return "{} {} {}".format(self.children[0].compile(), conditions.get(self.children[1].compile()),
                             self.children[2].compile())

@addToClass(AST.ForNode)
def compile(self):
    return "for({};{};{}) \n {{ \n {} }} \n".format(self.children[0].compile(),
        self.children[1].compile(), self.children[2].compile(), self.children[3].compile())

@addToClass(AST.SwitchNode)
def compile(self):
    return "switch({}){{\n{}}}".format(self.children[0].compile(), self.children[1].compile())

@addToClass(AST.CaseNode)
def compile(self):
    c_code = ""
    i = 0
    while i < len(self.children):
        c_code += "case {}:\n".format(self.children[i].compile())
        c_code += self.children[i+1].compile() + "break; \n"
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

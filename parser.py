import ply.yacc as yacc
from lexems import tokens
import AST

vars = {}


def p_programme_statement(p):
    ''' programme : statement '''
    p[0] = AST.ProgramNode(p[1])


def p_programme_recursive(p):
    ''' programme : statement ';' programme '''
    p[0] = AST.ProgramNode([p[1]] + p[3].children)


def p_programmeswitch_statement(p):
    ''' programmeswitch : GLOUGLOUG NUMBER ':' programme SIR ';'
                        | GLOUGLOUG DEFAULT ':' programme SIR ';' '''
    p[0] = AST.CaseNode([AST.TokenNode(p[2]), p[4]])

def p_programmeswitch_recursive(p):
    ''' programmeswitch : GLOUGLOUG NUMBER ':' programme SIR ';' programmeswitch '''
    p[0] = AST.CaseNode([AST.TokenNode(p[2]), p[4]] + p[7].children)


def p_statement_print(p):
    ''' statement : BOURBIE expression '''
    p[0] = AST.PrintNode(AST.TokenNode(p[2]))


def p_statement(p):
    ''' statement : assignation
        | structure
        | declaration '''
    p[0] = p[1]


def p_assign(p):
    ''' assignation : IDENTIFIER SLARK expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


def p_structure_Switch(p):
    ''' structure : GELIHAST '(' IDENTIFIER ')' '{' programmeswitch '}' '''
    p[0] = AST.SwitchNode([AST.TokenNode(p[3]), p[6]])

def p_structure_For(p):
    ''' structure : FONDEBOUE '(' assignation ';' condition ';' assignation ')' '{' programme '}'
                  | FONDEBOUE '(' declaration ';' condition ';' assignation ')' '{' programme '}' '''
    p[0] = AST.ForNode([p[3], p[5], p[7], p[10]])


def p_structure_While(p):
    ''' structure : BRACK '(' condition ')' '{' programme '}' '''
    p[0] = AST.WhileNode([p[3], p[6]])


def p_structure_IF(p):
    ''' structure : SCARGIL '(' condition ')' '{' programme '}' '''
    p[0] = AST.ScargilNode([p[3], p[6]])


def p_declaration(p):
    ''' declaration : TYPE_DEF assignation '''
    p[0] = AST.DeclarationNode([AST.TokenNode(p[1]), p[2]])


def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]


def p_condition(p):
    '''condition : expression SLARKY expression
                 | expression JINYU expression
                 | expression BIGSLARK expression
                 | expression LITTLESLARK expression
                 | expression BIGY expression
                 | expression LITTY expression
                 '''
    p[0] = AST.ConditionNode([p[1], AST.TokenNode(p[2]), p[3]])


def p_expression_op(p):
    '''expression : expression ADD_OP expression
            | expression MUL_OP expression '''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])


def p_expression_num_or_var(p):
    '''expression : NUMBER
        | IDENTIFIER
        | STRING '''
    p[0] = AST.TokenNode(p[1])


def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS '''
    p[0] = AST.OpNode(p[1], [p[2]])


def p_error(p):
    if p:
        print("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print("Sytax error: unexpected end of file!")


precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)


def parse(program):
    return yacc.parse(program)


yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        print(result)

        import os

        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0] + '-ast.pdf'
        graph.write_pdf(name)
        print("wrote ast to", name)
    else:
        print("Parsing returned no result!")

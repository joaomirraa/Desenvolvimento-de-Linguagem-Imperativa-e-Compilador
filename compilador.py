import ply.lex as lex
import ply.yacc as yacc

# Definição dos tokens
tokens = [
    'ID',
    'NUM',

    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',

    'MAIOR',
    'MAIOROUIGUAL',
    'MENOR',
    'MENOROUIGUAL',

    'LPAREN',
    'RPAREN',

    'SE',
    'ENTAO',
    'SENAO',
    'FIM_COND',

    'ENQUANTO',
    'FAZ',
    'FIM_ENQUANTO',

    'INPUT',
    'IMPRIMIR',
    'VIRGULA',
    'PONTOVIRGULA',
    'IGUAL',
    '2PONTOS',

    'COMENTADO',
    'ASPAS'
]

# Regras dos tokens
#servem para reconhecer os tokens definidos anteriromente
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

t_MAIOR = r'>'
t_MAIOROUIGUAL = r'>='
t_MENOR = r'<'
t_MENOROUIGUAL = '<='

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_SE = r'se'
t_ENTAO = r'entao'
t_SENAO = r'senao'
t_FIM_COND = r'fim_cond'

t_ENQUANTO = r'enquanto'
t_FAZ = r'faz'
t_FIM_ENQUANTO = r'fim_enquanto'

t_INPUT = r'input'
t_IMPRIMIR = r'imprimir'
t_VIRGULA = r','
t_PONTOVIRGULA = r';'
t_IGUAL = r'='
t_2PONTOS = r':'



#t_COMENTADO = r'\\\\'  # Verificar se esta correto, tem de apanhar: "\\"
t_COMENTADO = r'\\\\[^\n]*'

#t_ASPAS = r'\"[^\"]*\"'
t_ASPAS = r'\"'

def t_ID(t):
    r'[a-zA-ZáéíóúÁÉÍÓÚãõÃÕâêîôûÂÊÎÔÛçÇ_][a-zA-Z0-9áéíóúÁÉÍÓÚãõÃÕâêîôûÂÊÎÔÛçÇ_]*'
    t.type = 'ID'
    return t


def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    #converte o valor do token para um inteiro(Inicialmente em string)
    return t

# Ignorar espaços em branco e tabulações
t_ignore = ' \t'

# Tratamento de quebra de linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
#t.lexer.lineno += len(t.value): Incrementa o número da linha (lineno) no 
# objeto lexer (t.lexer) pelo número de quebras de linha 
# encontradas (len(t.value)). Isso é usado para manter o controle 
# da linha atual no código-fonte enquanto o lexer processa os tokens.

# Tratamento de erro léxico
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Construção do analisador léxico
lexer = lex.lex()


# Definição da gramática
def p_program(p):
    '''program : declarations statements'''
    p[0] = p[1] + p[2]

def p_declarations(p):
    '''declarations : declarations declaration
                    | empty'''
    if len(p) > 2:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_declaration(p):
    '''declaration : ID PONTOVIRGULA'''
    p[0] = {'type': 'declaration', 'id': p[1]}

def p_statements(p):
    '''statements : statements statement
                  | empty'''
    if len(p) > 2:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_statement(p):
    '''statement : assignment
                 | if_statement
                 | while_statement
                 | read_statement
                 | write_statement'''
#                 | comentado'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : ID IGUAL expression PONTOVIRGULA'''
    p[0] = {'type': 'assignment', 'id': p[1], 'value': p[3]}

###
def p_condition(p):
    '''condition : expression'''
    p[0] = p[1]
###
    

def p_if_statement(p):
    '''if_statement : SE condition ENTAO statements SENAO statements FIM_COND PONTOVIRGULA'''
    p[0] = {'type': 'if', 'condition': p[2], 'then_statements': p[4], 'else_statements': p[6]}

def p_while_statement(p):
    '''while_statement : ENQUANTO condition FAZ statements FIM_ENQUANTO PONTOVIRGULA'''
    p[0] = {'type': 'while', 'condition': p[2], 'statements': p[4]}

def p_read_statement(p):
    '''read_statement : INPUT ID PONTOVIRGULA'''
    p[0] = {'type': 'read', 'id': p[2]}

def p_write_statement(p):
    '''write_statement : IMPRIMIR LPAREN ASPAS expression ASPAS VIRGULA ID RPAREN PONTOVIRGULA'''
    p[0] = {'type': 'write', 'value': p[4]}

def p_expression(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | term'''
    if len(p) > 2:
        p[0] = {'type': 'binop', 'op': p[2], 'left': p[1], 'right': p[3]}
    else:
        p[0] = p[1]

def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    if len(p) > 2:
        p[0] = {'type': 'binop', 'op': p[2], 'left': p[1], 'right': p[3]}
    else:
        p[0] = p[1]

def p_factor(p):
    '''factor : '(' expression ')'
              | ID
              | NUM'''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = {'type': 'literal', 'value': p[1]}

"""def p_comentado(p):
    ''' comentado: ID'''
    pass
"""
def p_empty(p):
    'empty :'
    pass


# Manipulação de erros
def p_error(p):
    print(f"Erro de sintaxe na entrada: {p.value}")



# Construção do analisador sintático
parser = yacc.yacc()

# Exemplo de uso
code = '''
int x;
int y;

x = 5;
y = 10;

se x > y entao
  escrever("x é maior que y");
senao
  escrever("y é maior que x");
fim_cond;

// do while
enquanto x > 0 faz
  escrever("x: ", x);
  x = x - 1;
fim_enquanto;

fim_programa;
'''

lexer.input(code)
for tok in lexer:
    print(tok)

#python compilador.py
#python yacc.py testes/testeA.plc
# lex.py

import ply.lex as lex # Import do ply.lex

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
    'IGUALIGUAL',
    'DIFERENTE',
    'EE',
    'OU',

    'LPAREN',
    'RPAREN',
    'LPAREN_RETO',
    'RPAREN_RETO',

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

    'COMENTADO',
  #  'ASPAS',

    'INT',

    'FRASE',

    'ALTERA',

    'LISTA',
    'MATRIZ'
]

# Regras dos tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

t_MAIOR = r'>'
t_MAIOROUIGUAL = r'>='
t_MENOR = r'<'
t_MENOROUIGUAL = '<='
t_IGUALIGUAL = '=='
t_DIFERENTE = '!='
t_EE = '\\/'
t_OU = '\\/'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LPAREN_RETO = r'\['
t_RPAREN_RETO = r'\]'

t_SE = r'ifse'
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

t_COMENTADO = r'%[^\n]*'
#t_COMENTADO = r'%.*'


#t_ASPAS = r'\"[^\"]*\"'
#t_ASPAS = r'"'
#t_ASPAS = r'\".*\"'

t_INT = r'int'

t_ID = r'\w+'

t_FRASE = r'"[^"]+"'

t_ALTERA = r'altera'

t_LISTA = r'lista'
t_MATRIZ = r'matriz'


"""def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'ID'
    return t"""

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

"""def t_COMENTADO(t):
    r'\\\\[^\n]*'
    return None"""

# Ignorar espacos em branco e tabulacoes
t_ignore = ' \t'

# Tratamento de quebra de linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erro léxico
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Construção do analisador léxico
lexer = lex.lex()
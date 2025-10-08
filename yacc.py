##############
import ply.yacc as yacc
from lex import *

##
import sys
import os
##


def p_Programa_Empty(p):
    '''
    Programa : Decls
             | Atrib
    '''
    parser.assembly = f'{p[1]}'


def p_Programa(p):
    '''
    Programa : Decls Corpo
             | Atrib Corpo
    '''
    parser.assembly = f'{p[1]}START\n{p[2]}STOP\n'


def p_Programa_Corpo(p):
    '''
    Programa : Corpo
    '''
    parser.assembly = f"START\n{p[1]}STOP\n"

def p_Corpo(p):
    '''
    Corpo : Codigo
    '''
    p[0] = f"{p[1]}"


def p_Codigo_Rec(p):
    '''
    Codigo : Proc Codigo
           | Decls Codigo
           | Atrib Codigo
           | COMENTARIO Codigo
    '''
    p[0] = f"{p[1]}{p[2]}"


def p_Codigo(p):
    '''
    Codigo : Proc
           | Atrib
           | Decls
           | COMENTARIO
    '''
    p[0] = f"{p[1]}"


def p_Decls(p):
    "Decls : Decl PONTOVIRGULA"
    p[0] = f'{p[1]}'


def p_DeclsRec(p):
    "Decls : Decl VIRGULA Decls"
    p[0] = f'{p[1]}{p[3]}'


def p_expr_arit(p):
    '''
    expr : exprArit
         | exprRel
    '''
    p[0] = p[1]


def p_Proc(p):
    '''
    Proc : IF
         | WHILE
         | PRINTAR
    '''
    p[0] = p[1]


# Declaração de uma variavel sem valor
def p_Decl(p):
    "Decl : INT ID"
    varName = p[2]
    if varName not in parser.variaveis:
        parser.variaveis[varName] = (parser.stackPointer, None)
        p[0] = "PUSHI 0\n"
        parser.stackPointer += 1
    else:
        parser.exito = False
        parser.error = f"Variável com o nome {varName} já existe"
    parser.linhaDeCodigo +=1


# Declaração de uma variável com atribuição de um valor
def p_Atrib_expr(p):
    "Atrib : INT ID IGUAL expr PONTOVIRGULA"
    varName = p[2]
    if varName not in parser.variaveis:
        value = p[4]
        parser.variaveis[varName] = (parser.stackPointer, None)
        p[0] = f"{value}STOREG {parser.stackPointer}\n"
        parser.stackPointer += 1
    else:
        parser.exito = False
        parser.error = f"Variável com o nome {varName} já existe"
    parser.linhaDeCodigo +=1

# atribuição de uma variavel ja declarada
def p_Atrib_sem_decl(p):
    "Atrib : ID IGUAL expr PONTOVIRGULA"
    varName = p[1]
    if varName in parser.variaveis:
        value = p[3]
        parser.variaveis[varName] = (parser.stackPointer, None)
        p[0] = f"{value}STOREG {parser.stackPointer}\n"
        parser.stackPointer += 1
    else:
        parser.exito = False
        parser.error = f"Variável com o nome {varName} não existe"
    parser.linhaDeCodigo +=1


# Altera valor de um variável
def p_alterna_var(p):
    "Atrib : ALTERA ID IGUAL expr PONTOVIRGULA"
    varName = p[2]
    if varName in parser.variaveis:
        p[0] = f"{p[4]}STOREG {parser.variaveis[varName][0]}\n"
    parser.linhaDeCodigo +=1


def p_expr(p):
    "expr : NUM"
    p[0] = f"PUSHI {int(p[1])}\n"


def p_expr_var(p):
    "expr : ID"
    varName = p[1]
    if varName in parser.variaveis:
        p[0] = f"PUSHG {parser.variaveis[varName][0]}\n"


def p_expr_input(p):
    "expr : INPUT"
    p[0] = f"READ\nATOI\n"


# Declara lista com tamanho INT
def p_DeclLista_Size(p):
    #"Atrib : LISTA ID INT"
    '''Decl : LISTA INT NUM VIRGULA ID''' # lista int 5, arr;
    listName = p[5]
    size = int(p[3])
    if listName not in parser.variaveis:
        if size > 0:
            parser.variaveis[listName] = (parser.stackPointer, size)
            p[0] = f"PUSHN {size}\n"
            parser.stackPointer += size
        else:
            parser.error = f"Impossível declarar um array de tamanho {size}"
            parser.exito = False
    else:
        parser.error = (
            f"Variável com o nome {listName} já definida anteriormente.")
        parser.exito = False
    parser.linhaDeCodigo +=1


# Altera valor de um indice da lista
def p_AlteraLista_elem(p):
    #"Atrib : ALTERA ID ABREPR expr FECHAPR COM expr"
    "Atrib : ALTERA ID LPAREN_RETO expr RPAREN_RETO IGUAL expr PONTOVIRGULA" # altera arr[3] = 4;
    varName = p[2]
    #pos = p[4]
    if varName in parser.variaveis:
        p[0] = f"PUSHGP\nPUSHI {parser.variaveis[varName][0]}\nPADD\n{p[4]}{p[7]}STOREN\n"
    else:
        parser.error = f"Variável com o nome {varName} não definida"
        parser.exito = False
    parser.linhaDeCodigo +=1


# Função que vai buscar o valor do indice na lista
def p_AtribBusca_Lista(p):
    #"expr : BUSCA ID ABREPR expr FECHAPR"
    "expr : ID LPAREN_RETO expr RPAREN_RETO" # x = arr[4];
    varName = p[1]
    indice = p[3]
    if varName in parser.variaveis:
        p[0] = f"PUSHGP\nPUSHI {parser.variaveis[varName][0]}\nPADD\n{indice}LOADN\n"
    else:
        parser.error = (
            f"Variável com o nome {varName} não definida anteriormente.")
        parser.exito = False
    parser.linhaDeCodigo += 1


# Expressão Aritmética Soma
def p_PLUS(p):
    "exprArit : exprArit PLUS term"
    p[0] = f"{p[1]}{p[3]}ADD\n"


# Expressão Aritmética Subtração
def p_MINUS(p):
    "exprArit : exprArit MINUS term"
    p[0] = f"{p[1]}{p[3]}SUB\n"

def p_expr_arit_term(p):
    '''exprArit : term'''
    p[0] = p[1]


# Expressão Aritmética Multiplicação
def p_TIMES(p):
    "term : term TIMES factor"
    p[0] = f"{p[1]}{p[3]}MUL\n"


# Expressão Aritmética Divisão
def p_DIVIDE(p):
    "term : term DIVIDE factor"
    p[0] = f"{p[1]}{p[3]}DIV\n"

def p_term(p):
    "term : factor"
    p[0] = p[1]

def p_factor_num(p):
    '''factor : NUM'''
    p[0] = f"PUSHI {int(p[1])}\n"


def p_factor_id(p):
    '''factor : ID'''
    varName = p[1]
    if varName in parser.variaveis:
        p[0] = f"PUSHG {parser.variaveis[varName][0]}\n"



# Expressão Relativa Igual
def p_IGUALIGUAL(p):
    "exprRel : expr IGUALIGUAL expr"
    p[0] = f"{p[1]}{p[3]}EQUAL\n"


# Expressão Relativa Diferente
def p_DIFERENTE(p):
    "exprRel : expr DIFERENTE expr"
    p[0] = f"{p[1]}{p[3]}NOT\nEQUAL\n"


# Expressão Relativa Menor
def p_MENOR(p):
    "exprRel : expr MENOR expr"
    p[0] = f"{p[1]}{p[3]}INF\n"


# Expressão Relativa Menor ou Igual
def p_MENOROUIGUAL(p):
    "exprRel : expr MENOROUIGUAL expr"
    p[0] = f"{p[1]}{p[3]}INFEQ\n"


# Expressão Relativa Maior
def p_MAIOR(p):
    "exprRel : expr MAIOR expr"
    p[0] = f"{p[1]}{p[3]}SUP\n"


# Expressão Relativa Maior ou Igual
def p_MAIOROUIGUAL(p):
    "exprRel : expr MAIOROUIGUAL expr"
    p[0] = f"{p[1]}{p[3]}SUPEQ\n"


# Expressão Relativa E
def p_EE(p):
    "exprRel : expr EE expr"
    p[0] = f"{p[1]}{p[3]}ADD\nPUSHI 2\nEQUAL\n"


# Expressão Relativa OU
def p_OU(p):
    "exprRel : expr OU expr"
    p[0] = f"{p[1]}{p[3]}ADD\nPUSHI 1\nSUPEQ\n"


# Controlo de fluxo (if then)
def p_IF_THEN(p):
    "IF : SE LPAREN exprRel RPAREN ENTAO Codigo FIM_COND PONTOVIRGULA"
    p[0] = f"{p[3]}JZ l{parser.labels}\n{p[6]}l{parser.labels}: NOP\n"
    parser.labels += 1
    parser.linhaDeCodigo+=1


# Controlo de fluxo (if then else)
def p_IF_THEN_ELSE(p):
    "IF : SE LPAREN exprRel RPAREN ENTAO Codigo SENAO Codigo FIM_COND PONTOVIRGULA"
    p[0] = f"{p[3]}JZ l{parser.labels}\n{p[6]}JUMP l{parser.labels}f\nl{parser.labels}: NOP\n{p[8]}l{parser.labels}f: NOP\n"
    parser.labels += 1
    parser.linhaDeCodigo+=1


# Ciclo (while)
def p_WHILE(p):
    "WHILE : ENQUANTO LPAREN exprRel RPAREN FAZ Codigo FIM_ENQUANTO PONTOVIRGULA"
    p[0] = f'l{parser.labels}c: NOP\n{p[3]}JZ l{parser.labels}f\n{p[6]}JUMP l{parser.labels}c\nl{parser.labels}f: NOP\n'
    parser.labels += 1
    parser.linhaDeCodigo+=1


def p_PRINTAR_ID(p):
    '''PRINTAR : IMPRIMIR LPAREN FRASE RPAREN PONTOVIRGULA'''
    p[0] = f'PUSHS {p[3]}\nWRITES\n'
    parser.linhaDeCodigo+=1

def p_PRINTAR_var(p):
    '''PRINTAR : IMPRIMIR LPAREN ID RPAREN PONTOVIRGULA'''
    #p[0] = f'PUSHS {p[3]}\nWRITEI\n'
    #print(parser.variaveis)
    #print(p[3])
    p[0] = f'PUSHG {parser.variaveis[p[3]][0]}\nWRITEI\n'
    parser.linhaDeCodigo+=1


def p_COMENTARIO(p):
    '''COMENTARIO : COMENTADO'''
    p[0] = "NOP\n"


## ------------------------ matrizes
# Declara matriz com tamanho INT INT
def p_DeclMatriz(p):
    #"Decl : MATRIZ ID INT INT"
    "Decl : MATRIZ INT NUM NUM VIRGULA ID" # matriz int 3 2, mat;
    listName = p[6]
    size = int(p[3])
    size1 = int(p[4])
    if listName not in parser.variaveis:
        parser.variaveis[listName] = (parser.stackPointer, size, size1)
        p[0] = f"PUSHN {size*size1}\n"
        parser.stackPointer += size*size1
    else:
        parser.error = (
            f"Variável com o nome {listName} já definida anteriormente.")
        parser.exito = False
    parser.linhaDeCodigo +=1


# Função que altera o valor de um indice da matriz por outro
def p_AtribMatriz_comExpr(p):
    #"Atrib : ALTERNA ID ABREPR expr FECHAPR ABREPR expr FECHAPR COM expr"
    "Atrib : ALTERA ID LPAREN_RETO expr RPAREN_RETO LPAREN_RETO expr RPAREN_RETO IGUAL expr PONTOVIRGULA" # altera mat[0][1] = 2;
    matName = p[2]
    indice1 = p[4]
    indice2 = p[7]
    valor = p[10]
    if matName in parser.variaveis:
        if len(parser.variaveis[matName]) == 3:
            p[0] = f"PUSHGP\nPUSHI {parser.variaveis[matName][0]}\nPADD\n{indice1}PUSHI {parser.variaveis[matName][2]}\nMUL\nPADD\n{indice2}{valor}STOREN\n"
        else:
            parser.error = f"Operação inválida, variável {matName} não é uma matriz"
            parser.exito = False
    else:
        parser.error = f"Variável não declarada anteriormente"
        parser.exito = False
    parser.linhaDeCodigo +=1


# Função que altera uma lista da matriz por outra
def p_AtribMatriz_comLista(p):
    #"Atrib : ALTERNA ID ABREPR expr FECHAPR COM lista"
    "Atrib : ALTERA ID LPAREN_RETO expr RPAREN_RETO IGUAL LISTA"
    matName = p[2]
    if matName in parser.variaveis:
        if len(parser.variaveis[matName]) == 3:
            if len(p[7]) <= parser.variaveis[matName][2]:
                assm = ""
                j = 0
                for i in p[7]:
                    assm += f'''PUSHGP\nPUSHI {parser.variaveis[matName][0]}\nPADD\n{p[4]}PUSHI {parser.variaveis[matName][2]}\nMUL\nPADD\nPUSHI {j}\nPUSHI {i}\nSTOREN\n'''
                    j += 1
                p[0] = f'{assm}'
            else:
                parser.error = f"Tamanho da lista maior do que o alocado"
                parser.exito = False
        else:
            parser.error = f"Operação inválida, variável {matName} não é uma matriz"
            parser.exito = False
    else:
        parser.error = f"Variável não declarada anteriormente"
        parser.exito = False
    parser.linhaDeCodigo +=1


# Função que vai buscar o valor do indice na matriz
def p_AtribBusca_Matriz(p):
    #"expr : BUSCA ID ABREPR expr FECHAPR ABREPR expr FECHAPR"
    "expr : ID LPAREN_RETO expr RPAREN_RETO LPAREN_RETO expr RPAREN_RETO"
    varName = p[1]
    indice1 = p[3]
    indice2 = p[6]
    if varName in parser.variaveis:
        p[0] = f"PUSHGP\nPUSHI {parser.variaveis[varName][0]}\nPADD\n{indice1}PUSHI {parser.variaveis[varName][2]}\nMUL\nPADD\n{indice2}LOADN\n"
    else:
        parser.error = f"Variável com o nome {varName} não definida"
        parser.exito = False
    parser.linhaDeCodigo +=1


def p_error(p):
    print(f"Erro de sintaxe na entrada: {p.value}")


# ----------------------------------------

parser = yacc.yacc()
parser.exito = True
parser.error = ""
parser.assembly = ""
parser.variaveis = {}
parser.stackPointer = 0
parser.linhaDeCodigo = 0
parser.labels = 0

assembly = ""


if len(sys.argv) == 2:
    inputFileName = sys.argv[1]
    if inputFileName[-4:] == ".plc":
        file = open(inputFileName, "r")
        content = file.read()
        parser.parse(content)
        if parser.exito:
            assembly += parser.assembly
            print(parser.variaveis)
        else:
            print("--------------------------------------")
            print(parser.error)
            print(parser.variaveis)
            print("--------------------------------------")
            sys.exit()
        file.close()
        outputFileName = "a.vm"

        # Verifica se o arquivo de saída já existe e o remove antes de criar um novo
        if os.path.exists(outputFileName):
            os.remove(outputFileName)

        outputFile = open(outputFileName, "w")
        outputFile.write(assembly)
        outputFile.close()

        print("File saved successfully")

    else:
        print("Invalid file extension")
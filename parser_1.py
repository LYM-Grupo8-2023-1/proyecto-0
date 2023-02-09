import nltk as tk
from inspect import currentframe, getframeinfo


#definicion de componentes
comandos = ['M','R','C','B','c','b','P','J','G']
keywords = ['ROBOT_R','VARS','PROCS']
instrucciones = ['assignTo','goto','move','turn','face','put','pick','moveToThe','moveInDir','jumpToThe','jumpInDir','nop']
control = ['if','then','else','while','do','repeat']
condiciones = ['facing','canPut','canPick','canMoveInDir','canJumpInDir','canMoveToThe','canJumpToThe','not']
direcciones1 = ['front','right','left','back']
direcciones2 = ['right','left','around']
card = ['north','east','west','south']

#Se inicia asumiendo que se tiene una sintaxis correcta
correcto = True

def main():
    filename = 'archivoPrueba1.txt'
    file = open(filename).read()
    tokens = tk.word_tokenize(file,"",True)
    parser(tokens)

def identificadorDeSyntax(palabra, lista):
    count=0
    for each in lista:
        if palabra == each:
            count+=1

    if count == 1:
        return True
    else:
        return False


def syntaxError(frameinfo):
    print("Error de sintaxis detectado: ", frameinfo.lineno)
    exit()
    
def comprobarVARS(tokens: list, posLista: int, correcto: bool):
    fin = False
    while correcto == True and fin == False:
        if tokens[posLista] == ";":
            fin = True
            posLista += 1
            break
        if posLista % 2 == 0:
            correcto = tokens[posLista].isalnum()
        if posLista % 2 == 1 and tokens[posLista] != ",":
            correcto = False 
        posLista += 1
    return correcto, posLista

def comprobarPROCS(tokens: list, posLista: int, correcto: bool):
    return correcto, posLista

def inKeywords(tokens:list, keywords:list):
    correcto = True
    if tokens[0] != keywords[0]:
        correcto = False
    
    cont = 1   
    if correcto == True and tokens[cont] == keywords[1]:
        cont += 1
        correcto, cont = comprobarVARS(tokens, cont, correcto)
        
        if correcto == True and tokens[cont] == keywords[2]:
            cont += 1
            correcto, cont = comprobarPROCS(tokens, cont, correcto)
            
    if correcto == True and tokens[cont] == keywords[2]:
        cont += 1
        correcto, cont = comprobarPROCS(tokens, cont, correcto)
        
    return correcto, cont
    
    
        
        
def parser(tokens:list):
    print(tokens)
    correcto, cont = inKeywords(tokens, keywords)
    print(correcto)
    print(cont)
        

main()
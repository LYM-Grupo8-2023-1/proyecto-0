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

#Diccionario donde se guardaran las funciones del PROCS
funciones = {}

#Lista donde se guardaran las variables
variables = []

#Lista donde se guardaran las direcciones1
direcciones1 = []

#Lista donde se guardaran las direcciones2
direcciones2 = []


#Lista donde se guardaran las cardinalidades
cards = []

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
            variables.append(tokens[posLista])

        if posLista % 2 == 1 and tokens[posLista] != ",":
            correcto = False

        posLista += 1

    return correcto, posLista

def verificarParametros(tokens: list, posLista: int, correcto: bool, llaveDict: str):
    fin = False
    variablesTemporal = []
    for var in variables:
        variablesTemporal.append(var)
    if "|" not in tokens[posLista] and correcto == False:
        correcto = False
    else:
        x = tokens[posLista]
        if len(tokens[posLista]) > 1:
            if tokens[posLista][1:].isalnum():
                funciones[llaveDict].append(tokens[posLista][1:])
                variablesTemporal.append(tokens[posLista][1:])
                posLista += 1
            else:
                correcto = False
        else:
            posLista += 1
        while correcto == True and fin == False:
            x = tokens[posLista]
            if tokens[posLista] == ",":
                posLista += 1
            elif "|" not in tokens[posLista]:
                if tokens[posLista].isalnum():
                    funciones[llaveDict].append(tokens[posLista])
                    variablesTemporal.append(tokens[posLista])
                    posLista += 1
                else:
                    correcto = False
            else:
                fin = True
                if len(tokens[posLista]) > 1:
                    if tokens[posLista][:-1].isalnum():
                        funciones[llaveDict].append(tokens[posLista][:-1])
                        variablesTemporal.append(tokens[posLista][:-1])
                        posLista += 1
                    else:
                        correcto = False
                else:
                    posLista += 1
    return correcto, posLista, variablesTemporal


def comprobarPROCS(tokens: list, posLista: int, correcto: bool):
    fin = False
    if tokens[posLista] == "[":
        correcto = False
    while correcto == True and fin == False:
        if tokens[posLista].isalnum():
            llaveDict = tokens[posLista]
            llaveDict = llaveDict.lower()
            funciones[llaveDict] = []
            posLista += 1
            if tokens[posLista] != "[":
                correcto = False
                break
            posLista += 1
            correcto, posLista, variablesTemporal = verificarParametros(tokens, posLista, correcto, llaveDict)
            fin2 = False
            while correcto and fin2 == False:
                x = tokens[posLista]
                for ins in instrucciones:
                    if tokens[posLista] == ins and correcto:
                        correcto, posLista, fin2 = verificarComandos(tokens, posLista, instrucciones, correcto, variablesTemporal, fin2)
                if tokens[posLista] == "if" and correcto:
                    posLista += 1
                    if tokens[posLista] == ":":    
                        verificarCondicional()
                    else:
                        correcto = False
                elif tokens[posLista] == "while" and correcto:
                    posLista += 1
                    if tokens[posLista] == ":":    
                        verificarLoop()
                    else:
                        correcto = False
                elif tokens[posLista] == "repeat" and correcto:
                    posLista += 1
                    if tokens[posLista] == ":":    
                        verificarRepeat()
                    else:
                        correcto = False
                if tokens[posLista] == "]":
                    posLista += 1
                    fin2 = True
            if tokens[posLista] == "[":
                fin = True
                posLista += 1
        else:
            correcto = False
        
    return correcto, posLista

def verificarComandos(tokens: list, posLista: int, instrucciones: list, correcto: bool, variablesTemporal: list, fin2: bool):
    instruccion = tokens[posLista]
    if instruccion == instrucciones[0]:
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, fin2 = verificarAssingTo(tokens, posLista, correcto, variablesTemporal, fin2)
        else:
            correcto = False
    elif instruccion == instrucciones[1]:
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, fin2 = verificarGoTo(tokens, posLista, correcto, variablesTemporal, fin2)
        else:
            correcto = False
    elif instruccion == instrucciones[2]:
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, fin2 = verificarMove(tokens, posLista, correcto, variablesTemporal, fin2)
        else:
            correcto = False
    elif instruccion == instrucciones[3]:
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, fin2 = verificarTurn(tokens, posLista, correcto, direcciones2, fin2)
        else:
            correcto = False
    elif instruccion == instrucciones[4]:
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, fin2 = verificarFace(tokens, posLista, correcto, cards, fin2)
        else:
            correcto = False
    elif instruccion == instrucciones[5] or instruccion == instrucciones[6]:
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, fin2 = verificarPutPick(tokens, posLista, correcto, variablesTemporal, fin2)
        else:
            correcto = False
    elif instruccion == instrucciones[7] or instruccion == instrucciones[9]:
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, fin2 = verificarMoveToTheJumpToThe(tokens, posLista, correcto, variablesTemporal, direcciones1, fin2)
        else:
            correcto = False
    elif instruccion == instrucciones[8] or instruccion == instrucciones[10]:
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, fin2 = verificarMoveInDirJumpInDir(tokens, posLista, correcto, variablesTemporal, cards, fin2)
        else:
            correcto = False
    elif instruccion == instrucciones[11]:
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
        else:
            correcto = False
    return correcto, posLista, fin2
            
def verificarCondicional():
    pass #Arreglar como saber que condicion usar

def verificarLoop():
    pass #Arreglar como saber que condicion usar

def verificarRepeat():
    pass #Arreglar como saber que condicion usar

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
    
def verificarAssingTo(tokens:list, posicion: int, correcto: bool, variables: list, fin2: bool):
    
    if tokens[posicion].isdigit():
        posicion += 1
        if tokens[posicion] == ",":
            posicion += 1
            for i in variables:
                if tokens[posicion] == i:
                    posicion += 1
                    correcto = True
                    break
                else:
                    correcto = False
            if tokens[posicion] == ";":
                posicion += 1
            elif tokens[posicion] == "]":
                posicion += 1
                fin2 = True
            else:
                correcto = False
        else:
            correcto = False
    else:
        correcto = False
    return correcto, posicion, fin2

def verificarGoTo(tokens:list, posicion: int, correcto: bool, variables: list, fin2: bool):

    inVariable = False
    for i in variables:
        if tokens[posicion] == i:
            inVariable = True
            break

    if tokens[posicion].isdigit() or inVariable:
        posicion += 1
        if tokens[posicion] == ",":
            posicion += 1
            inVariable2 = False
            for i in variables:
                if tokens[posicion] == i:
                    inVariable2 = True
                    break
            if tokens[posicion].isdigit() or inVariable2:
                posicion += 1
            else:
                correcto = False
            if tokens[posicion] == ";":
                posicion += 1
            elif tokens[posicion] == "]":
                posicion += 1
                fin2 = True
            else:
                correcto = False
        else:
            correcto = False
    else:
        correcto = False

    return correcto, posicion, fin2


def verificarMove(tokens:list, posicion: int, correcto: bool, variables: list, fin2: bool):

    inVariable = False
    for i in variables:
        if tokens[posicion] == i:
            inVariable = True
            break

    if tokens[posicion].isdigit() or inVariable:
        posicion += 1

    else:
        correcto = False
    
    if tokens[posicion] == ";":
        posicion += 1
    elif tokens[posicion] == "]":
        posicion += 1
        fin2 = True
    else:
        correcto = False

    return correcto, posicion, fin2

def verificarTurn(tokens:list, posicion: int, correcto: bool, direcciones2: list, fin2: bool):

    inDireccion2 = False
    for i in direcciones2:
        if tokens[posicion] == i:
            inDireccion2 = True
            break

    if inDireccion2:
        posicion += 1

    else:
        correcto = False

    return correcto, posicion, fin2

def verificarFace(tokens:list, posicion: int, correcto: bool, cards: list, fin2: bool):

    cardinalidad = False
    for i in cards:
        if tokens[posicion] == i:
            cardinalidad = True
            break

    if cardinalidad:
        posicion += 1

    else:
        correcto = False
    
    if tokens[posicion] == ";":
        posicion += 1
    elif tokens[posicion] == "]":
        posicion += 1
        fin2 = True
    else:
        correcto = False

    return correcto, posicion, fin2

def verificarPutPick(tokens:list, posicion: int, correcto: bool, variables: list, fin2: bool):

    inVariable = False
    for i in variables:
        if tokens[posicion] == i:
            inVariable = True
            break

    if tokens[posicion].isdigit() or inVariable:
        posicion += 1
        if tokens[posicion] == ",":
            posicion += 1
            if tokens[posicion].lower() == "ballons" or tokens[posicion].lower() == "chips":
                posicion += 1
            else:
                correcto = False
            if tokens[posicion] == ";":
                posicion += 1
            elif tokens[posicion] == "]":
                posicion += 1
                fin2 = True
            else:
                correcto = False
        else:
            correcto = False
    else:
        correcto = False

    return correcto, posicion, fin2

def verificarMoveToTheJumpToThe(tokens:list, posicion: int, correcto: bool, variables: list, direcciones1: list, fin2: bool):
    inVariable = False
    for i in variables:
        if tokens[posicion] == i:
            inVariable = True
            break
    
    if tokens[posicion].isdigit() or inVariable:
        posicion += 1
        if tokens[posicion] == ",":
            posicion += 1
            for i in direcciones1:
                if tokens[posicion] == i:
                    posicion += 1
                    correcto = True
                    break
                else:
                    correcto = False
            if tokens[posicion] == ";":
                posicion += 1
            elif tokens[posicion] == "]":
                posicion += 1
                fin2 = True
            else:
                correcto = False
        else:
            correcto = False
    else:
        correcto = False

    return correcto, posicion, fin2
    

def verificarMoveInDirJumpInDir(tokens:list, posicion: int, correcto: bool, variables: list, cards: list, fin2: bool):
    
    inVariable = False
    for i in variables:
        if tokens[posicion] == i:
            inVariable = True
            break

    if tokens[posicion].isdigit() or inVariable:
        posicion += 1
        if tokens[posicion] == ",":
            posicion += 1
            for i in cards:
                if tokens[posicion] == i:
                    posicion += 1
                    correcto = True
                    break
                else:
                    correcto = False
            if tokens[posicion] == ";":
                posicion += 1
            elif tokens[posicion] == "]":
                posicion += 1
                fin2 = True
            else:
                correcto = False
        else:
            correcto = False
    else:
        correcto = False

    return correcto, posicion, fin2   
        


def parser(tokens:list):
    print(tokens)
    correcto, cont = inKeywords(tokens, keywords)
    print(correcto)
    print(cont)
        

main()
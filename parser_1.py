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
            tuVieja = False
            while correcto and tuVieja == False:
                for ins in instrucciones:
                    if tokens[posLista] == ins and correcto:
                        correcto, posLista, tuVieja = verificarComandos(tokens, posLista, instrucciones, correcto, variablesTemporal, tuVieja)
                if tokens[posLista] == "if" and correcto:
                    posLista += 1
                    if tokens[posLista] == ":":
                        posLista += 1    
                        correcto, posLista, tuVieja = verificarCondicional(tokens, posLista, variablesTemporal, correcto, tuVieja)
                    else:
                        correcto = False
                elif tokens[posLista] == "while" and correcto:
                    posLista += 1
                    if tokens[posLista] == ":":
                        posLista += 1    
                        correcto, posLista, tuVieja = verificarLoop(tokens, posLista, variablesTemporal, correcto, tuVieja)
                    else:
                        correcto = False
                elif tokens[posLista] == "repeat" and correcto:
                    posLista += 1
                    if tokens[posLista] == ":":
                        posLista += 1    
                        correcto, posLista, tuVieja = verificarRepeat(tokens, posLista, variablesTemporal, correcto, tuVieja)
                    else:
                        correcto = False
                if tokens[posLista] == "]":
                    posLista += 1
                    tuVieja = True
            if tokens[posLista] == "[":
                fin = True
                posLista += 1
        else:
            correcto = False
        
    return correcto, posLista

def verificarComandos(tokens: list, posLista: int, instrucciones: list, correcto: bool, variablesTemporal: list, tuVieja: bool):
    instruccion = tokens[posLista].lower()
    if instruccion == instrucciones[0].lower():
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, tuVieja = verificarAssingTo(tokens, posLista, correcto, variablesTemporal, tuVieja)
        else:
            correcto = False
    elif instruccion == instrucciones[1].lower():
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, tuVieja = verificarGoTo(tokens, posLista, correcto, variablesTemporal, tuVieja)
        else:
            correcto = False
    elif instruccion == instrucciones[2].lower():
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, tuVieja = verificarMove(tokens, posLista, correcto, variablesTemporal, tuVieja)
        else:
            correcto = False
    elif instruccion == instrucciones[3].lower():
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, tuVieja = verificarTurn(tokens, posLista, correcto, direcciones2, tuVieja)
        else:
            correcto = False
    elif instruccion == instrucciones[4].lower():
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, tuVieja = verificarFace(tokens, posLista, correcto, cards, tuVieja, True)
        else:
            correcto = False
    elif instruccion == instrucciones[5].lower() or instruccion == instrucciones[6].lower():
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, tuVieja = verificarPutPick(tokens, posLista, correcto, variablesTemporal, tuVieja, True)
        else:
            correcto = False
    elif instruccion == instrucciones[7].lower() or instruccion == instrucciones[9].lower():
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, tuVieja = verificarMoveToTheJumpToThe(tokens, posLista, correcto, variablesTemporal, direcciones1, tuVieja)
        else:
            correcto = False
    elif instruccion == instrucciones[8].lower() or instruccion == instrucciones[10].lower():
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, tuVieja = verificarMoveInDirJumpInDir(tokens, posLista, correcto, variablesTemporal, tuVieja, True)
        else:
            correcto = False
    elif instruccion == instrucciones[11].lower():
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1 
            if tokens[posLista] == ";":
                posLista += 1
            elif tokens[posLista] == "]":
                posLista += 1
                tuVieja = True
            else:
                correcto = False 
        else:
            correcto = False
    return correcto, posLista, tuVieja
            
def verificarCondicional(tokens: list, posLista: int, variables:list, correcto: bool, tuVieja: bool):
    for cond in condiciones:
        if tokens[posLista] == cond:
           correcto, posLista, tuVieja = verificarCondiciones(tokens, posLista, condiciones, correcto, variables, tuVieja)
           break
        else:
            correcto = False
    if tokens[posLista] == "then" and tokens[posLista+1] == ":":
        posLista += 2
        correcto, posLista, tuVieja = verificarBloque(tokens, posLista, variables, correcto, tuVieja, instrucciones)
        if correcto and tokens[posLista] == "else" and tokens[posLista+1] == ":":
            posLista += 2
            correcto, posLista, tuVieja = verificarBloque(tokens, posLista, variables, correcto, tuVieja, instrucciones)
        else:
            correcto = False
    else:
        correcto = False
    return correcto, posLista, tuVieja

def verificarBloque(tokens: list, posLista: int, variables:list, correcto: bool, tuVieja: bool, instrucciones: list):
    if tokens[posLista] == "[":
        posLista += 1
        for ins in instrucciones:
            if tokens[posLista].lower() == ins.lower() and correcto:
                correcto, posLista, tuVieja = verificarComandos(tokens, posLista, instrucciones, correcto, variables, tuVieja)
                break
        if tuVieja == True:
            tuVieja = False
        else:
            correcto = False
    else:
        correcto = False 
    return correcto, posLista, tuVieja

def verificarCondiciones(tokens: list, posLista: int, condiciones: list, correcto: bool, variablesTemporal: list, tuVieja: bool):
    condicion = tokens[posLista].lower()
    if condicion == condiciones[0].lower():
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, tuVieja = verificarFace(tokens, posLista, correcto, cards, variables, tuVieja, False)
        else:
            correcto = False
    elif condicion == condiciones[1].lower() or condicion == condiciones[2].lower():
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, tuVieja = verificarPutPick(tokens, posLista, correcto, variables, tuVieja, False)
        else:
            correcto = False
    elif condicion == condiciones[3].lower() or condicion == condiciones[4].lower():
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, tuVieja = verificarMoveInDirJumpInDir(tokens, posLista, correcto, variables, tuVieja, False)
        else:
            correcto = False
    elif condicion == condiciones[5].lower() or condicion == condiciones[6].lower():
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1    
            correcto, posLista, tuVieja = verificarMoveToTheJumpToThe(tokens, posLista, correcto, variables, direcciones1, tuVieja, False)
        else:
            correcto = False
    elif condicion == condiciones[7].lower():
        posLista += 1
        if tokens[posLista] == ":":
            posLista += 1
            correcto, posLista, tuVieja = verificarCondiciones(tokens, posLista, condiciones, correcto, variables, tuVieja)
        else:
            correcto = False
    return correcto, posLista, tuVieja

def verificarLoop(tokens: list, posLista: int, variables:list, correcto: bool, tuVieja: bool):
    for cond in condiciones:
        if tokens[posLista].lower() == cond.lower():
            correcto = True
            correcto, posLista, tuVieja = verificarCondiciones(tokens, posLista, condiciones, correcto, variables, tuVieja)
            posLista += 1
            break
        else:
            correcto = False
    if tokens[posLista] == "do" and tokens[posLista+1] == ":":
        posLista += 2
        correcto, posLista, tuVieja = verificarBloque(tokens, posLista, variables, correcto, tuVieja, instrucciones)
    else:
        correcto = False
    return correcto, posLista, tuVieja

def verificarRepeat(tokens: list, posLista: int, variables:list, correcto: bool, tuVieja: bool):
    if tokens[posLista].isdigit():
        posLista += 1
        correcto, posLista, tuVieja = verificarBloque(tokens, posLista, variables, correcto, tuVieja, instrucciones)
    else:
        correcto = False
    return correcto, posLista, tuVieja

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
    
def verificarAssingTo(tokens:list, posicion: int, correcto: bool, variables: list, tuVieja: bool):
    
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
                tuVieja = True
            else:
                correcto = False
        else:
            correcto = False
    else:
        correcto = False
    return correcto, posicion, tuVieja

def verificarGoTo(tokens:list, posicion: int, correcto: bool, variables: list, tuVieja: bool):

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
                tuVieja = True
            else:
                correcto = False
        else:
            correcto = False
    else:
        correcto = False

    return correcto, posicion, tuVieja


def verificarMove(tokens:list, posicion: int, correcto: bool, variables: list, tuVieja: bool):

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
        tuVieja = True
    else:
        correcto = False

    return correcto, posicion, tuVieja

def verificarTurn(tokens:list, posicion: int, correcto: bool, direcciones2: list, tuVieja: bool):

    inDireccion2 = False
    for i in direcciones2:
        if tokens[posicion] == i:
            inDireccion2 = True
            break

    if inDireccion2:
        posicion += 1

    else:
        correcto = False

    return correcto, posicion, tuVieja

def verificarFace(tokens:list, posicion: int, correcto: bool, cards: list, tuVieja: bool, isInstruccion: bool):

    cardinalidad = False
    for i in cards:
        if tokens[posicion] == i:
            cardinalidad = True
            break

    if cardinalidad:
        posicion += 1

    else:
        correcto = False
    
    if isInstruccion:
        if tokens[posicion] == ";":
            posicion += 1
        elif tokens[posicion] == "]":
            posicion += 1
            tuVieja = True
        else:
            correcto = False

    return correcto, posicion, tuVieja

def verificarPutPick(tokens:list, posicion: int, correcto: bool, variables: list, tuVieja: bool, isInstruccion: bool):

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
            if isInstruccion:
                if tokens[posicion] == ";":
                    posicion += 1
                elif tokens[posicion] == "]":
                    posicion += 1
                    tuVieja = True
                else:
                    correcto = False
        else:
            correcto = False
    else:
        correcto = False

    return correcto, posicion, tuVieja

def verificarMoveToTheJumpToThe(tokens:list, posicion: int, correcto: bool, variables: list, direcciones1: list, tuVieja: bool, isInstruccion: bool):
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
            if isInstruccion:
                if tokens[posicion] == ";":
                    posicion += 1
                elif tokens[posicion] == "]":
                    posicion += 1
                    tuVieja = True
                else:
                    correcto = False
        else:
            correcto = False
    else:
        correcto = False

    return correcto, posicion, tuVieja
    

def verificarMoveInDirJumpInDir(tokens:list, posicion: int, correcto: bool, variables: list, tuVieja: bool, isInstruccion: bool):
    
    inVariable = False
    for i in variables:
        if tokens[posicion] == i:
            inVariable = True
            break

    if tokens[posicion].isdigit() or inVariable:
        posicion += 1
        if tokens[posicion] == ",":
            posicion += 1
            for cardinal in card:
                if tokens[posicion] == cardinal:
                    posicion += 1
                    correcto = True
                    break
                else:
                    correcto = False
            if isInstruccion:
                if tokens[posicion] == ";":
                    posicion += 1
                elif tokens[posicion] == "]":
                    posicion += 1
                    tuVieja = True
                else:
                    correcto = False
        else:
            correcto = False
    else:
        correcto = False

    return correcto, posicion, tuVieja   
        
def verificarFunciones(tokens: list, posLista: int, funciones: dict, funcionActual: str, correcto: bool, variables: list, finfinal: bool):
    cantidadParametros = len(funciones[funcionActual])
    j = 0
    while j < cantidadParametros and correcto and finfinal == False:
        inVariable = False
        for i in variables:
            if tokens[posLista] == i:
                inVariable = True
                break

        if tokens[posLista].isdigit() or inVariable:
            posLista += 1
            j += 1
            if tokens[posLista] == ",":
                posLista += 1
            elif tokens[posLista] == "]":
                finfinal = True
        else:
            correcto = False
    return correcto, posLista, finfinal

def parser(tokens:list):
    print(tokens)
    correcto, cont = inKeywords(tokens, keywords)
    finfinal = False
    while finfinal == False and correcto:
        for ins in instrucciones:
            if tokens[cont].lower() == ins.lower():
                correcto, cont, finfinal = verificarComandos(tokens, cont, instrucciones, correcto, variables, finfinal)
        for funct in funciones.keys():
            x = tokens[cont]
            if tokens[cont].lower() == funct.lower():
                cont += 1
                if tokens[cont] == ":":
                    cont += 1
                    correcto, cont, finfinal = verificarFunciones(tokens, cont, funciones, funct, correcto, variables, finfinal)
                else:
                    correcto = False
    if correcto:
        print("Su sintaxis es correcta")
    else:
        print("Su sintaxis es incorrecta, porfavor revise de nuevo")
        

main()
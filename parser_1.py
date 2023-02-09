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


def parser(tokens):
    return true

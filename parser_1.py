#definicion de componentes
comandos = ["M","R","C","B","c","b","P","J","G"] 
instrucciones = ["assignTo", "goto", "move", "turn", "face", "put", "pick", "moveToThe", "moveInDir", "jumpToThe", "jumpInDir", "nop", "PROCS"]
condiciones = ["facing", "canPut", "canPick","canMoveInDir", "canJumpInDir", "canMoveToThe", "canJumpToThe", "not"]
funcionesCondicionales = ["while", "do", "if", "od", "fi", "else"]
direcciones = ["left","right","front","back"]

def main():
    filename = 'archivoPrueba1.txt'
    file = open(filename).read()
    tokens = tk.word_tokenize(file,"",True)
    parser(tokens)


#def parser(tokens):
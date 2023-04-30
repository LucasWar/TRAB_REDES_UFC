import random
import socket
import string

def generatorString(sizeString):
    random.randint(0,51)
    letras = string.ascii_letters
    stringFinal = ""
    for i in range(sizeString):
        stringFinal += letras[random.randint(0,51)]
    return stringFinal

def connecClientTCP():
    HORST ='localhost'
    PORT = 5000
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HORST,PORT))
    s.listen()
    conn, andress = s.accept()
    return conn, andress

while True:
    print("Aguardando conexão...")
    conn, adress = connecClientTCP()
    print("Conectado com cliente: ",adress)
    print("Aguardando mensagem do cliente")
    data = conn.recv(1024)
    print("Mensagem recebida: "+data.decode())
    print("Processando...")
    print("Valor recebido"+data.decode())
    if len(str(data.decode())) < 10:
        if(int(data.decode()) % 2 == 0):
            conn.sendall(str.encode("PAR"))
        else:
            conn.sendall(str.encode("IMPAR"))
    else:
        frase = generatorString(len(data.decode()))
        conn.sendall(str.encode(frase))
    print("Fim do processo")
    conn.close()
# if data.decode() == "sair":
#     print("Fechar conexão")
#     conn.close()
#     break
# else:
#     print("Cliente enviou: ",data.decode())
#     mensagem = input("Digite mensagem para cliente: ")
#     conn.sendall(str.encode(mensagem))

# conn.sendall(data)
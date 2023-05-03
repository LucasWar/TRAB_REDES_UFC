import random
import socket
import sys
import time


def connectTCP():
    HORST ='localhost'
    PORT = 5000
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((HORST,PORT))
    return s

def generatorNumber():
        numbers = ['0','1','2','3','4','5','6','7','8','9']
        number = ""
        sizeNumber = random.randint(1,30)
        for i in range(sizeNumber):
            number = random.choice(numbers) + number
        return number


while True:
    print(" ")
    print("Aguardando conexão...")
    conn = connectTCP()
    print("Conectado com servidor")
    number = str(generatorNumber())
    print("Valor enviado para o servidor: "+ number)
    conn.sendall(str.encode(number))
    print("Aguardando resposta...")
    data = conn.recv(1024)
    print("Resultado: "+data.decode()+" FIM")
    conn.close()
    for i in range(5, 0,-1):
        sys.stdout.write("\r Proxima request em: {0}s ".format(i))
        sys.stdout.flush()
        time.sleep(1)
        
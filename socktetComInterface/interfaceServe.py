import time
import PySimpleGUI as sg
import random
import socket
import string
import threading
import queue
from datetime import date

HOST = '127.0.0.1' #IP do servidor
PORT =  5000       #Porta em que o servidor vai esta rodando

cancel = False

sg.theme('Dark')

layout = [  [sg.Multiline(size=(60,25), key='servidor',disabled=True,text_color='green',background_color="black",font="Arial",autoscroll=True,no_scrollbar=True)],
            [sg.Button('Iniciar servidor',key='btnStartServ',disabled=False), sg.Button('Cancelar Conexão Servidor',key='btnCancelServ',disabled=True), sg.Button('Configurar servidor')]]



window = sg.Window('Controller Serve', layout)

def updateGUI(text, element):
    element.Update(text+"\n", append=True)
    
def generatorString(sizeString):
    random.randint(0,51)
    letras = string.ascii_letters
    stringFinal = ""
    for i in range(sizeString):
        stringFinal += letras[random.randint(0,51)]
    return stringFinal
def close(conn):
    conn.close()

def connecClientTCP(queue,host,port):
    global cancel
    while True:
        try:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Criação de uma variavel do tipo socket, socket.AF_INET indica endereços IP de 32 bits,socket.SOCK_STREAM e esse indica TCP/IP
            s.bind((host,port)) #Criação do servidor 
            s.listen()          #numero de clientes que ele irá aceitar
            s.settimeout(2)    #Indica o tempo limite que ele irá esperar para que alguma maquina se conecte a ele, no caso 2 segundos apos esse tempo caso naa aconteça dispara uma exeption
            conn, address = s.accept() #Espera ate que uma coneção seja realizada
            queue.put(conn) #Adincuina conn a fila 
            queue.put(address)#Adincuina address a fila 
            break
        except:
           if cancel:
                cancel = False
                break
def timeStop():
    while threading.active_count() > 2:
        time.sleep(3)

    window['Configurar servidor'].Update(disabled=False)
    window['btnStartServ'].Update(disabled=False)
    updateGUI("Servidor encerado", window['servidor'])

#Funcão para iniciar o servidor
def startServer():
    global cancel
    while True:   
        action = " "        # Variavel utlizada para sair do primeiro while
        q = queue.Queue()   # fila
        t = threading.Thread(target=connecClientTCP, args=(q,HOST,PORT))   #threding de configuração do servidor 
        t.start() # iniciar threding
        updateGUI("Aguardando conexão...", window['servidor']) #Mensagem de aguadaando conexão e mostrada na tela 
        while True:
            event, values = window.read(timeout=100)    # eventos e valores são lido da tela principal
            if event in (sg.WIN_CLOSED, 'Exit'): #Condicional para clique no icone de X da tela 
                break                            #sai do while
            if event == 'btnCancelServ':         # Caos evento na tela seja cancelar servidor função modifica valores da variveis e cancela a conexão com os clientes
                action = event
                cancel = True
                updateGUI("Servidor esta sendo encerrado", window['servidor'])
                updateGUI("Por favor aguarde alguns instantes", window['servidor'])
                updateGUI(" ", window['servidor'])
                break
            if not q.empty():   #Verifica se existe algo na fila se sim executa a operações deseja em cima o valor recebido do cliente 
                window['btnCancelServ'].Update(disabled=False)
                conn = q.get()      # Recebe a conexão do cliente
                andres = q.get()    # endereçõ do cliente
                updateGUI("Conectado com cliente: "+str(andres) , window['servidor'])
                updateGUI("Aguardando mensagem do cliente" , window['servidor'])
                data = conn.recv(1024) #Função para receber os dados, 1024 indica o número máximo de bytes que podem ser recebidos
                updateGUI("Mensagem recebida: "+data.decode() , window['servidor'])
                updateGUI("Processando...", window['servidor'])

                if len(str(data.decode())) < 10: # se seus caracteres forem meor que 10 retornara IMPAR ou PAR depedendo do valore recebido
                    updateGUI("Valor recebido tem menos de 10 caracteres", window['servidor'])
                    if(int(data.decode()) % 2 == 0):
                        conn.sendall(str.encode("PAR"))
                        updateGUI("Mensagem enviada: "+"PAR", window['servidor'])
                    else:
                        conn.sendall(str.encode("IMPAR"))
                        updateGUI("Mensagem enviada: " + "IMPAR", window['servidor'])
                else:   #Caso maior ou igual retorna uma string de mesmo tamanho
                    updateGUI("Valor recebido tem 10 ou mais caracteres", window['servidor'])
                    frase = generatorString(len(data.decode()))
                    updateGUI("Frase enviada: "+frase, window['servidor'])
                    conn.sendall(str.encode(frase))
                updateGUI("Fim processo", window['servidor'])
                updateGUI(" ", window['servidor'])
                conn.close() #Fecha a conexão com cliente
                break
        if action == 'btnCancelServ':
            
            break  
while True:
    
    event, values = window.read(timeout=100)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'btnStartServ':
        window['Configurar servidor'].Update(disabled=True)
        window['btnStartServ'].Update(disabled=True)
        startServer()
        window['btnCancelServ'].Update(disabled=True)
        t2 = threading.Thread(target=timeStop, args=())
        t2.start() 
        
        
       
    if event == 'Configurar servidor':
        layout2 = [[sg.Text("ID SERVIDOR: "),sg.Input(default_text=HOST,size=(10,3))],
                   [sg.Text("PORTA: "),sg.Column([],size=(28)),sg.Input(default_text=PORT,size=(10,3))],
                    [sg.Button("Confirmar")]]
        modal_window = sg.Window("Config",layout2,modal=True)
        while True:
            new_event, new_values = modal_window.read()
            if new_event in (sg.WIN_CLOSED, 'Exit'):
                break
            if new_event == "Confirmar":
                confirm_popup = sg.popup('Servidor configurado.', auto_close=True, auto_close_duration=2)
                HOST = new_values[0]
                PORT = int(new_values[1])
                modal_window.close()
                break
        

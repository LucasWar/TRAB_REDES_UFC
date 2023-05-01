import time
import PySimpleGUI as sg
import random
import socket
import threading
import queue
from datetime import date


#teste

HOST = '127.0.0.1'
PORT =  5000
tempo = 10
tempoText = str(tempo)



sg.theme('Dark')

layout = [  [sg.Multiline(size=(35,25), key='servidor',disabled=True,text_color='green',background_color="black",font="Arial",autoscroll=True,no_scrollbar=True),sg.Text(tempoText,key="time",font=("Arial",40),background_color='black',text_color='green')],
            [sg.Button('Iniciar conexão com servidor',key='btnStartServ',disabled=False), sg.Button('Cancelar Conexão Servidor',key='btnCancelServ',disabled=True),sg.Push(),sg.Button("Config",disabled=False)]]

cancel_connection = False

window = sg.Window('Controller Client', layout)

def updateGUI(teste, element, last_line=None):
    element.Update(teste+"\n", append=True)
    
    
def connectTCP(queue,host,port):
        conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        conn.connect((host,port))
        queue.put(conn)
            
def generatorNumber():
        numbers = ['0','1','2','3','4','5','6','7','8','9']
        number = ""
        sizeNumber = random.randint(1,30)
        for i in range(sizeNumber):
            number = random.choice(numbers) + number
        return number

def startServer():
    while not cancel_connection:
        updateGUI("Aguardando conexão...",window['servidor'])
        q = queue.Queue()
        t = threading.Thread(target=connectTCP, args=(q,HOST,PORT))
        t.start()
        t.join()
        if not q.empty():
            conn = q.get()  # aguarda até que um item esteja disponível na fila
            updateGUI("Conexão realizada",window['servidor'])
            number = str(generatorNumber())
            updateGUI("Valor enviado para o servdor: "+ number,window['servidor'])
            conn.sendall(str.encode(number))
            updateGUI("Aguardando resposta", window['servidor'])
            data = conn.recv(1024)
            if data != b"":
                updateGUI("Resultado:"+data.decode()+" FIM", window['servidor'])       
            updateGUI("Conexão encerrada", window['servidor'])
            updateGUI(" ", window['servidor'])
            conn.close()
            for i in range(tempo, 0,-1):
                if Cancel:
                    break
                if(i < 10):
                    window['time'].Update("0"+str(i))
                else:
                    window['time'].Update(str(i))
                time.sleep(1)
        else:
            break
def repeat_start_server():
    startServer()


# define o evento do botão
while True:
    event, values = window.read(timeout=100)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'btnStartServ':
        Cancel = False
        cancel_connection = False
        # desabilita o botão para evitar múltiplas threads
        window['btnStartServ'].Update(disabled=True)
        # inicia a thread
        threading.Thread(target=repeat_start_server, daemon=True).start()
        # habilita o botão novamente
        window['btnCancelServ'].Update(disabled=False) 
        window['Config'].Update(disabled=True) 
    elif event == 'btnCancelServ':
        Cancel = True
        cancel_connection = True
        window['btnStartServ'].Update(disabled=False)
        window['btnCancelServ'].Update(disabled=True) 
        window['Config'].Update(disabled=False) 
        updateGUI("Conexão encerrada",window['servidor'])

    if event == 'Config':
        layout2 = [[sg.Text("ID SERVIDOR: "),sg.Column([],size=(55)),sg.Input(default_text=HOST,size=(10,3))],
                   [sg.Text("PORTA: "),sg.Column([],size=(95)),sg.Input(default_text=PORT,size=(10,3))],
                   [sg.Text("TEMPO REQUEST: "),sg.Column([],size=(28)),sg.Input(default_text=tempo,size=(10,3))],
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
                tempo = int(new_values[2])
                modal_window.close()
                if tempo < 10:
                    tempoText = "0"+str(tempo)
                else:
                    tempoText = str(tempo)
                window['time'].Update(str(tempoText))
                break   

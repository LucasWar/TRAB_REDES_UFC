# TRAB_REDES_UFC
Este é um projeto que tem como finalidade mostra o funcionamento de um sockte e os conceitos de aplicação de cliente servidor.

COMO UTILIZAR:
1. Clone o repositorio na sua maquina com o seguinte comando: <br>
- <i>git clone https://github.com/LucasWar/TRAB_REDES_UFC<i/>

2. Acesse o diretorio do socket com interface:<br>
- <i>cd socketcominterface</i>

3.Execute ambom arquivos que estão na pasta:<br>
- <i>python interfaceServe.py</i>
- <i>python interfaceClient.py</i>

4. Instruções: 
<p>Apos a execução de ambos arquivos irá aparecer duas telas o Controller Serve e o Controler Client,ambas bem simples, após isso aerte no botão iniciar servidor do controler serve.</p>
<p>Com isso o servidor será inicializado,sera informado na tela, alem de algumas outras informações, como id do servidor e a porta em que ele esta rodando</p>
<p>Logo apos isso vá ate ao controler client e inicie conexão com o servidor.</p>
<p>Feito esses passos a troca de mensagens entre eles será exibida na tela de ambom onde as mensagens enviadas pelo cliente chegarão até o servidor e serão processadas e respondidas de acordo com regras estabelidas no trabalho</p>


DEPENDÊNCIAS<br>
-Bibliotecas nativas do python:<br>
  *Socket<br>
  *Queue<br>
  *Time<br>
  *random<br>
  *threading<br>
  *string<br>
-Bibliotecas que precisam de instalação<br>
  *PySimpleGui:<br> 
  <p>Abra a o prompt de comando e digite "pip install PySimpleGui" e a biblioteca será instalada</p>

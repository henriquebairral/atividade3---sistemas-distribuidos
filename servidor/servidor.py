import socket
import threading
import time
import cv2
import os

from protocolo import receber_mensagem, enviar_mensagem
from imagem import Imagem

def processar_imagem(img_obj):
    """
    Processa a imagem para detectar faces e desenhar retângulos.
    Não possui contato com a rede/sockets.
    """
    caminho_xml = os.path.join(os.path.relpath(
        cv2.__file__).replace('__init__.py', ''), 'data/haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(caminho_xml)
    
    matriz = img_obj.matriz
    
    gray = cv2.cvtColor(matriz, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(matriz, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    img_obj.matriz = matriz
    return img_obj


class Servidor():
    """
    Classe Servidor - Comunicação Concorrente
    """
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        """
        Inicia o servidor e o laço de aceitação de clientes.
        """
        endpoint = (self._host, self._port)
        try:
            self.__tcp.bind(endpoint)
            self.__tcp.listen(5)
            print(f"Servidor iniciado em {self._host}:{self._port}")
            
            while True:
                con, client = self.__tcp.accept()
                
                thread_cliente = threading.Thread(target=self._atender_cliente, args=(con, client))
                thread_cliente.start()
                
        except Exception as e:
            print("Erro ao inicializar o servidor:", e.args)

    def _atender_cliente(self, con, client):
        """
        Função executada dentro da Thread para atender um único cliente.
        """
        print(f"Iniciou - Cliente: {client}")
        
        # Pausa temporária para o Teste 3 (Remover na versão final)
        time.sleep(5) 
        
        try:
            dados_recebidos = receber_mensagem(con)
            
            if dados_recebidos:
                img_obj = Imagem.decodificar(dados_recebidos)
                img_processada = processar_imagem(img_obj)
                dados_resposta = img_processada.codificar()
                enviar_mensagem(con, dados_resposta)
                
        except Exception as e:
            print(f"Falha no atendimento ao cliente {client}: {e}")
        
        finally:
            con.close()
            print(f"Terminou - Cliente: {client}")
import socket
import cv2
import os

def processar_imagem(img_obj):
    """Processa a imagem para detectar faces isolado da rede."""
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
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        endpoint = (self._host, self._port)
        try:
            self.__tcp.bind(endpoint)
            self.__tcp.listen(5)
            print(f"Servidor iniciado em {self._host}:{self._port}")
            
            while True:
                con, client = self.__tcp.accept()
                self._atender_cliente(con, client)
                
        except Exception as e:
            print("Erro ao inicializar o servidor:", e.args)

    def _atender_cliente(self, con, client):
        print(f"Conectado a: {client}")
        con.close()
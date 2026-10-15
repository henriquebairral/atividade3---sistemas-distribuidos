
import socket
import sys
from pathlib import Path

import cv2

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ_PROJETO))

from utils.imagem import Imagem
from utils.protocolo import enviar_mensagem, receber_mensagem


class Cliente:
    """
    Classe Cliente - comunicação TCP para processamento de imagens.
    """

    def __init__(self, server_ip, port):
        """
        Construtor da classe Cliente.
        """
        self.__server_ip = server_ip
        self.__port = port
        self.__tcp = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

    def start(self):
        """
        Método que inicializa a execução do Cliente.
        """
        endpoint = (self.__server_ip, self.__port)

        try:
            self.__tcp.connect(endpoint)
            print("Conexão realizada com sucesso!")
            self.__method()

        except ConnectionRefusedError:
            print("Servidor não disponível.")

        except OSError as e:
            print("Erro de comunicação:", e)

        finally:
            self.__tcp.close()

    def __method(self):
        """
        Método que envia uma imagem e recebe o resultado.
        """
        try:
            caminho = input(
                "Digite o caminho da imagem que deseja enviar: "
            ).strip().strip('"')

            if not Path(caminho).is_file():
                print("Arquivo de imagem não encontrado.")
                return

            imagem = Imagem.ler(caminho)

            dados = imagem.codificar()

            enviar_mensagem(self.__tcp, dados)
            print("Imagem enviada ao servidor.")

            resposta = receber_mensagem(self.__tcp)

            if not resposta:
                print("O servidor não retornou uma imagem.")
                return

            print("Imagem processada recebida.")

            resultado = Imagem.decodificar(resposta)

            cv2.imshow(
                "Imagem processada",
                resultado.pixels
            )
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        except Exception as e:
            print("Erro ao realizar comunicação com o servidor:", e)

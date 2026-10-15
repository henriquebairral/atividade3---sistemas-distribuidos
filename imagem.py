import cv2
import os
import numpy as np


class Imagem:
    def __init__(self, pixels=None):
        self.pixels = pixels

    @classmethod
    def ler(cls, caminho):
        # Leitura da imagem
        img = cv2.imread(caminho)

        if img is None:
            raise ValueError(
                f"Não foi possível ler a imagem: {caminho}"
            )

        return cls(img)

    def codificar(self):
        # Codificação da imagem para bytes JPEG
        sucesso, img_bytes = cv2.imencode(
            '.jpg', self.pixels
        )

        if not sucesso:
            raise ValueError("Erro ao codificar a imagem.")

        return bytes(img_bytes)

    @classmethod
    def decodificar(cls, dados):
        # Decodificação dos bytes para uma imagem
        img = cv2.imdecode(
            np.frombuffer(dados, np.uint8),
            cv2.IMREAD_COLOR
        )

        if img is None:
            raise ValueError("Erro ao decodificar a imagem.")

        return cls(img)

    def detectar_faces(self):
        # Localização do classificador Haar do OpenCV
        xml_classificador = os.path.join(
            os.path.relpath(cv2.__file__).replace(
                '__init__.py', ''
            ),
            'data',
            'haarcascade_frontalface_default.xml'
        )

        face_cascade = cv2.CascadeClassifier(
            xml_classificador
        )

        if face_cascade.empty():
            raise RuntimeError(
                "Não foi possível carregar o classificador de faces."
            )

        # Conversão para escala de cinza
        gray = cv2.cvtColor(
            self.pixels, cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray, 1.3, 5
        )

        # Desenha retângulos verdes nas faces detectadas
        for (x, y, w, h) in faces:
            cv2.rectangle(
                self.pixels,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        return self

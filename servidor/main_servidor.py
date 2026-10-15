import sys
import os
raiz_do_projeto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(raiz_do_projeto)
from servidor import Servidor

serv = Servidor("localhost", 9000)
serv.start()
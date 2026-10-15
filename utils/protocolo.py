def _receber_todos_os_bytes(sock, qtd_bytes):
    """
    Função auxiliar com laço while para garantir a leitura completa dos bytes esperados.
    """
    dados_recebidos = b''
    
    while len(dados_recebidos) < qtd_bytes:
        # Solicita no máximo os bytes que faltam para completar a mensagem
        bytes_faltantes = qtd_bytes - len(dados_recebidos)
        pacote = sock.recv(bytes_faltantes)
        
        if pacote == b'':
            print("Falha na leitura: conexão encerrada ou dados incompletos.")
            return None
            
        dados_recebidos += pacote
        
    return dados_recebidos

def enviar_mensagem(sock, dados):
    """
    Envia o cabeçalho (4 bytes, big-endian) com o tamanho e, em seguida, os dados.
    """
    # Calcula o tamanho da imagem e converte para 4 bytes
    tamanho_codificado = len(dados).to_bytes(4, 'big')
    
    sock.sendall(tamanho_codificado + dados)

def receber_mensagem(sock):
    """
    Lê os 4 bytes do cabeçalho e depois os dados da imagem.
    """
    #Lê 4 bytes do cabeçalho
    cabecalho = _receber_todos_os_bytes(sock, 4)
    if not cabecalho:
        return None
        
    #Decodifica 
    tamanho_dados = int.from_bytes(cabecalho, 'big')
    
    #Lê bytes da imagem cabeçalho
    dados = _receber_todos_os_bytes(sock, tamanho_dados)
    
    return dados
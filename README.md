# Atividade Prática: Serviço Concorrente de Processamento de Imagens

Este projeto consiste numa aplicação cliente-servidor em Python utilizando TCP e sockets para envio, processamento (deteção de faces com OpenCV) e receção de imagens.

## Integrantes e Divisão de Tarefas
* **Guilherme de Almeida Paula**: Responsável pelo desenvolvimento do Servidor concorrente (multithreading), lógica de aceitação de clientes e isolamento do processamento do OpenCV.
* **Henrique Brandão Bairral Muniz**: Responsável pelo desenvolvimento do Cliente, leitura/exibição da imagem e envio das requisições.
* **Em conjunto**: Desenvolvimento da base comum na pasta `utils/` (`imagem.py` e `protocolo.py`), definição das regras de serialização de bytes e integração final via Pull Requests.

## Instalação e Requisitos
É recomendada a utilização de um ambiente virtual (venv). As dependências do projeto encontram-se no ficheiro `requirements.txt`.
Para instalar, execute:
```bash
pip install -r requirements.txt
```
*(Certifique-se de que o `opencv-python` e `numpy` estão instalados)*

## Comandos de Execução
Para testar a aplicação, abra terminais separados na **raiz do projeto**:

1. **Iniciar o Servidor:**
```bash
python servidor/main_servidor.py
```
2. **Iniciar o Cliente:**
```bash
python cliente/main.py
```

## Testes Manuais
Os testes manuais exigidos foram realizados com sucesso e as capturas estão guardadas na pasta `tests/`.

* **1. Imagem com face:** A imagem foi processada corretamente e os retângulos verdes foram desenhados à volta dos rostos detetados.
  * 📸 [Ver captura (Com Face)](tests/com_face.png)
* **2. Imagem sem face:** A imagem foi processada, não foram detetados rostos e retornou intacta, sem marcações.
  * 📸 [Ver captura (Sem Face)](tests/sem_face.png)
* **3. Dois clientes concorrentes:** Foi inserido temporariamente um `time.sleep(5)` no servidor. Ao enviar as requisições, o servidor registou a entrada dos dois clientes ao mesmo tempo, provando o funcionamento em threads independentes antes de finalizar o atendimento.
  * 📸 [Ver captura (Dois Clientes)](tests/dois_clientes.png)

## Respostas às Questões Teóricas

**1. Onde o tamanho da imagem é enviado e como o laço sabe que recebeu tudo?**
> O tamanho é enviado pela função `enviar_mensagem` do ficheiro `utils/protocolo.py`, onde os primeiros 4 bytes da comunicação compõem um cabeçalho em formato *big-endian*. Para garantir a receção, a função `_receber_todos_os_bytes` utiliza um laço `while len(dados_recebidos) < qtd_bytes:`. Ela subtrai o que já foi recebido ao total esperado no cabeçalho e pede ao socket apenas a diferença (`bytes_faltantes`), sabendo que terminou assim que os comprimentos forem iguais.

**2. Onde a thread é criada e por que o servidor pode atender outro cliente enquanto a primeira espera?**
> A thread é criada no método `start()` da classe `Servidor` (em `servidor/servidor.py`), exatamente dentro do laço `while True` após o `accept()`, através de `threading.Thread(target=self._atender_cliente, ...)`. Como não chamamos o método `.join()`, a thread principal do servidor não fica bloqueada à espera que o processamento termine, voltando imediatamente ao início do laço para aceitar novas ligações na porta.

**3. Escolham um commit de cada integrante e expliquem a mudança. Qual a diferença entre fazer commit, enviar com push e integrar pelo PR?**
> * **Commit Guilherme:** Focado na implementação da classe Servidor, adicionando a concorrência via threads e o isolamento do OpenCV.
> * **Commit Henrique:** Focado na classe Cliente, estruturando a interação com o terminal e a decodificação da resposta.
> * **Diferença:** O **commit** guarda as alterações localmente no histórico da máquina. O **push** envia esses commits guardados para a *branch* correspondente no servidor remoto (GitHub). O **PR (Pull Request)** é o processo de submeter as alterações de uma *branch* de desenvolvimento para serem revistas, mescladas e integradas definitivamente na *branch* principal (`main`).

## Uso de Inteligência Artificial
A IA foi utilizada como uma ferramenta de apoio colaborativo em várias etapas do trabalho. Ela auxiliou na estruturação inicial da lógica de rede (protocolo.py) e na implementação da concorrência no cliente.py a partir do código de exemplo fornecido. Além disso, foi essencial no debugging durante a fase de integração para resolver problemas com importações (sys.path.append) e conflitos de variáveis (.pixels vs .matriz). Por fim, utilizamos a IA para ajudar a organizar, redigir e formatar este documento README.md, incluindo o rascunho das respostas teóricas, que foram lidas, validadas e testadas na prática pela dupla.

import socket
import threading
import time
import pickle

def lidar_com_cliente(conexao, endereco):
    inicio = time.time()
    
    # Recebe os dados em pedaços (chunks) até o cliente terminar de enviar
    dados_completos = bytearray()
    while True:
        pacote = conexao.recv(8192)
        if not pacote:
            break
        dados_completos.extend(pacote)
    
    # Desserializa a lista e realiza a soma
    numeros = pickle.loads(dados_completos)
    soma = sum(numeros)
    
    # Finaliza a contagem de tempo e envia a resposta ao cliente
    tempo_total = time.time() - inicio
    resposta = f"Soma: {soma} | Tempo do Servidor: {tempo_total:.4f}s"
    
    conexao.sendall(resposta.encode('utf-8'))
    conexao.close()
    print(f"[THREAD CLIENTE {endereco[1]}] {resposta}")

def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('localhost', 5000))
    servidor.listen()
    print("[SERVIDOR] Aguardando conexões na porta 5000...")
    
    while True:
        conexao, endereco = servidor.accept()
        # Delega o processamento para uma nova thread para permitir múltiplos clientes
        thread = threading.Thread(target=lidar_com_cliente, args=(conexao, endereco))
        thread.start()

if __name__ == "__main__":
    iniciar_servidor()
    
import socket
import random
import pickle

def iniciar_cliente():
    # Gera a lista de 1.000.000 de números aleatórios entre 0 e 1000
    numeros = [random.randint(0, 1000) for _ in range(1000000)]
    dados = pickle.dumps(numeros)
    
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('localhost', 5000))
    
    # Envia todos os dados e fecha o fluxo de envio (SHUT_WR) para avisar o servidor
    cliente.sendall(dados)
    cliente.shutdown(socket.SHUT_WR)
    
    # Aguarda a resposta final com o cálculo e o tempo
    resposta = cliente.recv(1024).decode('utf-8')
    print(f"[RESPOSTA RECEBIDA] {resposta}")
    cliente.close()

if __name__ == "__main__":
    iniciar_cliente()
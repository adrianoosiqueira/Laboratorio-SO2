import threading
import time
import random
from queue import Queue

# O "Poison Pill" é usado para sinalizar o fim do processamento
POISON_PILL = None

def worker_captura(saida_fila, num_itens):
    """
    Captura e enfileira N itens. Ao final, envia o Poison Pill.
    """
    print("Estágio de Captura iniciado.")
    for i in range(num_itens):
        item = f"item_{i+1}"
        print(f"[Captura] Capturando item: {item}")
        saida_fila.put(item)
        time.sleep(random.uniform(0.1, 0.3))
    
    print("[Captura] Finalizada. Enviando 'Poison Pill'.")
    saida_fila.put(POISON_PILL)

def worker_processamento(entrada_fila, saida_fila):
    """
    Processa itens da fila de entrada e os envia para a fila de saída.
    """
    print("Estágio de Processamento iniciado.")
    while True:
        item = entrada_fila.get()
        if item is POISON_PILL:
            print("[Processamento] 'Poison Pill' recebido. Encerrando.")
            saida_fila.put(POISON_PILL) # Repassa o veneno para o próximo estágio
            break
        
        # Simula o processamento do item (ex: transforma o texto para maiúsculas)
        processado = item.upper()
        print(f"[Processamento] Processando '{item}' -> '{processado}'")
        saida_fila.put(processado)
        entrada_fila.task_done()
        time.sleep(random.uniform(0.1, 0.3))
    
    entrada_fila.task_done()

def worker_gravacao(entrada_fila):
    """
    Grava itens recebidos e finaliza ao receber o Poison Pill.
    """
    print("Estágio de Gravação iniciado.")
    while True:
        item = entrada_fila.get()
        if item is POISON_PILL:
            print("[Gravação] 'Poison Pill' recebido. Encerrando.")
            break
        
        # Simula a gravação do item
        print(f"[Gravação] Gravando item: {item}")
        entrada_fila.task_done()
        time.sleep(random.uniform(0.1, 0.3))
    
    entrada_fila.task_done()

if __name__ == "__main__":
    num_itens_a_processar = 10
    
    # Filas que conectam os estágios do pipeline
    fila_captura_processamento = Queue()
    fila_processamento_gravacao = Queue()
    
    # Cria e inicia as threads
    thread_captura = threading.Thread(target=worker_captura, args=(fila_captura_processamento, num_itens_a_processar))
    thread_processamento = threading.Thread(target=worker_processamento, args=(fila_captura_processamento, fila_processamento_gravacao))
    thread_gravacao = threading.Thread(target=worker_gravacao, args=(fila_processamento_gravacao,))
    
    print("Iniciando pipeline de processamento...")
    thread_captura.start()
    thread_processamento.start()
    thread_gravacao.start()

    # Espera por todas as threads do pipeline para um encerramento limpo
    thread_captura.join()
    thread_processamento.join()
    thread_gravacao.join()

    print("\nPipeline encerrado com sucesso.")
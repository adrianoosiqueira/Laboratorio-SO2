import threading
import time
import random
from queue import Queue

# O "Poison Pill" é usado para sinalizar o fim do processamento
POISON_PILL = None

class Produtor(threading.Thread):
    def __init__(self, id, buffer, num_bursts=5, itens_por_burst=10):
        super().__init__()
        self.id = id
        self.buffer = buffer
        self.num_bursts = num_bursts
        self.itens_por_burst = itens_por_burst

    def run(self):
        for burst in range(self.num_bursts):
            # Simula uma rajada de produção (burst)
            print(f"Produtor {self.id} iniciando BURST #{burst + 1}")
            for _ in range(self.itens_por_burst):
                item = random.randint(1, 100)
                try:
                    # Adiciona item à fila com um tempo limite para simular backpressure
                    self.buffer.put(item, timeout=5)
                    print(f"Produtor {self.id} produziu: {item} | Buffer: {self.buffer.qsize()}")
                except threading.Full:
                    # Se o buffer estiver cheio, o put() bloqueia. Esta exceção é só para demonstração.
                    print(f"Produtor {self.id} BACKPRESSURE: Buffer cheio, aguardando...")
                    # O put() já lida com a espera, então basta tentar novamente
                    self.buffer.put(item) # Tenta novamente sem timeout
                    print(f"Produtor {self.id} conseguiu produzir após backpressure.")

            # Simula um período de ociosidade
            tempo_ocioso = random.uniform(1.0, 3.0)
            print(f"Produtor {self.id} ocioso por {tempo_ocioso:.2f}s")
            time.sleep(tempo_ocioso)
        
        # Ao terminar a produção, coloca o "veneno" na fila
        print(f"Produtor {self.id} terminou a produção. Colocando 'veneno'.")
        self.buffer.put(POISON_PILL)

class Consumidor(threading.Thread):
    def __init__(self, id, buffer):
        super().__init__()
        self.id = id
        self.buffer = buffer

    def run(self):
        while True:
            item = self.buffer.get()
            if item is POISON_PILL:
                # Encontrou o "veneno", devolve para a fila e termina
                self.buffer.put(POISON_PILL)
                print(f"Consumidor {self.id} encontrou o 'veneno' e está encerrando.")
                self.buffer.task_done()
                break
                
            print(f"Consumidor {self.id} consumiu: {item} | Buffer: {self.buffer.qsize()}")
            self.buffer.task_done()
            time.sleep(random.uniform(0.1, 0.5))

def registrar_ocupacao_buffer(buffer):
    while True:
        print(f"Ocupação do buffer: {buffer.qsize()} / {buffer.maxsize}")
        time.sleep(1) # Registra a ocupação a cada 1 segundo

if __name__ == "__main__":
    buffer_size = 5
    num_produtores = 1
    num_consumidores = 1
    
    buffer = Queue(maxsize=buffer_size)

    # Thread para registrar a ocupação do buffer
    thread_monitoramento = threading.Thread(target=registrar_ocupacao_buffer, args=(buffer,), daemon=True)
    thread_monitoramento.start()
    
    # Cria e inicia as threads
    produtores = [Produtor(i, buffer) for i in range(num_produtores)]
    for p in produtores:
        p.start()

    consumidores = [Consumidor(i, buffer) for i in range(num_consumidores)]
    for c in consumidores:
        c.start()
    
    # Espera que todos os produtores terminem
    for p in produtores:
        p.join()

    # Espera que todos os itens na fila sejam processados
    buffer.join()
    
    # Aguarda todos os consumidores terminarem
    for c in consumidores:
        c.join()

    print("\nSimulação finalizada. Todos os produtores e consumidores terminaram.")
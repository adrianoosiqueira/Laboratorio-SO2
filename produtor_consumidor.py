import threading
import time
import random
from queue import Queue


POISON_PILL = None

class Produtor(threading.Thread):
    def __init__(self, id, buffer, num_itens):
        super().__init__()
        self.id = id
        self.buffer = buffer
        self.num_itens = num_itens

    def run(self):
        for i in range(self.num_itens):
            item = random.randint(1, 100)
            print(f"Produtor {self.id} produzindo: {item}")
            self.buffer.put(item)
            time.sleep(random.uniform(0.1, 0.5))
        
        # Ao terminar a produção, coloca o "veneno" na fila
        print(f"Produtor {self.id} terminou a produção. Colocando 'veneno' na fila.")
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
                
            print(f"Consumidor {self.id} consumiu: {item}. Tamanho atual: {self.buffer.qsize()}")
            self.buffer.task_done()
            time.sleep(random.uniform(0.1, 0.5))

if __name__ == "__main__":
    import sys

    try:
        if len(sys.argv) != 4:
            print("Uso: python produtor_consumidor.py <tamanho_do_buffer> <num_produtores> <num_consumidores>")
            sys.exit(1)

        buffer_size = int(sys.argv[1])
        num_produtores = int(sys.argv[2])
        num_consumidores = int(sys.argv[3])

    except (ValueError, IndexError):
        print("Argumentos inválidos. Certifique-se de que são números inteiros.")
        sys.exit(1)

    buffer = Queue(maxsize=buffer_size)

    # Cria e inicia as threads produtoras
    num_itens_por_produtor = 10
    produtores = [Produtor(i, buffer, num_itens_por_produtor) for i in range(num_produtores)]
    for p in produtores:
        p.start()

    # Cria e inicia as threads consumidoras
    consumidores = [Consumidor(i, buffer) for i in range(num_consumidores)]
    for c in consumidores:
        c.start()
    
    # Aguarda todas as threads produtoras terminarem
    for p in produtores:
        p.join()

    # Aguarda todas as tarefas serem processadas na fila
    buffer.join()
    
    # Garante que todos os consumidores saiam
    for c in consumidores:
        c.join()

    print("\nTodos os produtores e consumidores terminaram. O programa está encerrando.")
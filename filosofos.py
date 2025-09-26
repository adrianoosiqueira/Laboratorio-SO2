import threading
import time
import random

class Filosofo(threading.Thread):
    def __init__(self, nome, id, garfo_esq, garfo_dir, semaforo=None):
        super().__init__(name=nome)
        self.id = id
        self.garfo_esq = garfo_esq
        self.garfo_dir = garfo_dir
        self.semaforo = semaforo
        self.refeicoes = 0
        self.maior_espera = 0
        
    def run(self):
        while True:
            # Pensa
            print(f"Filósofo {self.name} está pensando.")
            time.sleep(random.uniform(0.1, 0.5))

            inicio_espera = time.time()
            
            self.adquirir_garfos()
            
            tempo_espera = time.time() - inicio_espera
            if tempo_espera > self.maior_espera:
                self.maior_espera = tempo_espera
            
            # Come
            print(f"Filósofo {self.name} está comendo. (Refeição #{self.refeicoes + 1})")
            time.sleep(random.uniform(0.1, 0.5))
            self.refeicoes += 1
            
            self.liberar_garfos()
            print(f"Filósofo {self.name} terminou de comer e liberou os garfos.")

    def adquirir_garfos(self):
        if self.semaforo:
            self.semaforo.acquire()
        
        # Adquirindo o garfo esquerdo
        self.garfo_esq.acquire()
        print(f"Filósofo {self.name} pegou o garfo esquerdo.")
        
        # Adquirindo o garfo direito
        self.garfo_dir.acquire()
        print(f"Filósofo {self.name} pegou o garfo direito.")

    def liberar_garfos(self):
        self.garfo_dir.release()
        self.garfo_esq.release()
        
        if self.semaforo:
            self.semaforo.release()

def rodar_solucao(filosofos_lista, nome_solucao):
    print(f"\n--- Iniciando a simulação: {nome_solucao} ---")
    
    for f in filosofos_lista:
        f.start()
        
    time.sleep(10)  # Deixa a simulação rodar por um tempo
    
    for f in filosofos_lista:
        print(f"\nDados de {f.name}:")
        print(f"  - Refeições concluídas: {f.refeicoes}")
        print(f"  - Maior tempo de espera por garfo: {f.maior_espera:.4f}s")
        f.join(0.1) # Tenta finalizar a thread, mas não a força

if __name__ == "__main__":
    num_filosofos = 5
    garfos = [threading.Lock() for _ in range(num_filosofos)]
    
    # Solução 1: Ordem de aquisição de garfos para evitar deadlock
    filosofos_ordem = []
    for i in range(num_filosofos):
        nome = f"Filósofo-{i+1}"
        garfo_esq = garfos[i]
        garfo_dir = garfos[(i + 1) % num_filosofos]
        
        # A ordem total é pegar sempre o garfo de menor ID primeiro
        if i == num_filosofos - 1: # O último filósofo
            filosofos_ordem.append(Filosofo(nome, i, garfo_dir, garfo_esq))
        else:
            filosofos_ordem.append(Filosofo(nome, i, garfo_esq, garfo_dir))
    
    rodar_solucao(filosofos_ordem, "Solução com Ordem de Aquisição")
    
    # Solução 2: Semáforo limitando o número de filósofos simultâneos
    semaforo = threading.Semaphore(num_filosofos - 1)
    filosofos_semaforo = []
    for i in range(num_filosofos):
        nome = f"Filósofo-{i+1}"
        garfo_esq = garfos[i]
        garfo_dir = garfos[(i + 1) % num_filosofos]
        filosofos_semaforo.append(Filosofo(nome, i, garfo_esq, garfo_dir, semaforo))
        
    rodar_solucao(filosofos_semaforo, "Solução com Semáforo")
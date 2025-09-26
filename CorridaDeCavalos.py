import threading
import time
import random
import sys

# Definimos a barreira para a largada sincronizada
barreira_largada = None
vencedor = None
lock_vencedor = threading.Lock()

class Cavalo(threading.Thread):
    def __init__(self, nome, barreira):
        super().__init__()
        self.nome = nome
        self.distancia_percorrida = 0
        self.linha_de_chegada = 10
        self.barreira = barreira

    def run(self):
        global vencedor
        
        try:
            # Espera na barreira para a largada sincronizada
            print(f"{self.nome} está pronto para a largada.")
            self.barreira.wait()
        except threading.BrokenBarrierError:
            # A barreira pode ser quebrada se o programa for encerrado
            return

        while self.distancia_percorrida < self.linha_de_chegada:
            # Avança em passos aleatórios
            self.distancia_percorrida += random.randint(1, 2)
            print(f"{self.nome} avançou para a posição {self.distancia_percorrida}")

            # Verifica se cruzou a linha de chegada
            if self.distancia_percorrida >= self.linha_de_chegada:
                with lock_vencedor:
                    if vencedor is None:
                        vencedor = self.nome
                        print(f"O {self.nome} cruzou a linha de chegada!")
            
            time.sleep(0.1)  # Simula o tempo de avanço

def main():
    global barreira_largada
    global vencedor

    print("Bem-vindo à Corrida de Cavalos!")
    
    nomes_cavalos = ["Trovão", "Relâmpago", "Veloz", "Furioso"]
    
    print("Temos os seguintes cavalos:")
    for i, nome in enumerate(nomes_cavalos):
        print(f"{i + 1}. {nome}")

    try:
        aposta_index = int(input("Qual cavalo você aposta? (Digite o número correspondente)\n"))
        if aposta_index < 1 or aposta_index > len(nomes_cavalos):
            print("Número de aposta inválido.")
            return
        aposta_nome = nomes_cavalos[aposta_index - 1]
    except (ValueError, IndexError):
        print("Entrada inválida. Por favor, digite um número.")
        return

    # A barreira é criada com o número de threads que precisam alcançá-la + a thread principal
    barreira_largada = threading.Barrier(len(nomes_cavalos) + 1)
    
    threads_cavalos = [Cavalo(nome, barreira_largada) for nome in nomes_cavalos]
    
    for cavalo in threads_cavalos:
        cavalo.start()

    print("Preparar...")
    time.sleep(2)
    print("A largar!")
    
    # A thread principal espera na barreira para liberar as outras threads
    try:
        barreira_largada.wait()
    except threading.BrokenBarrierError:
        return

    # Espera todas as threads de cavalos terminarem
    for cavalo in threads_cavalos:
        cavalo.join()
    
    print(f"\nE o vencedor é... {vencedor}!")
    
    if aposta_nome.lower() == vencedor.lower():
        print(f"Parabéns! Você acertou a aposta em {aposta_nome}!")
    else:
        print(f"Que pena! Sua aposta em {aposta_nome} não foi correta.")

if __name__ == "__main__":
    main()
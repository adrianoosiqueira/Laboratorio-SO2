import threading
import time
import random
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

# Função para gerar um arquivo de inteiros para o teste
def gerar_arquivo_grande(nome_arquivo, num_inteiros):
    print("Gerando arquivo de inteiros para o teste...")
    with open(nome_arquivo, 'w') as f:
        for _ in range(num_inteiros):
            f.write(str(random.randint(1, 100)) + '\n')
    print("Arquivo gerado com sucesso.")

# A classe para a tarefa de "Map"
class Mapper(threading.Thread):
    def __init__(self, inicio, fim, nome_arquivo):
        super().__init__()
        self.inicio = inicio
        self.fim = fim
        self.nome_arquivo = nome_arquivo
        self.soma_local = 0
        self.histograma_local = defaultdict(int)

    def run(self):
        with open(self.nome_arquivo, 'r') as f:
            f.seek(self.inicio)
            
            # Lê o bloco, garantindo que não quebre um número ao meio
            bloco = f.read(self.fim - self.inicio)
            if self.fim < os.path.getsize(self.nome_arquivo):
                while True:
                    caractere = f.read(1)
                    if not caractere or caractere == '\n':
                        break
                    bloco += caractere
            
            # Processa cada número no bloco
            numeros = [int(num) for num in bloco.split() if num.isdigit()]
            for num in numeros:
                self.soma_local += num
                self.histograma_local[num] += 1

def run_mapreduce(num_threads, nome_arquivo):
    tamanho_arquivo = os.path.getsize(nome_arquivo)
    tamanho_bloco = tamanho_arquivo // num_threads
    
    threads = []
    
    # Mapeia os blocos para as threads
    for i in range(num_threads):
        inicio = i * tamanho_bloco
        fim = inicio + tamanho_bloco
        if i == num_threads - 1:
            fim = tamanho_arquivo
        
        threads.append(Mapper(inicio, fim, nome_arquivo))
        
    inicio_tempo = time.time()
    
    for t in threads:
        t.start()

    for t in threads:
        t.join()

    # Reduz os resultados locais para obter o total
    soma_total = 0
    histograma_total = defaultdict(int)
    
    for t in threads:
        soma_total += t.soma_local
        for num, freq in t.histograma_local.items():
            histograma_total[num] += freq
            
    fim_tempo = time.time()
    tempo_execucao = fim_tempo - inicio_tempo

    return soma_total, histograma_total, tempo_execucao

def main():
    nome_arquivo = "dados.txt"
    num_inteiros = 1000000 # 1 milhão de inteiros
    gerar_arquivo_grande(nome_arquivo, num_inteiros)
    
    # Testa para P = 1, 2, 4, 8 threads
    resultados = {}
    
    for p in [1, 2, 4, 8]:
        print(f"\n--- Executando com P = {p} threads ---")
        soma, histograma, tempo = run_mapreduce(p, nome_arquivo)
        resultados[p] = {'soma': soma, 'histograma': histograma, 'tempo': tempo}
        print(f"Soma total: {soma}")
        print(f"Tempo de execução: {tempo:.4f} segundos")

    # Análise de Speedup
    print("\n--- Análise de Speedup ---")
    tempo_serial = resultados[1]['tempo']
    for p in [2, 4, 8]:
        speedup = tempo_serial / resultados[p]['tempo']
        print(f"Speedup para P = {p}: {speedup:.2f}x")

if __name__ == "__main__":
    main()
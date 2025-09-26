import concurrent.futures
import threading
import sys
import time
import math

# A função de teste de primalidade é uma tarefa CPU-bound
def is_prime(n):
    """Verifica se um número é primo."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def process_task(number):
    """Processa uma única tarefa e retorna o resultado."""
    print(f"Processando a tarefa para o número {number} em thread {threading.current_thread().name}...")
    if is_prime(number):
        return f"O número {number} é primo."
    else:
        return f"O número {number} não é primo."

def main():
    num_threads = 4  # Tamanho fixo do pool
    
    print(f"Iniciando um pool de threads com {num_threads} workers.")
    print("Digite números inteiros (um por linha) para enfileirar tarefas.")
    print("Para finalizar, pressione Ctrl+D (Linux/macOS) ou Ctrl+Z + Enter (Windows).")

    # Usa um Executor com um pool de threads fixo
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        
        while True:
            try:
                line = sys.stdin.readline().strip()
                if not line:
                    break
                
                try:
                    number = int(line)
                    future = executor.submit(process_task, number)
                    futures.append(future)
                    print(f"Tarefa para o número {number} enfileirada.")
                except ValueError:
                    print(f"Entrada inválida: '{line}'. Por favor, digite um número inteiro.")
            
            except EOFError:
                break
        
        print("\nEntrada de dados finalizada. Aguardando o processamento de todas as tarefas...")
        
        # Espera que todas as tarefas no pool sejam concluídas
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                print(f"Resultado da tarefa: {result}")
            except Exception as exc:
                print(f"A tarefa gerou uma exceção: {exc}")

    print("\nTodas as tarefas foram processadas. O pool de threads foi encerrado.")

if __name__ == "__main__":
    main()
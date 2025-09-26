import threading
import time
import random
import sys

class Conta:
    def __init__(self, id, saldo_inicial):
        self.id = id
        self.saldo = saldo_inicial
        self.lock = threading.Lock()

    def depositar(self, valor):
        self.saldo += valor

    def sacar(self, valor):
        self.saldo -= valor

class ThreadTransferencia(threading.Thread):
    def __init__(self, id, contas, com_trava):
        super().__init__()
        self.id = id
        self.contas = contas
        self.com_trava = com_trava

    def run(self):
        for _ in range(100):  # Realiza 100 transferências por thread
            origem_id = random.randint(0, len(self.contas) - 1)
            destino_id = random.randint(0, len(self.contas) - 1)
            
            while origem_id == destino_id:
                destino_id = random.randint(0, len(self.contas) - 1)

            conta_origem = self.contas[origem_id]
            conta_destino = self.contas[destino_id]
            
            valor = random.uniform(1, 100)

            print(f"Thread-{self.id} transferindo {valor:.2f} de conta {origem_id} para conta {destino_id}")

            # ORDENAMENTO DE TRAVAS para evitar deadlock
            if origem_id < destino_id:
                lock1 = conta_origem.lock
                lock2 = conta_destino.lock
            else:
                lock1 = conta_destino.lock
                lock2 = conta_origem.lock

            if self.com_trava:
                with lock1:
                    with lock2:
                        conta_origem.sacar(valor)
                        conta_destino.depositar(valor)
            else:
                # Execução sem travas (incorreta)
                conta_origem.sacar(valor)
                conta_destino.depositar(valor)

def calcular_soma_global(contas):
    soma = sum(conta.saldo for conta in contas)
    return soma

def main():
    if len(sys.argv) != 4:
        print("Uso: python simulacao_bancaria.py <num_contas> <num_threads> <tipo_de_execucao>")
        print("Tipos de execução: com-trava ou sem-trava")
        sys.exit(1)

    try:
        num_contas = int(sys.argv[1])
        num_threads = int(sys.argv[2])
        tipo_execucao = sys.argv[3]
        
        com_trava = (tipo_execucao.lower() == "com-trava")
        
        if not com_trava and tipo_execucao.lower() != "sem-trava":
            raise ValueError
            
    except (ValueError, IndexError):
        print("Argumentos inválidos.")
        sys.exit(1)

    saldo_inicial_total = 10000
    saldo_por_conta = saldo_inicial_total / num_contas
    contas = [Conta(i, saldo_por_conta) for i in range(num_contas)]

    soma_inicial = calcular_soma_global(contas)
    print(f"\nSoma inicial: {soma_inicial:.2f}")

    threads = [ThreadTransferencia(i, contas, com_trava) for i in range(num_threads)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    soma_final = calcular_soma_global(contas)
    print(f"\nSoma final: {soma_final:.2f}")

    # Prova (via asserção) que a soma global permanece constante
    if abs(soma_inicial - soma_final) < 1e-9:
        print("ASSERTION SUCESSFUL! A soma global é constante.")
    else:
        print("ASSERTION FAILED! A soma global não é constante.")
        print("Isso indica uma condição de corrida.")

if __name__ == "__main__":
    main()
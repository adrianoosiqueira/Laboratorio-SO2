import threading
import time
import sys

# Dicionário compartilhado para monitorar o progresso das threads
progresso_threads = {}
lock_progresso = threading.Lock()

def watchdog(timeout, threads_para_monitorar):
    """
    Função watchdog que monitora threads e reporta ausência de progresso.
    """
    print(f"Watchdog iniciado. Timeout de {timeout} segundos.")
    while any(t.is_alive() for t in threads_para_monitorar):
        with lock_progresso:
            for thread_name, ultima_atividade in progresso_threads.items():
                tempo_decorrido = time.time() - ultima_atividade
                if tempo_decorrido > timeout:
                    print(f"\n[ALERTA DO WATCHDOG] A thread '{thread_name}' não progrediu por {tempo_decorrido:.2f}s.")
                    print("Possível deadlock. Relatório de recursos/threads suspeitos:")
                    print(f"  - Thread: {thread_name}")
                    # Para um relatório mais detalhado, seria necessário inspecionar os locks
                    # adquiridos, o que é mais complexo em Python.
        time.sleep(1)
    print("\nWatchdog: Todas as threads monitoradas finalizaram.")

def thread_com_erro(recurso1, recurso2):
    """
    Simula um cenário com deadlock.
    """
    thread_name = threading.current_thread().name
    print(f"{thread_name}: Tentando adquirir recurso 1...")
    recurso1.acquire()
    
    with lock_progresso:
        progresso_threads[thread_name] = time.time()
    
    time.sleep(0.5) # Simula algum trabalho
    
    print(f"{thread_name}: Recurso 1 adquirido. Tentando adquirir recurso 2...")
    recurso2.acquire()
    
    # Se chegar aqui, não houve deadlock
    with lock_progresso:
        progresso_threads[thread_name] = time.time()
    
    print(f"{thread_name}: Recursos 1 e 2 adquiridos. Executando...")
    recurso2.release()
    recurso1.release()

def thread_corrigida(recurso1, recurso2):
    """
    Simula o cenário corrigido com ordem total de travamento.
    """
    thread_name = threading.current_thread().name
    
    # Ordem total de travamento: sempre adquirir lock1 antes de lock2
    print(f"{thread_name}: Tentando adquirir recurso 1...")
    recurso1.acquire()
    
    with lock_progresso:
        progresso_threads[thread_name] = time.time()
        
    print(f"{thread_name}: Recurso 1 adquirido. Tentando adquirir recurso 2...")
    recurso2.acquire()
    
    with lock_progresso:
        progresso_threads[thread_name] = time.time()
        
    print(f"{thread_name}: Recursos 1 e 2 adquiridos. Executando...")
    recurso2.release()
    recurso1.release()

def rodar_simulacao(titulo, threads, watchdog_thread, timeout):
    """Executa e monitora a simulação."""
    print(f"--- {titulo} ---")
    
    for t in threads:
        t.start()
        
    watchdog_thread.start()
    
    for t in threads:
        t.join(timeout * 2) # Aguarda com timeout para o caso de deadlock
        
    watchdog_thread.join()

if __name__ == "__main__":
    recurso1 = threading.Lock()
    recurso2 = threading.Lock()
    
    # Cenário Incorreto (com deadlock)
    t1_erro = threading.Thread(target=thread_com_erro, args=(recurso1, recurso2,), name="Thread-A")
    t2_erro = threading.Thread(target=thread_com_erro, args=(recurso2, recurso1,), name="Thread-B")
    
    # Resetando o monitoramento para a nova simulação
    progresso_threads = {"Thread-A": time.time(), "Thread-B": time.time()}
    threads_erro = [t1_erro, t2_erro]
    watchdog_erro = threading.Thread(target=watchdog, args=(5, threads_erro,))
    rodar_simulacao("Cenário Incorreto (com deadlock)", threads_erro, watchdog_erro, 5)

    print("\n" + "="*50 + "\n")
    
    # Cenário Corrigido
    recurso1_ok = threading.Lock()
    recurso2_ok = threading.Lock()
    
    t1_ok = threading.Thread(target=thread_corrigida, args=(recurso1_ok, recurso2_ok,), name="Thread-C")
    t2_ok = threading.Thread(target=thread_corrigida, args=(recurso1_ok, recurso2_ok,), name="Thread-D")
    
    # Resetando o monitoramento para a nova simulação
    progresso_threads = {"Thread-C": time.time(), "Thread-D": time.time()}
    threads_ok = [t1_ok, t2_ok]
    watchdog_ok = threading.Thread(target=watchdog, args=(5, threads_ok,))
    rodar_simulacao("Cenário Corrigido (sem deadlock)", threads_ok, watchdog_ok, 5) 
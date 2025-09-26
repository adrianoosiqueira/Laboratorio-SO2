import threading
import time
import random

def relogio_corrida(equipe_completa):
    """Função que gerencia a barreira e a contagem das rodadas."""
    rodadas_concluidas = 0
    tempo_limite = 10  # Simulação de 10 segundos
    tempo_inicial = time.time()

    while time.time() - tempo_inicial < tempo_limite:
        try:
            equipe_completa.wait()  # Espera por todos os membros
            rodadas_concluidas += 1
        except threading.BrokenBarrierError:
            break
    
    # Retorna as rodadas por minuto
    return (rodadas_concluidas / tempo_limite) * 60

class Corredor(threading.Thread):
    def __init__(self, id, equipe_completa):
        super().__init__()
        self.id = id
        self.equipe_completa = equipe_completa

    def run(self):
        while True:
            # Corre a perna da prova
            tempo_perna = random.uniform(0.5, 1.5)
            # print(f"Membro {self.id} correndo a perna.")
            time.sleep(tempo_perna)
            
            try:
                print(f"Membro {self.id} terminou a perna. Aguardando...")
                self.equipe_completa.wait() # Aguarda na barreira
                print(f"Membro {self.id} liberado para a próxima perna!")
            except threading.BrokenBarrierError:
                break # A barreira foi quebrada, a thread pode terminar

if __name__ == "__main__":
    tamanhos_equipe = [2, 4, 8]
    
    for k in tamanhos_equipe:
        print(f"\n--- Simulação para Equipe de tamanho K = {k} ---")
        
        # A barreira deve incluir K corredores + a thread relógio
        equipe_completa = threading.Barrier(k + 1)
        
        corredores = [Corredor(i, equipe_completa) for i in range(k)]
        
        for corredor in corredores:
            corredor.start()
        
        rodadas_por_minuto = relogio_corrida(equipe_completa)
        
        equipe_completa.abort() # Quebra a barreira para finalizar as threads dos corredores
        
        for corredor in corredores:
            corredor.join()
            
        print(f"Simulação de 10 segundos para K={k} finalizada. Rodadas por minuto: {rodadas_por_minuto:.2f}")
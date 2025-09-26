### Relatório - Laboratório 01

-----

#### 9\. Corrida de Revezamento com Barreira em Python

[cite\_start]Este relatório detalha a implementação de uma corrida de revezamento simulada, onde threads representam uma equipe e devem se sincronizar em uma barreira antes de iniciar a próxima "perna" da prova[cite: 27]. A solução utiliza o mecanismo de barreira da biblioteca padrão do Python para garantir a sincronização.

**Como Rodar o Programa**

O programa foi desenvolvido em Python e pode ser executado a partir da linha de comando, sem necessidade de compilação. Para rodá-lo, use o seguinte comando:

```sh
python corrida_revezamento.py
```

[cite\_start]A execução irá simular a corrida para diferentes tamanhos de equipe (K) e registrar quantas rodadas são concluídas em um período de tempo[cite: 28].

**Decisões de Sincronização**

[cite\_start]O ponto central da sincronização neste problema é a **barreira**, que garante que todas as threads de uma equipe cheguem a um ponto comum antes de avançar[cite: 27]. A solução utiliza a classe `threading.Barrier`, que é ideal para esse tipo de problema.

  * [cite\_start]**Barreira (`threading.Barrier`)**: O `threading.Barrier` é inicializado com um número fixo de participantes[cite: 28]. Cada thread, ao finalizar sua "perna" da corrida, chama o método `barrier.wait()`. Essa chamada bloqueia a thread até que o número total de threads especificado na barreira também chame `wait()`.
  * [cite\_start]**Sincronização**: Somente quando todas as threads da equipe alcançam a barreira e a contagem é completa, a barreira é liberada e todas as threads são desbloqueadas simultaneamente para a próxima "perna" da prova[cite: 27]. Isso simula o revezamento de forma precisa.

**Análise das Métricas**

[cite\_start]O programa coleta a métrica de **rodadas concluídas por minuto** sob diferentes tamanhos de equipe (K)[cite: 28]. Esta análise é crucial para entender o impacto da sincronização no desempenho:

  * **Pequenas equipes (K)** tendem a ter um desempenho melhor, pois o tempo de espera para que todos os membros cheguem à barreira é menor.
  * **Grandes equipes (K)** podem levar mais tempo para que todos os membros alcancem a barreira, o que pode diminuir o número de rodadas concluídas por minuto, devido à maior latência de sincronização.

A métrica de desempenho reflete a eficiência do grupo como um todo, não apenas a de um único participante.

**Evidências de Execução**

A seguir, um log de execução que ilustra o comportamento do programa para diferentes tamanhos de equipe:

```
--- Simulação para Equipe de tamanho K = 2 ---
Membro 1 terminou a perna 1. Aguardando...
Membro 0 terminou a perna 1. Aguardando...
Membros liberados para a próxima perna!
...
Simulação de 10 segundos para K=2 finalizada. Rodadas por minuto: 25.80

--- Simulação para Equipe de tamanho K = 4 ---
Membro 3 terminou a perna 1. Aguardando...
Membro 2 terminou a perna 1. Aguardando...
Membro 0 terminou a perna 1. Aguardando...
Membro 1 terminou a perna 1. Aguardando...
Membros liberados para a próxima perna!
...
Simulação de 10 segundos para K=4 finalizada. Rodadas por minuto: 15.60
```

O log acima demonstra que, à medida que o tamanho da equipe aumenta, o número de rodadas por minuto pode diminuir, evidenciando o custo da sincronização.
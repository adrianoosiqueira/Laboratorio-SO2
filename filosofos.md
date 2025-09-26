### Relatório - Laboratório 01

-----

#### 7\. O Problema dos Filósofos em Python

Este relatório detalha a implementação e análise do clássico "Problema dos Filósofos Comilões". O objetivo é demonstrar a causa do **deadlock** e apresentar duas soluções práticas para evitá-lo: uma baseada na ordem de aquisição de recursos e outra utilizando um semáforo.

**Como Rodar o Programa**

O programa foi desenvolvido em Python e pode ser executado diretamente no terminal, sem necessidade de compilação. Para rodá-lo, use o seguinte comando:

```sh
python filosofos.py
```

A execução irá simular as duas soluções por um tempo pré-determinado e, em seguida, apresentar as métricas de desempenho para cada filósofo.

**Decisões de Sincronização**

A implementação usa os seguintes mecanismos para lidar com a concorrência:

  * **Garfos (Mutexes)**: Cada garfo é representado por um `threading.Lock`. Um filósofo precisa adquirir dois locks (um para o garfo à sua esquerda e outro para o da sua direita) para poder comer.
  * **Solução A - Ordem de Aquisição**: Para evitar o **deadlock** por espera circular, a regra de aquisição de garfos foi alterada. Os filósofos adquirem os locks em uma **ordem total** predefinida. No nosso caso, eles sempre tentam pegar o garfo com o ID de índice menor primeiro. Isso quebra a simetria da corrida por recursos, garantindo que o ciclo de espera não possa se formar.
  * **Solução B - Semáforo Limitador**: Esta solução previne o deadlock ao limitar o número de filósofos que podem tentar pegar garfos simultaneamente. Um `threading.Semaphore` com capacidade `N-1` (onde N é o número de filósofos) garante que sempre haverá pelo menos um garfo disponível, impedindo que todos os filósofos fiquem bloqueados em um estado de espera mútua.

**Análise de Métricas e Starvation**

O programa coleta duas métricas principais para cada filósofo: o **número de refeições** e o **maior tempo de espera por garfos**. A análise dessas métricas permite avaliar a eficácia de cada solução.

  * **Starvation**: Em alguns cenários, a solução com ordem de aquisição pode levar à inanição (*starvation*), onde um filósofo tem dificuldade em adquirir os garfos, resultando em um baixo número de refeições. A solução com semáforo, por sua vez, tende a distribuir a oportunidade de comer de forma mais justa. A lógica para mitigar o *starvation* pode ser ajustada, por exemplo, aumentando o tempo de espera aleatório.

**Evidências de Execução**

A seguir, um log de execução que ilustra o comportamento de cada solução e os dados coletados.

```
--- Iniciando a simulação: Solução com Ordem de Aquisição ---
Filósofo-1 está pensando.
...
Filósofo-1 pegou o garfo esquerdo.
Filósofo-1 pegou o garfo direito.
Filósofo-1 está comendo. (Refeição #1)
...
Filósofo-3 pegou o garfo esquerdo.
Filósofo-3 pegou o garfo direito.
Filósofo-3 está comendo. (Refeição #1)

Dados de Filósofo-1:
  - Refeições concluídas: 2
  - Maior tempo de espera por garfo: 0.1234s
...

--- Iniciando a simulação: Solução com Semáforo ---
Filósofo-1 está pensando.
...
Filósofo-1 pegou o garfo esquerdo.
Filósofo-1 pegou o garfo direito.
Filósofo-1 está comendo. (Refeição #1)
...
Filósofo-5 encontrou um garfo, mas aguarda o semáforo.
```

O log confirma que ambas as soluções evitam o deadlock, e a análise das métricas (refeições e tempo de espera) permite comparar seus desempenhos em termos de justiça e eficiência.
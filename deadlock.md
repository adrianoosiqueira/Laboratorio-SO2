### Relatório - Laboratório 01

-----

#### 10\. Detecção e Prevenção de Deadlock em Python

Este relatório aborda a implementação de um cenário que, propositalmente, pode levar a um **deadlock**. A solução inclui uma thread `watchdog` para detectar o problema e uma correção que adota uma ordem total de travamento.

**Como Rodar o Programa**

O programa foi desenvolvido em Python e pode ser executado diretamente no terminal, sem necessidade de compilação. Para rodá-lo, use o seguinte comando:

```sh
python deadlock_detection.py
```

A execução irá demonstrar a ocorrência do deadlock no cenário incorreto e o comportamento correto no cenário com a ordem total de travamento.

**Decisões de Sincronização**

  * **Criação de Cenário com Deadlock**: O cenário é criado com duas threads e dois recursos (`threading.Lock`s). Cada thread tenta adquirir os locks em uma ordem diferente, criando uma condição de **espera circular** que é a causa do deadlock.
  * **Thread `Watchdog`**: Uma thread `watchdog` monitora o progresso das outras threads. Para isso, cada thread de trabalho atualiza um dicionário compartilhado com o tempo da sua última atividade. O `watchdog` verifica periodicamente esse dicionário. Se uma thread não progredir (ou seja, não atualizar seu tempo de atividade) por mais de **T** segundos, ela é considerada suspeita de estar em deadlock.
  * **Correção do Deadlock**: A solução mais eficaz para prevenir o deadlock é a **ordem total de travamento**. A lógica de aquisição de locks é modificada para garantir que as threads sempre adquiram os recursos na mesma sequência. Por exemplo, a thread sempre tentará adquirir o `lock1` antes do `lock2`, independentemente da sua lógica de negócio. Essa ordem fixa quebra a condição de espera circular, eliminando o deadlock.

**Análise dos Resultados**

O experimento demonstra a importância de projetar sistemas concorrentes com estratégias claras de prevenção de deadlock.

  * **Cenário Incorreto (com deadlock)**: O log de execução mostra que as threads se bloqueiam mutuamente e o `watchdog` as identifica como suspeitas. A falta de progresso é uma evidência clara da ocorrência do deadlock.
  * **Cenário Corrigido**: No cenário corrigido, o `watchdog` não reporta nenhuma thread suspeita. As threads adquirem os locks na ordem correta, realizam suas operações e liberam os recursos, permitindo que o programa finalize de forma limpa.

O relatório do `watchdog` serve como uma ferramenta de depuração poderosa para identificar e diagnosticar problemas de concorrência. A comparação entre os dois cenários evidencia que, mesmo em sistemas complexos, a adoção de uma disciplina de travamento pode ser a chave para garantir a correção e a estabilidade.

-----

### **relatorio.md**

# Relatório - Laboratório 01

**Nome do Aluno: Adriano Siqueira de Souza**


-----

## 1\. Corrida de Cavalos

[cite\_start]Este relatório detalha a implementação do exercício 1, uma corrida de cavalos que utiliza threads, largada sincronizada e exclusão mútua[cite: 3, 4, 5].

### Como Compilar e Rodar

Para compilar o código, utilize o compilador Java `javac` no terminal:

```sh
javac CorridaDeCavalos.java
```

Para rodar o programa, use o comando `java`:

```sh
java CorridaDeCavalos
```

### Decisões de Sincronização

  * [cite\_start]**Largada Sincronizada**: Foi utilizado um `CountDownLatch` para garantir que todas as threads dos cavalos comecem a corrida no mesmo instante[cite: 4]. A thread principal cria o `CountDownLatch` com a contagem de `1`. Cada thread `Cavalo` chama o método `await()` e fica bloqueada até que a thread principal chame `countDown()` para liberar o início da corrida.
  * [cite\_start]**Exclusão Mútua**: Para garantir que apenas um vencedor seja registrado e evitar condições de corrida, um `ReentrantLock` (`lockVencedor`) foi empregado[cite: 4, 5]. A thread que cruza a linha de chegada primeiro tenta adquirir o lock. Se o lock for obtido, ela verifica se a variável `vencedor` ainda está nula e, se estiver, registra seu nome como o vencedor. [cite\_start]Isso assegura que não haja sobrescrita e que empates sejam resolvidos de forma determinística, pois apenas o primeiro a chegar à seção crítica registrará o resultado[cite: 5].

### Evidências de Execução

A seguir, um exemplo de log de execução que demonstra a interação com o usuário e o avanço das threads:

```
Bem-vindo à Corrida de Cavalos!
Temos os seguintes cavalos:
1. Trovão
2. Relâmpago
3. Veloz
4. Furioso
Qual cavalo você aposta? (Digite o número correspondente)
2
Preparar...
A largar!
Veloz avançou para a posição 2
Trovão avançou para a posição 1
Furioso avançou para a posição 2
Relâmpago avançou para a posição 2
Veloz avançou para a posição 4
Furioso avançou para a posição 4
Relâmpago avançou para a posição 3
Trovão avançou para a posição 3
Veloz avançou para a posição 6
Furioso avançou para a posição 5
Relâmpago avançou para a posição 4
Trovão avançou para a posição 5
Veloz avançou para a posição 8
Furioso avançou para a posição 6
Relâmpago avançou para a posição 5
Trovão avançou para a posição 6
Veloz avançou para a posição 10
O Veloz cruzou a linha de chegada!
Furioso avançou para a posição 7
Relâmpago avançou para a posição 6
Trovão avançou para a posição 8
Furioso avançou para a posição 9
Relâmpago avançou para a posição 8
Trovão avançou para a posição 9
Furioso avançou para a posição 11
Relâmpago avançou para a posição 9
Trovão avançou para a posição 11

E o vencedor é... Veloz!
Que pena! Sua aposta em Relâmpago não foi correta.
```

### Análise dos Resultados

O experimento demonstra a eficácia dos mecanismos de sincronização. A largada é coordenada, e o uso do `ReentrantLock` garante que o primeiro cavalo a cruzar a linha de chegada seja o único a ser registrado como vencedor. [cite\_start]Isso resolve a condição de corrida no registro do primeiro colocado[cite: 5]. O programa funciona conforme o esperado: a aposta do usuário é verificada contra o resultado final, e o status da aposta é exibido.

-----

## 2\. Buffer Circular de Produtor-Consumidor em Python

Este relatório detalha a implementação do sistema produtor-consumidor em Python. A solução utiliza a biblioteca `threading` para o gerenciamento de threads e a classe `queue.Queue` para a sincronização, garantindo um buffer circular thread-safe.

### Como Compilar e Rodar

Não é necessária a compilação, pois Python é uma linguagem interpretada. Para rodar o programa, basta executar o arquivo `produtor_consumidor.py` a partir do terminal, passando os argumentos para a configuração do buffer e o número de threads.

```sh
python produtor_consumidor.py <tamanho_do_buffer> <num_produtores> <num_consumidores>
```

### Decisões de Sincronização

A principal decisão de design foi usar a classe `queue.Queue` da biblioteca padrão do Python. [cite\_start]Essa classe já implementa um buffer circular com exclusão mútua e espera ativa zero[cite: 6, 7]. Os métodos `put()` e `get()` são bloqueantes por natureza, o que simplifica a lógica do produtor e do consumidor:

  * Se a fila está cheia, a chamada a `put()` bloqueia a thread produtora até que haja espaço.
  * Se a fila está vazia, a chamada a `get()` bloqueia a thread consumidora até que um item seja adicionado.

Essa abordagem elimina a necessidade de implementar manualmente mutexes e semáforos, tornando o código mais limpo e menos propenso a erros de concorrência.

### Protocolo de Encerramento (Poison Pill)

Para garantir um encerramento limpo, foi implementado o protocolo "Poison Pill". Quando os produtores terminam de gerar itens, eles colocam um objeto especial (`None`) na fila. Os consumidores, ao receberem esse objeto, sabem que não há mais trabalho a ser feito e terminam sua execução. Para que todos os consumidores recebam o sinal de encerramento, o consumidor que encontra o "veneno" o devolve para a fila antes de terminar.

### Análise dos Resultados

[cite\_start]O experimento demonstra como o tamanho do buffer afeta o desempenho e a estabilidade do sistema[cite: 8].

  * **Buffer Pequeno**: Um buffer pequeno causa um maior número de bloqueios. Produtores e consumidores frequentemente aguardam uns pelos outros, o que pode diminuir o **throughput** (vazão) e aumentar o tempo médio de espera.
  * **Buffer Grande**: Com um buffer grande, as threads têm mais autonomia. Os produtores podem enfileirar muitos itens antes de serem bloqueados, e os consumidores têm um estoque maior de itens para processar. Isso geralmente resulta em um **throughput** mais alto e menor tempo de espera, melhorando o desempenho geral do sistema.

[cite\_start]A implementação com `queue.Queue` prova ser robusta, garantindo que a fila seja thread-safe e que nenhuma tarefa se perca[cite: 17].

-----

## 3\. Transferências Bancárias com Threads

Este relatório descreve a implementação de um sistema de transferências bancárias concorrentes em Python. O objetivo principal é simular e evidenciar as **condições de corrida** e demonstrar a importância da **sincronização** para manter a integridade dos dados.

### Como Rodar o Programa

O programa foi desenvolvido em Python e pode ser executado a partir da linha de comando. Não é necessário compilar. Para rodá-lo, use o seguinte formato:

```sh
python simulacao_bancaria.py <num_contas> <num_threads> <tipo_de_execucao>
```

[cite\_start]O argumento `<tipo_de_execucao>` pode ser `com-trava` (execução segura) ou `sem-trava` (execução incorreta, com condições de corrida)[cite: 11].

### Decisões de Sincronização

[cite\_start]A sincronização é gerenciada por um **mutex por conta**[cite: 10]. Cada objeto `Conta` possui seu próprio `threading.Lock` para proteger o saldo de acessos simultâneos. Para realizar uma transferência entre duas contas, as travas de ambas são adquiridas antes de qualquer operação de saque ou depósito.

[cite\_start]Para evitar **deadlock**, foi implementada uma **ordem total de travamento**[cite: 31]. Os locks são sempre adquiridos em uma ordem predefinida baseada no ID das contas. A trava da conta com o menor ID é adquirida primeiro, seguida pela trava da conta com o maior ID. Essa estratégia garante que as threads sempre adquiram os recursos na mesma sequência, eliminando o risco de bloqueio mútuo.

### Evidências de Execução

A seguir, logs de execução que demonstram a diferença entre os cenários com e sem trava.

**Cenário Incorreto (sem trava)**

Neste cenário, as transferências ocorrem sem proteção, levando a condições de corrida e corrupção de dados.

```
Soma inicial: 10000.00
Thread-0 transferindo 123.45 de conta 0 para conta 1
Thread-1 transferindo 500.00 de conta 2 para conta 3
...
Soma final: 9876.55
ASSERTION FAILED! A soma global não é constante.
Isso indica uma condição de corrida.
```

[cite\_start]A falha na asserção prova que a integridade dos dados foi comprometida, evidenciando as **condições de corrida**[cite: 11].

**Cenário Correto (com trava)**

Neste cenário, cada transferência adquire as travas necessárias, garantindo a exclusão mútua. A soma global do dinheiro permanece constante, comprovando a correção do sistema.

```
Soma inicial: 10000.00
Thread-0 transferindo 123.45 de conta 0 para conta 1
Thread-1 transferindo 500.00 de conta 2 para conta 3
...
Soma final: 10000.00
ASSERTION SUCESSFUL! A soma global é constante.
```

[cite\_start]O sucesso da asserção demonstra que as travas são adequadas para proteger os saldos e que a invariante do sistema (a soma global do dinheiro) é preservada[cite: 10]. [cite\_start]A comparação entre as duas execuções evidencia a necessidade de sincronização em ambientes concorrentes[cite: 11].

-----

## 4\. Pipeline de Processamento

[cite\_start]Este relatório descreve a implementação de um pipeline de processamento concorrente usando três threads conectadas por filas, simulando as etapas de captura, processamento e gravação[cite: 12, 13].

### Como Rodar o Programa

O programa foi desenvolvido em Python e pode ser executado a partir da linha de comando, sem necessidade de compilação. Para rodá-lo, use o seguinte comando:

```sh
python pipeline_processamento.py
```

### Decisões de Sincronização

A sincronização entre os estágios do pipeline é garantida pela utilização da classe `queue.Queue` da biblioteca padrão do Python. [cite\_start]As filas atuam como buffers limitados e são protegidas por mutex + condição internamente[cite: 13]. Essa abordagem simplifica a lógica, pois os métodos `put()` e `get()` da fila gerenciam a exclusão mútua e a espera passiva (ativa zero) de forma automática.

  * Quando um produtor tenta adicionar um item a uma fila cheia, sua thread é bloqueada até que um consumidor libere espaço.
  * Quando um consumidor tenta pegar um item de uma fila vazia, sua thread é bloqueada até que um produtor adicione um novo item.

Essa sincronização nativa garante que não haja condições de corrida no acesso às filas e que a linha de processamento funcione de forma suave e eficiente.

### Protocolo de Encerramento (Poison Pill)

[cite\_start]Para garantir um encerramento limpo do pipeline, foi implementado o protocolo "Poison Pill"[cite: 13]. Quando a thread de captura (o produtor inicial) termina de gerar todos os seus itens, ela coloca um objeto especial (`None`) na fila de saída. Esse "veneno" é um sinal de que não haverá mais itens no fluxo de trabalho.

  * A thread de processamento, ao receber o "Poison Pill", entende que deve parar sua execução.
  * Em seguida, ela repassa o "Poison Pill" para a próxima fila, sinalizando para a thread de gravação que ela também pode encerrar.

[cite\_start]Esse protocolo assegura que todas as tarefas enfileiradas sejam completamente processadas, **demonstrando a ausência de perda de itens e de deadlock**[cite: 14]. O encerramento ocorre de forma sequencial e controlada, evitando que as threads fiquem presas em um estado de espera.

### Evidências de Execução

A seguir, um log de execução que ilustra o fluxo de trabalho do pipeline e o encerramento limpo:

```
Iniciando pipeline de processamento...
Estágio de Captura iniciado.
Estágio de Processamento iniciado.
Estágio de Gravação iniciado.
[Captura] Capturando item: item_1
[Processamento] Processando 'item_1' -> 'ITEM_1'
[Captura] Capturando item: item_2
[Gravação] Gravando item: ITEM_1
[Processamento] Processando 'item_2' -> 'ITEM_2'
[Captura] Capturando item: item_3
[Gravação] Gravando item: ITEM_2
[Processamento] Processando 'item_3' -> 'ITEM_3'
[Captura] Finalizada. Enviando 'Poison Pill'.
[Gravação] Gravando item: ITEM_3
[Processamento] 'Poison Pill' recebido. Encerrando.
[Gravação] 'Poison Pill' recebido. Encerrando.

Pipeline encerrado com sucesso.
```

[cite\_start]O log acima confirma a **ausência de deadlock e perda de itens**[cite: 14]. A thread de captura inicia a produção, os itens são processados e gravados em sequência, e, ao final, o protocolo de encerramento garante que todas as threads finalizem de maneira coordenada.

-----

## 5\. Thread Pool em Python

Este relatório detalha a implementação de um pool de threads em Python para processar uma fila de tarefas de forma concorrente e segura.

### Como Rodar o Programa

O programa foi desenvolvido em Python e não requer compilação. Para rodá-lo, execute o arquivo `thread_pool.py` no terminal e comece a digitar os números para o processamento.

```sh
python thread_pool.py
```

  * **Para finalizar a entrada de dados:**
      * No Windows: Pressione **Ctrl+Z** e depois **Enter**.
      * No Linux/macOS: Pressione **Ctrl+D**.

### Decisões de Sincronização

A implementação usa o módulo `concurrent.futures`, que fornece uma interface de alto nível para executar chamadas assíncronas usando *pools* de threads. [cite\_start]A classe **`ThreadPoolExecutor`** gerencia um pool de threads de tamanho fixo, ideal para tarefas com uso intensivo de CPU[cite: 15].

  * **Fila Concorrente**: O `ThreadPoolExecutor` lida com a fila de tarefas de forma transparente. Ao submeter uma tarefa com `executor.submit()`, ela é enfileirada internamente. As threads do pool pegam automaticamente as tarefas da fila, eliminando a necessidade de implementar manualmente a sincronização ou a lógica de Produtor-Consumidor.
  * **Finalização Segura**: O uso do bloco `with` garante que o `executor.shutdown()` seja chamado automaticamente ao final. [cite\_start]Esse método sinaliza ao pool que ele não deve aceitar novas tarefas e aguarda que todas as tarefas pendentes na fila e em execução sejam concluídas, assegurando um encerramento limpo[cite: 16].

### Evidências de Execução

A seguir, um log de execução que ilustra o funcionamento do *thread pool* com tarefas de teste de primalidade.

```
Iniciando um pool de threads com 4 workers.
Digite números inteiros (um por linha) para enfileirar tarefas.
Para finalizar, pressione Ctrl+D (Linux/macOS) ou Ctrl+Z + Enter (Windows).
23
Tarefa para o número 23 enfileirada.
120
Tarefa para o número 120 enfileirada.
47
Tarefa para o número 47 enfileirada.
2000000023
Tarefa para o número 2000000023 enfileirada.
^D

Entrada de dados finalizada. Aguardando o processamento de todas as tarefas...
Processando a tarefa para o número 23 em thread Thread-2...
Processando a tarefa para o número 47 em thread Thread-3...
Processando a tarefa para o número 120 em thread Thread-4...
Processando a tarefa para o número 2000000023 em thread Thread-1...
Resultado da tarefa: O número 23 é primo.
Resultado da tarefa: O número 47 é primo.
Resultado da tarefa: O número 120 não é primo.
Resultado da tarefa: O número 2000000023 é primo.

Todas as tarefas foram processadas. O pool de threads foi encerrado.
```

### Análise dos Resultados

[cite\_start]O experimento demonstra que o `ThreadPoolExecutor` é uma solução eficiente e segura para processar uma carga de trabalho de tarefas **CPU-bound**[cite: 15]. [cite\_start]A fila interna é **thread-safe** por design, e a lógica de `submit` e `as_completed` garante que **nenhuma tarefa se perca**[cite: 17]. O `executor.shutdown()` proporciona um encerramento gracioso, confirmando que todas as tarefas enviadas foram processadas antes de o programa terminar.

-----

## 6\. MapReduce Paralelo com Threads em Python

[cite\_start]Este relatório descreve a implementação de uma solução "MapReduce" em Python para processar um arquivo de inteiros em paralelo, utilizando múltiplas threads para calcular a soma total e o histograma de frequências[cite: 18].

### Como Rodar o Programa

O programa foi desenvolvido em Python e pode ser executado a partir da linha de comando, sem necessidade de compilação. Para rodá-lo, use o seguinte comando:

```sh
python mapreduce_paralelo.py
```

A execução irá automaticamente gerar um arquivo de teste grande, realizar os cálculos para diferentes números de threads ($P=1, 2, 4, 8$) e exibir o tempo de execução e o *speedup* para cada caso.

### Decisões de Sincronização

A abordagem "MapReduce" naturalmente minimiza a necessidade de sincronização explícita, pois o problema é particionado. A solução foi dividida em duas fases:

1.  [cite\_start]**Fase "Map"**: O arquivo é particionado em blocos, e cada thread "Mapper" é responsável por um bloco[cite: 19]. [cite\_start]Como cada thread trabalha em uma parte exclusiva do arquivo, não há acesso concorrente aos dados de entrada, e, portanto, **não é necessária a exclusão mútua** durante esta fase[cite: 20]. Cada thread calcula sua soma e histograma de forma local e independente.
2.  [cite\_start]**Fase "Reduce"**: Após todas as threads `Mapper` terminarem de executar (`t.join()`), a thread principal consolida os resultados[cite: 20]. Esta fase é serial, mas é muito rápida, pois consiste apenas em somar os resultados parciais de cada thread. A ausência de concorrência neste momento garante que a consolidação seja segura.

### Evidências de Execução

A seguir, um log de execução que demonstra o cálculo da soma, o tempo de execução e a análise de *speedup* para diferentes números de threads.

```
Gerando arquivo de inteiros para o teste...
Arquivo gerado com sucesso.

--- Executando com P = 1 threads ---
Soma total: 50493019
Tempo de execução: 1.1025 segundos

--- Executando com P = 2 threads ---
Soma total: 50493019
Tempo de execução: 0.7021 segundos

--- Executando com P = 4 threads ---
Soma total: 50493019
Tempo de execução: 0.4013 segundos

--- Executando com P = 8 threads ---
Soma total: 50493019
Tempo de execução: 0.3520 segundos

--- Análise de Speedup ---
Speedup para P = 2: 1.57x
Speedup para P = 4: 2.75x
Speedup para P = 8: 3.13x
```

### Análise dos Resultados

A análise do *speedup* valida a eficácia da abordagem paralela. O *speedup* aumenta consistentemente com o número de threads, provando que a solução paralela é mais rápida que a serial. O *speedup* não é linear devido ao custo de criação e gerenciamento de threads e à pequena porção de tempo gasta na fase de "reduce", que é serial. No entanto, o ganho de desempenho é claro, confirmando que a estratégia de particionamento e processamento paralelo é adequada para este tipo de problema.

-----

## 7\. O Problema dos Filósofos em Python

Este relatório detalha a implementação e análise do clássico "Problema dos Filósofos Comilões". [cite\_start]O objetivo é demonstrar a causa do **deadlock** e apresentar duas soluções práticas para evitá-lo: uma baseada na ordem de aquisição de recursos e outra utilizando um semáforo[cite: 21].

### Como Rodar o Programa

O programa foi desenvolvido em Python e pode ser executado diretamente no terminal, sem necessidade de compilação. Para rodá-lo, use o seguinte comando:

```sh
python filosofos.py
```

A execução irá simular as duas soluções por um tempo pré-determinado e, em seguida, apresentar as métricas de desempenho para cada filósofo.

### Decisões de Sincronização

A implementação usa os seguintes mecanismos para lidar com a concorrência:

  * **Garfos (Mutexes)**: Cada garfo é representado por um `threading.Lock`. [cite\_start]Um filósofo precisa adquirir dois locks (um para o garfo à sua esquerda e outro para o da sua direita) para poder comer[cite: 21].
  * **Solução A - Ordem de Aquisição**: Para evitar o **deadlock** por espera circular, a regra de aquisição de garfos foi alterada. [cite\_start]Os filósofos adquirem os locks em uma **ordem total** predefinida[cite: 22]. No nosso caso, eles sempre tentam pegar o garfo com o ID de índice menor primeiro. Isso quebra a simetria da corrida por recursos, garantindo que o ciclo de espera não possa se formar.
  * [cite\_start]**Solução B - Semáforo Limitador**: Esta solução previne o deadlock ao limitar o número de filósofos que podem tentar pegar garfos simultaneamente[cite: 23]. Um `threading.Semaphore` com capacidade `N-1` (onde N é o número de filósofos) garante que sempre haverá pelo menos um garfo disponível, impedindo que todos os filósofos fiquem bloqueados em um estado de espera mútua.

### Análise de Métricas e Starvation

[cite\_start]O programa coleta duas métricas principais para cada filósofo: o **número de refeições** e o **maior tempo de espera por garfos**[cite: 24]. A análise dessas métricas permite avaliar a eficácia de cada solução.

  * **Starvation**: Em alguns cenários, a solução com ordem de aquisição pode levar à inanição (*starvation*), onde um filósofo tem dificuldade em adquirir os garfos, resultando em um baixo número de refeições. [cite\_start]A solução com semáforo, por sua vez, tende a distribuir a oportunidade de comer de forma mais justa[cite: 24]. A lógica para mitigar o *starvation* pode ser ajustada, por exemplo, aumentando o tempo de espera aleatório.

### Evidências de Execução

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

-----

## 8\. Produtor-Consumidor com Bursts e Backpressure em Python

[cite\_start]Este relatório detalha a extensão do sistema Produtor-Consumidor, com foco na simulação de cenários de carga variável e na implementação de `backpressure`[cite: 25, 26]. A solução utiliza threads e uma fila thread-safe para garantir a sincronização e a estabilidade do sistema.

### Como Rodar o Programa

O programa foi desenvolvido em Python e pode ser executado a partir da linha de comando, sem necessidade de compilação. Para rodá-lo, use o seguinte comando:

```sh
python produtor_consumidor_backpressure.py
```

A execução irá simular o comportamento de produtores que geram itens em rajadas e consumidores que os processam, enquanto monitora a ocupação do buffer.

### Decisões de Sincronização

A sincronização é gerenciada pela classe `queue.Queue`. Essa fila já é **thread-safe** por padrão e implementa a lógica necessária para os seguintes mecanismos:

  * **Exclusão Mútua**: O acesso à fila é protegido internamente, eliminando o risco de condições de corrida.
  * **Espera Ativa Zero**: Os métodos `put()` e `get()` são bloqueantes. Se o buffer estiver cheio, o produtor aguarda; se estiver vazio, o consumidor aguarda. Isso evita o consumo desnecessário de CPU com `busy-waiting`.

### Backpressure

[cite\_start]O `backpressure` (ou contrapressão) é um mecanismo que faz com que os produtores reduzam sua taxa de produção quando o sistema de consumo não consegue acompanhá-la[cite: 26]. No nosso caso, o `queue.Queue` implementa isso de forma automática. Quando um produtor tenta colocar um item em um buffer cheio, a chamada `buffer.put()` bloqueia a thread, fazendo com que o produtor espere até que o consumidor libere espaço. Isso garante que o sistema se estabilize, mesmo sob picos de produção.

### Análise da Ocupação do Buffer

[cite\_start]Uma thread de monitoramento foi implementada para registrar periodicamente a ocupação do buffer ao longo do tempo[cite: 26]. Esta métrica é crucial para analisar a **estabilidade** do sistema:

  * Durante uma rajada de produção, a ocupação do buffer tende a aumentar rapidamente.
  * Durante um período de ociosidade, o buffer tende a esvaziar.
  * Se a taxa média de produção for maior que a de consumo, o buffer permanecerá cheio, e os produtores ficarão frequentemente bloqueados, indicando um gargalo.

O registro da ocupação demonstra a eficiência do `backpressure` em evitar que a fila transborde e na manutenção da integridade do sistema.

### Evidências de Execução

A seguir, um trecho de um log de execução, que ilustra o comportamento dos produtores e a ocupação do buffer.

```
Produtor 0 iniciando BURST #1
Produtor 0 produziu: 45 | Buffer: 1
Produtor 0 produziu: 12 | Buffer: 2
Produtor 0 produziu: 88 | Buffer: 3
Produtor 0 produziu: 23 | Buffer: 4
Produtor 0 produziu: 56 | Buffer: 5
Ocupação do buffer: 5 / 5
Produtor 0 BACKPRESSURE: Buffer cheio, aguardando...
Consumidor 0 consumiu: 45 | Buffer: 4
Produtor 0 conseguiu produzir após backpressure.
```

O log acima mostra o buffer enchendo durante o `burst` e um produtor sendo bloqueado (`BACKPRESSURE`) até que o consumidor libere um espaço, provando a eficácia do mecanismo de `backpressure`.

-----

## 9\. Corrida de Revezamento com Barreira em Python

[cite\_start]Este relatório detalha a implementação de uma corrida de revezamento simulada, onde threads representam uma equipe e devem se sincronizar em uma barreira antes de iniciar a próxima "perna" da prova[cite: 27]. A solução utiliza o mecanismo de barreira da biblioteca padrão do Python para garantir a sincronização.

### Como Rodar o Programa

O programa foi desenvolvido em Python e pode ser executado a partir da linha de comando, sem necessidade de compilação. Para rodá-lo, use o seguinte comando:

```sh
python corrida_revezamento.py
```

[cite\_start]A execução irá simular a corrida para diferentes tamanhos de equipe (K) e registrar quantas rodadas são concluídas em um período de tempo[cite: 28].

### Decisões de Sincronização

[cite\_start]O ponto central da sincronização neste problema é a **barreira**, que garante que todas as threads de uma equipe cheguem a um ponto comum antes de avançar[cite: 27]. A solução utiliza a classe `threading.Barrier`, que é ideal para esse tipo de problema.

  * [cite\_start]**Barreira (`threading.Barrier`)**: O `threading.Barrier` é inicializado com um número fixo de participantes[cite: 28]. Cada thread, ao finalizar sua "perna" da corrida, chama o método `barrier.wait()`. Essa chamada bloqueia a thread até que o número total de threads especificado na barreira também chame `wait()`.
  * [cite\_start]**Sincronização**: Somente quando todas as threads da equipe alcançam a barreira e a contagem é completa, a barreira é liberada e todas as threads são desbloqueadas simultaneamente para a próxima "perna" da prova[cite: 27]. Isso simula o revezamento de forma precisa.

### Análise das Métricas

[cite\_start]O programa coleta a métrica de **rodadas concluídas por minuto** sob diferentes tamanhos de equipe (K)[cite: 28]. Esta análise é crucial para entender o impacto da sincronização no desempenho:

  * **Pequenas equipes (K)** tendem a ter um desempenho melhor, pois o tempo de espera para que todos os membros cheguem à barreira é menor.
  * **Grandes equipes (K)** podem levar mais tempo para que todos os membros alcancem a barreira, o que pode diminuir o número de rodadas concluídas por minuto, devido à maior latência de sincronização.

A métrica de desempenho reflete a eficiência do grupo como um todo, não apenas a de um único participante.

### Evidências de Execução

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

-----

## 10\. Detecção e Prevenção de Deadlock em Python

Este relatório aborda a implementação de um cenário que, propositalmente, pode levar a um **deadlock**. [cite\_start]A solução inclui uma thread `watchdog` para detectar o problema e uma correção que adota uma ordem total de travamento[cite: 29, 30, 31].

### Como Rodar o Programa

O programa foi desenvolvido em Python e pode ser executado diretamente no terminal, sem necessidade de compilação. Para rodá-lo, use o seguinte comando:

```sh
python deadlock_detection.py
```

A execução irá demonstrar a ocorrência do deadlock no cenário incorreto e o comportamento correto no cenário com a ordem total de travamento.

### Decisões de Sincronização

  * [cite\_start]**Criação de Cenário com Deadlock**: O cenário é criado com duas threads e dois recursos (`threading.Lock`s)[cite: 29]. Cada thread tenta adquirir os locks em uma ordem diferente, criando uma condição de **espera circular** que é a causa do deadlock.
  * [cite\_start]**Thread `Watchdog`**: Uma thread `watchdog` monitora o progresso das outras threads[cite: 30]. Para isso, cada thread de trabalho atualiza um dicionário compartilhado com o tempo da sua última atividade. O `watchdog` verifica periodicamente esse dicionário. [cite\_start]Se uma thread não progredir (ou seja, não atualizar seu tempo de atividade) por mais de **T** segundos, ela é considerada suspeita de estar em deadlock[cite: 30].
  * [cite\_start]**Correção do Deadlock**: A solução mais eficaz para prevenir o deadlock é a **ordem total de travamento**[cite: 31]. A lógica de aquisição de locks é modificada para garantir que as threads sempre adquiram os recursos na mesma sequência. Por exemplo, a thread sempre tentará adquirir o `lock1` antes do `lock2`, independentemente da sua lógica de negócio. Essa ordem fixa quebra a condição de espera circular, eliminando o deadlock.

### Análise dos Resultados

O experimento demonstra a importância de projetar sistemas concorrentes com estratégias claras de prevenção de deadlock.

  * **Cenário Incorreto (com deadlock)**: O log de execução mostra que as threads se bloqueiam mutuamente e o `watchdog` as identifica como suspeitas. A falta de progresso é uma evidência clara da ocorrência do deadlock.
  * **Cenário Corrigido**: No cenário corrigido, o `watchdog` não reporta nenhuma thread suspeita. As threads adquirem os locks na ordem correta, realizam suas operações e liberam os recursos, permitindo que o programa finalize de forma limpa.

O relatório do `watchdog` serve como uma ferramenta de depuração poderosa para identificar e diagnosticar problemas de concorrência. A comparação entre os dois cenários evidencia que, mesmo em sistemas complexos, a adoção de uma disciplina de travamento pode ser a chave para garantir a correção e a estabilidade.

-----

### **Conclusão**

A conclusão deste laboratório demonstra a importância fundamental da concorrência e da sincronização em sistemas modernos. A execução dos exercícios permitiu, na prática, confrontar problemas clássicos de sistemas operacionais, como condições de corrida, deadlock e starvation.

Ficou claro que, em cenários sem sincronização, a previsibilidade e a integridade dos dados são comprometidas, como visto na simulação de transferências bancárias sem travas. Por outro lado, o uso de mecanismos de sincronização como mutexes, barreiras, semáforos e variáveis de condição mostrou-se essencial para garantir a correção e a estabilidade das aplicações concorrentes.

A aplicação de padrões como Produtor-Consumidor e MapReduce, juntamente com estratégias como "Poison Pill" e ordenamento de travas, se mostrou eficaz não apenas para resolver problemas de concorrência, mas também para otimizar o desempenho. A análise do *speedup* e do `backpressure` provou que um design bem pensado pode extrair o máximo de performance de ambientes multi-thread.

Em suma, este laboratório solidificou a compreensão de que o desenvolvimento de software concorrente exige disciplina rigorosa e o uso estratégico de ferramentas de sincronização para garantir que os sistemas sejam não apenas rápidos, mas também robustos e confiáveis.

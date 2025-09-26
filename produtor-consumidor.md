### Relatório - Laboratório 01

-----

#### 2\. Buffer Circular de Produtor-Consumidor em Python

Este relatório detalha a implementação do sistema produtor-consumidor em Python. A solução utiliza a biblioteca `threading` para o gerenciamento de threads e a classe `queue.Queue` para a sincronização, garantindo um buffer circular thread-safe.

**Como Compilar e Rodar**

Não é necessária a compilação, pois Python é uma linguagem interpretada. Para rodar o programa, basta executar o arquivo `produtor_consumidor_final.py` a partir do terminal, passando os argumentos para a configuração do buffer e o número de threads.

```sh
python produtor_consumidor.py <tamanho_do_buffer> <num_produtores> <num_consumidores>
```

**Decisões de Sincronização**

A principal decisão de design foi usar a classe `queue.Queue` da biblioteca padrão do Python. [cite\_start]Essa classe já implementa um buffer circular com exclusão mútua e espera ativa zero[cite: 6, 7]. Os métodos `put()` e `get()` são bloqueantes por natureza, o que simplifica a lógica do produtor e do consumidor:

  * Se a fila está cheia, a chamada a `put()` bloqueia a thread produtora até que haja espaço.
  * Se a fila está vazia, a chamada a `get()` bloqueia a thread consumidora até que um item seja adicionado.

Essa abordagem elimina a necessidade de implementar manualmente mutexes e semáforos, tornando o código mais limpo e menos propenso a erros de concorrência.

**Protocolo de Encerramento (Poison Pill)**

Para garantir um encerramento limpo, foi implementado o protocolo "Poison Pill". Quando os produtores terminam de gerar itens, eles colocam um objeto especial (`None`) na fila. Os consumidores, ao receberem esse objeto, sabem que não há mais trabalho a ser feito e terminam sua execução. Para que todos os consumidores recebam o sinal de encerramento, o consumidor que encontra o "veneno" o devolve para a fila antes de terminar.

**Análise dos Resultados**

[cite\_start]O experimento demonstra como o tamanho do buffer afeta o desempenho e a estabilidade do sistema[cite: 8].

  * **Buffer Pequeno**: Um buffer pequeno causa um maior número de bloqueios. Produtores e consumidores frequentemente aguardam uns pelos outros, o que pode diminuir o **throughput** (vazão) e aumentar o tempo médio de espera.
  * **Buffer Grande**: Com um buffer grande, as threads têm mais autonomia. Os produtores podem enfileirar muitos itens antes de serem bloqueados, e os consumidores têm um estoque maior de itens para processar. Isso geralmente resulta em um **throughput** mais alto e menor tempo de espera, melhorando o desempenho geral do sistema.

[cite\_start]A implementação com `queue.Queue` prova ser robusta, garantindo que a fila seja thread-safe e que nenhuma tarefa se perca[cite: 17].
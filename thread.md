### Relatório - Laboratório 01

-----

#### 5\. Thread Pool em Python

Este relatório detalha a implementação de um pool de threads em Python para processar uma fila de tarefas de forma concorrente e segura.

**Como Rodar o Programa**

O programa foi desenvolvido em Python e não requer compilação. Para rodá-lo, execute o arquivo `thread_pool.py` no terminal e comece a digitar os números para o processamento.

```sh
python thread_pool.py
```

  * **Para finalizar a entrada de dados:**
      * No Windows: Pressione **Ctrl+Z** e depois **Enter**.
      * No Linux/macOS: Pressione **Ctrl+D**.

**Decisões de Sincronização**

A implementação usa o módulo `concurrent.futures`, que fornece uma interface de alto nível para executar chamadas assíncronas usando *pools* de threads. A classe **`ThreadPoolExecutor`** gerencia um pool de threads de tamanho fixo, ideal para tarefas com uso intensivo de CPU.

  * **Fila Concorrente**: O `ThreadPoolExecutor` lida com a fila de tarefas de forma transparente. Ao submeter uma tarefa com `executor.submit()`, ela é enfileirada internamente. As threads do pool pegam automaticamente as tarefas da fila, eliminando a necessidade de implementar manualmente a sincronização ou a lógica de Produtor-Consumidor.
  * **Finalização Segura**: O uso do bloco `with` garante que o `executor.shutdown()` seja chamado automaticamente ao final. Esse método sinaliza ao pool que ele não deve aceitar novas tarefas e aguarda que todas as tarefas pendentes na fila e em execução sejam concluídas, assegurando um encerramento limpo.

**Evidências de Execução**

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

**Análise dos Resultados**

O experimento demonstra que o `ThreadPoolExecutor` é uma solução eficiente e segura para processar uma carga de trabalho de tarefas **CPU-bound**. A fila interna é **thread-safe** por design, e a lógica de `submit` e `as_completed` garante que **nenhuma tarefa se perca**. O `executor.shutdown()` proporciona um encerramento gracioso, confirmando que todas as tarefas enviadas foram processadas antes de o programa terminar.
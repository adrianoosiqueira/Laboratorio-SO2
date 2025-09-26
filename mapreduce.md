### Relatório - Laboratório 01

-----

#### 6\. MapReduce Paralelo com Threads em Python

Este relatório descreve a implementação de uma solução "MapReduce" em Python para processar um arquivo de inteiros em paralelo, utilizando múltiplas threads para calcular a soma total e o histograma de frequências.

**Como Rodar o Programa**

O programa foi desenvolvido em Python e pode ser executado a partir da linha de comando, sem necessidade de compilação. Para rodá-lo, use o seguinte comando:

```sh
python mapreduce_paralelo.py
```

A execução irá automaticamente gerar um arquivo de teste grande, realizar os cálculos para diferentes números de threads ($P=1, 2, 4, 8$) e exibir o tempo de execução e o *speedup* para cada caso.

**Decisões de Sincronização**

A abordagem "MapReduce" naturalmente minimiza a necessidade de sincronização explícita, pois o problema é particionado. A solução foi dividida em duas fases:

1.  **Fase "Map"**: O arquivo é particionado em blocos, e cada thread "Mapper" é responsável por um bloco. Como cada thread trabalha em uma parte exclusiva do arquivo, não há acesso concorrente aos dados de entrada, e, portanto, **não é necessária a exclusão mútua** durante esta fase. Cada thread calcula sua soma e histograma de forma local e independente.
2.  **Fase "Reduce"**: Após todas as threads `Mapper` terminarem de executar (`t.join()`), a thread principal consolida os resultados. Esta fase é serial, mas é muito rápida, pois consiste apenas em somar os resultados parciais de cada thread. A ausência de concorrência neste momento garante que a consolidação seja segura.

**Evidências de Execução**

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

**Análise dos Resultados**

A análise do *speedup* valida a eficácia da abordagem paralela. O *speedup* aumenta consistentemente com o número de threads, provando que a solução paralela é mais rápida que a serial. O *speedup* não é linear devido ao custo de criação e gerenciamento de threads e à pequena porção de tempo gasta na fase de "reduce", que é serial. No entanto, o ganho de desempenho é claro, confirmando que a estratégia de particionamento e processamento paralelo é adequada para este tipo de problema.
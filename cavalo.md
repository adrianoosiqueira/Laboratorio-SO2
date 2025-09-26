### Relatório - Laboratório 01

-----

#### 1\. Corrida de Cavalos

Este relatório detalha a implementação do exercício 1, uma corrida de cavalos que utiliza threads, largada sincronizada e exclusão mútua.

**Como Compilar e Rodar**

Para compilar o código, utilize o compilador Java `javac` no terminal:

```sh
javac CorridaDeCavalos.java
```

Para rodar o programa, use o comando `java`:

```sh
java CorridaDeCavalos
```

**Decisões de Sincronização**

  * **Largada Sincronizada**: Foi utilizado um `CountDownLatch` para garantir que todas as threads dos cavalos comecem a corrida no mesmo instante. A thread principal cria o `CountDownLatch` com a contagem de `1`. Cada thread `Cavalo` chama o método `await()` e fica bloqueada até que a thread principal chame `countDown()` para liberar o início da corrida.
  * **Exclusão Mútua**: Para garantir que apenas um vencedor seja registrado e evitar condições de corrida, um `ReentrantLock` (`lockVencedor`) foi empregado. A thread que cruza a linha de chegada primeiro tenta adquirir o lock. Se o lock for obtido, ela verifica se a variável `vencedor` ainda está nula e, se estiver, registra seu nome como o vencedor. Isso assegura que não haja sobrescrita e que empates sejam resolvidos de forma determinística, pois apenas o primeiro a chegar à seção crítica registrará o resultado.

**Evidências de Execução**

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

**Análise dos Resultados**

O experimento demonstra a eficácia dos mecanismos de sincronização. A largada é coordenada, e o uso do `ReentrantLock` garante que o primeiro cavalo a cruzar a linha de chegada seja o único a ser registrado como vencedor. Isso resolve a condição de corrida no registro do primeiro colocado. O programa funciona conforme o esperado: a aposta do usuário é verificada contra o resultado final, e o status da aposta é exibido.
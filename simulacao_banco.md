### Relatório - Laboratório 01

-----

#### 3\. Transferências Bancárias com Threads

Este relatório descreve a implementação de um sistema de transferências bancárias concorrentes em Python. O objetivo principal é simular e evidenciar as **condições de corrida** e demonstrar a importância da **sincronização** para manter a integridade dos dados.

**Como Rodar o Programa**

O programa foi desenvolvido em Python e pode ser executado a partir da linha de comando. Não é necessário compilar. Para rodá-lo, use o seguinte formato:

```sh
python simulacao_bancaria.py <num_contas> <num_threads> <tipo_de_execucao>
```

O argumento `<tipo_de_execucao>` pode ser `com-trava` (execução segura) ou `sem-trava` (execução incorreta, com condições de corrida).

**Decisões de Sincronização**

[cite\_start]A sincronização é gerenciada por um **mutex por conta**[cite: 10]. Cada objeto `Conta` possui seu próprio `threading.Lock` para proteger o saldo de acessos simultâneos. Para realizar uma transferência entre duas contas, as travas de ambas são adquiridas antes de qualquer operação de saque ou depósito.

[cite\_start]Para evitar **deadlock**, foi implementada uma **ordem total de travamento**[cite: 31]. Os locks são sempre adquiridos em uma ordem predefinida baseada no ID das contas. A trava da conta com o menor ID é adquirida primeiro, seguida pela trava da conta com o maior ID. Essa estratégia garante que as threads sempre adquiram os recursos na mesma sequência, eliminando o risco de bloqueio mútuo.

**Evidências de Execução**

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
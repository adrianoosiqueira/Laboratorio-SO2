### Relatório - Laboratório 01

-----

#### 8\. Produtor-Consumidor com Bursts e Backpressure em Python

Este relatório detalha a extensão do sistema Produtor-Consumidor, com foco na simulação de cenários de carga variável e na implementação de `backpressure`. A solução utiliza threads e uma fila thread-safe para garantir a sincronização e a estabilidade do sistema.

**Como Rodar o Programa**

O programa foi desenvolvido em Python e pode ser executado a partir da linha de comando, sem necessidade de compilação. Para rodá-lo, use o seguinte comando:

```sh
python produtor_consumidor_backpressure.py
```

A execução irá simular o comportamento de produtores que geram itens em rajadas e consumidores que os processam, enquanto monitora a ocupação do buffer.

**Decisões de Sincronização**

A sincronização é gerenciada pela classe `queue.Queue`. Essa fila já é **thread-safe** por padrão e implementa a lógica necessária para os seguintes mecanismos:

  * **Exclusão Mútua**: O acesso à fila é protegido internamente, eliminando o risco de condições de corrida.
  * **Espera Ativa Zero**: Os métodos `put()` e `get()` são bloqueantes. Se o buffer estiver cheio, o produtor aguarda; se estiver vazio, o consumidor aguarda. Isso evita o consumo desnecessário de CPU com `busy-waiting`.

**Backpressure**

O `backpressure` (ou contrapressão) é um mecanismo que faz com que os produtores reduzam sua taxa de produção quando o sistema de consumo não consegue acompanhá-la. No nosso caso, o `queue.Queue` implementa isso de forma automática. Quando um produtor tenta colocar um item em um buffer cheio, a chamada `buffer.put()` bloqueia a thread, fazendo com que o produtor espere até que o consumidor libere espaço. Isso garante que o sistema se estabilize, mesmo sob picos de produção.

**Análise da Ocupação do Buffer**

Uma thread de monitoramento foi implementada para registrar periodicamente a ocupação do buffer ao longo do tempo. Esta métrica é crucial para analisar a **estabilidade** do sistema:

  * Durante uma rajada de produção, a ocupação do buffer tende a aumentar rapidamente.
  * Durante um período de ociosidade, o buffer tende a esvaziar.
  * Se a taxa média de produção for maior que a de consumo, o buffer permanecerá cheio, e os produtores ficarão frequentemente bloqueados, indicando um gargalo.

O registro da ocupação demonstra a eficiência do `backpressure` em evitar que a fila transborde e na manutenção da integridade do sistema.

**Evidências de Execução**

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
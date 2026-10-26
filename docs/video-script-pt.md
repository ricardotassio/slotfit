# Roteiro do vídeo SlotFit — Português

Duração alvo: **105 segundos**. Esta é uma adaptação natural do roteiro principal
em inglês. Os primeiros 73 segundos (aproximadamente 70%) explicam o problema e a
demonstração. Somente os 32 segundos finais entram nas escolhas de engenharia.

Tom: calmo, curioso e direto. Ritmo médio de 135–145 palavras por minuto. Fazer
uma pequena pausa quando o gap de 60 minutos aparecer.

## Narração e direção

### 0–6s — Abertura direta com a animação pronta

**Narração**

“Um cancelamento nem sempre cria capacidade perdida. Às vezes, quem cria o
desperdício é a regra de agendamento.”

**Na tela**

- Começar diretamente na agenda animada, sem introdução com logotipo.
- Mostrar o segundo horário vazio e pausar antes da recuperação.
- Legenda: `Dois horários · Duas solicitações · Um gap evitável`.

### 6–20s — Tornar o problema de negócio concreto

**Narração**

“Imagine dois horários livres de uma hora. Uma solicitação é flexível e pode usar
qualquer um deles. A outra só pode usar o primeiro. Isso é comum em agendamento:
a disponibilidade parece simples até as restrições se cruzarem.”

**Na tela**

- Revelar os dois horários à esquerda e as solicitações à direita.
- Usar rótulos simples: `Flexível: A ou B` e `Restrita: somente A`.
- Não exibir identificadores técnicos nesta parte.

### 20–38s — Mostrar por que uma regra local razoável falha

**Narração**

“Uma regra de ordem de chegada faz uma escolha totalmente compreensível: coloca a
solicitação flexível primeiro. Mas agora a solicitação restrita não tem para onde
ir. O resultado é um horário preenchido e um gap de 60 minutos, mesmo que as duas
solicitações coubessem na agenda.”

**Na tela**

- Animar a solicitação flexível entrando no horário A.
- Tentar colocar a restrita em B e mostrar `Não compatível`.
- Pulsar o horário não utilizado uma única vez.

### 38–57s — Revelar a agenda candidata

**Narração**

“Agora, avalie os dois horários em conjunto. Preserve o único horário compatível
para a solicitação restrita e mova a flexível para o segundo. Neste exemplo
sintético, o tempo alocado passa de 60 para 120 minutos, usando a mesma capacidade.”

**Na tela**

- Reproduzir a animação de otimização já implementada.
- Finalizar nos calendários lado a lado.
- Mostrar apenas: `60 → 120 min`, `2 solicitações`, `0 ações externas`.

### 57–73s — Traduzir o resultado em valor de negócio

**Narração**

“A proposta não é automatizar o cuidado nem tomar uma decisão clínica. É dar à
equipe de operações uma opção mais clara antes que a capacidade desapareça. O
software propõe um plano; uma pessoa ainda aceita, rejeita ou pede outra opção.”

**Na tela**

- Rolar até os controles de revisão humana.
- Selecionar `Pedir alternativa` e mostrar a confirmação local.
- Legenda: `Apoio à decisão, não agendamento automático`.

## 30% finais — decisões de engenharia

### 73–86s — Por que não usar IA generativa

**Narração**

“Eu decidi não usar IA generativa aqui. As regras são explícitas, a resposta deve
ser reproduzível e cada alocação precisa ser testável. Um pequeno algoritmo de
restrições é mais adequado do que um chatbot gerando uma resposta plausível.”

**Na tela**

- Mostrar: `Regras conhecidas → solver determinístico → plano explicável`.
- Riscar discretamente: `Prompt → recomendação gerada`.
- Tarja: `CP-SAT · resolução determinística de restrições`.

### 86–97s — Demonstrar julgamento de engenharia sênior

**Narração**

“Mantive as regras de agendamento independentes da API e da interface, criei
testes contrafactuais para ordem e identificadores e registrei as revisões humanas
como eventos imutáveis. Assim, fica mais fácil questionar, reproduzir e substituir
o protótipo.”

**Na tela**

- Animar quatro blocos: `Regras`, `API`, `Interface`, `Auditoria`.
- Mostrar rapidamente o resumo dos testes, sem digitação no terminal.

### 97–105s — Limitação, integridade e encerramento

**Narração**

“Mas a demo atraente não é o resultado completo. Em 40 execuções sintéticas de
desenvolvimento, a política mais próxima chegou a 10,80 pontos percentuais diante
de um limite de 10. Por isso, eu a rejeitei. O código, os testes e o experimento
que falhou estão no repositório.”

**Na tela**

- Mostrar a faixa de no-go e depois o endereço do GitHub.
- Rodapé obrigatório: `POC sintética · Não agenda · No-go no desenvolvimento`.
- Pergunta final: `Onde você colocaria o limite entre utilização e exclusão recorrente?`

## Checklist de gravação

- Gravar em 1920×1080 com zoom do navegador em 100%.
- Usar legendas em português embutidas e também enviar um arquivo `.srt`.
- Manter música pelo menos 18 dB abaixo da voz; silêncio é aceitável.
- Não usar “otimizado por IA”, “justo”, “mais pacientes”, “receita” ou “pronto para produção”.
- Substituir o endereço do repositório somente quando o link público estiver funcionando.


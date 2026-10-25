# Roteiro de vídeo — Português

Meta: 100–115 segundos. Os valores exibidos devem vir da UI ou dos comandos
versionados. URLs do repositório/vídeo entram somente depois que existirem.

## Roteiro

**0–12s — Mostrar duas aberturas e duas solicitações**

“Depois de dez anos trabalhando com software na área de saúde, eu sempre volto à
mesma lição de engenharia: a solução útil nem sempre é a mais barulhenta. Um
cancelamento cria um pequeno problema de alocação. Uma solicitação é flexível; a
outra só pode usar o primeiro horário.”

**12–30s — Selecionar FIFO e melhor encaixe local**

“FIFO e melhor encaixe são baselines compreensíveis. Neste cenário controlado, os
dois fazem a mesma escolha local e recuperam 60 dos 120 minutos disponíveis. A
lógica é explicável, mas não enxerga o conflito entre os dois horários.”

**30–46s — Selecionar o plano controlado com CP-SAT**

“Um pequeno modelo de restrições move a solicitação flexível para o segundo
horário e coloca a restrita no primeiro. Ele recupera 120 minutos, com as três
fases lexicográficas provadas como ótimas. Não é preciso machine learning nem um
chatbot embutido, porque esta parte do problema é uma alocação explícita.”

**46–72s — Mostrar o painel de no-go do desenvolvimento**

“Mas um cenário perfeito não sustenta uma afirmação responsável de produto. Eu
testei quatro políticas longitudinais em 40 seeds sintéticas de desenvolvimento e
medi exclusão recorrente separadamente da utilização. O candidato mais próximo
ainda degradou o pior slice suportado em 10,80 pontos percentuais. O limite havia
sido definido em 10. Por isso, eu o rejeitei.”

**72–92s — Mostrar arquitetura, testes e controles de revisão**

“O domínio continua independente de FastAPI, Vue e SQLite. IDs e ordem de entrada
têm testes contrafactuais. Os eventos de revisão são append-only e idempotentes. A
interface mantém o calendário ao lado de uma tabela acessível e mostra o guardrail
reprovado antes do resultado atraente do otimizador.”

**92–110s — Registrar uma rejeição simulada e mostrar o repositório**

“Esta é uma prova de julgamento de engenharia, não um agendamento automático. Ela
usa somente dados sintéticos, não agenda nem contata pacientes e não faz afirmação
clínica, de acesso ou de receita. O repositório inclui os experimentos rejeitados,
os trade-offs e os testes reproduzíveis—não apenas a demo bonita.”

## Tela final obrigatória

`POC sintética · Nenhuma ação externa · No-go no desenvolvimento · Não pronta para produção`

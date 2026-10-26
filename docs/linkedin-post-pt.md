# Rascunho para LinkedIn — Português

Um solver dobrou o tempo recuperado na minha demo—e, mesmo assim, eu rejeitei a
estratégia.

Foi exatamente essa tensão que me levou a construir o SlotFit.

Depois de dez anos trabalhando com software na área de saúde, quis explorar um
problema operacional conhecido sem adicionar mais um chatbot: quando um
cancelamento cria dois horários, um software simples e explicável consegue alocar
solicitações compatíveis de forma mais eficiente?

Em um cenário sintético controlado, FIFO e melhor encaixe local recuperam 60 dos
120 minutos. Um pequeno modelo de restrições CP-SAT enxerga o conflito global e
recupera os 120 minutos, com três fases lexicográficas ótimas.

Mas otimização em um cenário perfeito não basta. Em 40 seeds sintéticas de
desenvolvimento, testei quatro políticas longitudinais e mantive utilização
separada de exclusão recorrente. O candidato mais próximo degradou o pior slice
suportado em 10,80 pontos percentuais. O limite definido antes do resultado era
10,00.

Então eu parei. Não ajustei o limite. Não abri calibração. Não executei o conjunto
final reservado.

Um ponto que faço questão de deixar claro: não há machine learning nem chatbot
neste projeto. Nada é treinado. O motor é programação por restrições: primeiro
regras explícitas de elegibilidade, depois o OR-Tools CP-SAT buscando toda
atribuição válida com um objetivo lexicográfico (minutos recuperados, depois
pessoas atendidas, depois idade da espera). Cada plano é provado ótimo dentro
desse modelo, e a mesma entrada produz sempre o mesmo plano. Escolhi isso em vez
de um modelo aprendido porque uma clínica tem regras explícitas, não tem dados de
treino no primeiro dia e precisa de uma resposta que possa conferir, não de uma
previsão.

O repositório também contém:

- cenários sintéticos determinísticos e reason codes estáveis;
- testes contrafactuais para IDs opacos e ordem de entrada;
- domínio independente de framework, com adapters FastAPI e Vue;
- log append-only e idempotente de revisão simulada;
- comparação acessível em calendário/tabela e limite humano explícito.

Esta POC usa dados sintéticos e não agenda, não contata pacientes e não define
prioridade clínica. Ela não afirma melhoria de receita, acesso, tempo de espera ou
segurança do paciente. O que ela demonstra é o que mais me interessa: escolher a
tecnologia mais simples que resolve o problema, medir o trade-off desconfortável e
preservar um no-go quando a evidência diz não.

Repositório: `https://github.com/ricardotassio/slotfit`

Vídeo: `{VIDEO_URL}`

#EngenhariaDeSoftware #ConstraintProgramming #HealthTech #IAResponsável

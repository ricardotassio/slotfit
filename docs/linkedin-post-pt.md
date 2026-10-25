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

Repositório: `{GITHUB_REPOSITORY_URL}`

Vídeo: `{VIDEO_URL}`

#EngenhariaDeSoftware #ConstraintProgramming #HealthTech #IAResponsável

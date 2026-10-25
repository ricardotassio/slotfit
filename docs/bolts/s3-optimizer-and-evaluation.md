# Card S3 — Otimizador e avaliação controlada

**Estado:** em andamento; candidatos V1–V4 rejeitados no desenvolvimento.
**Spec:** [`SF-003`](../../specs/003-optimizer-and-evaluation.md).  
**ADR:** [`ADR-0002`](../adr/0002-lexicographic-cp-sat.md).

## 💡 Propósito e analogia

Resolver conflitos globais que políticas locais não enxergam. É como montar um
quebra-cabeça: usar a primeira peça que cabe pode bloquear a única posição de outra
peça. O CP-SAT entra somente depois que o cenário multi-slot demonstra essa falha.

## ⚙️ Mecânica

O adapter cria variável binária apenas para pares elegíveis, limita cada request e
intervalo a uma atribuição e executa três objetivos lexicográficos: minutos,
quantidade servida e wait-age (`src/slotfit/optimizer.py:70-160`). Cada fase precisa
ser `OPTIMAL`; timeout ou limite permanece explícito. O comparador executa 40 seeds,
cinco rodadas, contrafactuais e guardrails (`src/slotfit/comparison.py:385-480`).

Falhas evitadas: score ponderado arbitrário, relaxamento silencioso de restrições,
fallback disfarçado, tuning no teste final e narrativa que confunde eficiência com
equidade.

## ⚖️ Avaliação crítica

**Veredito: CP-SAT é justificado; a primeira política longitudinal é insuficiente.**
O solver recuperou 96,81% em média, mas o candidato ultrapassou o guardrail de
déficit de exposição. LangGraph, LLM e deep learning seriam excessivos: o problema
é de atribuição com regras explícitas, não de geração ou predição.

V2 adicionou dívida por oportunidades compatíveis perdidas como desempate residual.
O teste unitário funcionou, mas a política mudou zero decisões nos 40 seeds. Isso
mostrou que um sinal correto pode ser ineficaz quando objetivos anteriores deixam
nenhuma alternativa relevante.

O diagnóstico seguinte refinou essa conclusão: 34 de 200 rodadas tinham alternativas
primárias equivalentes, e 8 poderiam melhorar localmente o slice moderado sem perda
de eficiência. Portanto, há alternativas; V2 simplesmente não as distingue.

V3 priorizou requests compatíveis com menos intervalos e mudou 17 decisões. O pior
desvio caiu de 12,58 para 12,35 p.p., insuficiente para o limite de 10 p.p. O próximo
passo é mostrar a fronteira eficiência/exposição, não acumular heurísticas.

A fronteira local mostrou que um piso de 90% por rodada realiza 99,43% dos minutos
ótimos no agregado e leva o slice curto a 8,24 p.p. O resultado fundamenta um V4
label-free, mas não valida o oracle pós-hoc nem abre calibração.

V4 confirmou essa cautela: no caminho longitudinal real, atingiu 95,71% de
utilização média e 10,80 p.p. de degradação. Melhorou, mas falhou. Após quatro
candidatos, o próximo passo é revisão metodológica/no-go, não V5 automático.

## ✅ Evidência e Definition of Done

- 40/40 execuções com três fases `OPTIMAL`;
- zero violações, flips de ID ou de ordem;
- K=3 starvation de 0%;
- degradação de exposure shortfall: 12,58 p.p., limite 10 p.p.;
- decisão: **rejeitado antes da calibração**;
- DoD pendente: revisar a política no mesmo desenvolvimento, passar os guardrails,
  calibrar e somente então congelar configuração. O conjunto final ainda não existe.

## 🎯 Entrevista

“Usei otimização exata porque havia um conflito global demonstrável. Mantive
objetivos lexicográficos para evitar pesos difíceis de justificar. O ponto mais
importante foi rejeitar um resultado de 96,81% porque ele falhou um guardrail
definido antes do experimento.”

**Pergunta difícil:** “Então o otimizador falhou?”  
**Resposta:** ele resolveu corretamente o objetivo estático; o experimento mostrou
que o objetivo ainda não representa toda a política longitudinal desejada.

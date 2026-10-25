# Catálogo de Bolts do SlotFit

Este catálogo transforma o roadmap AI-DLC em cards de aprendizado e execução.
Cada card distingue fatos observados de decisões futuras para que a documentação
possa ser usada no desenvolvimento, no vídeo e em entrevistas técnicas.

## Mapa

| Bolt | Resultado de negócio/técnico | Estado | Card |
|---|---|---|---|
| S1 | Domínio determinístico e baselines explicáveis | Aceito com follow-up | [S1](s1-domain-and-baselines.md) |
| S2 | Geração reproduzível e controles contra bias operacional | Concluído | [S2](s2-scenarios-and-controls.md) |
| S3 | Otimizador global e avaliação controlada | Em andamento; candidato 1 rejeitado | [S3](s3-optimizer-and-evaluation.md) |
| S4 | Fronteira HTTP com FastAPI/Pydantic | Concluído | [S4](s4-api-boundary.md) |
| S5 | Persistência e revisão humana idempotente | Concluído | [S5](s5-persistence-and-review.md) |
| S6 | Interface visual para comparar planos | Concluído | [S6](s6-review-ui.md) |
| S7 | Avaliação congelada e análise final | Não executado; gate falhou corretamente | [S7](s7-frozen-evaluation.md) |
| S8 | Hardening, vídeo e publicação baseada em evidências | Concluído; não publicado | [S8](s8-hardening-and-publication.md) |

## Contrato de um card

Todos os cards respondem às mesmas perguntas:

1. **Propósito e analogia:** qual problema este Bolt resolve e por que vem agora?
2. **Mecânica:** o que entra, o que sai e quais falhas são evitadas?
3. **Avaliação crítica:** a solução é necessária, suficiente ou excessiva para a POC?
4. **Evidência e DoD:** como sabemos que terminou?
5. **Entrevista:** como explicar a decisão, o trade-off e um caso de falha?

## Regras transversais

- somente dados sintéticos;
- nenhuma comunicação, agendamento ou alteração externa;
- restrições duras nunca viram penalidades;
- slices de auditoria não entram na decisão;
- eficiência e exclusão são reportadas separadamente;
- um guardrail reprovado interrompe a progressão;
- apenas um spec pode estar ativo por vez;
- itens planejados não são evidência de funcionalidade existente.

Fontes canônicas: [`../../AGENTS.md`](../../AGENTS.md),
[`../../aidlc-docs/execution-plan.md`](../../aidlc-docs/execution-plan.md) e
[`../../aidlc-docs/state.md`](../../aidlc-docs/state.md).

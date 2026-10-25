# Card S7 — Avaliação congelada

**Estado:** encerrado sem execução; o gate de entrada falhou corretamente.
**Dependência:** candidato e guardrails congelados após desenvolvimento/calibração.  
**Requisitos principais:** SF-FR-007–009; SF-NFR-006–008.

## 💡 Propósito e analogia

Executar a prova final sem mover a linha de chegada. É o equivalente a lacrar a
prova e o gabarito antes do exame: seeds, distribuição, objetivos e limites ficam
imutáveis antes que o resultado final seja observado.

## ⚙️ Mecânica planejada

Um manifest final novo conterá 400 seeds nunca exercidos, checksums, versões de
Python/OR-Tools, solver, distribuição e guardrails. A execução produzirá
`scenario-results.jsonl`, `slice-summary.json` e `decision.json`. Diferenças
pareadas e intervalos bootstrap de 95% usarão seed como unidade de análise. Slices
com suporte insuficiente serão reportados, nunca fundidos silenciosamente.

Falhas a evitar: leakage entre desenvolvimento e teste, pseudo-replicação por
request, tuning pós-resultado, ausência de proveniência e cherry-picking.

## ⚖️ Avaliação crítica

**Veredito: necessário para credibilidade; 400 seeds são uma escolha POC, não
escala clínica.** O tamanho limita a margem de erro binária de pior caso a cerca de
4,9 p.p. Uma plataforma de experimentação distribuída seria excessiva: a execução
atual é local e rápida. O bootstrap deve ser implementado somente após o contrato
estatístico estar testado.

## ✅ Definition of Ready / Done

Ready: candidato passou desenvolvimento e calibração; commit de freeze existe;
seeds finais nunca foram executados. Done: execução única; artefatos imutáveis;
checksums/proveniência válidos; decisão automática dos guardrails; revisão de risco
e de testes. O estado Ready não foi alcançado: V1–V4 falharam em desenvolvimento,
calibração não abriu e o manifest final **não existe**, corretamente. O gate está
registrado em [`../../specs/007-frozen-evaluation-gate.md`](../../specs/007-frozen-evaluation-gate.md).

## 🎯 Entrevista

“Separei desenvolvimento, calibração, regressão e teste congelado para evitar
otimização contra o benchmark. Usei seed como unidade independente e preservei
resultados desfavoráveis. O experimento pode concluir que a política não é
aceitável; isso é um resultado válido.”

**Pergunta difícil:** “Por que não olhar os seeds finais durante debugging?”  
**Resposta:** depois de observados eles deixam de ser teste final; falhas técnicas
devem ser reproduzidas em regressão, sem reutilizar o resultado para tuning.

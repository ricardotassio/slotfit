# Card S1 — Domínio determinístico e baselines

**Estado:** aceito com follow-up de teach-back.  
**Spec:** [`SF-001`](../../specs/001-domain-and-baselines.md).  
**Requisitos:** SF-FR-001–003; SF-NFR-001 e SF-NFR-003.

## 💡 Propósito e analogia

Criar a menor versão executável do problema antes de otimizar. É como marcar no
chão as regras de um estacionamento antes de desenvolver um sistema que escolha a
melhor vaga. Neste ponto do fluxo, o Bolt define o que é intervalo, solicitação,
elegibilidade, atribuição e plano.

## ⚙️ Mecânica

Entrada: fixture sintética `demo-1400`. Saída: planos FIFO e best-fit em JSON, com
atribuições e motivos de exclusão. Valores imutáveis e timezone-aware rejeitam
estados inválidos (`src/slotfit/domain.py:7-102`). A elegibilidade avalia
consentimento, provider, sala, duração, aviso e disponibilidade, emitindo reason
codes (`src/slotfit/eligibility.py:15-45`). FIFO prioriza ordem de entrada; best-fit
minimiza a sobra local (`src/slotfit/strategies.py:69-85`).

Falhas evitadas: datas ingênuas, seleção de pessoa inelegível, comportamento não
reproduzível e comparação entre estratégias com entradas diferentes.

## ⚖️ Avaliação crítica

**Veredito: necessário e suficiente.** Dataclasses e funções puras mantêm o núcleo
testável sem rede. Banco, API, ML e microserviços seriam excessivos aqui. A
alternativa mais simples — dicionários livres — reduziria código, mas perderia
invariantes e clareza de contrato.

## ✅ Evidência e Definition of Done

- FIFO recupera 30 minutos com `WR-001`.
- Best-fit recupera 75 minutos com `WR-002`.
- `WR-003` é excluída por `REQUIRED_ROOM_UNAVAILABLE`.
- `make demo` declara `automatic_action: none`.
- Pendência humana: Ricardo explicar por que FIFO e best-fit representam políticas
  diferentes; não bloqueia a progressão, mas impede o status `Done`.

## 🎯 Entrevista

“Comecei pelo domínio e por dois baselines porque um otimizador só demonstra valor
quando comparado com políticas simples e compreensíveis. Mantive as restrições no
núcleo, independente de frameworks. O primeiro fixture prova contratos, não
superioridade estatística.”

**Pergunta difícil:** “Por que não começar com CP-SAT?”  
**Resposta:** um único slot não evidencia conflito global; o solver acrescentaria
complexidade sem uma necessidade demonstrada.

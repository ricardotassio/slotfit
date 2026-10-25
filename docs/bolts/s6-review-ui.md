# Card S6 — Interface de comparação e revisão

**Estado:** planejado; não implementado.  
**Dependências:** S4; S5 apenas para persistir revisão.  
**Requisitos principais:** SF-FR-005, SF-FR-006 e SF-FR-009.

## 💡 Propósito e analogia

Tornar trade-offs visíveis para um humano. A interface é uma mesa de comparação,
não um botão mágico: mostra quais opções cabem, por que outras não cabem e qual
guardrail foi acionado.

## ⚙️ Mecânica planejada

Vue 3, TypeScript e FullCalendar apresentarão o calendário sintético e até três
planos. Cada card de plano separará restrições, minutos recuperados, pessoas
servidas, exposição/espera, pior slice e status do solver. O usuário poderá
registrar aceitar, rejeitar ou pedir alternativa; nenhuma escolha altera agenda ou
envia mensagem.

Falhas a evitar: anchoring pelo primeiro plano, cor que sugere “resposta certa”,
motivos escondidos, score único que mistura dimensões e double-submit.

## ⚖️ Avaliação crítica

**Veredito: UI pequena é suficiente.** FullCalendar é útil para tornar o conflito
visual; um design system completo ou microfrontend seria excessivo. Uma tabela
seria mais barata e deve permanecer como fallback acessível. A escala e requisitos
de acessibilidade ainda precisam ser confirmados antes da implementação.

## ✅ Definition of Ready / Done

Ready: wireflow, hierarquia neutra, estados de erro/loading/vazio e contrato de
acessibilidade aprovados. Done: Playwright cobre comparação, explicações e revisão
idempotente; teclado e contraste verificados; guardrail reprovado fica visível;
nenhum controle sugere integração real. Estado atual: somente storyboard e fluxo
planejado.

## 🎯 Entrevista

“O desafio da UI não é renderizar calendário; é evitar que uma recomendação seja
percebida como decisão automática. Por isso separei métricas, expus exclusões e
mantive o humano responsável. Testei também estados de falha e duplicidade, não só
o happy path.”

**Pergunta difícil:** “Como você reduz presentation bias?”  
**Resposta:** tratamento visual neutro, regra de ordenação declarada, dimensões
separadas e motivos/guardrails acessíveis no mesmo nível do ganho de utilização.

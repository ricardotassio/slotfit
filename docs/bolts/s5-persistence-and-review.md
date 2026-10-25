# Card S5 — Persistência e revisão humana

**Estado:** planejado; não implementado.  
**Dependência:** contrato HTTP estável no S4.  
**Requisitos principais:** SF-FR-006, SF-FR-007 e SF-NFR-004.

## 💡 Propósito e analogia

Guardar a trilha de evidências sem transformar a POC em agenda clínica. É o livro
de registro: conserva qual cenário e plano foram vistos e qual decisão simulada o
humano registrou, mas não executa a decisão fora do laboratório.

## ⚙️ Mecânica planejada

PostgreSQL armazenará runs versionadas e eventos append-only de revisão. Uma chave
de idempotência impedirá que o mesmo clique gere decisões duplicadas. Cada evento
referenciará checksum de entrada, versão da estratégia e plano apresentado. Não
haverá PHI/PII, mensagem, booking ou integração com PMS/EHR.

Falhas a evitar: perda de proveniência, update destrutivo do histórico, duplo
registro, corrida entre revisões e reconstrução impossível do resultado.

## ⚖️ Avaliação crítica

**Veredito: PostgreSQL é suficiente, mas deve entrar somente quando a revisão
existir.** SQLite seria mais simples para demo individual, porém PostgreSQL permite
mostrar transação, unicidade e eventos idempotentes com um caminho realista. Kafka,
event sourcing completo, Redis e banco vetorial seriam excessivos na escala não
confirmada da POC.

## ✅ Definition of Ready / Done

Ready: schema, retenção, estados permitidos e semântica da idempotência revisados.
Done: migrations reproduzíveis; constraint única; testes concorrentes básicos;
replay por checksum; append-only protegido; erro de persistência não provoca ação
externa. Nada disso está implementado hoje.

## 🎯 Entrevista

“Escolhi um banco relacional porque as invariantes são transacionais e o volume é
baixo. Modelei revisão como evento imutável para preservar auditoria, mas evitei um
framework de event sourcing. A idempotência fica apoiada por constraint no banco,
não apenas por um `if` na aplicação.”

**Pergunta difícil:** “Por que PostgreSQL e não uma fila?”  
**Resposta:** não existe processamento assíncrono ou entrega externa neste escopo;
o problema é consistência e auditoria local, não backpressure.

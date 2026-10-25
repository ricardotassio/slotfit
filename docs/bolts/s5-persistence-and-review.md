# Card S5 — Persistência e revisão humana

**Estado:** concluído e verificado.
**Dependência:** contrato HTTP estável no S4.  
**Requisitos principais:** SF-FR-006, SF-FR-007 e SF-NFR-004.

## 💡 Propósito e analogia

Guardar a trilha de evidências sem transformar a POC em agenda clínica. É o livro
de registro: conserva qual cenário e plano foram vistos e qual decisão simulada o
humano registrou, mas não executa a decisão fora do laboratório.

## ⚙️ Mecânica planejada

SQLite armazenará eventos append-only de revisão no POC local. Uma chave
de idempotência impedirá que o mesmo clique gere decisões duplicadas. Cada evento
referenciará checksum de entrada, versão da estratégia e plano apresentado. Não
haverá PHI/PII, mensagem, booking ou integração com PMS/EHR.

Falhas a evitar: perda de proveniência, update destrutivo do histórico, duplo
registro, corrida entre revisões e reconstrução impossível do resultado.

## ⚖️ Avaliação crítica

**Veredito: SQLite é suficiente na escala atual.** A revisão agora existe, mas
continua local, individual e sem processamento assíncrono. Transação, unicidade e
proteção append-only podem ser demonstradas sem operar um serviço. PostgreSQL fica
deferido até existir implantação compartilhada ou contenção real. Kafka, event
sourcing completo, Redis e banco vetorial seriam excessivos.

## ✅ Definition of Ready / Done

Ready: schema, retenção, estados permitidos e semântica da idempotência revisados em
[`../../specs/005-persistence-and-review.md`](../../specs/005-persistence-and-review.md).
Done: migrations reproduzíveis; constraint única; testes concorrentes básicos;
replay por checksum; append-only protegido; erro de persistência não provoca ação
externa. O adapter SQLite, os triggers e os contratos HTTP implementam essa lista.

## 🎯 Entrevista

“Escolhi um banco relacional porque as invariantes são transacionais e o volume é
baixo. Modelei revisão como evento imutável para preservar auditoria, mas evitei um
framework de event sourcing. A idempotência fica apoiada por constraint no banco,
não apenas por um `if` na aplicação.”

**Pergunta difícil:** “Por que PostgreSQL e não uma fila?”  
**Resposta:** não existe processamento assíncrono ou entrega externa neste escopo;
o problema é consistência e auditoria local, não backpressure.

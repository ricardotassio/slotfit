# Card S4 — Fronteira FastAPI/Pydantic

**Estado:** concluído e verificado.
**Dependência:** S3 encerrado, inclusive por no-go terminal.
**Requisitos principais:** SF-FR-005, SF-NFR-004 e SF-NFR-005.

## 💡 Propósito e analogia

Transformar o núcleo em um serviço local com uma porta de entrada explícita. A API
funciona como a recepção de uma clínica: valida o formulário, encaminha ao domínio
e devolve uma resposta compreensível, sem tomar a decisão pelo profissional.

## ⚙️ Mecânica planejada

Entrada: cenário sintético ou referência a uma execução reproduzível. Pydantic
validará payload e versão; FastAPI chamará casos de uso que convertem DTOs para os
objetos de domínio. Saída: até três planos, motivos, métricas separadas, status do
solver e `automatic_action: none`. O domínio continuará sem importar FastAPI.

Falhas a evitar: validação duplicada, modelos HTTP vazando para o domínio, exceção
interna exposta ao cliente, operação não idempotente e contrato sem versão.

## ⚖️ Avaliação crítica

**Veredito: suficiente para a UI local.** FastAPI/Pydantic é compatível com a POC
e reduz código de validação. GraphQL, gRPC, gateway e microserviço separado seriam
excessivos para um único consumidor local. A API também torna o resultado negativo
inspecionável pela futura UI; por isso ela pode avançar após o no-go de S3 sem
transformar um candidato rejeitado em recomendação.

## ✅ Definition of Ready / Done

Ready: schemas e endpoints especificados em
[`../../specs/004-api-boundary.md`](../../specs/004-api-boundary.md); erros e versionamento definidos; nenhum
dado real permitido. Done: testes de contrato e integração sem rede externa,
OpenAPI verificável, limites de payload, respostas determinísticas e nenhuma ação
automática. Como S4 possui apenas `GET`, não existe payload de entrada arbitrário
a limitar. Os contratos, smoke test e suite completa fornecem a evidência atual.

## 🎯 Entrevista

“Usei a API como adapter, não como lugar para regra de negócio. Isso preserva o
nucleo testável e permite trocar a interface sem reimplementar elegibilidade ou
otimização. Para a escala da POC, REST síncrono é mais simples que introduzir
mensageria.”

**Pergunta difícil:** “Por que não expor os dataclasses diretamente?”  
**Resposta:** DTOs de fronteira precisam versionamento, validação e mensagens de
erro próprias; o domínio não deve carregar decisões de transporte.

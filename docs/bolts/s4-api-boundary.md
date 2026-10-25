# Card S4 — Fronteira FastAPI/Pydantic

**Estado:** planejado; não implementado.  
**Dependência:** S3 aceito e configuração apta a progredir.  
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

**Veredito: suficiente quando houver UI.** FastAPI/Pydantic é compatível com a POC
e reduz código de validação. GraphQL, gRPC, gateway e microserviço separado seriam
excessivos para um único consumidor local. Uma CLI permanece mais barata até S6;
por isso S4 não deve começar antes do gate de S3.

## ✅ Definition of Ready / Done

Ready: schemas e endpoints especificados; erros e versionamento definidos; nenhum
dado real permitido. Done: testes de contrato e integração sem rede externa,
OpenAPI verificável, limites de payload, respostas determinísticas e nenhuma ação
automática. Esta lista é contrato futuro, não evidência atual.

## 🎯 Entrevista

“Usei a API como adapter, não como lugar para regra de negócio. Isso preserva o
nucleo testável e permite trocar a interface sem reimplementar elegibilidade ou
otimização. Para a escala da POC, REST síncrono é mais simples que introduzir
mensageria.”

**Pergunta difícil:** “Por que não expor os dataclasses diretamente?”  
**Resposta:** DTOs de fronteira precisam versionamento, validação e mensagens de
erro próprias; o domínio não deve carregar decisões de transporte.

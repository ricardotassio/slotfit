# Card S8 — Hardening e publicação

**Estado:** planejado; não implementado.  
**Dependência:** avaliação S7 concluída e revisada.  
**Saída:** repositório reproduzível, vídeo e publicação com claims limitados.

## 💡 Propósito e analogia

Transformar o experimento em demonstração verificável. É preparar uma bancada de
laboratório para visita: instruções, controles, falhas e limitações precisam estar
visíveis, não apenas o resultado bonito.

## ⚙️ Mecânica planejada

O Bolt consolidará setup limpo, Docker quando justificado, testes finais,
arquitetura, ADRs, threat/risk review, licença e artefatos de avaliação. O vídeo
mostrará problema, baseline, conflito global, solução, candidato rejeitado ou
aceito, guardrails, intervenção humana e limites. A publicação ligará para o GitHub
e usará apenas números reproduzíveis do relatório final.

Falhas a evitar: demo que funciona só na máquina do autor, segredo ou dado real no
repo, claim clínico/financeiro sem evidência, esconder resultado negativo e vídeo
que chama POC de produto pronto.

## ⚖️ Avaliação crítica

**Veredito: necessário; infraestrutura promocional pesada é excessiva.** README,
make targets, CI simples e vídeo curto são suficientes. Kubernetes, observabilidade
de produção e cloud deployment não demonstrariam valor para uma POC local sem
carga real. A licença ainda é uma decisão aberta.

## ✅ Definition of Ready / Done

Ready: S7 encerrado e claims aprovados contra evidência. Done: clone limpo
reproduzível; testes/artefatos verificáveis; nenhum segredo; vídeo e texto revisados
em inglês principal e português; links válidos; limitações visíveis; nenhuma ação
publicada automaticamente. Publicar exige autorização explícita.

## 🎯 Entrevista

“Tratei comunicação como parte da engenharia: cada claim aponta para um teste ou
artefato. Mostrei também o caso rejeitado, porque ele prova que os guardrails são
reais. Evitei infraestrutura teatral e concentrei o hardening no que outra pessoa
precisa para reproduzir e criticar o experimento.”

**Pergunta difícil:** “O que você não afirmaria?”  
**Resposta:** impacto em receita, acesso, segurança do paciente, ausência de bias ou
prontidão de produção sem dados representativos e validação no workflow real.

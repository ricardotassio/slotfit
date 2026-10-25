# Card S2 — Cenários reproduzíveis e controles

**Estado:** concluído.  
**Spec:** [`SF-002`](../../specs/002-scenarios-and-fairness-controls.md).  
**Requisitos:** SF-NFR-001, SF-NFR-002, SF-NFR-006 e SF-NFR-008.

## 💡 Propósito e analogia

Substituir uma fotografia por um laboratório controlado. Um único fixture mostra
como o sistema funciona; uma população sintética versionada mostra se o
comportamento se repete, muda arbitrariamente ou exclui certos perfis operacionais.

## ⚙️ Mecânica

Entrada: seed, versão do gerador e configuração da distribuição. Saída: `Scenario`
para decisão e `ScenarioManifest` separado para auditoria. Escolhas são derivadas
de SHA-256, permitindo replay (`src/slotfit/generation.py:78-108`). Slices de
duração, disponibilidade, recurso, espera e aviso permanecem fora do objeto
consumido pelas estratégias (`src/slotfit/generation.py:38-63`). Rodadas
longitudinais contam oportunidades compatíveis e exposições sem fingir tempo real.

Falhas evitadas: leakage de atributo de auditoria, IDs influenciando decisão,
dependência da ordem de entrada, dupla atribuição e ajuste do teste final depois de
ver o resultado.

## ⚖️ Avaliação crítica

**Veredito: necessário.** Dados sintéticos não provam ausência de bias; servem para
expor hipóteses e testar invariantes. Hypothesis poderia ampliar property testing,
mas não é necessário para o primeiro contrato determinístico. Dados reais seriam
prematuros e incompatíveis com o limite de privacidade da POC.

## ✅ Evidência e Definition of Done

- splits de desenvolvimento, calibração, regressão e challenge são distintos;
- mesmo seed e versão reproduzem o cenário; seeds diferentes variam conteúdo;
- troca de IDs, reordenação e registro inelegível não mudam a decisão;
- mutation sentinel demonstra que o teste detecta uma política lexical quebrada;
- opportunity counts são inputs de avaliação, não “tempo de espera de pacientes”.

## 🎯 Entrevista

“Separei atributos decisórios de metadados de auditoria estruturalmente, em vez de
confiar apenas em disciplina. Versionei seed, gerador, distribuição e checksum.
Depois usei testes metamórficos para detectar dependências arbitrárias que exemplos
felizes não revelariam.”

**Pergunta difícil:** “Dados sintéticos removem bias?”  
**Resposta:** não. Eles ajudam a descobrir bias introduzido pelo desenho, mas uma
conclusão real exige dados representativos, governança e validação local.

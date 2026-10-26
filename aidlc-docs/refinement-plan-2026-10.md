# Plano de refino — Ciclo 2: "Um dia na clínica"

- Status: **Proposta aguardando gate humano** (`blocking-approval`). Nenhum código
  foi escrito para este ciclo.
- Data: 2026-10-26
- Dono do gate: Ricardo Tassio
- Fase AI-DLC: Inception do ciclo 2 (o ciclo 1, S1–S8, permanece `Complete`)
- Specs propostas: SF-009 a SF-014 (criadas somente após aprovação das Units)

## 1. Por que um segundo ciclo

O ciclo 1 entregou um experimento reproduzível com resultado negativo preservado.
Ele é convincente para quem lê código e specs. Ele **não** é compreensível em
noventa segundos para quem administra uma clínica, nem mostra o motor por baixo
dos panos para um engenheiro sênior que quer julgar a decisão técnica.

O ciclo 2 adiciona uma camada de narrativa e de explicação sobre o mesmo motor,
sem alterar o motor, sem alterar os números observados e sem ampliar a fronteira
de claims. A regra operacional é: **todo número exibido continua vindo de código
versionado e testado; a narrativa só muda a ordem e a linguagem.**

## 2. Qual é a aplicação real

### O problema no mundo real

Clínicas ambulatoriais (fisioterapia, odontologia, imagem, especialidades) operam
com agenda cheia e lista de espera. Cancelamentos de última hora abrem buracos
que a equipe tenta preencher ligando para a lista de espera, normalmente na ordem
de chegada, e aceitando o primeiro encaixe que funciona. Cada buraco não
preenchido é capacidade já paga (profissional, sala, equipe) que não produz
atendimento.

### O que o mercado faz hoje

Produtos de "waitlist automática" disparam mensagens para a lista e dão a vaga a
quem responde primeiro. Isso é uma política FIFO por velocidade de resposta.
Ela resolve o **contato**, não a **decisão**: não olha o dia inteiro, e tende a
excluir repetidamente quem tem restrições (sala específica, profissional
específico, janela estreita de disponibilidade, pouca antecedência).

### Onde o SlotFit se encaixa

O SlotFit é a camada de **decisão antes do contato**: dado o conjunto de
aberturas do dia e as restrições de cada solicitação, qual combinação de ofertas
preenche o dia inteiro respeitando as regras duras, e o que acontece com quem
fica repetidamente de fora. A coordenadora continua decidindo e executando o
contato. O sistema nunca liga, nunca agenda, nunca prioriza clinicamente.

A pesquisa feita no ciclo 1 sustenta exatamente essa fronteira:

- a fixture de conflito global mostra que a escolha local razoável desperdiça
  capacidade (60 de 120 minutos) e que avaliar o dia em conjunto recupera tudo;
- a comparação longitudinal de 40 seeds mostra que recuperar mais minutos **não
  basta**: as quatro políticas testadas aumentaram a exclusão repetida do pior
  slice acima do limite pré-declarado e foram rejeitadas.

### Sobre a tela de "pessoas marcando e desmarcando com prejuízo"

A ideia está meio certa. O **gatilho** é o cancelamento, e a narrativa deve
começar com uma agenda cheia que perde dois horários durante a manhã. Dois ajustes:

1. As pessoas da lista de espera não estão "tentando marcar" ao vivo; elas já
   estão esperando, cada uma com restrições. A história ganha força quando o
   público vê as restrições antes de ver a regra falhar.
2. O **prejuízo financeiro não pode ser calculado nem afirmado pelo sistema.**
   `AGENTS.md` proíbe converter resultados controlados em claims financeiros.
   A perda deve ser mostrada em **capacidade não entregue** (minutos de
   profissional ociosos, atendimentos não realizados, sala vazia). Qualquer
   valor em dinheiro só pode existir como hipótese explícita do próprio
   espectador, fora da superfície de evidência, e isso é uma decisão sua
   (seção 8, decisão D1).

### Por que não IA generativa, e qual IA é esta

Este problema tem estrutura: variáveis discretas (solicitação × abertura),
restrições duras conhecidas (sala, profissional, duração, consentimento,
antecedência, janela de disponibilidade) e objetivos declarados. Para essa
estrutura, programação por restrições (CP-SAT, OR-Tools) oferece o que um
modelo generativo não oferece:

| Necessidade | CP-SAT | Modelo generativo |
|---|---|---|
| Resposta repetível para a mesma entrada | sim, por construção | não garantido |
| Prova de que não existe plano melhor no modelo | status `OPTIMAL` por fase | inexistente |
| Rejeição provável de uma atribuição inválida | restrição dura | depende de validação externa |
| Explicação estável | reason codes + fases | texto plausível, variável |
| Dados de treino | nenhum necessário | clínica nova não tem histórico |
| Auditoria do porquê | objetivo lexicográfico explícito | opaco |

Programação por restrições é IA simbólica clássica (busca com satisfação de
restrições), não aprendizado de máquina. A mensagem sênior é: **escolher a classe
de IA pela estrutura do problema, não pela moda.** IA generativa poderia ajudar
em tarefas de linguagem na borda (interpretar uma observação em texto livre,
rascunhar uma mensagem de oferta), e ficou deliberadamente fora do escopo porque
não há problema de linguagem no caminho de decisão.

Frase-guia para vídeo e post: *"uma resposta que você pode conferir, em vez de
um palpite."* A palavra "prova" só pode aparecer na mesma frase que "dentro do
modelo declarado", e o teste de contrato de publicação passa a exigir isso
(achado MEDIUM-5 do risk-reviewer). O `OPTIMAL` do solver prova otimalidade do
objetivo dentro do modelo em uma fixture; não prova que o plano é certo, seguro
ou justo.

Dois limites de comunicação, também do risk-reviewer:

- a descrição do "mercado" acima é premissa de design, não medição; ela não
  entra em artefato público, ou entra rotulada como premissa;
- a tabela CP-SAT × generativo é justificativa de design, não resultado medido;
  qualquer cartão de UI ou post que a use recebe o rótulo "design rationale,
  not a measured result".

## 3. A história em seis capítulos

Cada capítulo mapeia para um estado observável da aplicação. Nenhum capítulo
inventa número.

| # | Capítulo | O que o público vê | Fonte do número |
|---|---|---|---|
| 1 | Manhã cheia | Agenda sintética de um dia com atendimentos marcados; lista de espera ao lado com restrições em linguagem simples | nova fixture `clinic-day` |
| 2 | Dois cancelamentos | Dois horários ficam vazios (14:00 e 15:30, mesmos da fixture atual); contador de capacidade ociosa sobe | fixture + `remaining_gap_minutes` |
| 3 | A regra de todo mundo | FIFO preenche o primeiro; a solicitação restrita não cabe no segundo; `60 min sem uso` | plano `fifo` |
| 4 | Avaliar as duas aberturas em conjunto | O plano CP-SAT move a flexível e preserva a vaga da restrita; `120 de 120 min`; cada solicitação mostra o motivo em linguagem simples; a disclosure da API ("não torna aceitável o candidato longitudinal rejeitado") acompanha o número | plano `cp_sat` + tradução de reason codes + `demo.disclosure` |
| 5 | A pessoa decide | Aceitar, rejeitar ou pedir alternativa; confirmação de que nada foi enviado | `/api/v1/reviews` |
| 6 | Por baixo dos panos | Regras → fases do solver (minutos, atendidos, idade da espera) com status `OPTIMAL` → testes contrafactuais → faixa de no-go 10,80 vs 10 → por que não IA generativa | `optimizer_evidence`, `development-decision` |

A ordem é deliberada: 70% negócio, 30% engenharia, como já definido no plano de
vídeo. O capítulo 6 é a porta para o modo "Evidence".

**Regra de integridade (achado HIGH-1 do risk-reviewer):** a faixa de no-go
(`data-testid="research-no-go"`, mesma fonte da API) é **persistente em todos os
capítulos**, não só no 6. Links diretos `?chapter=4` e `?chapter=5`, capturas de
tela e cortes de vídeo são superfícies de claim; sem a faixa persistente, o
capítulo 4 apresentaria o resultado da fixture como aceitação do V4, o que o
SF-008 proíbe. Teste Playwright obrigatório: ao navegar direto para
`?chapter=4` ou `?chapter=5`, a faixa está visível antes de qualquer botão de
revisão ficar habilitado.

Frase "olhar o dia inteiro" fica fora da copy: a fixture tem duas aberturas e
três solicitações; o texto diz "avaliar as duas aberturas em conjunto".

## 4. Princípios de produto e design

Adaptados das Apple Human Interface Guidelines para uma aplicação web local. A
HIG orienta princípios, não cromo de plataforma.

- **Conteúdo acima de cromo.** A agenda é o único elemento ousado; todo o resto
  é silencioso. Nada de cards idênticos com sombra, nada de eyebrow em caixa alta.
- **Divulgação progressiva.** Um capítulo por vez; detalhes técnicos só quando o
  espectador pede ("ver por baixo dos panos").
- **Feedback para toda ação.** Cada revisão simulada responde com o estado
  registrado e com `external_action: none` visível.
- **Movimento com significado.** A única animação importante é o cartão da
  solicitação entrando na abertura. `prefers-reduced-motion` troca por crossfade.
- **Sem modal desnecessário.** Revisão é inline; não há "tem certeza?".
- **Acessibilidade desde o início.** Tabela semântica continua ao lado da agenda;
  navegação por teclado entre capítulos; contraste AA; axe sem violações sérias.
- **Linguagem do usuário.** "Abertura", "solicitação flexível", "solicitação
  restrita", "avaliar o dia em conjunto". Termos técnicos aparecem só no
  capítulo 6, com a palavra simples ao lado.
- **Neutralidade preservada.** Nenhum plano é "recomendado"; a ordem segue
  baseline primeiro; métricas separadas (SF-006 continua valendo).
- **Sinteticidade visível.** Um selo "dados sintéticos" permanece em todas as
  telas; nomes de personas, se usados, são claramente fictícios e sem sobrenome.

## 5. Bolts propostos

Cada Bolt vira uma spec em `specs/` só depois do gate. Todos herdam as regras de
`AGENTS.md`. Nível de controle: `blocking-approval` em cada gate de design e de
claim; `timed-veto` para refatorações internas sem mudança observável. Todo
commit é atômico e segue conventional commits.

### SF-009 — Reconciliação de governança (pré-requisito)

**Por quê primeiro.** `AGENTS.md`: se docs e código conflitam, parar e corrigir
o documento dono antes de qualquer código novo.

Escopo:

- fazer `tests/test_publication_contract.py` aceitar a forma "against a limit of
  10" ou ajustar o roteiro EN; commitar `docs/video-*.md` e
  `docs/video-production-plan.md`; linkar o plano de produção no README;
- adendo ao SF-006 que **reavalia** o redesign da UI (commits `0826cdf` e
  `5fb9094`) contra as condições de rejeição do SF-006, em vez de só registrar
  (achado HIGH-2 do risk-reviewer). Pontos observados em `web/src/App.vue`:
  pílulas `neutral` versus `optimized` com estilos diferentes; ponte
  "Constraint-aware allocation → +N min" que só computa ganho a favor do CP-SAT;
  rodapés assimétricos ("blind to the next request" versus "Both requests
  placed"); título "Make every opening work harder." em registro de marketing.
  Resultado exigido: tratamento visual igual entre planos, rótulo neutro
  ("difference in this fixture") e título descritivo; ou reabertura explícita
  do SF-006 com gate humano. Teste de frases proibidas também na aba Evidence;
- decisão sobre `@fullcalendar/vue3` e `temporal-polyfill`: remover de
  `package.json`, do spec, do README e da ADR, ou restaurar o uso. Recomendação:
  remover, porque a grade de tempo própria já cobre o SF-006 e reduz dependência;
- reformatar `web/src/App.vue` em componentes legíveis (`ResearchStrip.vue`,
  `ScheduleGrid.vue`, `AssignmentTable.vue`, `ReviewPanel.vue`), sem mudar
  comportamento; os cinco testes Playwright são a rede de regressão;
- atualizar `docs/bolts/README.md`, card S3 e "Open decisions" do audit;
- mensagens de commit no formato convencional.

DoD: `make verify` verde; `git status` limpo; spec-reviewer e test-reviewer sem
achados bloqueantes; audit atualizado. Sem nova funcionalidade.

### SF-010 — Fixture "clinic-day" e explicações em linguagem simples (domínio + API)

Escopo de domínio:

- `slotfit.scenarios.clinic_day_story(seed: int = 1600) -> tuple[Scenario, DayContext]`:
  um dia sintético (2026-11-04, `America/Toronto`) com as **mesmas** duas
  aberturas e duas solicitações do contra-exemplo atual, mais uma terceira
  solicitação inelegível por sala, para que os reason codes apareçam. A
  estrutura de decisão é um superconjunto da fixture
  `multi-slot-counterexample-1500`, então os planos FIFO, best-fit e CP-SAT
  devem reproduzir 60/60/120 minutos;
- `DayContext` é um tipo novo e separado (atendimentos já marcados, janela do
  dia) usado apenas para exibição. Ele nunca entra em `Scenario` nem nas
  estratégias. Teste metamórfico: remover o contexto não altera nenhum plano;
- `slotfit.explanations.explain(reason_code: str) -> str` com texto curto em
  inglês para cada um dos seis códigos existentes
  (`NO_COMMUNICATION_CONSENT`, `PROVIDER_NOT_ELIGIBLE`,
  `REQUIRED_ROOM_UNAVAILABLE`, `DURATION_EXCEEDS_INTERVAL`,
  `INSUFFICIENT_NOTICE`, `REQUEST_NOT_AVAILABLE`) e para o estado elegível.
  Função pura; teste garante cobertura total e falha se um código novo surgir
  sem texto.

Escopo de API:

- `GET /api/v1/demos/clinic-day` devolve `DemoResponse` estendido com
  `day_context` e, em cada `CandidateEvaluationResponse`,
  `explanations: list[str]`;
- `schema_version` incrementada; teste de contrato para o novo demo.

Testes primeiro: replay determinístico por seed; igualdade dos planos com a
fixture 1500 nas aberturas compartilhadas; zero violações duras; cobertura de
explicações; invariância do contexto.

Disciplina de seeds: `1600` é uma fixture construída à mão, fora de
`SPLIT_SEEDS` e `MULTI_SLOT_SEEDS`; registrar isso na spec para que nunca seja
confundida com um seed de desenvolvimento. A copy de `explain()` não pode usar
vocabulário das bandas de auditoria ("scarce resource", "narrow availability",
"aging"), para que a UI não pareça consciente de slices.

DoD: `make test` e `make api-smoke` verdes; nenhuma estratégia alterada;
traceability recebe `SF-FR-010` (fixture narrativa) e `SF-FR-011` (explicações).

### SF-011 — Modo "Um dia na clínica" (UI narrativa)

Escopo:

- nova aba `Story` ao lado de `Evidence`; a página atual vira a aba `Evidence`
  sem mudanças funcionais;
- seis capítulos navegáveis por botões, teclado (setas, Home/End) e barra de
  progresso; o capítulo vai para a URL (`?chapter=3`) para link direto na
  gravação do vídeo;
- capítulos 1–2: agenda do dia com atendimentos marcados e os dois horários que
  se abrem; contador "capacidade sem uso" em minutos e atendimentos;
- capítulos 3–4: animação única do cartão entrando na abertura; mensagem
  `Not compatible` para a restrita no segundo horário; plano CP-SAT com motivos
  em linguagem simples vindos de `explanations`;
- capítulo 5: painel de revisão existente reutilizado;
- capítulo 6: resumo e botão "ver por baixo dos panos" que leva ao SF-013;
- `prefers-reduced-motion` respeitado; tabela semântica mantida em todos os
  capítulos com agenda;
- faixa de no-go persistente em todos os capítulos, com teste de link direto
  (seção 3, regra de integridade);
- copy revisada pela skill `design:ux-copy` e pelo `risk-reviewer`. Frases
  proibidas, testadas em Story e Evidence: "AI optimized", "fair", "unbiased",
  "bias-free", "guarantee", "more patients", "patient", "care",
  "appointments delivered", "revenue", "production ready", e "proves"/"prova"
  sem "within the declared model"/"dentro do modelo declarado" na mesma frase.

Condição de rejeição do SF-011: qualquer capítulo, captura ou link direto em
que o resultado `120` apareça sem a faixa de no-go visível.

Testes Playwright novos: navegação completa por teclado; números exibidos iguais
aos da API; texto `No external action` após revisão; axe sem violações sérias
em cada capítulo; reduced-motion não quebra o fluxo.

DoD: `make verify` com os testes novos; `ecc:a11y-architect` sem achados
bloqueantes; captura de tela de cada capítulo em `artifacts/story/` para o
vídeo; nenhuma frase proibida (teste de contrato de UI).

### SF-012 — Enquadramento de capacidade dentro da fronteira de claims

Escopo:

- definir e testar as métricas narrativas com nomes que não viram claim de
  acesso ou cuidado (achado HIGH-3 do risk-reviewer): `requests_not_placed`,
  `openings_unfilled` e o já existente `remaining_gap_minutes`, exibido como
  "opening minutes not assigned". Não existem `idle_provider_minutes` nem
  `appointments_not_delivered`: uma solicitação sintética não colocada não é um
  atendimento que deixou de ser entregue a alguém. A frase "capacidade já paga"
  fica fora de qualquer copy pública, porque é enquadramento financeiro por
  outro nome;
- decidir e documentar (ADR-0004) se existe um "cenário hipotético" com valor
  por hora informado pelo espectador. Recomendação firme: **não neste ciclo**
  (D1a). Se um dia for adotado: apenas no modo Story, desligado por padrão,
  nunca persistido, nunca enviado à API, nunca no campo `rationale`, desligado
  em toda captura de tela e trace usados em artefatos, com o rótulo "your
  assumption, not a result of this study", com teste que garante ausência no
  modo Evidence e nas capturas, e com "dinheiro em qualquer artefato público"
  listado como condição de rejeição na ADR;
- atualizar `docs/fairness-and-bias-plan.md` seção "Human factors and
  presentation bias" com o novo risco de ancoragem monetária.

Gate: `blocking-approval` com `risk-reviewer`. Esta é a única spec que toca a
fronteira de claims.

### SF-013 — Explorador do motor ("por baixo dos panos")

Escopo:

- painel técnico com três camadas abertas uma a uma: **regras** (tabela de
  elegibilidade solicitação × abertura com reason codes e explicação),
  **solver** (as três fases com `status`, `objective_value` e a frase "optimal
  within the declared model"; uma visualização bipartida simples das variáveis
  solicitação × abertura e das restrições ativas) e **integridade** (testes
  contrafactuais de ID e ordem, faixa de no-go 10,80 vs 10, por que não há V5);
- cartão "why not generative AI" com a tabela da seção 2 em versão curta e o
  rótulo "design rationale, not a measured result";
- dados: `optimizer_evidence.phases` já existe; adicionar ao
  `OptimizerEvidenceResponse` os campos `variable_count` e `constraint_count`,
  expostos pelo `OptimizationResult`; teste garante igualdade com o modelo
  construído. Como `OptimizationResult` é um tipo de domínio congelado, o Bolt
  reexecuta os testes de igualdade de plano do V1 e declara "nenhuma estratégia
  alterada" na DoD. O risk-reviewer confirmou que variáveis e restrições vêm só
  de atributos de decisão; slices de auditoria não entram.

Testes: contrato da API para os campos novos; Playwright verificando que o
painel mostra `OPTIMAL` três vezes para o plano CP-SAT e `reject` quatro vezes
na seção de integridade; axe.

DoD: `make verify`; `test-reviewer` confirma que nenhum número do painel é
literal no código da UI.

### SF-014 — Refresh de comunicação

Escopo:

- roteiros EN/PT e storyboard reescritos sobre os seis capítulos, mantendo os
  mesmos números e o contrato de publicação; o teste de paridade numérica
  amplia o conjunto de números para cobrir os novos (3 solicitações, 14:00,
  15:30) e não só `40|60|120|10.80`;
- capturas e GIF são superfícies de claim: toda captura usada em README, post
  ou vídeo inclui a faixa de no-go e é gerada com qualquer hipótese monetária
  desligada;
- README ganha "Start here": três capturas (capítulo 3, capítulo 4, faixa de
  no-go) e o fluxo de 2 minutos; GIF do capítulo 4 gerado a partir do trace do
  Playwright, não de gravação manual;
- rascunhos de LinkedIn com a frase-guia e a explicação de "qual IA" em duas
  linhas;
- placeholders de URL substituídos **somente** após a criação do remote, que é
  ação externa e exige autorização explícita;
- checklist de publicação com os gates de qualidade do plano de vídeo.

DoD: testes de contrato de publicação verdes; links relativos resolvem;
`risk-reviewer` sem achados; nada publicado automaticamente.

## 6. Ordem, dependências e esforço

```
SF-009 ──► SF-010 ──► SF-011 ──► SF-013 ──► SF-014
                         │
                         └──► SF-012 (gate de claims; pode correr em paralelo
                                     com SF-013, mas antes de SF-014)
```

| Bolt | Tamanho | Sessões estimadas | Gate |
|---|---|---|---|
| SF-009 | pequeno | 1 | timed-veto (sem mudança observável) + blocking para remoção do FullCalendar |
| SF-010 | médio | 1–2 | blocking (contrato de API) |
| SF-011 | grande | 2–3 | blocking (design) |
| SF-012 | pequeno | 1 | blocking (claims) |
| SF-013 | médio | 1–2 | blocking (contrato de API) |
| SF-014 | médio | 1 | blocking (publicação) |

Uma spec ativa por vez, conforme `AGENTS.md`. Cada Bolt começa pelo menor teste
que falha, termina com `make verify` e com `make demo` quando a saída observável
muda, registra evidência na spec e atualiza traceability e audit.

## 7. Riscos e como o plano os controla

| Risco | Controle |
|---|---|
| A narrativa "vende" e contradiz a neutralidade do SF-006 | SF-011 mantém ordem baseline-first, nenhum plano "recomendado", teste de frases proibidas |
| Prejuízo financeiro vira claim | SF-012 com gate de risco; métricas só em capacidade; hipótese do espectador, se existir, isolada e rotulada |
| Personas sintéticas parecem pessoas reais | sem sobrenome, selo "synthetic data" permanente, `risk-reviewer` revisa a copy |
| Números da história divergem do motor | toda métrica vem da API; testes comparam UI e API; nenhuma constante numérica na UI |
| Animação bonita esconde o no-go | capítulo 6 obrigatório; faixa de no-go permanece no modo Evidence e no fim da história |
| Escopo cresce para "produto" | nenhuma integração, nenhum dado real, nenhuma autenticação; qualquer um desses exige novo ciclo e novo threat model |
| Dependência nova sem necessidade | SF-009 remove FullCalendar; nenhuma biblioteca de animação; CSS e `requestAnimationFrame` bastam |
| Links diretos, capturas e GIFs contornam os testes de contrato de publicação | faixa de no-go persistente e testada em link direto; capturas geradas por Playwright com a faixa visível; nenhuma hipótese monetária em captura |
| Nomes fictícios viram proxy demográfico ligado ao resultado "restrita" | D2a por padrão; se D2b, nomes só em `DayContext`/mapa de rótulos da UI, nunca em `Scenario`, payloads de decisão, eventos de revisão ou exportações, com teste; nota "placeholders aleatórios, não pacientes" |
| Aba Evidence já perdeu neutralidade no redesign | SF-009 reavalia contra as condições de rejeição do SF-006 antes de qualquer Bolt novo |

## 8. Decisões que só você pode tomar

Em ordem de impacto. Cada uma muda o que será construído.

- **D1 — Valor monetário.** (a) Nunca mostrar dinheiro, só capacidade.
  (b) Permitir hipótese do espectador, isolada e rotulada, como descrito em
  SF-012. Recomendação: **(a)** para o primeiro ciclo de publicação; (b) só
  se a audiência de negócio pedir, e nunca no vídeo.
- **D2 — Personas com nome.** (a) Rótulos funcionais ("flexible request",
  "restricted request"). (b) Primeiros nomes fictícios com selo sintético.
  Recomendação revisada após o risk-reviewer: **(a)** em ambos os modos.
  Privacidade não é o problema; o problema é que um primeiro nome carrega
  sinal de gênero e etnia, e ligar um nome à solicitação "restrita" que fica de
  fora associa visualmente um marcador demográfico a uma exclusão, exatamente a
  associação que o projeto evitou em oito specs. Se você preferir (b), valem os
  controles da tabela de riscos.
- **D3 — FullCalendar.** Remover a dependência ou restaurar o uso.
  Recomendação: remover.
- **D4 — Idioma da UI.** Somente inglês, ou alternância EN/PT no modo Story.
  Recomendação: somente inglês na UI; PT fica nos roteiros e no post.
- **D5 — Segunda linha de pesquisa.** Reabrir S7 com nova hipótese e novos
  registries fica fora deste ciclo. Confirmar que continua fora.

## 9. Rastreabilidade a adicionar após aprovação

| Requisito novo | Descrição | Bolt |
|---|---|---|
| SF-FR-010 | fixture narrativa de um dia sintético, superconjunto do contra-exemplo | SF-010 |
| SF-FR-011 | explicação em linguagem simples para todo reason code | SF-010 |
| SF-FR-012 | modo narrativo em seis capítulos com os mesmos números do motor | SF-011 |
| SF-FR-013 | métricas de capacidade não entregue derivadas do plano | SF-012 |
| SF-FR-014 | explorador do motor com fases, contagens e integridade | SF-013 |
| SF-NFR-009 | nenhuma constante numérica de resultado na UI | SF-011, SF-013 |
| SF-NFR-010 | `prefers-reduced-motion` respeitado em toda animação | SF-011 |

## 10. Evidência que fecha o ciclo

- `make verify` verde com os testes novos (Python, API, build, Playwright);
- capturas de cada capítulo em `artifacts/story/`;
- `aidlc-docs/state.md` com o ciclo 2 completo e gates registrados;
- `audit.md` com cada decisão D1–D5 e seu resultado;
- roteiros, storyboard e posts alinhados aos seis capítulos e aos mesmos números;
- nada publicado, nada enviado, nenhum dado real.

## Revisão de risco da proposta

O `risk-reviewer` do repositório avaliou esta proposta em 2026-10-26 com o
veredito **aprovar com mudanças**. As mudanças exigidas foram incorporadas acima:
faixa de no-go persistente e testada em link direto (HIGH-1); reavaliação da
aba Evidence contra o SF-006 (HIGH-2); métricas renomeadas sem conotação de
acesso ou cuidado (HIGH-3); D1a recomendado e controles extras se D1b (HIGH-4);
frase-guia reescrita e "prova" gateada por teste (MEDIUM-5); D2a recomendado e
controles para D2b (MEDIUM-6); comparações de mercado e com IA generativa
rotuladas como premissa ou justificativa de design (MEDIUM-7); guardrails para
`explain()` e para a mudança em `OptimizationResult` (LOW-8); seed 1600,
paridade numérica ampliada e capturas como superfície de claim (LOW-9).

## Mock visual

Um mock dos capítulos 2 a 4 foi produzido como artefato de design para aprovação
dos beats antes de qualquer código. O link fica registrado no audit quando a
decisão de design for tomada. O mock é ilustração de layout e linguagem; os
números nele são os da fixture atual (60/120) e não substituem a API. O mock
usa rótulos funcionais (D2a) e carrega a faixa de no-go em todas as telas.

Este diretório contém uma série de prompts com conhecimento específico sobre cada metadado de projetos Salesforce. Esses prompts serão usados como apoio em agentes.

A ideia é refiná-los com contexto suficiente para que, mesmo quando for necessária busca adicional na web, ela seja **pontual, direcionada e assertiva**.

O objetivo é atingir um nível de conhecimento de referência sobre cada componente da plataforma Salesforce, com foco em **estrutura, fontes de configuração, objetos internos relacionados, formas de extração, limitações e interpretação correta dos dados**.

O material gerado deve servir como **referência técnica inicial**, e não como documentação funcional exaustiva.  
Por isso, a resposta pode e deve ser longa quando necessário, priorizando **completude técnica, rastreabilidade e precisão** em vez de concisão.

---

## Objetivo do markdown

Refatorar o markdown do componente solicitado para que ele explique, de forma estruturada:

- o que é o componente;
- para que ele serve;
- em quais clouds/contextos ele se aplica;
- como ele aparece no metadata;
- como ele se relaciona com objetos internos da plataforma;
- quais dados podem ser extraídos por XML, API padrão, Tooling API, Apex ou UI;
- quais campos e estruturas existem de fato;
- quais limitações, lacunas e ambiguidades precisam ser respeitadas na interpretação.

---

## Requisitos gerais

### 1. Usar nomes internos reais
Sempre usar os **nomes internos exatos** dos artefatos técnicos, sem substituir por nomes genéricos ou traduzidos, incluindo:
- metadata types;
- tags XML;
- objetos internos;
- campos;
- enums e valores possíveis;
- componentes relacionados.

Quando existir diferença entre nome de UI e nome interno, mostrar ambos, deixando claro qual é qual.

### 2. Não simplificar indevidamente
Não gerar texto excessivamente resumido.  
O markdown deve funcionar como base de consulta para agentes, então pode ser extenso.

### 3. Separar claramente fontes de informação
Diferenciar explicitamente:
- configuração declarada no XML/metadata;
- configuração observável em objetos internos;
- configuração observável em Tooling API;
- configuração observável em UI ou outras fontes;
- estado efetivo de acesso, uso, autorização ou comportamento operacional.

### 4. Priorizar rastreabilidade
Sempre deixar claro **de onde vem cada informação**:
- metadata retrieve;
- arquivo XML;
- SOQL na API padrão;
- Tooling API;
- Apex executado dentro da org;
- UI/admin setup;
- documentação oficial;
- limitação conhecida / informação não exposta.

---

## Informações obrigatórias que devem constar no markdown

### A. Contexto do componente
- explicação do que o componente principal é;
- explicação de para que serve;
- cenários típicos de uso;
- cloud(s) ou contexto(s) onde está disponível ou faz sentido, por exemplo:
  - Salesforce Core
  - Service Cloud
  - Sales Cloud
  - Experience Cloud
  - Data Cloud
  - Marketing Cloud
  - Agentforce
  - ou outros contextos relevantes

Se a disponibilidade variar por produto, edição, licença ou contexto, isso deve ser apontado.

---

### B. Mapa estrutural do componente principal e relacionados
Para o **componente principal** e também para os **componentes relacionados relevantes**, informar:

- nome funcional;
- nome exato do metadata type no `package.xml`;
- nome exato da pasta/estrutura no projeto Salesforce após retrieve;
- nome exato do(s) objeto(s) interno(s) associados;
- se cada objeto/fonte é acessível via:
  - Metadata API retrieve/deploy
  - API padrão / SOQL
  - Tooling API
  - Apex dentro da org
  - UI apenas
  - não acessível / não confirmado

Também indicar:
- limitações de acesso;
- diferenças entre componente custom e standard, quando aplicável;
- lacunas conhecidas de cobertura.

Se algum componente standard não tiver representação completa ou recuperável, isso deve ser explicitamente apontado no markdown.

Exemplo do tipo de observação esperada:
- existe registro interno;
- mas não possui retrieve completo em metadata;
- ou não expõe todos os dados por API;
- ou há diferença entre configuração operacional e representação em metadata.

---

### C. Inventário técnico da configuração interna
Para o **componente principal**, separar obrigatoriamente as informações em camadas.

#### 1. Estrutura XML / Metadata
Incluir uma seção específica com:
- lista das **tags, blocos e estruturas XML reais** do componente;
- nomes exatos das tags;
- explicação prática do que cada tag representa;
- possíveis valores/configurações quando conhecidos;
- observação sobre obrigatoriedade, recorrência, valor padrão ou comportamento associado, quando isso puder ser afirmado com segurança.

Não basta citar os nomes: é necessário explicar **o que cada campo significa na prática**.

#### 2. Objeto interno via API padrão
Se existir objeto consultável por API padrão, listar:
- nome real do objeto;
- campos relevantes para entendimento do componente;
- explicação prática de cada campo;
- relação entre os campos do objeto e a configuração do componente;
- limitações do que pode ou não ser consultado.

#### 3. Objeto interno via Tooling API
Se existir exposição relevante via Tooling API, listar:
- nome real do objeto;
- campos relevantes;
- explicação prática de cada campo;
- contexto em que esse acesso é necessário ou útil;
- limitações e diferenças em relação à API padrão.

#### 4. Configuração observável em outras fontes
Listar o que pode ser visto ou validado apenas em:
- UI;
- setup;
- telas administrativas;
- políticas relacionadas;
- permission sets;
- profiles;
- objetos relacionados;
- outras fontes complementares.

#### 5. Campos mascarados, omitidos, protegidos ou irrecuperáveis
Destacar explicitamente:
- campos que não aparecem no retrieve;
- campos que aparecem mascarados;
- campos que existem na UI mas não no XML;
- campos cujo valor não é exposto por segurança;
- informações que não podem ser confirmadas apenas com os artefatos disponíveis.

---

### D. Dados relevantes dos componentes relacionados
Para cada componente relacionado, incluir apenas os dados realmente importantes para:
- entendimento do componente principal;
- parametrização;
- governança;
- auditoria;
- documentação técnica;
- validação de comportamento;
- análise de acesso ou dependências.

Não listar relacionados de forma decorativa; explicar por que cada relacionado importa.

---

## Regras de interpretação

### Sobre XML e metadata
- Não inventar nomes de tags.
- Não normalizar nomes de tags para português.
- Não presumir que ausência de tag significa desativação sem validar o comportamento padrão.
- Não assumir que o XML contém tudo o que aparece na UI.
- Não assumir equivalência 1:1 entre UI, XML, objeto interno e estado operacional.
- Quando houver inferência, marcar explicitamente como inferência.
- Quando algo não puder ser confirmado, declarar explicitamente a limitação.

### Sobre objetos internos
- Usar nomes reais e exatos.
- Não assumir que a existência de um objeto interno implica acesso simples via query.
- Diferenciar claramente objeto existente, objeto consultável, objeto acessível via Tooling e objeto apenas conhecido conceitualmente/documentalmente.

### Sobre estado efetivo
Sempre separar:
1. **configuração declarada no metadata/XML**;
2. **configuração observada em outras fontes**;
3. **estado efetivo de acesso/autorização/comportamento**.

Não inferir estado efetivo apenas com base em metadata, salvo quando isso for comprovadamente suficiente.

---

## Consultas e formas de extração

### Query via API padrão
Quando houver consulta relevante via API padrão, incluir:
- exemplo de query;
- explicação do que ela retorna;
- observações sobre filtros úteis;
- cuidados com permissões;
- explicação de como tratar paginação automaticamente quando houver mais de 200 registros.

### Tooling API / Apex
Quando houver consulta relevante via Tooling API, incluir:
- exemplo de uso por Apex ou outra abordagem viável;
- explicação de como isso poderia ser usado:
  - dentro da org;
  - no VS Code;
  - em automações;
- formato esperado de retorno;
- orientação sobre como converter ou tratar saída em:
  - texto,
  - CSV,
  - JSON,
  - ou outros formatos úteis.

---

## Boas práticas e pontos de atenção
Incluir:
- boas práticas de configuração do componente principal;
- riscos comuns;
- armadilhas de interpretação;
- dependências importantes;
- impactos de segurança, integração, governança ou manutenção;
- diferenças entre o que é configurado, o que é observável e o que é efetivamente aplicado.

---

## Links
Incluir links oficiais de referência, preferencialmente:
- Salesforce Help
- Salesforce Developer Documentation
- documentação do componente principal
- documentação dos componentes relacionados relevantes

---

## Diretriz de escrita
A ideia aqui é **contextualizar tecnicamente** o componente e mapear suas fontes de verdade e limitações, e **não** fazer uma documentação funcional completa de ponta a ponta.

O markdown deve ser útil como:
- referência inicial;
- base para agentes;
- ponto de partida para investigação;
- guia para buscas adicionais altamente direcionadas.

Se alguma informação não estiver disponível de forma confiável, isso deve ser explicitamente declarado no markdown, em vez de ser preenchido por suposição.

---

## Tarefa inicial
Vamos começar por tudo que for relacionado a **integração**.

Refatore o markdown do **Named  Credential** para validação inicial, seguindo todas as regras acima.


OBS: siga o mesmo padrão de esteutura e explicação de: ./tools/templates/exemplos-prompts/prompt-connected-app.md

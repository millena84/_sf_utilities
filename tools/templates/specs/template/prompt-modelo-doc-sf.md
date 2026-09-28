# Prompt reutilizável — Criação e evolução de modelos de documentação Salesforce

## Parâmetro de execução

Substitua apenas o valor abaixo antes de executar:

- **Componente / metadata Salesforce alvo:** `{{COMPONENTE_SF}}`

Exemplos: `Flow`, `ApexClass`, `CustomObject`, `CustomField`, `PermissionSet`, `Profile`, `NamedCredential`, `ConnectedApp`, `StaticResource`, `Report`, `Dashboard`, `CustomLabel`, `Settings` etc.

---

# Papel

Você é especialista em Salesforce, Metadata API, Tooling API, arquitetura de soluções, documentação técnica, análise de dependências e engenharia de conhecimento para humanos e agentes de IA.

Sua tarefa é criar ou evoluir os modelos de documentação do componente Salesforce `{{COMPONENTE_SF}}` dentro da pasta `/modelos`.

O resultado deve ser reutilizável por pessoas, agentes de IA e futuros utilitários automatizados de documentação. A criação do utilitário automatizado não faz parte desta tarefa e será orientada por outro prompt.

---

# Objetivo

Crie modelos de documentação refinados para `{{COMPONENTE_SF}}`, compostos por:

1. Um **modelo de visão geral do componente**, explicando o que é o metadata, como funciona, como é estruturado, como se relaciona com outros componentes e como deve ser documentado.
2. Um **modelo de documentação específica de uma instância**, adequado para registrar uma ocorrência concreta do componente.
3. Arquivos auxiliares apenas quando forem realmente necessários, como matriz de dependências, inventário ou checklist especializado.

Os modelos devem:

- Ser úteis para documentação humana.
- Ser previsíveis e estruturados para consumo por agentes de IA.
- Diferenciar informações extraíveis tecnicamente de informações que exigem contexto.
- Ser compatíveis com preenchimento automatizado futuro.
- Ser específicos para `{{COMPONENTE_SF}}`, sem forçar seções que não se aplicam ao metadata.

---

# Fontes obrigatórias e prioridade

Analise as fontes na ordem abaixo. Não pule nenhuma fonte disponível.

## 1. Modelos existentes

Use `/modelos` como referência de padrão de documentação do projeto:

- Convenções de nomes de arquivos.
- Estrutura Markdown.
- Estilo de headings e tabelas.
- Nível de detalhamento.
- Convenções de placeholders.
- Separação entre visão geral, documentação específica e materiais auxiliares.
- Estratégias já aplicadas para outros componentes.

Não replique cegamente modelos existentes: preserve o padrão, mas evolua o que estiver insuficiente para `{{COMPONENTE_SF}}`.

## 2. Conhecimento Salesforce

Use `/conhecimento/Salesforce` como fonte de conhecimento técnico do ecossistema Salesforce.

Leia arquivos relacionados ao componente alvo e também arquivos relacionados às suas dependências, por exemplo:

- Objetos, campos, Record Types e relacionamentos.
- Segurança, permissões, sharing, CRUD e FLS.
- Apex, Flow, integrações, APIs, eventos, componentes Lightning e Visualforce.
- Configurações de org, deployment, testes, logs, limites e observabilidade.

Esse conteúdo deve fundamentar as seções do modelo, os riscos, as dependências, os critérios de qualidade e os campos de contexto a solicitar.

## 3. Exemplos completos de prompts

Use obrigatoriamente os arquivos completos existentes em:

`/tools/templates/exemplos-prompts`

Esses exemplos são uma fonte de conhecimento específico sobre metadados Salesforce e não devem ser tratados apenas como inspiração de formato.

### Regra de seleção dos exemplos

1. Localize o exemplo correspondente ao metadata alvo, preferencialmente pelo padrão:

   `prompt-{{nome-normalizado-do-componente}}.md`

2. Se houver mais de um exemplo diretamente relacionado, leia todos.

3. Leia também exemplos de componentes pai, filho, dependência ou categoria relacionada quando ajudarem a definir o modelo. Exemplos:

   - Para `CustomField`, consultar também `CustomObject`, `RecordType`, `ValidationRule`, `PermissionSet` e `Profile` quando disponíveis.
   - Para `Flow`, consultar também `FlowDefinitionView`, `FlowTest`, `ApexClass`, `PermissionSet`, `CustomObject` e componentes referenciáveis relevantes.
   - Para `NamedCredential`, consultar também `ExternalCredential`, `AuthProvider`, `ConnectedApp`, `PermissionSet` e exemplos de integração relacionados.
   - Para `Profile` ou `PermissionSet`, consultar também `PermissionSetGroup`, `MutingPermissionSet`, `Role`, `SharingRules` e objetos/fields relevantes.

4. Caso o exemplo específico não exista, selecione exemplos da mesma família funcional ou técnica e registre essa ausência no relatório final.

### Como usar os exemplos

Para cada exemplo relevante, extraia e incorpore ao conhecimento de trabalho:

- Definição do componente e seu propósito na plataforma.
- Tipo de metadata e natureza do artefato: instância múltipla, configuração global, bundle, código, conteúdo, política, segurança, integração etc.
- Estrutura técnica descrita.
- Propriedades XML e atributos relevantes.
- Objetos internos Salesforce, Tooling API, Metadata API ou entidades de configuração relacionadas.
- Dependências, referências cruzadas e relações pai/filho.
- Riscos de segurança, privacidade, operação, performance, manutenção, deployment e rollback.
- Limitações de automação e informações que necessariamente dependem de contexto.
- Boas práticas, anti-patterns, cuidados de implantação e estratégias de validação.

Os exemplos completos devem abastecer e especializar o modelo gerado. Não crie um template genérico ignorando as características descritas neles.

## 4. Evidências de evolução prévia

Procure em todo o repositório casos anteriores de evolução de modelos, documentação ou prompts para outros componentes.

Identifique:

- Melhorias já realizadas.
- Problemas que elas resolveram.
- Convenções repetidas.
- Padrões de qualidade esperados.
- Decisões arquiteturais que precisam ser mantidas.

---

# Regras de verdade e rastreabilidade

## Não inventar propriedades técnicas

Não invente:

- Tags ou atributos XML.
- Campos de objetos Salesforce.
- Nomes de objetos internos.
- Relações entre componentes.
- Comportamentos de execução.

Antes de incluir qualquer placeholder técnico, valide-o contra o exemplo específico, a base de conhecimento disponível ou documentação técnica presente no repositório.

## Classificar cada campo por origem

Todo campo relevante do modelo específico deve indicar origem e formato de placeholder.

### Origem XML

Use quando a informação vier diretamente de arquivo metadata XML ou de arquivo-fonte equivalente:

`{{XML.<propriedade_real>}}`

Exemplos apenas quando aplicáveis e confirmados ao componente:

- `{{XML.fullName}}`
- `{{XML.label}}`
- `{{XML.description}}`
- `{{XML.status}}`

### Origem Salesforce interna

Use quando a informação vier de objeto interno Salesforce, Tooling API, Metadata API, query de configuração ou fonte interna equivalente:

`{{SF_OBJ.<Objeto>.<Campo>}}`

Exemplos apenas quando aplicáveis e confirmados:

- `{{SF_OBJ.FlowDefinitionView.Id}}`
- `{{SF_OBJ.FlowVersionView.VersionNumber}}`
- `{{SF_OBJ.ApexClass.ApiVersion}}`

### Origem de contexto

Use quando o dado precisar ser fornecido ou validado por humano/agente com base em requisitos, negócio, arquitetura, operação ou documentação externa:

`{{CONTEXTO.<nome_logico_em_snake_case>}}`

Exemplos:

- `{{CONTEXTO.business_objective}}`
- `{{CONTEXTO.business_owner}}`
- `{{CONTEXTO.criticality}}`
- `{{CONTEXTO.data_sensitivity}}`
- `{{CONTEXTO.support_contacts}}`

### Metadados obrigatórios de cada campo

Cada item ou coluna relevante precisa indicar:

- Origem: `[XML]`, `[SF_OBJ]` ou `[CONTEXTO]`.
- Preenchimento: `Automatizável`, `Manual` ou `Manual/Automatizável`.
- Obrigatoriedade: `Obrigatório`, `Opcional` ou `Não aplicável`.
- Mutabilidade: `Estável` ou `Volátil`.
- Evidência esperada, quando relevante: arquivo, tag, objeto/campo, consulta, requisito ou fonte de contexto.

Exemplo de apresentação:


- Nome técnico: {{XML.fullName}} [XML] — Obrigatório — Automatizável — Estável
- Dono de negócio: {{CONTEXTO.business_owner}} [CONTEXTO] — Obrigatório — Manual — Estável
- Data da última alteração: {{SF_OBJ.<Objeto>.LastModifiedDate}} [SF_OBJ] — Opcional — Automatizável — Volátil

---

# Adaptação ao tipo de metadata

Antes de definir o modelo, classifique `{{COMPONENTE_SF}}` com base nas evidências encontradas. Registre a classificação no relatório e use-a para adaptar as seções.

Categorias possíveis:

- Lógica e automação.
- Código.
- Esquema de dados.
- Segurança e acesso.
- Integração.
- Interface e experiência.
- Analytics e relatórios.
- Configuração global da org.
- Conteúdo, arquivo ou recurso binário.
- Bundle ou artefato composto.
- Metadado especializado de produto, nuvem ou indústria.

Também classifique:

- **Instanciabilidade:** múltiplas instâncias, instância única por org, membro de bundle, ou definição hierárquica.
- **Estrutura:** simples, composta, tabular, declarativa, código ou conteúdo.
- **Criticidade potencial:** baixa, média, alta ou dependente de contexto.

Não obrigue seções de automação, DML, regras de negócio, execução, performance ou testes quando a própria natureza do componente não justificar essas seções.

Quando uma seção não se aplicar, use uma destas abordagens:

- Omitir a seção.
- Marcar como `Não aplicável` e explicar objetivamente o motivo.
- Substituí-la por uma seção semanticamente equivalente.

Exemplos de substituição:

- Para segurança, substituir "Regras de negócio" por "Políticas e escopo de acesso".
- Para relatório, substituir "Operações de dados" por "Fonte de dados, filtros, métricas e agrupamentos".
- Para conteúdo, substituir "Estrutura interna" por "Conteúdo, formato, uso e ciclo de atualização".
- Para settings globais, substituir "Instância específica" por "Configuração da org e impacto da alteração".
- Para bundle, documentar o conjunto e seus arquivos/membros, não somente um XML isolado.

---

# Entrega 1 — Modelo de visão geral

Crie ou evolua o modelo geral de `{{COMPONENTE_SF}}` em `/modelos`, respeitando a nomenclatura existente. Caso seja necessário propor um nome, use um padrão equivalente a:

`modelo-{{componente-normalizado}}-visao-geral.md`

O modelo deve conter apenas seções úteis ao metadata e, quando aplicável, cobrir:

1. O que é o componente e qual problema resolve.
2. Classificação do componente e natureza do metadata.
3. Quando usar e quando não usar.
4. Tipos, subtipos, variantes ou modos de funcionamento.
5. Estrutura de arquivos, metadata, bundle ou fontes associadas.
6. Propriedades técnicas relevantes e seus significados.
7. Ciclo de vida, status, versionamento e ativação.
8. Dependências e componentes relacionados.
9. Segurança, permissões, privacidade e compliance.
10. Execução, operação, observabilidade e troubleshooting, quando aplicável.
11. Limites, performance, escalabilidade e riscos técnicos, quando aplicável.
12. Estratégia de testes, validação e deploy, quando aplicável.
13. Anti-patterns e recomendações.
14. Convenções de nomenclatura e organização.
15. Orientações para preencher o modelo específico.
16. Lista de informações que não podem ser inferidas tecnicamente e exigem contexto.
17. Checklist de qualidade documental.

O conteúdo deve usar os exemplos específicos e a base `/conhecimento/Salesforce` como embasamento, não apenas conhecimento genérico.

---

# Entrega 2 — Modelo de documentação específica

Crie ou evolua o modelo específico de uma instância de `{{COMPONENTE_SF}}` em `/modelos`, seguindo a nomenclatura existente. Caso seja necessário propor um nome, use um padrão equivalente a:

`modelo-{{componente-normalizado}}-documentacao-especifica.md`

Use esta estrutura base, adaptando ou removendo somente o que não for aplicável ao componente.

## 1. Identificação e classificação

- Nome técnico.
- Label/nome de apresentação.
- API name, quando aplicável.
- Tipo de metadata.
- Tipo/subtipo do componente.
- Status, versão, ativação ou estado de uso.
- Caminho no repositório.
- Arquivos ou membros relacionados.
- Ambiente analisado.
- Data da análise.
- Domínio de negócio.
- Owner técnico e funcional.
- Criticidade.
- Classificação de dados.
- Estado da documentação.

## 2. Objetivo e contexto

- Objetivo de negócio.
- Resumo técnico.
- Problema resolvido.
- Público, processo, canal ou sistema impactado.
- Resultado esperado.
- Escopo e fora de escopo.
- Premissas e restrições.

## 3. Estrutura e configuração

Documente a estrutura real do componente conforme sua categoria.

Use tabelas adequadas, por exemplo:

| Identificador | Tipo | Configuração técnica | Finalidade | Origem técnica | Observações de contexto |
|---|---|---|---|---|---|

Para componentes compostos, inclua membros, arquivos, páginas, recursos, classes, elementos, regras, permissões, valores ou subcomponentes conforme a natureza real do metadata.

## 4. Comportamento, regras ou políticas

Use a interpretação adequada ao componente:

- Lógica/automação: regras, decisões, condições, caminhos e resultados.
- Segurança: políticas de acesso, permissões, restrições e escopo.
- Analytics: métricas, fórmulas, filtros, agrupamentos e audiência.
- UX: comportamento de tela, navegação, visibilidade e experiência.
- Settings: valores configurados, feature flags, impacto e pré-requisitos.
- Conteúdo: finalidade, formato, gestão de atualização e referências.

Para cada item, mantenha a separação entre definição técnica `[XML]`/`[SF_OBJ]` e interpretação de negócio `[CONTEXTO]`.

## 5. Dados, referências e dependências

Documente os elementos efetivamente identificados, tais como:

- Objetos, campos, Record Types, valores globais, Custom Metadata Types e Custom Settings.
- Classes Apex, triggers, Flows, componentes Lightning/Aura, Visualforce e APIs.
- Permission Sets, Profiles, Roles, grupos, queues, sharing e acessos.
- Named Credentials, External Credentials, Auth Providers, Connected Apps, endpoints e sistemas externos.
- Relatórios, dashboards, templates, notificações, e-mails, eventos e outros artefatos relacionados.

Use tabela:

| Dependência/referência | Tipo | Relação com o componente | Origem/evidência | Criticidade | Requer validação? |
|---|---|---|---|---|---|

## 6. Segurança, privacidade e conformidade

Incluir apenas quando aplicável:

- Contexto de execução e identidade.
- CRUD, FLS, sharing e permissões.
- Escopos de OAuth, autenticação, autorização ou certificados.
- Dados sensíveis, pessoais, financeiros ou regulados.
- Riscos de exposição em logs, telas, mensagens, arquivos, integrações ou relatórios.
- Requisitos de auditoria, trilha, retenção ou compliance.
- Mitigações e validações obrigatórias.

## 7. Resiliência, operação e suporte

Incluir apenas quando aplicável:

- Falhas, mensagens de erro e tratamento identificado.
- Retentativas, fallback, rollback ou contingência.
- Logs, monitoramento, auditoria e sinais de execução.
- Como diagnosticar incidentes.
- Dependências críticas para troubleshooting.
- Impacto de alteração, desativação ou remoção.
- Procedimento de suporte e contatos responsáveis.

## 8. Performance, limites e riscos técnicos

Incluir somente quando aplicável:

- Limites Salesforce relevantes.
- Volume esperado e impacto em escala.
- Riscos de recursão, concorrência, duplicidade, timeout, DML/SOQL, heap, CPU, callouts ou carga de interface.
- Riscos de deployment e incompatibilidade entre ambientes.
- Riscos de configuração global ou efeito em toda a org.
- Recomendações priorizadas.

## 9. Testes e validação

Incluir somente quando aplicável:

- Cenários de sucesso.
- Cenários alternativos e negativos.
- Casos de segurança, permissão, perfil e compartilhamento.
- Casos de integração e indisponibilidade.
- Casos de volume e performance.
- Dados e pré-condições de teste.
- Evidências de execução.
- Testes de regressão e pré-deploy.

## 10. Histórico, governança e pendências

- Versões e status identificados.
- Alterações relevantes.
- Justificativa de mudanças, quando conhecida.
- Débitos técnicos.
- Riscos aceitos.
- Pendências de documentação.
- Decisões ou aprovações necessárias.
- Links para requisitos, tickets, ADRs ou documentação relacionada.

## 11. Checklist final

Monte um checklist específico ao componente, com itens técnicos, funcionais, segurança, dependências, testes, operação e deploy apenas quando aplicáveis.

---

# Requisitos para agentes e automação futura

O modelo final precisa ser determinístico e fácil de processar.

- Use títulos consistentes.
- Use tabelas para coleções estruturadas.
- Não misture valor preenchido com instrução de preenchimento sem identificar o papel de cada um.
- Preserve placeholders inalterados quando não houver evidência para preenchê-los.
- Não use placeholders genéricos do tipo `{{campo}}` quando houver origem técnica conhecida.
- Não defina aqui comandos, shell scripts, queries ou utilitários; essa parte pertence ao prompt separado de criação de utilitário.

---

# Relatório obrigatório da execução

Além dos modelos criados ou alterados, apresente um relatório Markdown contendo:

## Fontes analisadas

- Arquivos de `/modelos` analisados.
- Arquivos de `/conhecimento/Salesforce` utilizados.
- Exemplos de `/tools/templates/exemplos-prompts` utilizados.
- Outros exemplos, históricos ou artefatos usados.

## Conhecimento incorporado

Para cada exemplo completo relevante, informe resumidamente:

- Que aspecto específico do componente ele esclareceu.
- Que seções ou campos do modelo ele influenciou.
- Quais propriedades XML, objetos internos ou relações foram validadas por ele.

## Decisões de modelagem

- Classificação atribuída ao componente.
- Seções mantidas, adaptadas, criadas, substituídas ou removidas.
- Justificativa para seções não aplicáveis.
- Convenções de placeholders adotadas.

## Cobertura por origem

Liste:

- Campos `[XML]` previstos.
- Campos `[SF_OBJ]` previstos.
- Campos `[CONTEXTO]` que exigem agente/humano.
- Limitações conhecidas e validações pendentes.

## Arquivos entregues

- Arquivos criados.
- Arquivos alterados.
- Arquivos auxiliares propostos ou criados, com justificativa.

---

# Critérios de aceite

A tarefa estará concluída somente se:

- Os arquivos em `/tools/templates/exemplos-prompts` foram pesquisados e os exemplos relevantes foram efetivamente usados como conhecimento específico do componente.
- Os arquivos de `/conhecimento/Salesforce` foram usados como referência conceitual e técnica.
- Os modelos existentes em `/modelos` foram analisados e suas convenções relevantes foram preservadas ou evoluídas justificadamente.
- Existe um modelo geral e um modelo específico adequados a `{{COMPONENTE_SF}}`.
- O modelo foi adaptado à natureza real do metadata, em vez de aplicar um conjunto fixo de seções inadequadas.
- Todo placeholder relevante possui origem clara: `{{XML.*}}`, `{{SF_OBJ.*}}` ou `{{CONTEXTO.*}}`.
- Os placeholders XML e Salesforce usam nomes reais, validados nas fontes analisadas.
- Campos de contexto usam nomes lógicos em `snake_case` e indicam claramente a necessidade de validação humana/agente.
- Cada campo relevante informa origem, obrigatoriedade, método de preenchimento e estabilidade.
- O modelo é útil para humanos, agentes de IA e automação futura.
- O prompt não cria nem implementa o utilitário automatizado.
- O relatório final demonstra, de forma rastreável, como os exemplos específicos do componente influenciaram o resultado.


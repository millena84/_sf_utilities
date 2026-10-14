# Prompt — FlowCategory

## 1. Contexto do componente

### 1.1 O que é
`FlowCategory` (nome funcional: **Flow Category**) é um metadata type/componente de configuração do Salesforce que deve ser analisado para extração, normalização, comparação e documentação técnica.

### 1.2 Para que serve
- Documentar a configuração funcional e técnica do componente.
- Apoiar análise de impacto em automações, segurança e integrações.
- Permitir snapshots comparáveis entre ambientes e versões.

### 1.3 Cenários típicos de uso
- Auditoria e inventário técnico de metadata.
- Diagnóstico de diferenças entre orgs/projetos.
- Suporte a revisão de mudanças e governança de configuração.

### 1.4 Clouds / contextos
- Salesforce Core (Setup e Metadata API).
- Clouds e produtos relacionados conforme o componente (Sales, Service, Experience, Industries, Data/AI quando aplicável).

---

## 2. Mapa estrutural

### 2.1 Componente principal: `FlowCategory`

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Flow Category |
| Metadata type exact | `FlowCategory` |
| Pasta no projeto SFDX | Validar no projeto (`FlowCategory` pode variar por tipo) |
| Arquivo padrão | Validar padrão `*-meta.xml` específico do tipo |
| Objeto interno (API padrão) | Validar objeto(s) de suporte para consulta |
| Objeto interno (Tooling API) | Validar disponibilidade e campos expostos |
| Acessível por Metadata API | Sim (quando suportado pelo metadata type) |
| Acessível por API padrão / SOQL | Validar por componente |
| Acessível por Tooling API | Validar por componente |
| Acessível por Apex | Validar consultabilidade e limites |
| Acessível por UI | Sim — Setup relacionado ao componente |

### 2.2 Componentes relacionados relevantes

| Componente / artefato | Nome real no metadata / API | Por que importa |
|---|---|---|
| Dependências diretas | Validar tipo e relação | Impacta consistência da documentação |
| Segurança/acesso | `PermissionSet`, `Profile`, objetos de acesso | Define uso efetivo do componente |
| Automações | `Flow`, Apex, regras e orquestrações | Pode alterar comportamento em runtime |
| Integrações | Named/External Credential, APIs, conectores | Pode depender de políticas e permissões |

### 2.3 Matriz de acessibilidade

| Fonte | Estrutura/metadata | Consulta API padrão | Tooling API | Setup/UI | Estado efetivo |
|---|---|---|---|---|---|
| Nome/identidade | Sim | Validar | Validar | Sim | Sim |
| Configurações principais | Sim | Parcial/validar | Parcial/validar | Sim | Sim |
| Relacionamentos/dependências | Parcial | Sim (queries dedicadas) | Sim (quando suportado) | Parcial | Sim |
| Segurança/permissões | Não centralizado | Sim (objetos de permissão) | Parcial | Sim | Sim |

---

## 3. Inventário técnico da configuração interna

### 3.1 Estrutura XML / Metadata (`FlowCategory`)

- Identificar tags obrigatórias e opcionais do metadata type.
- Mapear cardinalidade de cada bloco (`0..1`, `0..N`, `1`).
- Registrar campos de identidade, escopo, status, ativação e referências.
- Diferenciar valores declarados localmente vs estado efetivo na org.

### 3.2 Objetos internos via API padrão

- Definir objeto(s) oficiais para leitura analítica.
- Listar campos críticos para documentação e comparação.
- Validar permissões necessárias para consulta.

### 3.3 Tooling API

- Verificar se o componente possui representação em Tooling API.
- Confirmar disponibilidade de `Metadata`/campos equivalentes.
- Tratar limitações de tamanho, paginação e visibilidade.

### 3.4 Configuração observável em outras fontes

- Setup/UI de administração do componente.
- `SetupAuditTrail` para rastreabilidade.
- Código e configuração do projeto (Apex, Flow, arquivos declarativos).

### 3.5 Campos mascarados, omitidos, protegidos ou irrecuperáveis

- Identificar dados sensíveis não exportáveis/mascarados.
- Registrar diferenças entre o que aparece em XML, API e UI.
- Garantir documentação sem exposição de secrets.

---

## 4. Dados relevantes dos componentes relacionados

- Relacionar entidades/configurações que compõem o comportamento real do `FlowCategory`.
- Mapear dependências de segurança, automação e integração.
- Explicitar impacto de mudanças no componente principal sobre os relacionados.

---

## 5. Consultas e formas de extração

### 5.1 Extração por Metadata API
- Retrieve do tipo `FlowCategory` no escopo necessário.
- Normalização de XML para comparação entre snapshots.

### 5.2 Extração por API padrão (`sf data query`)
- Definir queries com campos explícitos (evitar `FIELDS(ALL)` quando houver limitação).
- Tratar paginação, limites e permissões de acesso.

### 5.3 Extração por Tooling API (quando aplicável)
- Usar queries focadas em identidade, status e payload técnico.
- Separar leitura de metadados de leitura de estado operacional.

### 5.4 Consolidação
- Unificar dados de XML, APIs e Setup em tabela interna padronizada.
- Registrar evidências, data/hora, API version e ambiente de origem.

---

## 6. Boas práticas e pontos de atenção

- Não assumir que a estrutura de `FlowCategory` é igual à de outros metadata types.
- Separar claramente configuração declarada de estado efetivo da org.
- Validar contratos de API por versão antes da implementação.
- Priorizar leitura somente (`read-only`) durante coleta técnica.
- Documentar limitações, lacunas e campos indisponíveis por fonte.
- Proteger dados sensíveis e nunca expor secrets.

### 6.1 Particularidades específicas deste componente
- define um rótulo e uma descrição para um agrupamento lógico de Flows;
- vincula um ou mais Flows à categoria;
- pode ser usado para organizar Flows por negócio, time, produto ou função;
- não altera a execução ou comportamento dos Flows — é puramente classificatório.
- Organizar e catalogar Flows em grupos lógicos.
- Facilitar a governança e a busca na lista de Flows.
- Documentar a propriedade/área de negócio de cada Flow.
- Melhorar a manutenção em orgs com grande volume de automações declarativas.
- Categorizar Flows por produto (Sales, Service, Marketing).
- Separar Flows transversais dos específicos de um objeto.

---

## 7. Links de referência oficial

- Salesforce Developer Documentation (Metadata API, Object Reference e Tooling API do componente).
- Salesforce Help do componente e recursos correlatos.
- Notas de release para mudanças de comportamento/campos por versão de API.

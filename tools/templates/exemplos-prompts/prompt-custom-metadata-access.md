# Prompt — Acesso a Custom Metadata Types

## 1. Contexto do componente

### 1.1 O que é
`Acesso a Custom Metadata Types` é um guia composto de documentação e não um metadata type único. O foco é documentar o acesso e a governança de tipos e registros de Custom Metadata no Salesforce.

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

### 2.1 Escopo principal: guia composto de acesso a Custom Metadata Types

| Item | Valor / Nome real |
|---|---|
| Nome funcional UI | Acesso a Custom Metadata Types |
| Metadata type exact | N/A — guia composto (não é metadata type único) |
| Pasta no projeto SFDX | `objects/<TypeName>__mdt/` (definição), além de artefatos de segurança/acesso |
| Arquivo padrão | `<TypeName>__mdt.object-meta.xml` e componentes relacionados de acesso |
| Objeto interno (API padrão) | `CustomMetadata`, `EntityDefinition`, `FieldDefinition`, objetos de permissão |
| Objeto interno (Tooling API) | `CustomObject`/`CustomField` (para definição), quando aplicável |
| Acessível por Metadata API | Parcial — via metadata types reais relacionados |
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

### 3.1 Estrutura XML / Metadata (tipos reais envolvidos)

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

- Relacionar entidades/configurações que compõem o comportamento real do acesso a Custom Metadata Types.
- Mapear dependências de segurança, automação e integração.
- Explicitar impacto de mudanças no componente principal sobre os relacionados.

---

## 5. Consultas e formas de extração

### 5.1 Extração por Metadata API
- Retrieve dos tipos reais envolvidos (`CustomObject` de `__mdt`, `CustomField`, permissões e componentes correlatos).
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

- Não assumir que a estrutura de `acesso a Custom Metadata Types` é igual à de outros metadata types.
- Separar claramente configuração declarada de estado efetivo da org.
- Validar contratos de API por versão antes da implementação.
- Priorizar leitura somente (`read-only`) durante coleta técnica.
- Documentar limitações, lacunas e campos indisponíveis por fonte.
- Proteger dados sensíveis e nunca expor secrets.

### 6.1 Particularidades específicas deste componente
- Identificar tipo, proteção, visibilidade, Profile, PermissionSet e permissão de leitura.
- Diferenciar tipo e registros.
- Documentar proteção de pacote e acesso por API quando disponível.
- Não expor valores sensíveis de registros.
- Comparar alterações de visibilidade e permissões.

---

## 7. Links de referência oficial

- Salesforce Developer Documentation (Metadata API, Object Reference e Tooling API do componente).
- Salesforce Help do componente e recursos correlatos.
- Notas de release para mudanças de comportamento/campos por versão de API.

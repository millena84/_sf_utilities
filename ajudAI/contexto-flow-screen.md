Peço desculpas pela confusão anterior! Compreendido: o foco correto é um **Screen Flow** (Fluxo de Tela / `processType = Flow`), que possui uma dinâmica totalmente voltada para interface de usuário, componentes interativos (como LWC/Aura na tela), regras de visibilidade, validações de campo, escolhas dinâmicas e navegação por etapas (*Stages*).

Abaixo está o **modelo de documentação evoluído e completo para Screen Flow**, alinhado 1:1 com a **Metadata API do Salesforce (`.flow-meta.xml`)** e a **Tooling API**, acompanhado do **JSON Schema** para alimentar utilitários automáticos.

---

# 📑 Modelo Evoluído: Documentação Técnica de Screen Flow (DETI - Screen Flow Module)

---

## 1. Identificação e Metadados do Fluxo de Tela
* **Nome de Exibição (`label`):** `{Flow.label}`
* **Nome API (`fullName` / `apiName`):** `{Flow.fullName}`
* **Tipo de Processo (`processType`):** `Flow` *(Screen Flow)*
* **Status (`status`):** `Active` | `Draft` | `Obsolete`
* **Versão da API (`apiVersion`):** `{Flow.apiVersion}` (ex: `62.0`)
* **Descrição Funcional (`description`):** `{Flow.description}`
* **Modo de Execução e Segurança (`runInMode`):**
  * `DefaultMode` (Respeita as permissões do usuário logado)
  * `SystemModeWithSharing` (Modo Sistema - Respeita regras de compartilhamento)
  * `SystemModeWithoutSharing` (Modo Sistema - Permissão total / Bypass de FLS)
* **Ponto de Entrada Inicial (`startElementReference`):** `{Flow.startElementReference}`

---

## 2. Estrutura e Navegação das Telas (`<screens>`)

Relação de todas as telas apresentadas ao usuário durante o fluxo:

### Tabela Geral de Telas:
| Nome API (`name`) | Rótulo (`label`) | Cabeçalho (`showHeader`) | Rodapé (`showFooter`) | Voltar (`allowBack`) | Concluir (`allowFinish`) | Pausar (`allowPause`) | Rótulo do Botão Avançar/Concluir |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `{screen.name}` | `{screen.label}` | `true/false` | `true/false` | `true/false` | `true/false` | `true/false` | `{screen.nextOrFinishButtonLabel}` |

---

## 3. Inventário de Componentes e Campos das Telas (`<fields>`)

Detalhamento de cada campo, componente de entrada, texto formatado ou componente customizado (LWC / Aura) inserido dentro das telas:

### 3.1. Campos Nativos e Entradas de Dados
| Tela Pai (`screen`) | Nome API (`name`) | Tipo do Campo (`fieldType`) | Tipo de Dado (`dataType`) | Obrigatório (`isRequired`) | Somente Leitura (`isReadOnly`) | Rótulo/Texto (`fieldText`) | Texto de Ajuda (`helpText`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `{screen.name}` | `{field.name}` | `InputField` \| `DropdownBox` \| `RadioButtons` \| `LargeTextField` \| `DisplayText` | `String` \| `Number` \| `Boolean` \| `Date` \| `Currency` | `true/false` | `true/false` | `{field.fieldText}` | `{field.helpText}` |

### 3.2. Componentes Personalizados (LWC / Aura na Tela)
Componentes Web Lightning ou Aura embarcados na tela (`fieldType = ComponentInstance`):

| Tela (`screen`) | Nome API (`name`) | Nome do Componente LWC/Aura (`extensionName`) | Armazenar Saída Automática (`storeOutputAutomatically`) | Parâmetros de Entrada (`inputParameters`) | Parâmetros de Saída (`outputParameters`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `{screen.name}` | `{field.name}` | `{field.extensionName}` (ex: `c:customFileUploadLwc`) | `true/false` | `{name=value}` | `{name=variable}` |

### 3.3. Regras de Visibilidade e Validação nos Campos
* **Regras de Visibilidade Condicional (`visibilityRule`):**
  * *Lógica de Filtro (`booleanFilter`):* `{visibilityRule.booleanFilter}` (ex: `1 AND 2`)
  * *Condições (`conditions`):* `{field.name}` `{operator}` `{value}`
* **Regras de Validação de Campo (`validationRule`):**
  * *Fórmula de Validação (`formulaExpression`):* `{validationRule.formulaExpression}`
  * *Mensagem de Erro (`errorMessage`):* `{validationRule.errorMessage}`

---

## 4. Conjuntos de Escolhas e Listas Dinâmicas (`<choices>` e `<dynamicChoiceSets>`)

Definição das opções exibidas em Picklists, Radio Buttons e Checkboxes na tela:

### 4.1. Conjuntos de Escolhas Estáticas (`<choices>`)
| Nome API (`name`) | Rótulo Exibido (`choiceText`) | Tipo de Dado (`dataType`) | Valor Atribuído (`value`) |
| :--- | :--- | :--- | :--- |
| `{choice.name}` | `{choice.choiceText}` | `String` \| `Number` | `{choice.value}` |

### 4.2. Conjuntos de Escolhas Dinâmicas de Registros (`<dynamicChoiceSets>`)
Consultas automáticas a objetos Salesforce para montar listas de seleção:

| Nome API (`name`) | Objeto Origem (`object`) | Campo do Valor (`valueField`) | Campo do Rótulo (`displayField`) | Filtros da Consulta (`filters`) | Ordenação (`sortField` / `sortOrder`) | Limite (`limit`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `{dcs.name}` | `{dcs.object}` | `{dcs.valueField}` | `{dcs.displayField}` | `{field operator value}` | `{sortField}` (`ASC/DESC`) | `{dcs.limit}` |

---

## 5. Indicadores de Progresso e Estágios (`<stages>`)
Se o fluxo utilizar barra de progresso ou indicador de etapas (*Stage Navigation*):

| Nome API (`name`) | Rótulo (`label`) | Ordem (`stageOrder`) | Ativo por Padrão (`isActive`) |
| :--- | :--- | :--- | :--- |
| `{stage.name}` | `{stage.label}` | `{stage.stageOrder}` | `true/false` |

---

## 6. Processamento, Invocações Apex e Subfluxos

Ações executadas nos bastidores entre uma tela e outra:

### 6.1. Chamadas de Ações e Apex (`<actionCalls>`)
| Elemento (`name`) | Tipo (`actionType`) | Classe/Ação Chamada (`actionName`) | Parâmetros de Entrada (`inputParameters`) | Saídas Capturadas (`outputParameters`) |
| :--- | :--- | :--- | :--- | :--- |
| `{action.name}` | `apex` \| `emailAlert` \| `quickAction` | `{action.actionName}` | `{key=value}` | `{key=variable}` |

### 6.2. Subfluxos Aninhados (`<subflows>`)
| Elemento (`name`) | Fluxo Invocado (`flowName`) | Mapeamento de Entradas (`inputAssignments`) |
| :--- | :--- | :--- |
| `{subflow.name}` | `{subflow.flowName}` | `{sourceVar -> targetVar}` |

---

## 7. Operações no Banco de Dados (DML e SOQL)
* **Buscas (`<recordLookups>`):** Registros consultados para preencher a tela ou validar dados.
* **Criações (`<recordCreates>`):** Registros salvos no banco a partir das entradas da tela.
* **Atualizações (`<recordUpdates>`):** Registros alterados ao avançar a tela.
* **Exclusões (`<recordDeletes>`):** Registros removidos durante a execução.

---

## 8. Variáveis, Fórmulas e Entradas/Saídas (`<variables>`, `<formulas>`, `<textTemplates>`)
* **Variáveis de Entrada (`isInput = true`):** Campos ou IDs recebidos via URL, página de registro ou LWC pai (ex: `recordId`).
* **Variáveis de Saída (`isOutput = true`):** Valores devolvidos para a tela ou componente chamador.
* **Fórmulas (`<formulas>`):** Cálculos dinâmicos e validações lógicas utilizadas na tela.
* **Templates de Texto (`<textTemplates>`):** Textos HTML/Rich Text formatados exibidos em componentes de `DisplayText`.

---

# 🤖 Esquema de Extração Automatizada para Screen Flow (JSON Schema)

Utilize este esquema para validar e estruturar o parser do utilitário autômato (ex: script Python que lê o arquivo `.flow-meta.xml` de um Screen Flow):

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceScreenFlowDocumentation",
  "type": "object",
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "fullName": { "type": "string" },
        "label": { "type": "string" },
        "processType": { "type": "string", "enum": ["Flow"] },
        "status": { "type": "string" },
        "apiVersion": { "type": "string" },
        "description": { "type": "string" },
        "runInMode": { "type": "string" },
        "startElementReference": { "type": "string" }
      },
      "required": ["fullName", "label", "processType", "status"]
    },
    "screens": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "label": { "type": "string" },
          "showHeader": { "type": "boolean" },
          "showFooter": { "type": "boolean" },
          "allowBack": { "type": "boolean" },
          "allowFinish": { "type": "boolean" },
          "allowPause": { "type": "boolean" },
          "nextOrFinishButtonLabel": { "type": "string" },
          "fields": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": { "type": "string" },
                "fieldType": { "type": "string" },
                "dataType": { "type": "string" },
                "isRequired": { "type": "boolean" },
                "isReadOnly": { "type": "boolean" },
                "fieldText": { "type": "string" },
                "helpText": { "type": "string" },
                "extensionName": { "type": "string" },
                "storeOutputAutomatically": { "type": "boolean" },
                "inputParameters": { "type": "object" },
                "outputParameters": { "type": "object" },
                "visibilityRule": {
                  "type": "object",
                  "properties": {
                    "booleanFilter": { "type": "string" },
                    "conditions": { "type": "array" }
                  }
                },
                "validationRule": {
                  "type": "object",
                  "properties": {
                    "formulaExpression": { "type": "string" },
                    "errorMessage": { "type": "string" }
                  }
                }
              }
            }
          }
        }
      }
    },
    "dynamic_choice_sets": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "object": { "type": "string" },
          "valueField": { "type": "string" },
          "displayField": { "type": "string" },
          "sortField": { "type": "string" },
          "sortOrder": { "type": "string" },
          "limit": { "type": "integer" }
        }
      }
    },
    "invoked_actions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "elementName": { "type": "string" },
          "actionType": { "type": "string" },
          "actionName": { "type": "string" },
          "inputs": { "type": "object" },
          "outputs": { "type": "object" }
        }
      }
    },
    "subflows": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "elementName": { "type": "string" },
          "flowName": { "type": "string" }
        }
      }
    }
  },
  "required": ["metadata", "screens"]
}
```

---

### 💡 Destaques da Ajuste para Screen Flow:

1. **Foco em Componentes da UI (`<screens>` e `<fields>`):** Mapeia individualmente os campos e suas regras de visibilidade e validação.
2. **Componentes LWC/Aura Embarcados:** Captura a tag `<extensionName>` para documentar quando um desenvolvedor colocou um componente customizado dentro do fluxo de tela.
3. **Listas Dinâmicas (`<dynamicChoiceSets>`):** Mapeia quais objetos e consultas SOQL implícitas o fluxo faz para alimentar Radio Buttons e Picklists na tela.

Quer que eu monte o script em Python que lê um arquivo `.flow-meta.xml` de Screen Flow e gera exatamente este relatório formatado em Markdown?

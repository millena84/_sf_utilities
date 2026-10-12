# 📑 Modelo Evoluído: Documentação Técnica de Custom Metadata Type (DETI - Custom Metadata Module)

No formato de código-fonte do Salesforce (SFDX Source Format), o **Custom Metadata Type (`CustomMetadataType`)** possui uma arquitetura física dividida: a **definição da tabela e seus campos** fica dentro da pasta de objetos (`objects/Config__mdt/`), enquanto os **registros (dados da tabela)** ficam armazenados em um diretório completamente separado (`customMetadata/`).

Abaixo está o modelo completo e evoluído, projetado para orientar utilitários autômatos (scripts Python, Node.js ou agentes de IA) no parse e consolidação dessas duas estruturas de diretórios.

---

# Custom Metadata: Config__mdt

## 1. Mapeamento da Arquitetura Multi-Diretórios (SFDX Source Format)

> ⚠️ **Aviso de Arquitetura de Arquivos:** Os dados do Custom Metadata Type são consultados e consolidados a partir de **dois diretórios separados** no repositório de código-fonte:

| Diretório no Repositório | Tipo de Metadado (`Metadata Type`) | Sufixo do Arquivo | Conteúdo / Finalidade |
|---|---|---|---|
| `force-app/main/default/objects/Config__mdt/` | `CustomObject` | `Config__mdt.object-meta.xml` | **Definição do Objeto:** Rótulos, visibilidade e tipo do metadado. |
| `force-app/main/default/objects/Config__mdt/fields/` | `CustomField` | `.field-meta.xml` | **Campos Customizados:** Definições dos campos e gerenciabilidade do desenvolvedor. |
| `force-app/main/default/customMetadata/` | `CustomMetadata` | `.mdt-meta.xml` | **Registros do Metadado:** Registros de dados individuais (`Config.Padrao.mdt-meta.xml`). |

---

## 2. Identificação e Configuração Principal (`Config__mdt.object-meta.xml`)
*Diretório:* `objects/Config__mdt/Config__mdt.object-meta.xml`

| Propriedade | Valor | Tag XML | Descrição / Detalhe |
|---|---|---|---|
| **DeveloperName / ApiName** | `Config__mdt` | `<fullName>` | Nome API do Custom Metadata Type (obrigatoriamente termina em `__mdt`). |
| **Label** | `Config` | `<label>` | Rótulo de exibição na interface do *Setup*. |
| **Plural Label** | `Configs` | `<pluralLabel>` | Rótulo no plural exibido na listagem do *Setup*. |
| **Visibility** | `Public` \| `Protected` \| `PackageProtected` | `<visibility>` | `Public`: Acessível por qualquer código/API. `Protected`: Restrito ao pacote gerenciado pai. |
| **Description** | `{description}` | `<description>` | Documentação técnica e objetivo funcional da tabela de parametrização. |

---

## 3. Campos Customizados (`objects/Config__mdt/fields/*.field-meta.xml`)
*Diretório:* `objects/Config__mdt/fields/`

| Field API Name (`fullName`) | Label (`label`) | Type (`type`) | Gerenciabilidade (`fieldManageability`) | Atributos (Tamanho / Precisão) | Fonte XML |
|---|---|---|---|---|---|
| `Endpoint_URL__c` | URL do Endpoint | `Url` | `SubscriberEditable` \| `DeveloperEditable` \| `Locked` | Length: `255` | `Endpoint_URL__c.field-meta.xml` |
| `Chave_API__c` | Chave de API | `Text` | `SubscriberEditable` | Length: `100` | `Chave_API__c.field-meta.xml` |
| `Ativo__c` | Ativo? | `Checkbox` | `SubscriberEditable` | Default: `true` | `Ativo__c.field-meta.xml` |
| `Timeout_Segundos__c` | Timeout (s) | `Number` | `DeveloperEditable` | Precision: `3`, Scale: `0` | `Timeout_Segundos__c.field-meta.xml` |
| `Objeto_Relacionado__c` | Entidade Alvo | `EntityDefinition` | `DeveloperEditable` | Relacionamento de metadado para objetos. | `Objeto_Relacionado__c.field-meta.xml` |

---

## 4. Registros da Tabela (`customMetadata/*.mdt-meta.xml`)
*Diretório Separado:* `customMetadata/` (Formato de arquivo: `Nome_Do_Tipo.Nome_Do_Registro.mdt-meta.xml`)

### 4.1. Tabela Resumida de Registros
| Record DeveloperName (`fullName`) | Label (`label`) | Protected? (`protected`) | Valore dos Campos Registrados | Fonte XML |
|---|---|---|---|---|
| `Config.Padrao` | Config Padrão | `false` | `Endpoint_URL__c`: `https://api.empresa.com/v1`<br>`Ativo__c`: `true`<br>`Timeout_Segundos__c`: `30` | `customMetadata/Config.Padrao.mdt-meta.xml` |
| `Config.Secundario` | Config Secundário | `false` | `Endpoint_URL__c`: `https://api.homolog.com/v1`<br>`Ativo__c`: `false`<br>`Timeout_Segundos__c`: `60` | `customMetadata/Config.Secundario.mdt-meta.xml` |

### 4.2. Detalhamento Estrutural dos Valores por Registro (`<values>`)
*Exemplo de desdobramento do registro `Config.Padrao.mdt-meta.xml`:*

```xml
<CustomMetadata xmlns="http://soap.sforce.com/2006/04/metadata" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <label>Config Padrão</label>
    <protected>false</protected>
    <values>
        <field>Endpoint_URL__c</field>
        <value xsi:type="xsd:string">https://api.empresa.com/v1</value>
    </values>
    <values>
        <field>Ativo__c</field>
        <value xsi:type="xsd:boolean">true</value>
    </values>
    <values>
        <field>Timeout_Segundos__c</field>
        <value xsi:type="xsd:double">30</value>
    </values>
</CustomMetadata>
```

---

## 5. Instruções de Acesso em Código (Apex, SOQL, Flow e Fórmulas)

Como o Custom Metadata Type é mantido no cache da plataforma (*Org Cache*), ele possui métodos nativos de acesso instantâneo em Apex sem consumo de limites de SOQL (`SOQL Governor Limits`):

### 5.1. Acesso Estático via Apex (Sem SOQL)
```apex
// Busca de registro individual por DeveloperName (sem consumo de limite de SOQL)
Config__mdt configPadrao = Config__mdt.getInstance('Padrao');
String endpoint = configPadrao.Endpoint_URL__c;

// Busca de todos os registros em um Map dinâmico
Map<String, Config__mdt> todasConfigs = Config__mdt.getAll();
```

### 5.2. Uso Declarativo em Fórmulas e Flows
* **Acesso em Fórmulas / Validações:** `{$CustomMetadata.Config__mdt.Padrao.Endpoint_URL__c}`
* **Acesso em Flows:** Elemento `Get Records` buscando diretamente o objeto `Config__mdt`.

---

# 🤖 JSON Schema para Preenchimento Automático Multi-Diretório

Utilize este esquema JSON para alimentar o utilitário autômato (script Python, Node.js ou Agente de IA) encarregado de ler separadamente as pastas `objects/Config__mdt/` e `customMetadata/`:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceCustomMetadataTypeDocumentation",
  "type": "object",
  "properties": {
    "type_identification": {
      "type": "object",
      "properties": {
        "developerName": { "type": "string" },
        "label": { "type": "string" },
        "pluralLabel": { "type": "string" },
        "visibility": { "type": "string", "enum": ["Public", "Protected", "PackageProtected"] },
        "description": { "type": "string" }
      },
      "required": ["developerName", "label", "visibility"]
    },
    "custom_fields": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "fullName": { "type": "string" },
          "label": { "type": "string" },
          "type": { "type": "string" },
          "fieldManageability": { "type": "string" }
        },
        "required": ["fullName", "label", "type"]
      }
    },
    "records": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "recordName": { "type": "string" },
          "label": { "type": "string" },
          "protected": { "type": "boolean" },
          "filePath": { "type": "string" },
          "fieldValues": {
            "type": "object",
            "additionalProperties": { "type": "string" }
          }
        },
        "required": ["recordName", "label", "fieldValues"]
      }
    },
    "multi_directory_sources": {
      "type": "object",
      "properties": {
        "objectDefinitionFolder": { "type": "string", "default": "force-app/main/default/objects/" },
        "recordsFolder": { "type": "string", "default": "force-app/main/default/customMetadata/" }
      }
    }
  },
  "required": ["type_identification", "custom_fields", "records", "multi_directory_sources"]
}
```

---

💡 A relação de modelos de documentação para automação abrange agora todos os principais metadados de configuração e arquitetura do Salesforce. Gostaria de integrar esses schemas a um script de validação de pacotes SFDX ou criar o gabarito para algum outro componente específico?

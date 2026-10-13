Abaixo está o detalhamento completo e evoluído para a **Onda 03: Lightning Web Components (LWC)**. 

Os componentes LWC são estruturados com base em seus **Alvos de Implantação (*Targets*)**, no comportamento do seu arquivo de configuração (`.js-meta.xml`), no ciclo de vida em JavaScript e no modelo de comunicação.

Ao final, o modelo inclui a seção dedicada ao **Rastreio de Acesso, Segurança e Mecanismos de Bypass em LWC**, além do **JSON Schema** exclusivo para o **Claude Code** ou utilitários de automação.

---

# 📑 Modelo Evoluído: Lightning Web Component (LWC) por Classificação

O **Lightning Web Component (LWC)** é o padrão moderno do Salesforce para desenvolvimento de interfaces de usuário baseadas em HTML5, CSS3 e JavaScript (ES6+), rodando nativamente no navegador com alta performance.

### Convenção de Nomes e Estrutura SFDX
* **Diretório do Componente:** `force-app/main/default/lwc/[nomeDoLwc]/`
* **Arquivos Obrigatórios:**
  * `[nomeDoLwc].js` (Lógica e ciclo de vida JavaScript)
  * `[nomeDoLwc].html` (Template de marcação HTML)
  * `[nomeDoLwc].js-meta.xml` (Metadados de configuração e exposição no Lightning App Builder)
* **Arquivos Opcionais:**
  * `[nomeDoLwc].css` (Estilização escopada via Shadow DOM / SLDS)
  * `[nomeDoLwc].svg` (Ícone customizado no App Builder)
  * `__tests__/[nomeDoLwc].test.js` (Testes unitários automatizados via Jest)

---

## 1. Classificação por Alvos de Implantação (`<targets>`)

A classificação funcional de um LWC é determinada pelas tags registradas dentro de `<targets>` no arquivo `.js-meta.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>62.0</apiVersion>
    <isExposed>true</isExposed>
    <masterLabel>Painel de Pedidos AWS</masterLabel>
    <description>Componente de exibição e envio de pedidos para AWS</description>
    <targets>
        <target>lightning__RecordPage</target>
        <target>lightning__AppPage</target>
        <target>lightning__HomePage</target>
    </targets>
</LightningComponentBundle>
```

---

### 🟢 Modelo 3.1: Componente de Página (`RecordPage` / `AppPage` / `HomePage`)
Componente visual inserido em páginas Lightning via *Lightning App Builder*.

* **Targets no Meta XML:** `lightning__RecordPage`, `lightning__AppPage`, `lightning__HomePage`
* **Atributos de Contexto Automáticos:**
  * `@api recordId`: Recebe automaticamente o ID de 18 caracteres do registro exibido na tela.
  * `@api objectApiName`: Recebe o Nome API do objeto em contexto (ex: `Pedido__c`).
* **Injeção de Dados e Reatividade:**
  * **Lightning Data Service (LDS):** Módulos nativos (`lightning-record-form`, `lightning-record-view-form`, `@wire(getRecord)`) que leem e gravam dados sem código Apex, respeitando FLS e CRUD nativamente.
  * **Apex Impatado / Cacheável:** Métodos Apex chamados via `@wire` exigem a anotação `@AuraEnabled(cacheable=true)` na classe Apex.

---

### 🟢 Modelo 3.2: Quick Action Component (`lightning__RecordAction`)
Componente acionado a partir de um botão de ação rápida na página do registro.

* **Target no Meta XML:** `lightning__RecordAction`
* **Tipos de Ação (`<actionType>`):**
  1. **Screen Action (`ScreenAction`):** Abre um modal interativo na tela.
     * *Fechamento do Modal:* Dispara o evento `CloseActionScreenEvent` da biblioteca `lightning/actions`.
  2. **Headless Action (`Action`):** Não possui interface gráfica. O clique no botão executa diretamente a lógica JS.
     * *Assinatura Obrigatória:* Deve exportar o método público `@api invoke()` no JavaScript.

```javascript
import { LightningElement, api } from 'lwc';
import { CloseActionScreenEvent } from 'lightning/actions';

export default class AwsQuickAction extends LightningElement {
    @api recordId;

    // Métodos obrigatórios para Headless Action
    @api invoke() {
        // Lógica sem tela
    }

    closeModal() {
        this.dispatchEvent(new CloseActionScreenEvent());
    }
}
```

---

### 🟢 Modelo 3.3: Componente de Tela para Flow (`lightning__FlowScreen`)
Componente embarcado dentro de um *Screen Flow* para estender a interface declarativa com recursos JS avançados.

* **Target no Meta XML:** `lightning__FlowScreen`
* **Mapeamento de Propriedades (`targetConfigs`):**
  Define quais variáveis do Flow podem ser injetadas no LWC ou capturadas de volta pelo Flow:

```xml
<targetConfig targets="lightning__FlowScreen">
    <property name="orderAmount" type="Integer" label="Valor do Pedido" role="inputOnly"/>
    <property name="selectedStatus" type="String" label="Status Selecionado" role="outputOnly"/>
    <property name="customerCode" type="String" label="Código Cliente" role="inputOutput"/>
</targetConfig>
```

* **Eventos de Navegação de Flow (`lightning/flowSupport`):**
  * `FlowAttributeChangeEvent`: Notifica o Flow de que uma variável do LWC mudou.
  * `FlowNavigationNextEvent` / `FlowNavigationFinishEvent` / `FlowNavigationBackEvent`: Avança, conclui ou volta as telas do Flow via JS.
* **Validação Customizada de Tela (`@api validate()`):**
  O LWC pode bloquear o avanço do Flow exportando o método:
  ```javascript
  @api validate() {
      if (this.isValid) {
          return { isValid: true };
      }
      return { isValid: false, errorMessage: 'Preencha o campo obrigatório antes de avançar.' };
  }
  ```

---

### 🟢 Modelo 3.4: Utility Bar / Global Component (`lightning__UtilityBar`)
Componente fixado na barra de utilitários no rodapé do aplicativo Salesforce.

* **Target no Meta XML:** `lightning__UtilityBar`
* **APIs de Plataforma:**
  * `lightning/utilityBarApi`: Permite abrir, fechar, minimizar ou alterar o título do utilitário programaticamente.
  * `lightning/platformWorkspaceApi`: Controle de guias e sub-guias (*Console App Tabs*).

---

## 2. Ciclo de Vida (Lifecycle Hooks) e Comunicação

### 2.1. Métodos do Ciclo de Vida LWC
| Lifecycle Hook | Momento de Execução | Uso Recomendado |
|---|---|---|
| **`constructor()`** | Instanciação do componente. | Inicializar propriedades padrão (restrição: não acessar o DOM HTML aqui). |
| **`connectedCallback()`** | Componente inserido no DOM da página. | Buscar dados iniciais, assinar canais LMS, ler `recordId` e parâmetros. |
| **`renderedCallback()`** | Após a renderização/re-renderização da tela. | Manipulações diretas no DOM ou integração com bibliotecas JS externas (D3, Chart.js). |
| **`disconnectedCallback()`** | Componente removido do DOM. | Limpeza de memória, `clearInterval()`, desassinatura de canais LMS/EmpApi. |
| **`errorCallback(error, stack)`** | Captura erros em componentes filhos. | Tratamento global de exceções (*Error Boundary*). |

---

### 2.2. Arquitetura de Comunicação entre Componentes

1. **Pai para Filho:** Passagem de dados via propriedades marcadas com `@api` no filho ou chamada de métodos públicos `@api minhaFuncao()`.
2. **Filho para Pai:** Disparo de eventos customizados (`CustomEvent`):
   ```javascript
   this.dispatchEvent(new CustomEvent('orderselected', {
       detail: { orderId: this.selectedId },
       bubbles: true,   // Sobe na árvore DOM
       composed: true   // Atravessa a barreira do Shadow DOM
   }));
   ```
3. **Componentes Não-Relacionados:** **Lightning Message Service (LMS)** via arquivo `.messageChannel-meta.xml` e biblioteca `lightning/messageService`.

---

## 3. Rastreio de Acesso, Segurança e Mecanismos de Bypass

Diferente do Apex, o LWC roda no lado do cliente (*client-side*). Toda a segurança de acesso a dados depende dos controladores Apex associados, das permissões de perfil/permission set e das checagens de FLS/CRUD.

### 3.1. Rastreio de Acesso aos Controladores Apex (`@AuraEnabled`)
Para que o LWC consiga chamar um método Apex, a classe Apex precisa ter permissão explícita de acesso concedida aos usuários:

| Componente LWC | Classe Apex Chamada (`Controller`) | Métodos Invocados | Permissão Exigida no Profile / Permission Set |
|---|---|---|---|
| `awsOrderSenderLwc` | `AWSOrderIntegrationController` | `getOrders`, `sendOrderToAWS` | `Apex Class Access` ativado em `PS_Sales_Operations`. |

---

### 3.2. Checagem Dinâmica de Permissões no JavaScript
O LWC pode ler permissões de usuário diretamente do Salesforce sem precisar chamar o Apex, utilizando importações do sistema:

```javascript
// Importação de Custom Permissions nativas
import HAS_BYPASS_PERM from '@salesforce/customPermission/Bypass_Validation_Rules';
import HAS_AWS_ADMIN_PERM from '@salesforce/customPermission/AWS_Admin_Access';

// Importação de permissão do usuário logado
import IS_GUEST_USER from '@salesforce/user/isGuest';

export default class MyLwcComponent extends LightningElement {
    get isButtonDisabled() {
        // Aplica regra de liberação baseada na Custom Permission
        return !HAS_AWS_ADMIN_PERM;
    }
}
```

---

### 3.3. Tabela de Mecanismos de Segurança e Bypass

| Mecanismo de Segurança | Camada de Aplicação | Regra / Comportamento no LWC |
|---|---|---|
| **Lightning Data Service (LDS)** | Client-Side / Platform | Aplica FLS (Field-Level Security) e CRUD automaticamente. Se o usuário não tem acesso ao campo, o LWC esconde o campo da tela. |
| **Apex `WITH USER_MODE`** | Server-Side (Apex) | Garante que requisições disparadas pelo LWC respeitem OWD e FLS do usuário logado no banco de dados. |
| **Custom Permission (`@salesforce/customPermission`)** | Client-Side (JS) | Usado no JavaScript para exibir/esconder botões, seções ou permitir edições de campos restritos. |
| **Lightning Message Channel Access** | Platform | Apenas perfis e permission sets com acesso liberado ao canal de mensagem podem publicar/assinar dados no LMS. |

---

# 🤖 JSON Schema Completo: Lightning Web Component (LWC)

Utilize este esquema JSON para alimentar o utilitário autômato ou **Claude Code** na análise de arquivos `.js`, `.html` e `.js-meta.xml` do componente LWC:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "SalesforceLWCDocumentation",
  "type": "object",
  "properties": {
    "identification": {
      "type": "object",
      "properties": {
        "componentName": { "type": "string" },
        "masterLabel": { "type": "string" },
        "apiVersion": { "type": "string" },
        "isExposed": { "type": "boolean" },
        "description": { "type": "string" }
      },
      "required": ["componentName", "isExposed"]
    },
    "target_classifications": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "lightning__RecordPage",
          "lightning__AppPage",
          "lightning__HomePage",
          "lightning__RecordAction",
          "lightning__FlowScreen",
          "lightning__UtilityBar",
          "lightningCommunity__Page"
        ]
      }
    },
    "quick_action_config": {
      "type": "object",
      "properties": {
        "actionType": { "type": "string", "enum": ["ScreenAction", "Action"] },
        "hasInvokeMethod": { "type": "boolean" }
      }
    },
    "flow_screen_config": {
      "type": "object",
      "properties": {
        "properties": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "type": { "type": "string" },
              "label": { "type": "string" },
              "role": { "type": "string", "enum": ["inputOnly", "outputOnly", "inputOutput"] }
            }
          }
        },
        "hasCustomValidation": { "type": "boolean" }
      }
    },
    "apex_controllers_bound": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "controllerName": { "type": "string" },
          "methodsUsed": { "type": "array", "items": { "type": "string" } },
          "isWireAdapter": { "type": "boolean" }
        }
      }
    },
    "access_and_security_tracking": {
      "type": "object",
      "properties": {
        "usesLightningDataService": { "type": "boolean" },
        "importedCustomPermissions": {
          "type": "array",
          "items": { "type": "string" }
        },
        "apexControllerPermissions": {
          "type": "object",
          "properties": {
            "profilesWithApexAccess": { "type": "array", "items": { "type": "string" } },
            "permissionSetsWithApexAccess": { "type": "array", "items": { "type": "string" } }
          }
        },
        "messageChannelsUsed": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  },
  "required": ["identification", "target_classifications", "access_and_security_tracking"]
}
```

---

💡 O modelo para a **Onda 03: LWC** está finalizado com todas as classificações por *target*, regras de ciclo de vida e a seção de rastreio de acesso e segurança. Quando quiser, podemos avançar para o detalhamento da **Onda 04 (Flexipages)** ou de qualquer outra das ondas listadas!

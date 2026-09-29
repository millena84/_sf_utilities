Com base nos documentos Salesforce, que tipo de metadadoa ficam nas pastas extClntApp*? São dados que se conectam com o External Client App? Pensando em documentação, deveriam ser documentados juntos, unindo os dados de todos xmls?

## Resposta curta

Sim. As pastas `extClntApp*` normalmente armazenam **metadados complementares de uma External Client App (ECA)**, principalmente configurações de OAuth e políticas administrativas. Elas não representam aplicações externas diferentes; em geral, são partes separadas da configuração da mesma ECA.

A documentação deve relacionar esses XMLs em conjunto, mas **não necessariamente consolidar tudo em um único arquivo físico**. O ideal é manter os XMLs separados conforme o padrão do Salesforce e criar uma documentação funcional/técnica única que mostre como eles se relacionam.

## O que fica em cada pasta

A estrutura típica pode conter componentes como estes:

| Pasta / metadado | O que representa | Natureza da configuração |
|---|---|---|
| `externalClientApps/` | Cabeçalho e identidade da External Client App | Nome, label, descrição, contatos, estado de distribuição e identificadores |
| `extlClntAppOauthSettings/` | Configurações OAuth da aplicação | Fluxos OAuth, callback URL, scopes e configurações definidas pelo desenvolvedor |
| `extlClntAppGlobalOauthSets/` | Configurações OAuth globais | Informações sensíveis e configurações globais do OAuth |
| `extlClntAppOauthPolicies/` | Políticas administrativas do OAuth | Usuários permitidos, validade de refresh token, políticas de sessão e controles de segurança |
| `extlClntAppConfigurablePolicies/` | Políticas gerais da ECA | Ativação ou desativação de plugins e outras políticas controladas pelo administrador |
| `extlClntAppCanvasSettings/` | Configurações de Canvas, quando aplicável | Integração da ECA com Canvas |
| `extlClntAppMobileConfigurablePolicies/` | Políticas específicas para uso mobile | Restrições e comportamento em dispositivos móveis |
| `extlClntAppSamlConfigurablePolicies/` | Políticas relacionadas a SAML | Configurações de SSO e identidade, quando aplicável |

A Salesforce descreve `ExternalClientApplication` como o **arquivo de cabeçalho** da aplicação. Já `ExtlClntAppOauthSettings` representa as configurações do plugin OAuth, enquanto `ExtlClntAppOauthConfigurablePolicies` representa políticas configuradas pelo administrador.[1][2][3]

Os nomes exatos das pastas podem variar conforme a versão da API, o formato retornado pelo Metadata API ou o projeto Salesforce DX. Por isso, vale confirmar o `package.xml`, a versão da API e os nomes dos arquivos presentes no repositório.

## Eles se conectam com a ECA?

Sim, conceitualmente todos esses metadados se conectam à mesma External Client App.

Uma forma simples de visualizar é:

```text
External Client App
│
├── externalClientApps/
│   └── MinhaApp.eca-meta.xml
│       Identidade e informações gerais da aplicação
│
├── extlClntAppOauthSettings/
│   └── MinhaApp_oauth.ecaOauth-meta.xml
│       Configuração OAuth packageável
│
├── extlClntAppOauthPolicies/
│   └── MinhaApp_oauth_policy.ecaOauthPlcy-meta.xml
│       Políticas OAuth administráveis
│
└── extlClntAppGlobalOauthSets/
    └── MinhaApp_global.ecaGlblOauth-meta.xml
        Configurações globais e sensíveis
```

A relação não é necessariamente feita por um único campo explícito em todos os XMLs. Normalmente, ela ocorre pela combinação de:

- nome lógico da aplicação;
- nome do componente;
- referência ao plugin OAuth;
- identificadores internos da ECA;
- relacionamento mantido pelo Salesforce no ambiente;
- convenções de nomenclatura e estrutura do Metadata API.

Portanto, é melhor tratar todos os arquivos como **componentes de uma mesma unidade funcional**, e não como configurações independentes.

## O que deve ser unido na documentação

Recomendo criar uma documentação única por External Client App, com seções separadas para cada tipo de XML.

### 1. Identificação da aplicação

Documente os dados do `ExternalClientApplication`:

- nome técnico;
- label;
- descrição;
- finalidade da integração;
- sistema consumidor;
- área responsável;
- ambiente;
- proprietário técnico e funcional;
- distribuição: local, packaged ou managed;
- URL de contato;
- dependências.

Exemplo:

| Campo | Exemplo |
|---|---|
| ECA | `FraudDetectionIntegration` |
| Sistema consumidor | Plataforma antifraude |
| Finalidade | Consulta de risco e envio de eventos |
| Ambiente | Produção |
| Proprietário | Arquitetura de Integração |
| Protocolo | OAuth 2.0 |
| Distribuição | Local |

### 2. Configuração OAuth

Documente os elementos de `ExtlClntAppOauthSettings`:

- fluxo OAuth utilizado;
- callback URL;
- scopes;
- tipo de cliente;
- permissões concedidas;
- uso de refresh token;
- audience, quando aplicável;
- dependências externas;
- comportamento esperado após expiração do token.

A Salesforce diferencia as configurações controladas pelo desenvolvedor das políticas controladas pelo administrador. Fluxos OAuth, callback URLs e scopes entram normalmente no primeiro grupo; validade do refresh token, usuários permitidos e timeouts entram no segundo.[4]

### 3. Políticas administrativas

Documente separadamente os arquivos de policies:

- quem pode usar a aplicação;
- se o acesso é permitido para usuários pré-autorizados;
- duração do refresh token;
- comportamento após logout;
- limitações de sessão;
- restrições de IP ou rede, quando aplicáveis;
- plugins habilitados;
- alterações feitas diretamente pelo administrador.

Essa separação é importante porque políticas podem variar entre ambientes, enquanto a configuração base da aplicação deveria permanecer consistente.

### 4. Dados sensíveis

Não copie secrets, consumer secrets ou chaves privadas para a documentação nem para o Git.

A Salesforce informa que `ExtlClntAppGlobalOauthSettings` pode conter informações privadas e sensíveis de OAuth, que não devem ser empacotadas nem adicionadas ao controle de versão.[5][6]

Na documentação, registre apenas:

- onde o segredo é armazenado;
- quem pode acessá-lo;
- como ocorre a rotação;
- quando foi feita a última rotação;
- qual processo deve ser seguido em caso de comprometimento;
- referência ao cofre corporativo, sem incluir o valor do segredo.

Exemplo seguro:

```text
Client secret:
- Armazenamento: cofre corporativo
- Acesso: grupo Integration-Admins
- Rotação: a cada 180 dias
- Última rotação: consultar registro do cofre
- Valor: não documentado neste repositório
```

## Unir os XMLs ou apenas relacioná-los?

A recomendação é:

| Abordagem | Recomendação |
|---|---|
| Fundir fisicamente todos os XMLs em um único XML | Não fazer |
| Manter os XMLs separados nas pastas padrão | Fazer |
| Criar uma página única por ECA | Fazer |
| Documentar cada XML em uma subseção | Fazer |
| Copiar secrets para uma página técnica | Não fazer |
| Criar uma matriz de rastreabilidade | Fazer |

O Salesforce espera tipos de metadados distintos, com estruturas e sufixos diferentes. Por exemplo, `ExtlClntAppOauthConfigurablePolicies` usa componentes com o sufixo `.ecaOauthPlcy`, enquanto `ExtlClntAppGlobalOauthSettings` usa componentes com o sufixo `.ecaGlblOauth`.[2][6]

Assim, “unir” deve significar **unir a visão documental e funcional**, não misturar os conteúdos XML.

## Modelo recomendado de documentação

Sugiro uma página com este formato:

```text
# External Client App: FraudDetectionIntegration

## 1. Objetivo

Permitir que a plataforma antifraude consulte e envie informações ao Salesforce
por meio de OAuth 2.0.

## 2. Sistemas envolvidos

- Salesforce
- Plataforma antifraude
- API Gateway
- Serviço de gestão de segredos

## 3. Componentes de metadados

| Tipo | Arquivo | Responsabilidade |
|---|---|---|
| ExternalClientApplication | FraudDetectionIntegration.eca-meta.xml | Identidade da ECA |
| ExtlClntAppOauthSettings | FraudDetectionIntegration_oauth.ecaOauth-meta.xml | Configuração OAuth |
| ExtlClntAppOauthConfigurablePolicies | FraudDetectionIntegration_oauth_policy.ecaOauthPlcy-meta.xml | Políticas OAuth |
| ExtlClntAppGlobalOauthSettings | arquivo protegido | Dados globais e sensíveis |

## 4. Autenticação

- Fluxo OAuth:
- Callback URL:
- Scopes:
- Tipo de cliente:
- Uso de refresh token:

## 5. Políticas

- Usuários autorizados:
- Validade do refresh token:
- Timeout:
- Plugins habilitados:

## 6. Segurança

- Local do secret:
- Responsável pela rotação:
- Frequência de rotação:
- Processo de revogação:

## 7. Implantação

- Dependências:
- Ordem de deployment:
- API version:
- Ambientes:
- Validações pós-deployment:

## 8. Troubleshooting

- Erro de callback:
- Scope inválido:
- Usuário não autorizado:
- Token expirado:
- Secret inválido:
```

## Ponto importante sobre deployment

Nem todos os XMLs têm o mesmo papel no deployment.

Em linhas gerais:

- `ExternalClientApplication` descreve a aplicação;
- `ExtlClntAppOauthSettings` contém configurações OAuth que podem ser empacotáveis;
- políticas administrativas podem ser geradas ou ajustadas no ambiente de destino;
- configurações globais e secrets possuem restrições especiais;
- o comportamento depende da versão da API, do tipo de distribuição e de o componente estar sendo usado em pacote ou em uma organização local.

A documentação oficial informa que `ExternalClientApplication` e `ExtlClntAppOauthSettings` aparecem juntos em exemplos de manifesto, enquanto as configurações globais OAuth possuem tratamento sensível e restrições de empacotamento.[3][6]

### Conclusão

A melhor decisão arquitetural é tratar a ECA como uma **unidade documental única composta por vários metadados**:

```text
Uma ECA = identidade + OAuth + políticas + segurança + operação
```

Mantenha cada XML na pasta e no formato exigido pelo Salesforce, mas documente todos sob uma única página ou capítulo. Para facilitar manutenção, crie também uma matriz relacionando:

```text
ECA → arquivo XML → finalidade → proprietário → sensibilidade → deployável?
```

Esse modelo evita dois problemas comuns: documentar apenas o arquivo principal e esquecer as políticas, ou copiar dados sensíveis dos XMLs para uma documentação que deveria ser compartilhável.

Citações:
[1] ExternalClientApplication | Metadata API Developer Guide https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_externalclientapplication.htm
[2] ExtlClntAppOauthConfigurableP... https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_extlclntappoauthconfigurablepolicies.htm
[3] ExtlClntAppOauthSettings | Metadata API Developer Guide https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_extlclntappoauthsettings.htm
[4] Secure Your Org with External Client Apps https://developer.salesforce.com/blogs/2025/01/secure-your-org-with-external-client-apps
[5] Metadata Types | Metadata API Developer Guide https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_types_list.htm
[6] ExtlClntAppGlobalOauthSettings | Metadata API ... https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_extlclntappglobaloauthsettings.htm
[7] Metadata API Developer Guide https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/api_meta.pdf
[8] Criar um aplicativo de cliente externo | Salesforce Trailhead https://trailhead.salesforce.com/pt-BR/content/learn/projects/create-an-external-client-app-using-metadata-api/create-an-external-client-app
[9] ExternalClientAppSettings | Metadata API Developer Guide | Salesforce Developers https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_externalclientappsettings.htm
[10] Comparison of Connected Apps and External Client ... - Salesforce https://help.salesforce.com/s/articleView?id=xcloud.connected_apps_and_external_client_apps_features.htm&language=en_US&type=5
[11] Tooling API Objects https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/reference_objects_list.htm
[12] Package and Distribute External Client Applications - Trailhead https://trailhead.salesforce.com/content/learn/modules/external-client-app-basics/package-and-distribute-external-client-apps
[13] Salesforce External Client Apps vs Connected Apps: A Deep Dive https://aquiva.com/blog/external-client-apps-the-next-generation-of-app-interoperability
[14] Rethinking Salesforce Integration Architecture: The Leap to External ... https://medium.com/@justusvandenberg/rethinking-salesforce-integration-architecture-the-leap-to-external-client-apps-b9a0489c8773
[15] ExtlClntAppConfigurablePolicies | Metadata API ... https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_extlclntappconfigurablepolicies.htm
[16] Metadata Coverage Report https://developer.salesforce.com/docs/success/metadata-coverage-report/references/coverage-report/metadata-coverage-report.html
[17] Metadata Coverage Report https://developer.salesforce.com/docs/metadata-coverage/48/LiveChatDeployment/scratch-def/developer
[18] ExternalServicesSettings | Metadata API Developer Guide https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_externalservicessettings.htm
[19] Role | Metadata API Developer Guide https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_role.htm
[20] メタデータ型 | メタデータ API 開発者ガイド | Salesforce Developers https://developer.salesforce.com/docs/atlas.ja-jp.api_meta.meta/api_meta/meta_types_list.htm
[21] ExtlClntAppOauthSettings | Object Reference for the Salesforce Platform | Salesforce Developers https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_extlclntappoauthsettings.htm
[22] First-Generation Managed Packaging Developer Guide https://developer.salesforce.com/docs/platform/pkg1-dev/guide/first-gen-packageable-components.html
[23] Create the Managed Package - Salesforce Developers https://developer.salesforce.com/docs/service/messaging-partner/guide/create-managed-package.html

---

Entao me ensine a unir os dados desses xmls.... preciso que vc faça uma lista completa das propriedades de cada xml envolvido em diferentes configurações de external Client app

# Como unir os XMLs

Você deve unir os dados **logicamente**, em uma documentação ou modelo consolidado, mas manter os XMLs separados para deployment.

A Salesforce define a External Client App como uma configuração distribuída entre múltiplos arquivos: um arquivo principal da aplicação, arquivos de plugins e arquivos de políticas. Cada plugin possui suas próprias configurações e políticas.[1]

A relação principal entre os arquivos é feita pelo campo:

```xml
<externalClientApplication>nome-da-eca</externalClientApplication>
```

Esse valor deve apontar para a mesma External Client App definida no arquivo principal.

A estrutura conceitual é:

```text
External Client App
│
├── Identidade da aplicação
│   └── externalClientApps/*.eca-meta.xml
│
├── Plugin OAuth
│   ├── extlClntAppOauthSettings/*.ecaOauth-meta.xml
│   ├── extlClntAppGlobalOauthSets/*.ecaGlblOauth-meta.xml
│   └── extlClntAppOauthPolicies/*.ecaOauthPlcy-meta.xml
│
└── Políticas gerais
    └── extlClntAppConfigurablePolicies/*.ecaPlcy-meta.xml
```

> Observação: a Salesforce utiliza `extlClntAppGlobalOauthSets` como diretório para `ExtlClntAppGlobalOauthSettings`, embora o nome do tipo contenha `Settings`.[2]

# Modelo de união

Imagine estes arquivos:

```text
force-app/main/default/
├── externalClientApps/
│   └── fraudDetection.eca-meta.xml
├── extlClntAppOauthSettings/
│   └── fraudDetectionOauth.ecaOauth-meta.xml
├── extlClntAppGlobalOauthSets/
│   └── fraudDetectionGlobal.ecaGlblOauth-meta.xml
└── extlClntAppOauthPolicies/
    └── fraudDetectionPolicy.ecaOauthPlcy-meta.xml
```

Você não deve transformar os quatro XMLs em um XML inválido. Em vez disso, deve montar uma estrutura consolidada, por exemplo:

```yaml
externalClientApplication:
  fullName: fraudDetection
  header:
    contactEmail: integration@example.com
    contactPhone: null
    description: Integração com plataforma antifraude
    distributionState: Local
    iconUrl: null
    infoUrl: null
    isProtected: false
    label: Fraud Detection
    logoUrl: null
    managedType: null
    orgScopedExternalApp: null

  oauth:
    settings:
      externalClientApplication: fraudDetection
      label: Fraud Detection OAuth
      commaSeparatedOauthScopes: "Api, Web, OpenID"
      oauthLink: null
      singleLogoutUrl: null
      trustedIpRanges: []
      customAttributes: []
      assetTokenAudiences: null
      assetTokenSigningCertificate: null
      assetTokenValidity: null
      areAttributesIncludedInAssetToken: false
      areCustomPermsIncludedInAssetToken: false
      clientAssertionCertificate: null
      isFirstPartyAppEnabled: false

    globalSettings:
      externalClientApplication: fraudDetection
      label: Fraud Detection Global OAuth
      callbackUrl: https://app.example.com/oauth/callback
      certificate: null
      consumerKey: "[SENSITIVE]"
      consumerSecret: "[SENSITIVE]"
      idTokenConfig: null
      isPkceRequired: true
      isRefreshTokenRotationEnabled: true
      isCodeCredFlowEnabled: true
      isClientCredentialsFlowEnabled: false
      isDeviceFlowEnabled: false
      isTokenExchangeEnabled: false
      isNamedUserJwtEnabled: false

    policies:
      externalClientApplication: fraudDetection
      label: Fraud Detection OAuth Policy
      permittedUsersPolicyType: AdminApprovedPreAuthorized
      commaSeparatedPermissionSet: "Fraud_Integration_User"
      commaSeparatedProfile: null
      refreshTokenPolicyType: SpecificLifetime
      refreshTokenValidityPeriod: 1
      refreshTokenValidityUnit: Days
      ipRelaxationPolicyType: Enforce
      sessionTimeoutInMinutes: 30
      requiredSessionLevel: HIGH_ASSURANCE
      policyAction: RaiseSessionLevel
```

Esse YAML é apenas um **modelo documental**. Ele não substitui os XMLs Salesforce.

# Lista completa de propriedades

A seguir está a lista consolidada dos campos documentados pela Salesforce para os principais tipos envolvidos.

## 1. ExternalClientApplication

Diretório:

```text
externalClientApps/
```

Sufixo:

```text
.eca-meta.xml
```

Tipo Metadata API:

```text
ExternalClientApplication
```

Esse é o arquivo de identidade ou “header” da aplicação.[3]

| Propriedade | Tipo | Finalidade |
|---|---|---|
| `fullName` | Herdado de `Metadata` | Nome técnico do componente |
| `contactEmail` | String | E-mail de contato do administrador ou responsável pela aplicação |
| `contactPhone` | String | Telefone de contato do administrador ou responsável |
| `description` | String | Descrição funcional da aplicação |
| `distributionState` | Enum | Define se a aplicação é `Local`, `Packaged` ou outro estado interno suportado |
| `iconUrl` | String | URL do ícone da aplicação |
| `infoUrl` | String | URL com informações adicionais; em algumas versões é reservado para uso futuro |
| `isProtected` | Boolean | Indica se o componente é protegido em contexto de empacotamento |
| `label` | String | Nome amigável exibido para a aplicação |
| `logoUrl` | String | URL do logo exibido na aplicação ou na tela de consentimento |
| `managedType` | Enum | Tipo de gerenciamento; documentado como uso interno |
| `orgScopedExternalApp` | String | Identificador composto pelo ID da organização e pelo nome da ECA |

O campo `orgScopedExternalApp` segue o formato:

```text
[Organization_ID]:[External_Client_App_Name]
```

Ele pode ser gerado no primeiro deployment e, depois disso, tornar-se necessário no arquivo.[3][4]

Exemplo:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ExternalClientApplication xmlns="http://soap.sforce.com/2006/04/metadata">
    <contactEmail>integration@example.com</contactEmail>
    <description>Integração com plataforma antifraude</description>
    <distributionState>Local</distributionState>
    <isProtected>false</isProtected>
    <label>Fraud Detection</label>
</ExternalClientApplication>
```

# 2. ExtlClntAppOauthSettings

Diretório:

```text
extlClntAppOauthSettings/
```

Sufixo:

```text
.ecaOauth-meta.xml
```

Tipo Metadata API:

```text
ExtlClntAppOauthSettings
```

Esse arquivo contém as configurações do plugin OAuth definidas pelo desenvolvedor. A Salesforce disponibiliza esse tipo a partir da API 59.0.[5]

| Propriedade | Tipo | Finalidade |
|---|---|---|
| `fullName` | Herdado de `Metadata` | Nome técnico do componente |
| `externalClientApplication` | String | Nome da ECA associada; é obrigatório |
| `label` | String | Nome amigável da configuração OAuth |
| `commaSeparatedOauthScopes` | String | Lista de scopes OAuth separada por vírgulas |
| `oauthLink` | String | Valor gerado automaticamente, combinando o ID da organização e o ID do OAuth Consumer |
| `callbackUrl` | Não listado nesse tipo | Normalmente tratado nas configurações globais OAuth |
| `singleLogoutUrl` | String | URL para a qual o Salesforce envia a solicitação de logout |
| `trustedIpRanges` | Lista | Faixas de IP confiáveis |
| `customAttributes` | Lista | Atributos personalizados definidos pelo desenvolvedor |
| `assetTokenAudiences` | String | Audiences dos asset tokens |
| `assetTokenSigningCertificate` | String | Certificado usado para assinar asset tokens |
| `assetTokenValidity` | Integer | Validade do asset token |
| `areAttributesIncludedInAssetToken` | Boolean | Inclui atributos personalizados no JWT do asset token |
| `areCustomPermsIncludedInAssetToken` | Boolean | Inclui permissões personalizadas no JWT do asset token |
| `clientAssertionCertificate` | String | Certificado usado para validar client attestation JWT |
| `isFirstPartyAppEnabled` | Boolean | Permite uso por aplicações first-party em determinados fluxos headless |

### Subestrutura `customAttributes`

Cada elemento de `customAttributes` possui:

| Propriedade | Tipo | Finalidade |
|---|---|---|
| `key` | String | Nome único do atributo |
| `formula` | String | Campo ou fórmula que fornece o valor |

Exemplo:

```xml
<customAttributes>
    <key>country</key>
    <formula>User.Country</formula>
</customAttributes>
```

A Salesforce informa que o limite é de 128 atributos personalizados e que cada chave deve ser única.[5]

### Subestrutura `trustedIpRanges`

Cada faixa possui:

| Propriedade | Tipo | Finalidade |
|---|---|---|
| `startIpAddress` | String | Primeiro endereço da faixa; obrigatório |
| `endIpAddress` | String | Último endereço da faixa; obrigatório |
| `description` | String | Descrição da finalidade da faixa |

Exemplo:

```xml
<trustedIpRanges>
    <startIpAddress>10.55.2.0</startIpAddress>
    <endIpAddress>10.55.2.255</endIpAddress>
    <description>Rede corporativa</description>
</trustedIpRanges>
```

# 3. ExtlClntAppGlobalOauthSettings

Diretório:

```text
extlClntAppGlobalOauthSets/
```

Sufixo:

```text
.ecaGlblOauth-meta.xml
```

Tipo Metadata API:

```text
ExtlClntAppGlobalOauthSettings
```

Esse arquivo contém configurações globais e informações relacionadas ao OAuth Consumer. Ele pode conter dados sensíveis, como consumer key e consumer secret.[2]

| Propriedade | Tipo | Finalidade |
|---|---|---|
| `fullName` | Herdado de `Metadata` | Nome técnico do componente |
| `externalClientApplication` | String | Nome da ECA associada |
| `label` | String | Nome amigável das configurações globais |
| `callbackUrl` | String | URL de callback usada no fluxo OAuth |
| `certificate` | String | Certificado usado em fluxos como JWT Bearer |
| `consumerKey` | String sensível | Chave pública do consumidor OAuth |
| `consumerSecret` | String sensível | Segredo do consumidor OAuth |
| `idTokenConfig` | Estrutura | Configurações do ID token |
| `isClientCredentialsFlowEnabled` | Boolean | Habilita o client credentials flow |
| `isCodeCredFlowEnabled` | Boolean | Habilita o fluxo Authorization Code and Credentials |
| `isCodeCredPostOnly` | Boolean | Controla a modalidade POST-only do fluxo |
| `isConsumerSecretOptional` | Boolean | Indica se o consumer secret é opcional |
| `isDeviceFlowEnabled` | Boolean | Habilita o device flow |
| `isIntrospectAllTokens` | Boolean | Permite introspecção de todos os tokens |
| `isNamedUserJwtEnabled` | Boolean | Habilita JWT para usuário nomeado |
| `isPkceRequired` | Boolean | Exige PKCE |
| `isRefreshTokenRotationEnabled` | Boolean | Habilita rotação de refresh token |
| `isSecretRequiredForRefreshToken` | Boolean | Exige secret para refresh token |
| `isSecretRequiredForTokenExchange` | Boolean | Exige secret no token exchange |
| `isTokenExchangeEnabled` | Boolean | Habilita token exchange |
| `shouldRotateConsumerKey` | Boolean | Indica solicitação de rotação da consumer key |
| `shouldRotateConsumerSecret` | Boolean | Indica solicitação de rotação do consumer secret |

### Subestrutura `idTokenConfig`

| Propriedade | Tipo | Finalidade |
|---|---|---|
| `idTokenAudience` | String | Audience incluída no ID token |
| `idTokenIncludeAttributes` | Boolean | Inclui atributos no ID token |
| `idTokenIncludeStandardClaims` | Boolean | Inclui claims padrão |
| `idTokenValidityInMinutes` | Integer | Tempo de validade do ID token em minutos |

Exemplo:

```xml
<idTokenConfig>
    <idTokenAudience>SalesforceAudience</idTokenAudience>
    <idTokenIncludeStandardClaims>true</idTokenIncludeStandardClaims>
    <idTokenValidityInMinutes>15</idTokenValidityInMinutes>
</idTokenConfig>
```

O `consumerSecret` não deve ser copiado para documentação comum nem versionado em texto aberto. Documente somente a existência, o local seguro de armazenamento e o processo de rotação. A Salesforce também informa que a implantação dos arquivos OAuth e Global OAuth pode gerar o OAuth Consumer.[6]

# 4. ExtlClntAppOauthConfigurablePolicies

Diretório:

```text
extlClntAppOauthPolicies/
```

Sufixo:

```text
.ecaOauthPlcy-meta.xml
```

Tipo Metadata API:

```text
ExtlClntAppOauthConfigurablePolicies
```

Esse arquivo contém as políticas configuradas pelo administrador para o plugin OAuth.[7]

| Propriedade | Tipo | Finalidade |
|---|---|---|
| `fullName` | Herdado de `Metadata` | Nome técnico do componente |
| `externalClientApplication` | String | Nome da ECA associada; obrigatório |
| `label` | String | Nome amigável da política |
| `apexHandler` | String | Nome do Apex handler |
| `executeHandlerAs` | String | Usuário de execução do Apex handler |
| `clientCredentialsFlowUser` | String | Usuário de execução do client credentials flow |
| `isClientCredentialsFlowEnabled` | Boolean | Habilita client credentials flow |
| `isGuestCodeCredFlowEnabled` | Boolean | Habilita variação guest do fluxo de código e credenciais |
| `isNamedUserJwtEnabled` | Boolean | Habilita JWT para usuário nomeado; campo depreciado em determinados contextos |
| `isTokenExchangeFlowEnabled` | Boolean | Habilita token exchange flow |
| `commaSeparatedCustomScopes` | String | Lista de custom scopes separada por vírgulas |
| `commaSeparatedPermissionSet` | String | Permission Set IDs permitidos |
| `commaSeparatedProfile` | String | Perfis autorizados |
| `customAttributes` | Lista | Atributos personalizados administráveis |
| `guestJwtTimeout` | Integer | Validade do JWT emitido para usuário guest |
| `ipRelaxationPolicyType` | Enum | Política de restrição de IP |
| `namedUserJwtTimeout` | Integer | Validade do JWT de usuário nomeado |
| `permittedUsersPolicyType` | Enum | Define quem pode utilizar a aplicação |
| `policyAction` | Enum | Ação relacionada à exigência de autenticação adicional |
| `refreshTokenPolicyType` | Enum | Política de validade do refresh token |
| `refreshTokenValidityPeriod` | Integer | Período de validade do refresh token |
| `refreshTokenValidityUnit` | Enum | Unidade do período de validade |
| `requiredSessionLevel` | Enum | Nível de segurança exigido para a sessão |
| `sessionTimeoutInMinutes` | Integer | Duração da sessão |
| `singleLogoutUrl` | String | URL usada no logout |
| `startUrl` | String | URL de destino após autenticação |

### Valores importantes

`permittedUsersPolicyType`:

```text
AdminApprovedPreAuthorized
AllSelfAuthorized
```

`ipRelaxationPolicyType`:

```text
Enforce
Bypass
Bypass_2factor
Enforce_RelaxRefresh
```

`refreshTokenPolicyType`:

```text
Infinite
SpecificInactivity
SpecificLifetime
Zero
```

`refreshTokenValidityUnit`:

```text
Days
Hours
Months
```

`requiredSessionLevel`:

```text
HIGH_ASSURANCE
LOW
STANDARD
```

`policyAction`:

```text
Block
RaiseSessionLevel
```

### Subestrutura `customAttributes`

A estrutura dos atributos de política é semelhante à dos atributos de settings:

| Propriedade | Tipo | Finalidade |
|---|---|---|
| `key` | String | Nome único do atributo |
| `formula` | String | Campo existente que fornece o valor |

Exemplo:

```xml
<customAttributes>
    <key>country</key>
    <formula>Organization.Country</formula>
</customAttributes>
```

# 5. ExtlClntAppConfigurablePolicies

Esse tipo representa políticas gerais da External Client App, não apenas políticas específicas do OAuth. A Salesforce o inclui no manifesto junto com os demais componentes da ECA.[3][7]

Como a documentação pública pode variar conforme a versão da API, recomendo capturar esse XML real e fazer a documentação campo a campo a partir dos elementos existentes. A identificação deve seguir este padrão:

```text
tipo: ExtlClntAppConfigurablePolicies
diretório: verificar o diretório retornado pelo retrieve
sufixo: verificar o sufixo retornado pela versão da API
escopo: políticas gerais e ativação/desativação de plugins
```

Na prática, a documentação dessa camada deve registrar:

- associação com a External Client App;
- label da política;
- plugins habilitados;
- plugins desabilitados;
- estado geral da aplicação;
- permissões administrativas;
- valores específicos do ambiente;
- data da última alteração;
- responsável pela alteração.

Essa camada não deve ser confundida com `ExtlClntAppOauthConfigurablePolicies`: uma trata das políticas gerais da aplicação; a outra trata especificamente do plugin OAuth.

# Como fazer a união passo a passo

## Passo 1: Identifique a ECA

Leia o arquivo da pasta `externalClientApps` e capture:

```xml
<label>Fraud Detection</label>
```

O nome técnico do componente vem do nome do arquivo e do `fullName`, quando presente.

Exemplo:

```text
fraudDetection.eca-meta.xml
```

O identificador lógico será:

```text
fraudDetection
```

## Passo 2: Localize os arquivos relacionados

Procure, nas demais pastas, o campo:

```xml
<externalClientApplication>fraudDetection</externalClientApplication>
```

Todos os arquivos com esse mesmo valor pertencem à mesma ECA.

## Passo 3: Separe configurações por responsabilidade

Organize os dados em cinco grupos:

```text
header
oauthSettings
globalOauthSettings
oauthPolicies
generalPolicies
```

Não misture, por exemplo:

- `commaSeparatedOauthScopes` com `commaSeparatedCustomScopes`;
- `callbackUrl` com `startUrl`;
- `consumerSecret` com `refreshTokenValidityPeriod`;
- configuração de desenvolvedor com política de administrador.

## Passo 4: Preserve origem e sensibilidade

Para cada propriedade, registre:

| Campo | Valor | Arquivo de origem | Sensibilidade | Deployável? |
|---|---|---|---|---|
| `label` | Fraud Detection | `fraudDetection.eca-meta.xml` | Público | Sim |
| `commaSeparatedOauthScopes` | `Api, Web` | `.ecaOauth-meta.xml` | Interno | Sim |
| `consumerSecret` | Não expor | `.ecaGlblOauth-meta.xml` | Secreto | Tratamento especial |
| `refreshTokenPolicyType` | `SpecificLifetime` | `.ecaOauthPlcy-meta.xml` | Interno | Sim |
| `sessionTimeoutInMinutes` | `30` | `.ecaOauthPlcy-meta.xml` | Interno | Sim |

Esse controle é importante porque o mesmo campo, como `label`, pode aparecer em diversos XMLs, mas cada ocorrência tem uma função diferente.

## Passo 5: Valide os vínculos

A validação mínima deve verificar:

```text
header.label ou nome técnico
=
externalClientApplication nos demais XMLs
```

Também verifique:

- todas as configurações OAuth apontam para uma ECA existente;
- não existem dois arquivos de política para o mesmo plugin sem justificativa;
- os scopes estão documentados;
- callback URLs estão coerentes;
- os permission sets existem no ambiente;
- o usuário do client credentials flow possui permissão API Only;
- secrets não aparecem em Git;
- `oauthLink` não foi tratado como valor manual.

# Exemplo de documentação unificada

Uma tabela operacional poderia ficar assim:

| Camada | Arquivo | Propriedades principais | Dono |
|---|---|---|---|
| Identidade | `.eca-meta.xml` | `label`, `description`, `distributionState`, `contactEmail` | Desenvolvedor/arquitetura |
| OAuth | `.ecaOauth-meta.xml` | `commaSeparatedOauthScopes`, `trustedIpRanges`, `customAttributes` | Desenvolvedor de integração |
| OAuth global | `.ecaGlblOauth-meta.xml` | `callbackUrl`, `certificate`, `consumerKey`, `isPkceRequired` | Segurança/integração |
| Política OAuth | `.ecaOauthPlcy-meta.xml` | usuários autorizados, refresh token, IP, sessão | Administrador Salesforce |
| Política geral | tipo configurável da ECA | plugins e controles gerais | Administrador Salesforce |

# Manifesto de referência

Para recuperar ou implantar os principais componentes, o manifesto pode seguir esta estrutura:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>*</members>
        <name>ExternalClientApplication</name>
    </types>
    <types>
        <members>*</members>
        <name>ExtlClntAppOauthSettings</name>
    </types>
    <types>
        <members>*</members>
        <name>ExtlClntAppGlobalOauthSettings</name>
    </types>
    <types>
        <members>*</members>
        <name>ExtlClntAppOauthConfigurablePolicies</name>
    </types>
    <types>
        <members>*</members>
        <name>ExtlClntAppConfigurablePolicies</name>
    </types>
    <version>60.0</version>
</Package>
```

A versão da API deve ser compatível com os campos utilizados. Por exemplo, `ExtlClntAppOauthSettings` está disponível a partir da API 59.






---


Lembrando que são 5 pastas

Você tem razão: estou considerando **5 pastas**, não apenas 4. A correção importante é que a pasta de políticas gerais se chama `extlClntAppPolicies`, enquanto `extlClntAppOauthPolicies` é a pasta específica das políticas OAuth.

## As cinco pastas

Para uma External Client App com OAuth, a estrutura deve ser entendida assim:

```text
force-app/main/default/
│
├── externalClientApps/
│   └── MinhaApp.eca-meta.xml
│
├── extlClntAppOauthSettings/
│   └── MinhaAppOauth.ecaOauth-meta.xml
│
├── extlClntAppGlobalOauthSets/
│   └── MinhaAppGlobalOauth.ecaGlblOauth-meta.xml
│
├── extlClntAppPolicies/
│   └── MinhaAppPolicy.ecaPlcy-meta.xml
│
└── extlClntAppOauthPolicies/
    └── MinhaAppOauthPolicy.ecaOauthPlcy-meta.xml
```

A Salesforce divide a configuração da ECA em arquivos de **settings**, configurados pelo desenvolvedor, e arquivos de **policies**, configurados pelo administrador ou pela organização que recebe a aplicação.[1]

| Pasta | Tipo de metadado | Sufixo | Responsabilidade |
|---|---|---|---|
| `externalClientApps` | `ExternalClientApplication` | `.eca-meta.xml` | Identidade e cabeçalho da ECA |
| `extlClntAppOauthSettings` | `ExtlClntAppOauthSettings` | `.ecaOauth-meta.xml` | Configurações OAuth locais |
| `extlClntAppGlobalOauthSets` | `ExtlClntAppGlobalOauthSettings` | `.ecaGlblOauth-meta.xml` | Configurações OAuth globais e protegidas |
| `extlClntAppPolicies` | `ExtlClntAppConfigurablePolicies` | `.ecaPlcy-meta.xml` | Habilitação dos plugins da ECA |
| `extlClntAppOauthPolicies` | `ExtlClntAppOauthConfigurablePolicies` | `.ecaOauthPlcy-meta.xml` | Políticas específicas do plugin OAuth |

A Salesforce confirma que as configurações OAuth são divididas entre um arquivo local e um arquivo global: o global contém os dados do OAuth Consumer, enquanto o local contém as demais configurações e referencia o global.[2]

## 1. `externalClientApps`

Tipo:

```text
ExternalClientApplication
```

Exemplo:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ExternalClientApplication xmlns="http://soap.sforce.com/2006/04/metadata">
    <contactEmail>integration@example.com</contactEmail>
    <contactPhone>+55 11 99999-9999</contactPhone>
    <description>Integração com plataforma antifraude</description>
    <distributionState>Local</distributionState>
    <isProtected>false</isProtected>
    <label>Fraud Detection</label>
</ExternalClientApplication>
```

### Propriedades

| Propriedade | Descrição |
|---|---|
| `contactEmail` | E-mail de contato da aplicação |
| `contactPhone` | Telefone de contato da aplicação |
| `description` | Descrição funcional e técnica |
| `distributionState` | Estado de distribuição, como `Local` |
| `iconUrl` | URL do ícone da aplicação |
| `infoUrl` | URL com informações adicionais |
| `isProtected` | Indica se o componente é protegido |
| `label` | Nome amigável da aplicação |
| `logoUrl` | URL do logotipo |
| `managedType` | Tipo de gerenciamento, quando aplicável |
| `orgScopedExternalApp` | Identificador da aplicação associado à organização |

O `label` é especialmente importante porque as demais configurações usam o nome da ECA pai em `externalClientApplication`. Na documentação oficial de SAML, por exemplo, a Salesforce orienta que esse campo receba o nome da aplicação pai conforme definido no `label`.[3]

## 2. `extlClntAppOauthSettings`

Tipo:

```text
ExtlClntAppOauthSettings
```

Arquivo:

```text
MinhaAppOauth.ecaOauth-meta.xml
```

Exemplo:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ExtlClntAppOauthSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <externalClientApplication>Fraud Detection</externalClientApplication>
    <label>Fraud Detection OAuth Settings</label>
    <commaSeparatedOauthScopes>Api, Web, OpenID</commaSeparatedOauthScopes>
    <oauthLink>FraudDetectionGlobal</oauthLink>
    <singleLogoutUrl>https://app.example.com/logout</singleLogoutUrl>
    <trustedIpRanges>
        <startIpAddress>10.55.2.0</startIpAddress>
        <endIpAddress>10.55.2.255</endIpAddress>
        <description>Rede corporativa</description>
    </trustedIpRanges>
</ExtlClntAppOauthSettings>
```

### Propriedades

| Propriedade | Descrição |
|---|---|
| `externalClientApplication` | Nome da ECA pai |
| `label` | Nome da configuração OAuth local |
| `commaSeparatedOauthScopes` | Scopes OAuth, separados por vírgula |
| `oauthLink` | Referência para o arquivo Global OAuth |
| `singleLogoutUrl` | URL de logout único |
| `trustedIpRanges` | Lista de faixas de IP confiáveis |
| `customAttributes` | Atributos personalizados |
| `assetTokenAudiences` | Audiences permitidas para asset tokens |
| `assetTokenSigningCertificate` | Certificado de assinatura de asset token |
| `assetTokenValidity` | Validade do asset token |
| `areAttributesIncludedInAssetToken` | Inclui atributos no asset token |
| `areCustomPermsIncludedInAssetToken` | Inclui permissões customizadas no asset token |
| `clientAssertionCertificate` | Certificado para validação de client assertion |
| `isFirstPartyAppEnabled` | Habilita comportamento de first-party app |

### `trustedIpRanges`

| Propriedade | Descrição |
|---|---|
| `startIpAddress` | Primeiro IP da faixa |
| `endIpAddress` | Último IP da faixa |
| `description` | Descrição da faixa |

### `customAttributes`

| Propriedade | Descrição |
|---|---|
| `key` | Nome do atributo |
| `formula` | Campo ou fórmula usada para obter o valor |

Esse arquivo é local. Ele pode ser distribuído para diferentes ambientes sem carregar necessariamente os segredos globais do OAuth.

## 3. `extlClntAppGlobalOauthSets`

Tipo:

```text
ExtlClntAppGlobalOauthSettings
```

Arquivo:

```text
MinhaAppGlobalOauth.ecaGlblOauth-meta.xml
```

Exemplo ilustrativo:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ExtlClntAppGlobalOauthSettings xmlns="http://soap.sforce.com/2006/04/metadata">
    <externalClientApplication>Fraud Detection</externalClientApplication>
    <label>Fraud Detection Global OAuth</label>
    <callbackUrl>https://app.example.com/oauth/callback</callbackUrl>
    <isPkceRequired>true</isPkceRequired>
    <isRefreshTokenRotationEnabled>true</isRefreshTokenRotationEnabled>
    <isCodeCredFlowEnabled>true</isCodeCredFlowEnabled>
</ExtlClntAppGlobalOauthSettings>
```

### Propriedades

| Propriedade | Descrição |
|---|---|
| `externalClientApplication` | Nome da ECA pai |
| `label` | Nome da configuração global |
| `callbackUrl` | URL de callback OAuth |
| `certificate` | Certificado usado em fluxos baseados em certificado |
| `consumerKey` | Chave pública do OAuth Consumer |
| `consumerSecret` | Segredo do OAuth Consumer |
| `idTokenConfig` | Configuração do ID token |
| `isClientCredentialsFlowEnabled` | Habilita Client Credentials Flow |
| `isCodeCredFlowEnabled` | Habilita Authorization Code and Credentials Flow |
| `isCodeCredPostOnly` | Exige envio POST no fluxo Code and Credentials |
| `isConsumerSecretOptional` | Torna o `client_secret` opcional |
| `isDeviceFlowEnabled` | Habilita Device Flow |
| `isIntrospectAllTokens` | Permite introspecionar todos os tokens |
| `isNamedUserJwtEnabled` | Habilita Named User JWT |
| `isPkceRequired` | Exige PKCE |
| `isRefreshTokenRotationEnabled` | Habilita rotação de refresh token |
| `isSecretRequiredForRefreshToken` | Exige secret na renovação do token |
| `isSecretRequiredForTokenExchange` | Exige secret no token exchange |
| `isTokenExchangeEnabled` | Habilita Token Exchange |
| `shouldRotateConsumerKey` | Solicita rotação da consumer key |
| `shouldRotateConsumerSecret` | Solicita rotação do consumer secret |

### `idTokenConfig`

| Propriedade | Descrição |
|---|---|
| `idTokenAudience` | Audience do ID token |
| `idTokenIncludeAttributes` | Inclui atributos no ID token |
| `idTokenIncludeStandardClaims` | Inclui claims padrão |
| `idTokenValidityInMinutes` | Validade do ID token em minutos |

Este é o arquivo mais sensível. A Salesforce divide as configurações justamente para evitar que os segredos OAuth sejam distribuídos junto com as demais configurações.[2]

Não documente assim:

```xml
<consumerSecret>abc123...</consumerSecret>
```

Documente assim:

```text
consumerSecret:
  valor: não armazenado no repositório
  local: cofre corporativo
  acesso: equipe de integração
  rotação: processo formal de segurança
```

## 4. `extlClntAppPolicies`

Tipo:

```text
ExtlClntAppConfigurablePolicies
```

Arquivo:

```text
MinhaAppPolicy.ecaPlcy-meta.xml
```

Essa é a pasta que estava faltando na resposta anterior.

Exemplo:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ExtlClntAppConfigurablePolicies xmlns="http://soap.sforce.com/2006/04/metadata">
    <externalClientApplication>Fraud Detection</externalClientApplication>
    <isEnabled>true</isEnabled>
    <isOauthPluginEnabled>true</isOauthPluginEnabled>
    <isSamlPluginEnabled>false</isSamlPluginEnabled>
</ExtlClntAppConfigurablePolicies>
```

### Propriedades

| Propriedade | Descrição |
|---|---|
| `externalClientApplication` | Nome da ECA pai |
| `isEnabled` | Habilita a ECA para uso de plugins |
| `isOauthPluginEnabled` | Habilita o plugin OAuth |
| `isSamlPluginEnabled` | Habilita o plugin SAML |
| `isCanvasPluginEnabled` | Habilita o plugin Canvas, quando suportado |
| `isMcpPluginEnabled` | Habilita plugin relacionado a MCP, quando disponível na versão da API |
| `isApiPluginEnabled` | Habilita plugin de API, quando disponível na versão da API |

A propriedade central dessa pasta é `isEnabled`. A Salesforce explica que ela pode habilitar os plugins da aplicação; em uma ECA somente SAML, por exemplo, o OAuth pode ser explicitamente desabilitado com `isOauthPluginEnabled=false`.[3]

Os campos exatos podem variar conforme a versão da API e os plugins habilitados na organização. Por isso, trate esta pasta como a configuração de **quais plugins a ECA pode utilizar**.

## 5. `extlClntAppOauthPolicies`

Tipo:

```text
ExtlClntAppOauthConfigurablePolicies
```

Arquivo:

```text
MinhaAppOauthPolicy.ecaOauthPlcy-meta.xml
```

Exemplo:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ExtlClntAppOauthConfigurablePolicies xmlns="http://soap.sforce.com/2006/04/metadata">
    <externalClientApplication>Fraud Detection</externalClientApplication>
    <label>Fraud Detection OAuth Policies</label>
    <permittedUsersPolicyType>AdminApprovedPreAuthorized</permittedUsersPolicyType>
    <commaSeparatedPermissionSet>Fraud_Integration_User</commaSeparatedPermissionSet>
    <refreshTokenPolicyType>SpecificLifetime</refreshTokenPolicyType>
    <refreshTokenValidityPeriod>1</refreshTokenValidityPeriod>
    <refreshTokenValidityUnit>Days</refreshTokenValidityUnit>
    <ipRelaxationPolicyType>Enforce</ipRelaxationPolicyType>
    <sessionTimeoutInMinutes>30</sessionTimeoutInMinutes>
</ExtlClntAppOauthConfigurablePolicies>
```

### Propriedades

| Propriedade | Descrição |
|---|---|
| `externalClientApplication` | Nome da ECA pai |
| `label` | Nome amigável da política |
| `apexHandler` | Apex handler associado |
| `executeHandlerAs` | Usuário de execução do handler |
| `clientCredentialsFlowUser` | Usuário usado pelo Client Credentials Flow |
| `isClientCredentialsFlowEnabled` | Habilita Client Credentials Flow |
| `isGuestCodeCredFlowEnabled` | Habilita variação guest do Code and Credentials |
| `isNamedUserJwtEnabled` | Habilita Named User JWT |
| `isTokenExchangeFlowEnabled` | Habilita Token Exchange Flow |
| `commaSeparatedCustomScopes` | Custom scopes autorizados |
| `commaSeparatedPermissionSet` | Permission Sets autorizados |
| `commaSeparatedProfile` | Perfis autorizados |
| `customAttributes` | Atributos definidos pela política |
| `guestJwtTimeout` | Validade do JWT de usuário guest |
| `ipRelaxationPolicyType` | Política de relaxamento de IP |
| `namedUserJwtTimeout` | Validade do JWT de usuário nomeado |
| `permittedUsersPolicyType` | Critério de autorização dos usuários |
| `policyAction` | Ação para o nível de sessão |
| `refreshTokenPolicyType` | Política de validade do refresh token |
| `refreshTokenValidityPeriod` | Período de validade do refresh token |
| `refreshTokenValidityUnit` | Unidade da validade |
| `requiredSessionLevel` | Nível de segurança exigido |
| `sessionTimeoutInMinutes` | Timeout da sessão |
| `singleLogoutUrl` | URL de logout |
| `startUrl` | URL de início após a autenticação |

### Valores frequentes

| Campo | Valores comuns |
|---|---|
| `permittedUsersPolicyType` | `AdminApprovedPreAuthorized`, `AllSelfAuthorized` |
| `refreshTokenPolicyType` | `Infinite`, `SpecificInactivity`, `SpecificLifetime`, `Zero` |
| `refreshTokenValidityUnit` | `Days`, `Hours`, `Months` |
| `requiredSessionLevel` | `LOW`, `STANDARD`, `HIGH_ASSURANCE` |
| `policyAction` | `Block`, `RaiseSessionLevel` |
| `ipRelaxationPolicyType` | `Enforce`, `Bypass`, `Bypass_2factor` |

A Salesforce usa essa pasta para configurar, entre outros itens, usuários permitidos, Permission Sets, duração de refresh tokens e timeout de sessão.[1]

# Como unir as cinco pastas

O processo correto é criar uma chave de relacionamento:

```text
externalClientApplication
```

Exemplo:

```text
externalClientApplication = Fraud Detection
```

Depois, monte o documento consolidado:

```yaml
externalClientApplication:
  name: Fraud Detection

  sourceFiles:
    header: externalClientApps/FraudDetection.eca-meta.xml
    oauthSettings: extlClntAppOauthSettings/FraudDetection.ecaOauth-meta.xml
    globalOauthSettings: extlClntAppGlobalOauthSets/FraudDetection.ecaGlblOauth-meta.xml
    policies: extlClntAppPolicies/FraudDetection.ecaPlcy-meta.xml
    oauthPolicies: extlClntAppOauthPolicies/FraudDetection.ecaOauthPlcy-meta.xml

  identity:
    label: Fraud Detection
    description: Integração com plataforma antifraude
    distributionState: Local

  plugins:
    enabled: true
    oauth: true
    saml: false

  oauth:
    scopes:
      - Api
      - Web
      - OpenID
    callbackUrl: https://app.example.com/oauth/callback
    pkceRequired: true
    refreshTokenRotation: true

  oauthPolicies:
    permittedUsers: AdminApprovedPreAuthorized
    permissionSet: Fraud_Integration_User
    refreshTokenPolicy: SpecificLifetime
    refreshTokenValidity: 1 day
    sessionTimeout: 30 minutes

  security:
    consumerSecret:
      value: not-exposed
      storage: corporate-secret-vault
```

# Regra final

A união deve seguir esta lógica:

```text
externalClientApps
        +
extlClntAppPolicies
        +
extlClntAppOauthSettings
        +
extlClntAppGlobalOauthSets
        +
extlClntAppOauthPolicies
        =
uma ECA documentada e rastreável
```

Mas os XMLs continuam separados:

```text
Documentação: unificada
Modelo analítico: unificado
Deployment Salesforce: separado
Secrets: protegidos
```

A correção mais importante é esta:

- `extlClntAppPolicies` informa **quais plugins estão habilitados**.
- `extlClntAppOauthPolicies` informa **como o plugin OAuth será governado**.
- `extlClntAppOauthSettings` informa **as configurações OAuth locais**.
- `extlClntAppGlobalOauthSets` informa **as configurações globais e sensíveis**.
- `externalClientApps` informa **a identidade da aplicação**.

Citações:
[1] OAuth Plugin Enablement with Metadata API https://help.salesforce.com/s/articleView?id=xcloud.meta_enable_oauth_plugin.htm&language=en_US&type=5
[2] External Client Apps https://help.salesforce.com/s/articleView?language=en_US&id=xcloud.external_client_apps.htm&type=5
[3] Integrate a SAML SSO Service Provider as an External ... https://help.salesforce.com/s/articleView?id=xcloud.meta_external_client_app_saml.htm&language=en_US&type=5
[4] Prepare Your SharePoint Unstructured (Site Pages & ... https://developer.salesforce.com/docs/data/data-cloud-int/guide/c360-a-prepare-microsoftsharepoint-unstructured-spsa-connection.html
[5] Configure External Client App Policies https://help.salesforce.com/s/articleView?language=en_US&id=xcloud.meta_configure_external_client_app_policies.htm&type=5
[6] Reading Excel Files Using the Apex Zip Functionality https://developer.salesforce.com/blogs/2025/02/reading-excel-files-using-the-apex-zip-functionality
[7] Headless Identity APIs: Configure an External Client App ... https://help.salesforce.com/s/articleView?language=en_US&id=xcloud.eca_authorization_code_credentials.htm&type=5
[8] Stage, Rotate, and Delete OAuth Credentials for an ... https://help.salesforce.com/s/articleView?id=xcloud.shr_configure_oauth_policies_stage_rotate_and_delete_oauth_credentials_for_an_external_client_app.htm&language=en&type=5
[9] External Client App Settings: Metadata Secrets Protection ... https://help.salesforce.com/s/articleView?id=xcloud.shr_external_client_app_settings_metadata_secrets_protection.htm&language=en&type=5
[10] Configure Packageable External Client Apps https://help.salesforce.com/s/articleView?language=en_US&id=xcloud.meta_configure_packageable_external_client_apps.htm&type=5
[11] Package an External Client App https://help.salesforce.com/s/articleView?id=xcloud.configure_packageable_external_client_apps.htm&language=en&type=5
[12] Configure the External Client App's SAML 2.0 Settings and ... https://help.salesforce.com/s/articleView?language=en_US&id=xcloud.configure_external_client_app_saml.htm&type=5






---












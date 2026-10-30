# Pacote de prompts — Documentação de Jornadas de Integração (Devin)

## Arquivos

| Arquivo | Uso |
|---|---|
| `00_regras_gerais.md` | Regras de todas as fases. Coloque em `<DIR_TRABALHO>/_projeto/` (ou no Knowledge do Devin) |
| `config.exemplo.json` | Modelo do `config.json` com todos os parâmetros. Copie para `<DIR_TRABALHO>/config.json` |
| `modelo_esqueletos/` | Esqueletos oficiais dos documentos (`01` sigla, `02` integração) e o registro de decisões (`00`). Copie `01` e `02` para `<DIR_TRABALHO>/_projeto/templates/` |
| `faseM_modelo_referencia.md` | Prompt que analisa o modelo do time e gera guia de estilo, sintaxe dos blocos, mapa de seções e gabarito |
| `fase0_reconhecimento.md` … `fase5_consolidacao.md` | Prompts. Cole um por sessão do Devin; os parâmetros vêm do `config.json` |
| `checklist_validacao.md` | Seu checklist de revisão, com portão, revisão humana e liberação |
| `base_de_conhecimento/` | Base de consulta das fases 1, 2 e 4: desenhos de integração (382 variantes), guia de evidências, regras de ligação, diagnóstico, limites e anti-padrões. Copie para `<DIR_TRABALHO>/_projeto/base_de_conhecimento/`. Ver o README da pasta e a seção 14 de `00_regras_gerais.md` |

## Preparação (uma vez)

1. Crie `<DIR_TRABALHO>/config.json` a partir de `config.exemplo.json` e preencha os valores.
2. Crie `<DIR_TRABALHO>/_projeto/` e copie para lá `00_regras_gerais.md`, a pasta `base_de_conhecimento/` e os esqueletos `modelo_esqueletos/01_*.md` e `02_*.md` em `_projeto/templates/`.
3. Crie `<DIR_TRABALHO>/_entradas/` com:
   - `tipos_metadata.txt`: um tipo por linha, com o nome da Metadata API (ex.: `ApexClass`, `ApexTrigger`, `Flow`, `CustomObject`, `NamedCredential`…)
   - `assuntos.csv`: coluna `assunto` obrigatória; `descricao` (ajuda muito) e `sigla` opcionais. Exemplo:
     ```
     assunto,descricao,sigla
     Geração de QR code para pix,Gera QR code de cobrança via gateway,FNN
     Retomada de bem,Processo de retomada de garantia,
     ```
     A coluna `sigla` liga cada assunto à sua sigla de documentação. As linhas da sigla do modelo são usadas na Fase M, e a Fase 4 de cada sigla lê seus assuntos daqui. Pode ficar vazia para assuntos ainda sem sigla.
   - `modelo_referencia/`: os documentos do modelo do time (de preferência exportados em `.md` ou `.html`)
4. Tipos de metadata recomendados para `tipos_metadata.txt` (a Fase M aponta os que faltarem):
   `CustomObject, ApexClass, ApexTrigger, Flow, LightningComponentBundle, AuraDefinitionBundle, ApexPage, FlexiPage, CustomMetadata, NamedCredential, ExternalCredential, ExternalClientApplication, ConnectedApp, Certificate, RemoteSiteSetting, CspTrustedSite, Workflow, PlatformEventChannel, ExternalServiceRegistration, Profile, PermissionSet, PermissionSetGroup`

   Também usados pela base de conhecimento (inclua os que existirem no repositório): `ExtlClntAppOauthSettings, ExtlClntAppGlobalOauthSettings, ExtlClntAppOauthConfigurablePolicies, ExtlClntAppConfigurablePolicies, AuthProvider, OauthCustomScope, ExternalDataSource, PlatformEventChannelMember, PlatformEventSubscriberConfig, EventRelayConfig, ManagedEventSubscription, EmailServicesFunction, CustomSite, QuickAction, CustomTab, FlexiPage, CustomLabels, PlatformCachePartition, OutboundNetworkConnection, SamlSsoConfig`
5. **Não há placeholders para trocar nos prompts.** Todo `<CHAVE> [busque no arquivo config.json]` é lido do `config.json`. Entre execuções da Fase 4, troque só a chave `SIGLA` (nunca `SIGLA_MODELO`).

## Ordem de execução (uma org por vez)

```
Fase M (uma vez, sem org) → revisão
Fase 0 → revisão → Fase 1 → revisão → Fase 2 → revisão → Fase 3 → revisão
      → Fase 4 (uma sessão por sigla; comece pela sigla do modelo) → revisão → Fase 5 → revisão
Depois da outra org: Fase 5 com ORG=AMBAS (5B)
```

## Fase 4 para todos os assuntos

A Fase 4 roda **uma vez por sigla**. Para cobrir todos os assuntos:
1. Liste as siglas distintas da coluna `sigla` do `assuntos.csv`. Para cada uma, ajuste `SIGLA` no `config.json` e rode a Fase 4.
2. Para cada assunto **sem sigla**, use `SIGLA = <id_assunto>` (ex.: `ASS-007`).
3. A Fase 5 mostra no índice o status de **todos** os assuntos; qualquer um como "Não documentado" indica uma execução que faltou.

## Teste de amanhã (execução em sequência, sem revisão entre fases)

- Use `MODO_TESTE=sim` em todos os prompts. As fases aceitam os arquivos `_proposto` sem aprovação, e tudo sai marcado como **NÃO VALIDADO**.
- Na fase 4, teste primeiro com a **sigla do modelo** (gera `comparacao_modelo.md`, a melhor medida de qualidade) e depois com 1 sigla difícil.
- Depois do teste, use o checklist para avaliar a **qualidade do método**, e não a documentação em si. Os pontos que mais revelam problemas: FM-H01, F0-H04, F1-H02, F2-H01, F3-H01, F3-H02, F4-H01, F4-H02 e F4-H04.

## Se uma fase falhar

| Sintoma | Onde olhar | Ação |
|---|---|---|
| `PRECHECK_FALHOU.md` | O próprio arquivo | Corrija o insumo indicado e rode a fase de novo |
| `REPROVADO` no relatório | Checks BLOQUEANTE com FALHOU | Peça ao Devin para corrigir os scripts e rodar de novo |
| Muitos ALERTAS | Final do `validation_report.md` | Siga o item do checklist correspondente |

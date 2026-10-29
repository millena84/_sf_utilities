# Pacote de prompts — Documentação de Jornadas de Integração (Devin)

## Arquivos

| Arquivo | Uso |
|---|---|
| `00_regras_gerais.md` | Regras de todas as fases. Coloque em `<DIR_TRABALHO>/_projeto/` (ou no Knowledge do Devin) |
| `template_jornada.md` | Template base (fallback e conteúdos mínimos). Coloque em `<DIR_TRABALHO>/_projeto/` |
| `faseM_modelo_referencia.md` | Prompt que analisa o modelo feito pelo time e gera `template_extraido.md` (que prevalece sobre o template base) |
| `fase0_reconhecimento.md` … `fase5_consolidacao.md` | Prompts. Cole um por sessão do Devin, depois de trocar os placeholders |
| `checklist_validacao.md` | Seu checklist de revisão, com portão, revisão humana e liberação |
| `base_conhecimento/desenhos_integracao/` | Base de consulta: 52 desenhos de integração Salesforce (IN/OUT, SYNC/ASYNC, middleware) em 374 variantes, com metadata types, papel, ordem e quem aciona quem. Ver o README da pasta |

## Preparação (uma vez)

1. Crie `<DIR_TRABALHO>/_projeto/` e copie para lá `00_regras_gerais.md` e `template_jornada.md`.
2. Crie `<DIR_TRABALHO>/_entradas/` com:
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
   `CustomObject, ApexClass, ApexTrigger, Flow, LightningComponentBundle, AuraDefinitionBundle, ApexPage, CustomMetadata, NamedCredential, ExternalCredential, ExternalClientApplication, ConnectedApp, Certificate, RemoteSiteSetting, CspTrustedSite, Workflow, PlatformEventChannel, ExternalServiceRegistration, Profile, PermissionSet, PermissionSetGroup`
3. Placeholders a substituir em cada prompt: `<ORG>`, `<CAMINHO_ORG>`, `<DIR_TRABALHO>`, `<sim|não>` (MODO_TESTE), `<AAAA-MM-DD>` (DATA_REFERENCIA, fases 1 e 5), e, na fase 4, `<SIGLA>` (os assuntos vêm da coluna `sigla` do `assuntos.csv`).

## Ordem de execução (uma org por vez)

```
Fase M (uma vez, sem org) → revisão
Fase 0 → revisão → Fase 1 → revisão → Fase 2 → revisão → Fase 3 → revisão
      → Fase 4 (uma sessão por sigla; comece pela sigla do modelo) → revisão → Fase 5 → revisão
Depois da outra org: Fase 5 com ORG=AMBAS (5B)
```

## Fase 4 para todos os assuntos

A Fase 4 roda **uma vez por sigla**. Para cobrir todos os assuntos:
1. Liste as siglas distintas da coluna `sigla` do `assuntos.csv` e rode a Fase 4 para cada uma.
2. Para cada assunto **sem sigla**, rode a Fase 4 com `SIGLA = <id_assunto>` (ex.: `ASS-007`).
3. A Fase 5 mostra no índice o status de **todos** os assuntos; qualquer um como "Não documentado" indica uma execução que faltou.

## Teste de amanhã (execução em sequência, sem revisão entre fases)

- Use `MODO_TESTE=sim` em todos os prompts. As fases aceitam os arquivos `_proposto` sem aprovação, e tudo sai marcado como **NÃO VALIDADO**.
- Na fase 4, teste primeiro com a **sigla do modelo** (gera `comparacao_modelo.md`, a melhor medida de qualidade) e depois com 1 sigla difícil.
- Depois do teste, use o checklist para avaliar a **qualidade do método**, e não a documentação em si. Os pontos que mais revelam problemas: FM-H01, F0-H04, F1-H02, F2-H01, F3-H01, F3-H02 e F4-H01.

## Se uma fase falhar

| Sintoma | Onde olhar | Ação |
|---|---|---|
| `PRECHECK_FALHOU.md` | O próprio arquivo | Corrija o insumo indicado e rode a fase de novo |
| `REPROVADO` no relatório | Checks BLOQUEANTE com FALHOU | Peça ao Devin para corrigir os scripts e rodar de novo |
| Muitos ALERTAS | Final do `validation_report.md` | Siga o item do checklist correspondente |

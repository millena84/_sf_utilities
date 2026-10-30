# Fase 1 — Resolver endpoints dinâmicos (segunda volta)

Faça uma segunda passada **somente** nos pontos de `fase1/integration_points.csv` com `host = DINAMICO` ou `sistema_externo_id = SIS::DESCONHECIDO` (direção OUTBOUND ou EVENTO), seguindo a trilha do endereço até o valor:

1. **Origem do valor:** a partir do `setEndpoint(...)` (ou da montagem da URL/Named Credential), identifique de onde vem o valor: variável, campo, parâmetro de método, concatenação (`'callout:' + x`).
2. **Siga a trilha** dentro do método e, se o valor vier de outra classe (ex.: `ConfigService.getEndpoint('pix')`), siga a chamada **até 2 níveis**.
3. **Custom Metadata:** se o valor vem de `Tipo__mdt.getInstance('Registro')`, `Tipo__mdt.getAll()` ou SOQL em `__mdt` (filtrando por `DeveloperName`/`MasterLabel`), abra o arquivo do registro em `customMetadata/Tipo.Registro.md-meta.xml` e leia o campo usado.
   - Se houver um registro por ambiente (ex.: `_PRD`, `_HML`, `_DEV`), liste todos e indique qual parece ser produção.
   - Se o registro for escolhido por uma variável, liste os registros candidatos do tipo e diga como a escolha é feita.
4. **Custom Label:** `System.Label.X` → leia o valor em `labels/CustomLabels.labels-meta.xml`.
5. **Resolva o valor encontrado:** URL → domínio; nome de Named Credential → abra a Named Credential e leia a URL.
6. **Custom Setting** (`Tipo__c.getInstance()`, `getOrgDefaults()`, `getValues()`): o valor **não** está no repositório. Mantenha `DINAMICO` e registre a observação "Custom Setting — valor fora do repositório (N06)", com o nome do Custom Setting e do campo.

Gere `fase1/revisao/endpoints_dinamicos.csv`:
`id_ponto,componente_id,trilha(resumo dos passos),fonte_final(NamedCredential|CustomMetadata|CustomLabel|CustomSetting|literal|nao_resolvido),registro_ou_componente,ambiente,host,evidencias`

Depois:
- Atualize em `fase1/integration_points.csv` o `host`, o `endpoint_ref` e o `sistema_externo_id` dos pontos resolvidos (sem mudar `id_ponto`).
- Refaça o agrupamento de `fase1/sistemas_externos_proposto.csv` (sistemas novos ou pontos que passaram para um sistema existente), mantendo `status_revisao = pendente`. Não crie o `_aprovado`.
- Atualize `fase1/config_por_ponto.csv` (tipo `Endpoint`) com a fonte encontrada.
- Rode `validate_fase1.py` de novo e mostre: quantos pontos estavam DINAMICO/DESCONHECIDO, quantos foram resolvidos por fonte final e quantos continuam sem resolução (com o motivo).

Registre em `decisions.md`.

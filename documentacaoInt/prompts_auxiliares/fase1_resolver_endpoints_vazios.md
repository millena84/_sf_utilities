# Fase 1 — Resolver endpoints vazios (OUTBOUND)

Faça uma nova passada em **todos** os pontos de `fase1/integration_points.csv` com `direcao = OUTBOUND` (e `CONFIG`, se aplicável) cujo `host` ou `endpoint_ref` esteja **vazio**, `DINAMICO` ou cujo `sistema_externo_id` seja `SIS::DESCONHECIDO` — **inclusive os que estão em branco**.

Para cada ponto:
1. **Para dentro:** siga a origem do valor passado ao `setEndpoint(...)` (variável, campo, concatenação `'callout:' + x`) e as classes chamadas, até 2 níveis.
2. **Para trás (quem chama):** se o endereço chega **por parâmetro** (ex.: classe genérica de HTTP como `XxxHttpClient.enviar(endpoint, body)`), localize **todas as classes que chamam esse método** e siga a origem do argumento em cada uma, até 3 níveis acima. Cada chamador com destino diferente vira uma linha própria em `endpoints_dinamicos.csv`, e o ponto deve ser associado ao(s) chamador(es) que de fato definem o destino.
3. **Fontes possíveis do valor:**
   - **Custom Metadata** (`Tipo__mdt.getInstance('X')`, `getAll()`, SOQL em `__mdt`): abra `customMetadata/Tipo.X.md-meta.xml` e leia o campo; com um registro por ambiente, registre todos e indique o de produção.
   - **Custom Label** (`System.Label.X`): leia em `labels/CustomLabels.labels-meta.xml`.
   - **Named Credential** (nome no valor): abra a Named Credential e leia a URL.
   - **Literal** no código: domínio da URL.
   - **Custom Setting**: valor fora do repositório → manter `DINAMICO`, com a observação "Custom Setting — valor fora do repositório (N06)".
4. Se mesmo assim não resolver, registre `fonte_final = nao_resolvido`, o motivo, e o **trecho de código** (até 8 linhas, com segredos mascarados) onde o endereço é montado ou usado.

Saídas:
- Acrescente/atualize as linhas em `fase1/revisao/endpoints_dinamicos.csv` (`id_ponto,componente_id,trilha,fonte_final,registro_ou_componente,ambiente,host,evidencias`), com a coluna extra `chamador` quando a trilha for para trás.
- Atualize `host`, `endpoint_ref` e `sistema_externo_id` em `fase1/integration_points.csv` (sem mudar `id_ponto`); se um ponto genérico atender vários destinos, registre os destinos na coluna `observacao` e associe o ponto ao sistema de cada chamador.
- Refaça o agrupamento de `fase1/sistemas_externos_proposto.csv` (mantendo `status_revisao = pendente` e as colunas `nome_sugerido`/`confianca_sugestao`, se existirem). Não crie o `_aprovado`.
- Atualize `fase1/config_por_ponto.csv` (tipo `Endpoint`).
- Rode `validate_fase1.py` de novo.

Mostre ao final: quantos pontos OUTBOUND estavam sem endereço, quantos foram resolvidos por fonte final (e quantos pela trilha "para trás"), e a lista dos que continuam sem resolução com o motivo e o trecho de código. Registre em `decisions.md`.

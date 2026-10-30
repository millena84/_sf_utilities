# Exemplos completos (fictícios)

> ⚠️ **Todos os exemplos são FICTÍCIOS.** Org, sistemas, classes, objetos, hosts e caminhos foram inventados para ilustrar o método. Não representam nenhuma org real e não devem ser copiados como fato.

Cada exemplo mostra o caminho completo que um agente percorre:

1. **Projeto encontrado:** os arquivos que existiriam no repositório.
2. **Diagnóstico:** sinais ([diagnostico.md](../diagnostico.md)), cadeia de ligação ([regras_ligacao.md](../regras_ligacao.md)), desenho e variante, confiança.
3. **Documento final:** no formato B de `documentacaoInt/template_jornada.md` (o `template_extraido.md` do time, quando existir, prevalece).
4. **Riscos e limites:** anti-padrões ([antipadroes.md](../antipadroes.md)), limites da plataforma ([limites_plataforma.md](../limites_plataforma.md)) e o que o repositório não mostra ([limites_da_fonte.md](../limites_da_fonte.md)).

| Exemplo | Direção | Desenho · variante |
|---|---|---|
| [EX01 — Envio de pedido ao ERP](EX01_envio_pedido_erp.md) | OUTBOUND · assíncrono | D.1.v11 (Trigger → Queueable · endpoint E5) |
| [EX02 — Recebimento de status de pagamento](EX02_status_pagamento.md) | INBOUND · síncrono | g.3.v5 (Apex REST · External Client App · JWT) |
| [EX03 — Sincronização de clientes via middleware](EX03_sync_clientes_cdc.md) | EVENTO · assíncrono | M.2.v4 (CDC · External Client App) |

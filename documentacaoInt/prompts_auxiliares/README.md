# Prompts auxiliares

Prompts curtos para corrigir ou completar uma fase **sem rodá-la inteira de novo**. Cole no Devin na mesma sessão da fase (ou numa nova, apontando para a mesma pasta de trabalho).

| Arquivo | Fase | Quando usar |
|---|---|---|
| `fase0_completar_termos_genericos.md` | 0 | A lista de termos genéricos veio curta ou com termos de negócio |
| `fase0_preencher_atributos.md` | 0 | A coluna `atributos` (ou `estado`) do inventário veio vazia |
| `fase0_reagrupar_nao_resolvidas.md` | 0 | A taxa de referências não resolvidas veio perto de 100% |
| `fase1_enriquecer_sistemas_externos.md` | 1 | Os sistemas externos vieram com nomes técnicos, `DINAMICO` ou `SIS::DESCONHECIDO` |
| `fase1_resolver_endpoints_dinamicos.md` | 1 | Pontos com endpoint `DINAMICO` ou sistema `SIS::DESCONHECIDO` (endereço vindo de Custom Metadata, Custom Label, classe de configuração) |
| `fase1_resolver_endpoints_vazios.md` | 1 | Pontos OUTBOUND com endereço em branco, inclusive quando o endereço chega por parâmetro de uma classe genérica de HTTP |

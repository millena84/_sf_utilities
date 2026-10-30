# Ponto de retomada

> Atualizado em 2026-10-30. Org em execução: a primeira org (sigla do modelo: FNN).

## Onde paramos
- **Fase M:** concluída e revisada (`mapa_secoes_aprovado.csv`).
- **Fase 0:** concluída e revisada. Correções feitas com prompts auxiliares: atributos do inventário, referências não resolvidas agregadas, termos genéricos completados.
- **Fase 1:** concluída e revisada. Voltas adicionais: endpoints dinâmicos (Custom Metadata/Label), endpoints vazios (trilha "para trás"), domínio das configurações, enriquecimento dos sistemas externos.
- **Fase 2:** **interrompida no meio** (cota do Devin).

## Como retomar
1. Renomear `docs_v2/<ORG>/fase2/` para `fase2_parcial/` (ou apagar) e apagar `docs_v2/<ORG>/tools/fase2/`. Não mexer em `fase0/` e `fase1/`.
2. Conferir que existem e estão sem `pendente`:
   - `fase0/relation_rules_aprovado.csv`, `fase0/termos_genericos_aprovado.csv`, `fase0/glossario_aprovado.csv`;
   - `_entradas/gabarito_<ORG>.csv` (um componente por linha);
   - `fase1/sistemas_externos_aprovado.csv` (feito depois do último enriquecimento).
3. Se a sessão do Devin for nova, colar antes do prompt:
   > Execução nova da Fase 2, do zero. Não reutilize scripts, lógica ou resultados de execuções anteriores. Escreva os scripts a partir deste prompt e leia as regras do arquivo `fase0/relation_rules_aprovado.csv` a cada execução.
4. Rodar `fase2_grafo.md` (versão mais nova: referências não resolvidas agregadas por nome e `revisao/diagnostico.md`).

## Conferir ao fim da Fase 2
- Tabela de arestas por regra no `validation_report.md`: nenhuma regra aprovada com 0 arestas sem explicação (atenção às regras 20–24).
- `revisao/diagnostico.md` com a conclusão "grafo consistente".
- Revisar `infra_hubs_proposto.csv` e salvar como `infra_hubs_aprovado.csv` (na dúvida sobre classe com regra de negócio: `rejeitado`).

## Depois
Fase 3 → Fase 4 (SIGLA = FNN) → Fase 4R (sessão nova) → revisão → demais siglas → Fase 5. Roteiro visual: https://claude.ai/artifact/MDek1K9N5a4jcHTbKF9spX

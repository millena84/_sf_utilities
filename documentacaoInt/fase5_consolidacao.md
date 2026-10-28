# Fase 5 — Consolidação (org <ORG>) e 5B — Consolidação entre orgs

## Antes de começar
Leia e siga integralmente `<DIR_TRABALHO>/_projeto/00_regras_gerais.md`.

## Parâmetros desta execução
- ORG: `<ORG>` (ou `AMBAS` para a 5B) · DIR_TRABALHO: `<DIR_TRABALHO>` · MODO_TESTE: `<sim|não>`

## Objetivo
Transformar as jornadas em uma documentação navegável: índice, catálogos e lacunas.

## Insumos
- Todos os artefatos aprovados das fases 0–3 e os docs/CSVs da fase 4 desta org.

## P. Pré-checagem
- Todo assunto com status aprovado na fase 3 tem pasta na fase 4 com `validation_report.md` aprovado; os que não têm são listados (ALERTA — não bloqueia, entram em "Pendentes" no índice).
- Falhou de forma bloqueante → `fase5/PRECHECK_FALHOU.md` e encerre.

## Etapas (por org)

### 5.1 Índice — `docs/README.md`
- Como ler esta documentação (5 linhas).
- Tabela de assuntos: assunto, nº de jornadas, direções, sistemas externos, confiança, status (Documentado | Pendente | Sem integração detectada), link.
- Atalhos: por sistema externo, por direção.

### 5.2 Catálogo de sistemas externos — `docs/sistemas/<sistema_externo_id>.md` + `docs/sistemas/README.md`
Por sistema: nome, hosts (só domínio), credenciais (nomes), mecanismos, direções, jornadas que o usam (links), pontos de integração.

### 5.3 Catálogo de infraestrutura — `docs/infraestrutura/README.md`
Componentes INFRA aprovados: o que fazem (1–2 frases), quem usa (assuntos), evidência. Documentados uma única vez.

### 5.4 Lacunas — `docs/lacunas.md`
Consolidar: INBOUND_PRESUMIDO, endpoints `DINAMICO`, `SIS::DESCONHECIDO`, pontos órfãos, configurações sem uso, assuntos sem integração detectada, assuntos pendentes, sinais em tipos fora do escopo, `questions.md` em aberto. Cada item com origem (fase/arquivo) e ação sugerida.

### 5.5 Glossário — `docs/glossario.md`
Termos de negócio dos assuntos e siglas técnicas usadas nos docs.

## Etapa 5B (somente com `ORG = AMBAS`, após 5.1–5.5 nas duas orgs)
- `_consolidado/README.md`: assuntos presentes em uma ou nas duas orgs, com links.
- Sistemas externos em comum (mesmo host/credencial) → `_consolidado/sistemas_comuns.md`.
- Integrações **entre as orgs** (endpoint de uma apontando para domínio Salesforce da outra) → `_consolidado/integracoes_entre_orgs.md`.

## Material de revisão humana (`fase5/revisao/`)
- `roteiro_navegacao.md` — 5 perguntas típicas de leitor (ex.: "quais jornadas usam o sistema X?") com o caminho de cliques para respondê-las.

## Autovalidação — `tools/fase5/validate_fase5.py`

| ID | Verificação | Severidade |
|---|---|---|
| F5-A01 | Pré-checagem executada | BLOQUEANTE |
| F5-A02 | Todo assunto aprovado aparece no índice com status correto | BLOQUEANTE |
| F5-A03 | Todos os links internos (de todos os docs) resolvem para arquivos existentes | BLOQUEANTE |
| F5-A04 | Todo sistema externo aprovado tem página; toda página referencia jornadas existentes ou está em lacunas | BLOQUEANTE |
| F5-A05 | Todo componente INFRA citado nas jornadas está no catálogo de infraestrutura | BLOQUEANTE |
| F5-A06 | Números do índice batem com os CSVs das fases 1–4 | BLOQUEANTE |
| F5-A07 | Fechamento de lacunas: todo item pendente/órfão/dinâmico/desconhecido das fases anteriores está em `lacunas.md` | BLOQUEANTE |
| F5-A08 | Nenhum segredo; hosts só com domínio | BLOQUEANTE |
| F5-A09 | Docs em MODO_TESTE marcados como NÃO VALIDADO | BLOQUEANTE |
| F5-A10 | (5B) Todo assunto das duas orgs aparece no consolidado | BLOQUEANTE |

## Entrega
Docs acima + `fase5/validation_report.md` + `fase5/RESUMO_FASE5.md`.

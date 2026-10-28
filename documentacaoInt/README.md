# Pacote de prompts — Documentação de Jornadas de Integração (Devin)

## Arquivos

| Arquivo | Uso |
|---|---|
| `00_regras_gerais.md` | Regras de todas as fases. Coloque em `<DIR_TRABALHO>/_projeto/` (ou no Knowledge do Devin) |
| `template_jornada.md` | Template dos documentos finais. Coloque em `<DIR_TRABALHO>/_projeto/` |
| `fase0_reconhecimento.md` … `fase5_consolidacao.md` | Prompts. Cole um por sessão do Devin, depois de trocar os placeholders |
| `checklist_validacao.md` | Seu checklist de revisão, com portão, revisão humana e liberação |

## Preparação (uma vez)

1. Crie `<DIR_TRABALHO>/_projeto/` e copie para lá `00_regras_gerais.md` e `template_jornada.md`.
2. Crie `<DIR_TRABALHO>/_entradas/` com:
   - `tipos_metadata.txt`: um tipo por linha, com o nome da Metadata API (ex.: `ApexClass`, `ApexTrigger`, `Flow`, `CustomObject`, `NamedCredential`…)
   - `assuntos.csv`: coluna `assunto` obrigatória e `descricao` opcional (ajuda muito)
3. Placeholders a substituir em cada prompt: `<ORG>`, `<CAMINHO_ORG>`, `<DIR_TRABALHO>`, `<sim|não>` (MODO_TESTE) e, na fase 4, `<ID_ASSUNTO>`.

## Ordem de execução (uma org por vez)

```
Fase 0 → revisão → Fase 1 → revisão → Fase 2 → revisão → Fase 3 → revisão
      → Fase 4 (uma sessão por assunto) → revisão → Fase 5 → revisão
Depois da outra org: Fase 5 com ORG=AMBAS (5B)
```

## Teste de amanhã (execução em sequência, sem revisão entre fases)

- Use `MODO_TESTE=sim` em todos os prompts. As fases aceitam os arquivos `_proposto` sem aprovação, e tudo sai marcado como **NÃO VALIDADO**.
- Na fase 4, teste com **2 assuntos**: um que você conhece bem e um difícil.
- Depois do teste, use o checklist para avaliar a **qualidade do método**, e não a documentação em si. Os pontos que mais revelam problemas: F0-H04, F1-H02, F2-H01, F3-H01 e F3-H02.

## Se uma fase falhar

| Sintoma | Onde olhar | Ação |
|---|---|---|
| `PRECHECK_FALHOU.md` | O próprio arquivo | Corrija o insumo indicado e rode a fase de novo |
| `REPROVADO` no relatório | Checks BLOQUEANTE com FALHOU | Peça ao Devin para corrigir os scripts e rodar de novo |
| Muitos ALERTAS | Final do `validation_report.md` | Siga o item do checklist correspondente |

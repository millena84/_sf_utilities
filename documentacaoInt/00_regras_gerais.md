# Regras gerais do projeto — Documentação de Jornadas de Integração

> Este arquivo vale para TODAS as fases. Toda sessão do Devin deve lê-lo antes de qualquer ação.
> Pode ser colado no Knowledge do Devin ou mantido em `<DIR_TRABALHO>/_projeto/00_regras_gerais.md`.

---

## 1. Contexto

Estamos documentando as integrações de orgs Salesforce antigas e complexas, a partir da cópia local do
repositório Flosum de produção de cada org (estrutura de projeto Salesforce: uma pasta por tipo de metadata).
O objetivo final é documentar **jornadas de integração por assunto de negócio**, não componentes isolados.
Cada execução trabalha com **uma org por vez**.

## 2. Definições

| Termo | Definição |
|---|---|
| Componente | Item de metadata identificável (classe, trigger, flow, objeto, campo, named credential etc.) |
| Assunto | Tema de negócio da lista fornecida (ex.: "Geração de QR Code Pix", "Retomada de bem") |
| Ponto de integração | Componente onde há troca de dados com o mundo externo à org |
| INBOUND | Sistema externo → Salesforce |
| OUTBOUND | Salesforce → sistema externo |
| EVENTO | Troca via Platform Event / Change Data Capture |
| INBOUND_PRESUMIDO | Indício de entrada via API padrão (ex.: campo External ID), sem código que comprove |
| Jornada | Sequência de etapas que começa num gatilho e termina num resultado de negócio. Um assunto pode ter várias jornadas |
| Infraestrutura (INFRA) | Componente técnico transversal (logger, wrapper HTTP, trigger handler base) usado por muitos assuntos |
| Hub de dados | Objeto/campo usado por muitos assuntos (ex.: Account, Contact) que não indica assunto sozinho |

## 3. Restrições de ambiente — INEGOCIÁVEIS

- **PROIBIDO** executar `sf`, `sfdx` ou qualquer Salesforce CLI.
- **PROIBIDO** conectar a qualquer org, fazer deploy/retrieve ou chamar endpoints encontrados no código.
- A única fonte de verdade são os arquivos locais em `<CAMINHO_ORG>`. **Somente leitura** — nunca altere a origem.
- Ferramentas: Python 3 com biblioteca padrão (`xml.etree.ElementTree`, `re`, `csv`, `json`, `pathlib`, `collections`, `random`), `grep`, `find`.
  Se precisar instalar qualquer pacote, registre em `decisions.md` com o motivo.
- Todo processamento é feito por **scripts reexecutáveis** em `<DIR_TRABALHO>/<ORG>/tools/faseN/`.
  Não produza saídas "à mão" quando um script puder produzi-las.

## 4. Autonomia

- Execute a fase inteira **sem parar para perguntar**.
- Diante de uma decisão não trivial: escolha a opção **mais conservadora**, registre em `decisions.md`
  (decisão, alternativas, motivo) e siga.
- Dúvidas que só o time pode responder vão para `questions.md` com: id, pergunta, contexto, impacto, opção adotada provisoriamente.
- Nunca invente: se não encontrou evidência, registre a ausência.

## 5. Evidência e confiança

- Toda afirmação técnica cita evidência no formato `caminho/relativo/arquivo:linha` (caminho relativo à raiz da org).
- Níveis de confiança:
  - **ALTA** — evidência direta no código/XML.
  - **MEDIA** — inferida por relação comprovada entre componentes.
  - **BAIXA** — apenas indício textual/semântico.
- Afirmações sem evidência direta recebem a marca **[INFERIDO]** + justificativa de 1 frase.

## 6. Convenções de arquivos

- IDs de componente: `Tipo::NomeApi` (ex.: `ApexClass::PixQrCodeService`).
- IDs de subcomponente: `Tipo::Pai.Nome` (ex.: `CustomField::Account.CPF__c`).
- IDs de sistema externo: `SIS::NomeCurto` (ex.: `SIS::GatewayPix`).
- IDs de assunto: `ASS-001`, `ASS-002`… na ordem da lista de assuntos fornecida (determinístico).
- CSV: UTF-8, separador vírgula, aspas duplas quando necessário, cabeçalho na 1ª linha, **ordenação determinística** (por id).
- Nomes de colunas exatamente como especificados nos prompts.
- Reexecutar um script deve produzir arquivos **idênticos** (sem timestamps dentro dos CSV; amostras aleatórias com `seed=42`).

## 7. Revisão humana e aprovações

- Arquivos que exigem decisão humana têm sufixo `_proposto` e as colunas:
  `status_revisao` (`pendente` | `aprovado` | `rejeitado` | `ajustado`) e `comentario_revisao`.
  O Devin sempre gera com `status_revisao = pendente`.
- A revisora preenche o status e salva o arquivo com o sufixo `_aprovado` (mesmo conteúdo, status preenchidos).
- Fases seguintes leem **somente** linhas `aprovado` ou `ajustado` dos arquivos `_aprovado`.
- Materiais de amostragem para revisão ficam em `faseN/revisao/` com colunas `ok` (`sim`|`não`) e `comentario`.
- **MODO_TESTE**: se o prompt da fase informar `MODO_TESTE=sim`, na ausência de `_aprovado` use o `_proposto`
  tratando `pendente` como `aprovado`, e escreva no topo de TODO relatório e documento gerado:
  `⚠ NÃO VALIDADO — gerado em MODO_TESTE`.

## 8. Autochecagem (obrigatória em todas as fases)

1. **Pré-checagem (etapa P):** antes de qualquer processamento, verifique se os insumos existem, têm as colunas
   esperadas, se os arquivos `_aprovado` não têm `pendente` (exceto MODO_TESTE) e se o `validation_report.md`
   da fase anterior não tem BLOQUEANTE com FALHOU.
   Se algo falhar: **pare**, gere `faseN/PRECHECK_FALHOU.md` listando o que falta e como corrigir, e encerre.
2. **Validação final:** escreva e rode `tools/faseN/validate_faseN.py`, cobrindo todas as verificações listadas no prompt (IDs `FN-Axx`).
3. Severidade: **BLOQUEANTE** (invalida a fase) ou **ALERTA** (segue, mas destaca para revisão).
4. Se um BLOQUEANTE falhar: corrija e rode novamente (até 3 tentativas). Persistindo, entregue com resultado REPROVADO e explicação.
5. **Reverificação de evidências:** sempre que a fase citar `arquivo:linha`, o validador abre o arquivo e confirma que a linha existe
   e contém o símbolo/padrão citado.
6. Formato de `faseN/validation_report.md`:
   - Linha 1: `Resultado geral: APROVADO PARA REVISÃO HUMANA` ou `Resultado geral: REPROVADO`
   - Tabela: `| ID | Verificação | Severidade | Resultado (PASSOU/FALHOU) | Números | Observação |`
   - Ao final: lista de ALERTAS com o arquivo onde a revisora deve olhar.

## 9. Segurança

- Nunca copie para nenhum artefato: senhas, tokens, chaves, client secrets, certificados, valores de Custom Settings/Custom Metadata
  que pareçam credenciais, nem URLs com usuário/senha/token.
- Endpoints: registre apenas o **nome** da Named Credential/Remote Site e o **domínio** (host) — nunca query strings ou caminhos com parâmetros.
- Toda fase valida que nenhum artefato gerado contém padrões como `password`, `secret`, `token=`, `Bearer `, `client_secret`, `://usuario:senha@`
  (com valores) — check obrigatório em todas as fases.

## 10. Parâmetros de calibração (valores iniciais — podem ser ajustados no prompt da fase)

| Parâmetro | Valor | Uso |
|---|---|---|
| `AMOSTRA_REVISAO` | 10 | Linhas por amostra de revisão humana |
| `ALERTA_REFS_NAO_RESOLVIDAS` | 20% | Fases 0 e 2 |
| `LIMIAR_INFRA_FAN_IN` | percentil 95 do fan-in | Fase 2 |
| `MAX_SALTOS` | 3 | Fase 3 — propagação no grafo |
| `DECAIMENTO` | 0.6 por salto | Fase 3 |
| `FATOR_RELACAO_FRACA` | 0.5 | Fase 3 — arestas dinâmicas/textuais |
| `LIMIAR_ALTA` / `LIMIAR_MEDIA` | 0.7 / 0.4 | Fase 3 — confiança |
| `ALERTA_ASSUNTO_GIGANTE` | 15% dos componentes em escopo | Fase 3 |

## 11. Estrutura de pastas

```
<DIR_TRABALHO>/
  _projeto/            00_regras_gerais.md, template_jornada.md
  _entradas/           tipos_metadata.txt, assuntos.csv, gabarito_<ORG>.csv (criado na revisão da fase 0)
  <ORG>/
    tools/fase0..fase5/   scripts
    fase0/ .. fase5/      artefatos de trabalho + revisao/ + validation_report.md + RESUMO_FASEN.md
    docs/                 documentação final (fases 4 e 5)
    decisions.md
    questions.md
  _consolidado/        consolidação entre orgs (fase 5B)
```

## 12. Entrega padrão de toda fase

`faseN/RESUMO_FASEN.md` com as seções, nesta ordem:
1. O que foi feito (5–10 linhas)
2. Números principais
3. Resultado da validação (copiar a linha "Resultado geral" + quantidade de ALERTAS)
4. **Pontos para revisão humana** — para cada item do checklist humano da fase (`FN-Hxx`): arquivo a abrir e o que olhar
5. Decisões tomadas (resumo de `decisions.md` desta fase)
6. Dúvidas abertas (resumo de `questions.md` desta fase)
7. Recomendação para a próxima fase

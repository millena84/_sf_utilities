import sys, os, json
from designs import SECOES
from blocks import ENDPOINTS, FLOWS
from evidencias import FONTES, TIPOS, CODIGO, NAO_CONFIRMADOS, evid
from ligacoes import LIGACOES
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
def esc(s): return str(s).replace("|", "\\|")
def fonte(ids):
    return ", ".join(f"[{i.strip()}]({FONTES[i.strip()]})" if i.strip() in FONTES else i for i in ids.split(","))
AVISO = "> Gerado a partir de `_fonte/`. Não edite este arquivo: altere as definições e rode `python3 _fonte/render.py .` nesta pasta."

# ---------- desenhos (um arquivo por seção) ----------
total = {}
for slug, titulo, ds in SECOES:
    L = [f"# {titulo}", "", AVISO, "", "Convenções, legenda e códigos de variante: [README](README.md). Fontes citadas entre colchetes: [fontes_validacao.md](fontes_validacao.md).", "", "## Índice", ""]
    for d in ds:
        L.append(f"- [{d['id']} — {d['titulo']}](#{d['id'].lower().replace('.', '')}) ({len(d['variantes'])} variantes)")
    for d in ds:
        L += ["", f"## {d['id']}", "", f"**{d['titulo']}**", "", d["resumo"], ""]
        for o in d["obs"]: L.append(f"> Observação: {o}")
        for v in d["validar"]: L.append(f"> ⚠️ A validar: {v}")
        if d["obs"] or d["validar"]: L.append("")
        for i, (nome, rows) in enumerate(d["variantes"], 1):
            fluxo = " → ".join(r[0] for r in rows if r[2] in ("executa", "ator", "executa (DML)") and r[6].startswith("Obrig"))
            L += [f"### {d['id']}.v{i} — {nome}", "", f"Fluxo principal: {fluxo}", "",
                  "| Ordem | Componente | Metadata type | Relação | Papel na integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |",
                  "|---|---|---|---|---|---|---|---|---|"]
            for k, r in enumerate(rows, 1):
                L.append("| " + " | ".join([str(k)] + [esc(x) for x in r] + [esc(evid(r[0], r[1]))]) + " |")
            L.append("")
    total[slug] = sum(len(d['variantes']) for d in ds)
    open(f"{out}/{slug}.md", "w").write("\n".join(L) + "\n")

# ---------- item 1: guia de evidências ----------
L = ["# Guia de evidências no projeto", "", AVISO, "",
     "Como reconhecer cada componente nos arquivos de um projeto Salesforce (cópia do repositório, sem acesso à org).",
     "Os fatos foram conferidos na documentação oficial em 2026-10-30 (Metadata API Developer Guide Winter '27, API 68.0, e os guias citados). `nv` = não validado na fonte nesta coleta.", "",
     "## 1. Formato do projeto", "",
     "- **Metadata API format:** uma pasta por tipo (ex.: `namedCredentials/`), arquivo `Nome.<sufixo>`; código Apex vem em par (`X.cls` + `X.cls-meta.xml`).",
     f"- **Source format (Salesforce DX):** o XML de cada componente ganha `-meta.xml` (ex.: `Case.object-meta.xml`), e tipos como CustomObject são decompostos em subpastas (`objects/X/fields/Y.field-meta.xml`). Fonte: {fonte('DX-FMT')}.",
     "- Ao procurar um sufixo da tabela abaixo, aceite as duas formas: `.namedCredential` e `.namedCredential-meta.xml`.", "",
     "## 2. Catálogo por metadata type", "",
     "| Metadata type | Pasta | Sufixo (Metadata API format) | Desde a API | O que procurar no XML | Campos sensíveis (nunca copiar o valor) | Fonte |",
     "|---|---|---|---|---|---|---|"]
for t, (pasta, suf, ver, xml, sens, f) in TIPOS.items():
    L.append(f"| `{t}` | `{pasta}` | {esc(suf)} | {ver} | {esc(xml)} | {esc(sens)} | {fonte(f)} |")
L += ["", "### Não confirmados", ""] + [f"- `{k}`: {v}" for k, v in NAO_CONFIRMADOS.items()]
L += ["", "## 3. Padrões de código Apex", "", "| ID | Procure | Significa | Fonte |", "|---|---|---|---|"]
for cid, pat, sig, f in CODIGO:
    L.append(f"| {cid} | {esc(pat)} | {esc(sig)} | {fonte(f)} |")
L += ["", "## 4. Evidência por eixo de variante", "",
      "| Eixo | Variante | Evidência que a confirma |", "|---|---|---|",
      "| Endpoint | E1 | C01 `callout:Nome` + `Nome.namedCredential` com `namedCredentialType`=SecuredEndpoint e parâmetro Authentication → `externalCredential` |",
      "| Endpoint | E2 | C01 `callout:Nome` + `Nome.namedCredential` com `namedCredentialType`=Legacy (campos `endpoint`, `protocol`) |",
      "| Endpoint | E3 | C03 URL literal no código + `remoteSiteSettings/*.remoteSite` com o mesmo host |",
      "| Endpoint | E4 | URL lida de `X__mdt` (L37) + registro em `customMetadata/` com a URL + Remote Site com o host |",
      "| Endpoint | E5 | registro em `customMetadata/` cujo valor é o nome de uma Named Credential + `callout:` montado no código |",
      "| Endpoint | E6 | URL vinda de Custom Setting (`objects/X__c` com tipo de setting) ou `labels/CustomLabels.labels` + Remote Site |",
      "| Entrada | Connected App | `connectedApps/*.connectedApp` com `oauthConfig` |",
      "| Entrada | External Client App | `externalClientApps/*.eca` + plugins (`.ecaOauth`, `.ecaGlblOauth`, `.ecaOauthPlcy`, `.ecaPlcy`) |",
      "| Fluxo OAuth | Client Credentials | Connected App: `isClientCredentialEnabled` + `oauthClientCredentialUser`; ECA: `isClientCredentialsFlowEnabled` + `clientCredentialsFlowUser` |",
      "| Fluxo OAuth | JWT Bearer | certificado no app (`oauthConfig.certificate` / `certificate` em `.ecaGlblOauth`) |",
      "| Fluxo OAuth | Web Server / Username-Password | não distinguíveis pelo XML do app: a escolha fica no cliente externo (registrar como \"não determinado\") |",
      "| Assíncrono | @future / Queueable / Batch / Flow assíncrono | C06 / C07 / C08 / `pathType`=AsyncAfterCommit |",
      "", "Estas linhas aplicam o catálogo acima; não são uma página oficial única.", "",
      "## 5. Coluna \"Como achar no projeto\" nos desenhos", "",
      "Cada tabela de variante (out-sync.md, in-sync.md...) tem a coluna **Como achar no projeto**, gerada a partir deste guia: o código `Cnn` aponta para a seção 3 e o `[ID]` para a fonte."]
open(f"{out}/guia_evidencias.md", "w").write("\n".join(L) + "\n")

# ---------- item 2: regras de ligação ----------
L = ["# Regras de ligação entre componentes", "", AVISO, "",
     "Como seguir de um componente para o próximo, no projeto, para montar a cadeia da integração (ex.: trigger → handler → Queueable → `callout:X` → Named Credential X → External Credential).", "",
     "**Tipos de regra:**",
     "- **documentado**: campo ou sintaxe confirmados na documentação oficial (fonte na linha).",
     "- **heurística**: padrão de código comum, não é regra da plataforma. Use, mas registre a confiança como média.",
     "- **nv**: a plataforma documenta, mas a página não foi conferida nesta coleta.", "",
     "| ID | De | Para | Como seguir no projeto | Tipo | Fonte |", "|---|---|---|---|---|---|"]
for lid, de, para, como, tipo, f in LIGACOES:
    L.append(f"| {lid} | {esc(de)} | {esc(para)} | {esc(como)} | {tipo} | {fonte(f) if f != '—' else '—'} |")
L += ["", "## Casos difíceis", "",
      "- **Endpoint concatenado** (`'callout:' + nome + path`, ou URL montada com variáveis): resolva só o que for literal; o resto fica \"não determinado\", com a linha do código como evidência.",
      "- **Nome vindo de configuração** (L36/L37): procure o registro de Custom Metadata, Custom Setting ou Custom Label que fornece o valor; sem ele, \"não determinado\".",
      "- **Despacho dinâmico** (`Type.forName`, interfaces, mapas de handlers): L39. Liste os candidatos (classes que implementam a interface) sem afirmar qual roda.",
      "- **Classe de teste**: C23. Nunca conte como ponto de integração.",
      "- **Ligação ausente**: um lado existe e o outro não (ex.: `callout:X` sem `X.namedCredential` no projeto) — registre como lacuna; não invente o componente."]
open(f"{out}/regras_ligacao.md", "w").write("\n".join(L) + "\n")

# ---------- fontes ----------
L = ["# Fontes e validação", "", AVISO, "",
     "Páginas oficiais consultadas em 2026-10-30. O ID entre colchetes é usado nos outros arquivos.", "",
     "| ID | Página |", "|---|---|"] + [f"| {k} | <{v}> |" for k, v in FONTES.items()]
L += ["", "## Resultado da validação dos itens ⚠️", "",
      "| Item | Resultado | Fonte |", "|---|---|---|",
      f"| Callout síncrono em trigger Apex | **confirmado**: \"Callouts must be made asynchronously from a trigger\" | {fonte('AX-TRG')} |",
      f"| Callout em trigger de Platform Event | **confirmado**: \"with some exceptions, you generally can’t make Apex callouts from triggers\" | {fonte('PE-SUB')} |",
      f"| Callout em DML pendente | **confirmado**: não é possível com operações pendentes (DML, async, e-mail) na mesma transação | {fonte('AX-LIM')} |",
      f"| Limites de callout | **confirmado**: 100 por transação; timeout padrão 10 s, máx. 120 s; 120 s acumulados | {fonte('AX-LIM')} |",
      f"| Continuation | **confirmado** para Visualforce e \"Lightning component\": 3 paralelos, 3 encadeados, 120 s. Anotação em LWC: não confirmada | {fonte('AX-CONT')}, {fonte('AX-CONTL')} |",
      f"| HTTP Callout do Flow | **confirmado**: gera ExternalServiceRegistration com `registrationProviderType`=SchemaInferred | {fonte('MA-ESR')} |",
      f"| MuleSoft como fonte de External Service | **confirmado**: `registrationProviderType` MuleSoft / Anypoint | {fonte('MA-ESR')} |",
      f"| Event Relay | **confirmado**: `destinationResourceName`=`callout:Nome` (conta AWS) e `eventChannel` `X__chn`. Tipo da Named Credential: não informado | {fonte('MA-ERC')} |",
      f"| `OauthTokenExchangeHandler` | **confirmado**: existe (API 60.0) | {fonte('MA-OTE')} |",
      f"| `ManagedEventSubscription` | **confirmado**: existe (Beta, API 60.0) | {fonte('MA-MES')} |",
      f"| External Client App com Canvas | **confirmado**: `ExtlClntAppCanvasSettings` (API 66.0) — variante adicionada em N.2 | {fonte('MA-ECAC')} |",
      f"| Named Credential nova × legada | **confirmado**: `namedCredentialType` SecuredEndpoint × Legacy; PrivateEndpoint com OutboundNetworkConnection | {fonte('MA-NC')} |",
      f"| Seleção de objetos do CDC | **confirmado**: `PlatformEventChannelMember` no canal ChangeEvents ou customizado | {fonte('CDC-SEL')} |",
      f"| Retry de trigger de evento | **confirmado**: até 10 execuções (1 + 9) com `EventBus.RetryableException` | {fonte('PE-RETRY')} |",
      f"| OmniStudio padrão como metadata | **não confirmado**: os tipos não estão na lista de Metadata Types (API 68.0) | {fonte('MA-TYPES')} |",
      f"| Outbound Message como ação de Flow | **não confirmado**: o valor não aparece em `actionType` | {fonte('MA-FLOW')} |",
      "| Callout em Platform Event–Triggered Flow e em Schedule-Triggered Flow | **não confirmado** nas páginas consultadas | — |",
      "| Data Cloud | **não confirmado** (não pesquisado nesta rodada) | — |"]
open(f"{out}/fontes_validacao.md", "w").write("\n".join(L) + "\n")

# ---------- JSON ----------
cols = ["componente", "metadata_type", "relacao", "papel", "acionado_por", "aciona", "obrigatoriedade"]
data = []
for slug, titulo, ds in SECOES:
    for d in ds:
        data.append({"secao": slug, "id": d["id"], "titulo": d["titulo"], "resumo": d["resumo"], "observacoes": d["obs"], "a_validar": d["validar"],
                     "variantes": [{"id": f"{d['id']}.v{i}", "nome": n, "componentes": [dict(ordem=k, **dict(zip(cols, r)), como_achar=evid(r[0], r[1])) for k, r in enumerate(rows, 1)]}
                                   for i, (n, rows) in enumerate(d["variantes"], 1)]})
json.dump({"eixos_endpoint": ENDPOINTS, "fluxos_oauth": FLOWS, "desenhos": data}, open(f"{out}/desenhos.json", "w"), ensure_ascii=False, indent=1)
json.dump({"fontes": FONTES,
           "tipos": {t: dict(zip(["pasta", "sufixo", "desde_api", "procurar_no_xml", "campos_sensiveis", "fonte"], v)) for t, v in TIPOS.items()},
           "nao_confirmados": NAO_CONFIRMADOS,
           "codigo": [dict(zip(["id", "procure", "significa", "fonte"], c)) for c in CODIGO],
           "ligacoes": [dict(zip(["id", "de", "para", "como_seguir", "tipo", "fonte"], l)) for l in LIGACOES]},
          open(f"{out}/evidencias_e_ligacoes.json", "w"), ensure_ascii=False, indent=1)
for k, v in total.items(): print(k, v)
print("TOTAL", sum(total.values()))

import sys, os, json
from designs import SECOES
from blocks import ENDPOINTS, FLOWS
from evidencias import FONTES, TIPOS, CODIGO, NAO_CONFIRMADOS, evid
from ligacoes import LIGACOES
from diagnostico import SINAIS
from limites import LIMITES
from antipadroes import ANTIPADROES
from limites_plataforma import LIMITES_PLATAFORMA
from glossario import GLOSSARIO
import re as _re

def tipos_de(mt):
    return [p.strip().split(' ')[0] for p in _re.split(r',| ou |/|\+', mt) if p.strip()]

def rss_info(rows):
    tipos = [t for r in rows for t in tipos_de(r[1])]
    if 'RemoteSiteSetting' in tipos:
        return 'Sim, obrigatório', 'a URL não vem de uma Named Credential, então o domínio precisa estar liberado'
    if 'NamedCredential' in tipos:
        return 'Não', 'a Named Credential já autoriza o domínio [AX-RSS]'
    if 'CspTrustedSite' in tipos:
        return 'Não', 'a chamada sai do navegador; quem libera é o CSP Trusted Site'
    if 'ExternalDataSource' in tipos:
        return 'Não', 'o Salesforce Connect usa a External Data Source'
    return 'Não se aplica', 'não há chamada de saída feita por Apex nesta variante'
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
def esc(s): return str(s).replace("|", "\\|")
def fonte(ids):
    return ", ".join(f"[{i.strip()}]({FONTES[i.strip()]})" if i.strip() in FONTES else i for i in ids.split(","))
AVISO = "> Gerado a partir de `_fonte/`. Não edite este arquivo: altere as definições e rode `python3 _fonte/render.py .` nesta pasta."

# ---------- desenhos (um arquivo por seção) ----------
total = {}
for slug, titulo, ds in SECOES:
    L = [f"# {titulo}", "", AVISO, "", "Convenções, legenda e códigos de variante: [README](README.md). Fontes citadas entre colchetes: [fontes_validacao.md](fontes_validacao.md).", "",
         "## Como ler", "",
         "- Cada **desenho** (ex.: b.1) começa com um **mapa das variantes**: de onde vem o endereço do sistema externo e se a variante precisa de **Remote Site Setting**.",
         "- **Remote Site Setting só é necessário quando o Apex chama uma URL que não vem de uma Named Credential** (URL fixa no código, em Custom Metadata, Custom Setting ou Custom Label). Com Named Credential (E1, E2, E5), não é preciso [AX-RSS].",
         "- Na tabela de cada variante, a coluna **O que faz nesta integração** explica o papel de cada peça; o glossário abaixo diz o que é cada metadata type.", "",
         "## O que é cada metadata type", "", "| Metadata type | O que é |", "|---|---|"]
    usados = sorted({t for d in ds for _, rows in d["variantes"] for r in rows for t in tipos_de(r[1]) if t in GLOSSARIO})
    L += [f"| `{t}` | {GLOSSARIO[t]} |" for t in usados]
    L += ["", "## Índice", ""]
    for d in ds:
        L.append(f"- [{d['id']} — {d['titulo']}](#{d['id'].lower().replace('.', '')}) ({len(d['variantes'])} variantes)")
    for d in ds:
        L += ["", f"## {d['id']}", "", f"**{d['titulo']}**", "", d["resumo"], ""]
        for o in d["obs"]: L.append(f"> Observação: {o}")
        for v in d["validar"]: L.append(f"> ⚠️ A validar: {v}")
        if d["obs"] or d["validar"]: L.append("")
        L += ["**Mapa das variantes**", "", "| Variante | Resumo | Usa Remote Site Setting? | Por quê |", "|---|---|---|---|"]
        for i, (nome, rows) in enumerate(d["variantes"], 1):
            usa, pq = rss_info(rows)
            L.append(f"| [{d['id']}.v{i}](#{(d['id']+'v'+str(i)).lower().replace('.', '')}) | {esc(nome)} | {usa} | {pq} |")
        L.append("")
        for i, (nome, rows) in enumerate(d["variantes"], 1):
            fluxo = " → ".join(r[0] for r in rows if r[2] in ("executa", "ator", "executa (DML)") and r[6].startswith("Obrig"))
            usa, pq = rss_info(rows)
            L += [f"<a id=\"{(d['id']+'v'+str(i)).lower().replace('.', '')}\"></a>", "", f"### {d['id']}.v{i} — {nome}", "", f"Fluxo principal: {fluxo}", "", f"Remote Site Setting: **{usa}** — {pq}.", "",
                  "| Ordem | Componente | Metadata type | Relação | O que faz nesta integração | Acionado por | Aciona | Obrigatoriedade | Como achar no projeto |",
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
      f"| Continuation | **confirmado**: 3 paralelos, 3 encadeados, 120 s; em LWC o método usa `@AuraEnabled(continuation=true)` | {fonte('AX-CONT')}, {fonte('AX-CONTL')}, {fonte('LWC-CONT')} |",
      f"| LWC chamando Apex | **confirmado**: `import x from '@salesforce/apex/[namespace.]Classe.metodo'` | {fonte('LWC-IMP')} |",
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
      "| Callout em Platform Event–Triggered Flow e em Schedule-Triggered Flow | **não confirmado**: a fonte é o help.salesforce.com, que não abre neste ambiente (depende de a.sfdcstatic.com, bloqueado) | — |",
      "| Data Cloud | **não confirmado** (não pesquisado nesta rodada) | — |"]
open(f"{out}/fontes_validacao.md", "w").write("\n".join(L) + "\n")

# ---------- item 3: diagnóstico ----------
L = ["# Matriz de diagnóstico", "", AVISO, "",
     "Do sinal encontrado no projeto para os desenhos candidatos. Use junto com [guia_evidencias.md](guia_evidencias.md) (códigos `Cnn`) e [regras_ligacao.md](regras_ligacao.md) (códigos `Lnn`).", "",
     "**Confiança** (critério desta base, não da Salesforce): **alta** = evidência direta e documentada; **média** = combinação de sinais ou heurística; **baixa** = presumido.",
     "Nunca promova um candidato a fato sem a evidência da coluna \"O que confirmar\".", "",
     "## 1. Sinais", "",
     "| ID | Sinal no projeto | Evidência | Direção · mecanismo | Desenhos candidatos | Confiança | O que confirmar |", "|---|---|---|---|---|---|---|"]
for r in SINAIS:
    L.append("| " + " | ".join(esc(x) for x in r) + " |")
L += ["", "## 2. Assinatura mínima por desenho", "",
      "Metadata types obrigatórios em **todas** as variantes do desenho (atores excluídos). Se algum faltar no projeto, o desenho fica improvável; o que varia entre variantes está nos arquivos de cada seção.", "",
      "| Desenho | Título | Assinatura mínima | Variantes |", "|---|---|---|---|"]
for slug, titulo, ds in SECOES:
    for d in ds:
        sets = [set(r[1] for r in rows if r[2] != "ator" and r[6].startswith("Obrig")) for _, rows in d["variantes"]]
        comum = sorted(set.intersection(*sets)) if sets else []
        L.append(f"| {d['id']} | {esc(d['titulo'])} | {esc(', '.join(f'`{t}`' for t in comum) or '—')} | {len(d['variantes'])} |")
L += ["", "## 3. Como usar", "",
      "1. Liste os sinais encontrados (seção 1) com a evidência `arquivo:linha`.",
      "2. Para cada candidato, confira a assinatura mínima (seção 2).",
      "3. Escolha a variante comparando a tabela da variante com os componentes achados (coluna \"Como achar no projeto\").",
      "4. Registre a confiança e o que ficou sem confirmação, usando [limites_da_fonte.md](limites_da_fonte.md) para o que o repositório não pode mostrar."]
open(f"{out}/diagnostico.md", "w").write("\n".join(L) + "\n")

# ---------- item 4: limites da fonte ----------
L = ["# O que o repositório não mostra", "", AVISO, "",
     "Informações que um agente **não** consegue tirar do projeto (cópia do repositório, sem acesso à org). Nesses casos, registre \"Não informado\" ou \"presumido\"; nunca deduza o valor.", "",
     "| ID | Informação | Por quê / onde fica | Efeito na documentação | Fonte |", "|---|---|---|---|---|"]
for i, info, porque, efeito, f in LIMITES:
    L.append(f"| {i} | {esc(info)} | {esc(porque)} | {esc(efeito)} | {fonte(f) if f not in ('nv', '—') else f} |")
open(f"{out}/limites_da_fonte.md", "w").write("\n".join(L) + "\n")

# ---------- item 5: anti-padrões ----------
def fo(f): return fonte(f) if f not in ("heurística", "nv", "—") else f
L = ["# Anti-padrões e riscos", "", AVISO, "",
     "O que a documentação de uma integração deve sinalizar como risco. Recomendações do Salesforce Well-Architected e dos guias oficiais (consultados em 2026-10-30); citações entre aspas são literais.",
     "Ao documentar: registre o anti-padrão na seção de pontos em aberto, com a evidência `arquivo:linha`, sem copiar valores sensíveis.", "",
     "| ID | Anti-padrão | Como detectar no projeto | Risco | Recomendação | Fonte |", "|---|---|---|---|---|---|"]
for a in ANTIPADROES:
    L.append("| " + " | ".join(esc(x) for x in a[:5]) + f" | {fo(a[5])} |")
open(f"{out}/antipadroes.md", "w").write("\n".join(L) + "\n")

# ---------- item 6: limites da plataforma ----------
L = ["# Limites da plataforma para integração", "", AVISO, "",
     "Valores consultados em 2026-10-30 (Winter '27, API 68.0). **Os números mudam entre releases e por edição/licença:** confira a fonte antes de usar em decisão e cite a data na documentação.", "",
     "| Área | Limite | Valor | Desenhos afetados | Fonte |", "|---|---|---|---|---|"]
for l in LIMITES_PLATAFORMA:
    L.append("| " + " | ".join(esc(x) for x in l[:4]) + f" | {fo(l[4])} |")
open(f"{out}/limites_plataforma.md", "w").write("\n".join(L) + "\n")

# ---------- JSON ----------
cols = ["componente", "metadata_type", "relacao", "papel", "acionado_por", "aciona", "obrigatoriedade"]
data = []
for slug, titulo, ds in SECOES:
    for d in ds:
        data.append({"secao": slug, "id": d["id"], "titulo": d["titulo"], "resumo": d["resumo"], "observacoes": d["obs"], "a_validar": d["validar"],
                     "variantes": [{"id": f"{d['id']}.v{i}", "nome": n, "usa_remote_site_setting": rss_info(rows)[0], "remote_site_motivo": rss_info(rows)[1], "componentes": [dict(ordem=k, **dict(zip(cols, r)), como_achar=evid(r[0], r[1])) for k, r in enumerate(rows, 1)]}
                                   for i, (n, rows) in enumerate(d["variantes"], 1)]})
json.dump({"eixos_endpoint": ENDPOINTS, "fluxos_oauth": FLOWS, "desenhos": data}, open(f"{out}/desenhos.json", "w"), ensure_ascii=False, indent=1)
json.dump({"fontes": FONTES,
           "tipos": {t: dict(zip(["pasta", "sufixo", "desde_api", "procurar_no_xml", "campos_sensiveis", "fonte"], v)) for t, v in TIPOS.items()},
           "nao_confirmados": NAO_CONFIRMADOS,
           "codigo": [dict(zip(["id", "procure", "significa", "fonte"], c)) for c in CODIGO],
           "ligacoes": [dict(zip(["id", "de", "para", "como_seguir", "tipo", "fonte"], l)) for l in LIGACOES]},
          open(f"{out}/evidencias_e_ligacoes.json", "w"), ensure_ascii=False, indent=1)
json.dump({"sinais": [dict(zip(["id", "sinal", "evidencia", "direcao_mecanismo", "desenhos_candidatos", "confianca", "confirmar"], r)) for r in SINAIS],
           "limites": [dict(zip(["id", "informacao", "por_que", "efeito", "fonte"], r)) for r in LIMITES]},
          open(f"{out}/diagnostico_e_limites.json", "w"), ensure_ascii=False, indent=1)
json.dump({"antipadroes": [dict(zip(["id", "antipadrao", "como_detectar", "risco", "recomendacao", "fonte"], a)) for a in ANTIPADROES],
           "limites_plataforma": [dict(zip(["area", "limite", "valor", "desenhos", "fonte"], l)) for l in LIMITES_PLATAFORMA],
           "consultado_em": "2026-10-30"},
          open(f"{out}/riscos_e_limites_plataforma.json", "w"), ensure_ascii=False, indent=1)
for k, v in total.items(): print(k, v)
print("TOTAL", sum(total.values()))

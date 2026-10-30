from blocks import *

def D(id, titulo, resumo, variantes, obs=None, validar=None):
    return dict(id=id, titulo=titulo, resumo=resumo, variantes=variantes, obs=obs or [], validar=validar or [])

USER = ator("Usuário", "inicia a ação na tela", "—", "página")

def origem_ui(kind):
    """Linhas de entrada para desenhos iniciados por usuário."""
    if kind == "LWC":
        return [USER,
         R("Página Lightning", "FlexiPage", "lê/referencia", "posiciona o componente na página de registro, app ou home", "Usuário", "LWC", "Opcional (ou CustomTab / QuickAction)"),
         R("Componente LWC", "LightningComponentBundle", "executa", "captura a ação e chama o Apex via `@AuraEnabled` (imperativo ou wire)", "Página Lightning", "Controller Apex"),
         R("Controller Apex", "ApexClass", "executa", "método `@AuraEnabled`: ponto de entrada no servidor", "Componente LWC", "próximo componente")], "Controller Apex"
    if kind == "FLOW":
        return [USER,
         R("Ponto de entrada", "FlexiPage, QuickAction ou CustomTab", "lê/referencia", "onde o Screen Flow é exposto ao usuário", "Usuário", "Screen Flow", "Opcional"),
         R("Screen Flow", "Flow", "executa", "coleta dados na tela e chama a ação Apex", "Ponto de entrada", "Classe invocável"),
         R("Versão ativa do Flow", "FlowDefinition", "lê/referencia", "indica a versão ativa (formato legado)", "plataforma", "—", "Opcional"),
         R("Classe invocável", "ApexClass", "executa", "método `@InvocableMethod`: ponto de entrada no servidor", "Screen Flow", "próximo componente")], "Classe invocável"
    raise KeyError(kind)

APEX_ACCESS = lambda por: R("Permission Set (acesso às classes Apex)", "PermissionSet", "autoriza", "libera ao usuário as classes Apex chamadas pela UI", "plataforma", "—")
ORIG_NOME = {"LWC": "LWC", "FLOW": "Screen Flow"}

def ui_callout(cadeia):
    var = []
    for o in ("LWC", "FLOW"):
        for e in ALL_E:
            rows, entry = origem_ui(o)
            rows = list(rows)
            caller = entry
            if cadeia:
                rows += [R("Classe de serviço", "ApexClass", "executa", "regra de negócio e montagem do payload", entry, "Classe cliente HTTP"),
                         R("Classe cliente HTTP", "ApexClass", "executa", "monta `HttpRequest`, faz o callout e trata a resposta", "Classe de serviço", "Sistema externo"),
                         R("Classes de DTO / wrapper", "ApexClass", "lê/referencia", "serializa e desserializa JSON", "Classe cliente HTTP", "—", "Opcional")]
                caller = "Classe cliente HTTP"
            else:
                rows[-1] = rows[-1][:3] + (rows[-1][3] + " e faz o callout (`HttpRequest`)",) + rows[-1][4:5] + ("Sistema externo",) + rows[-1][6:]
            rows += endpoint(e, caller)
            rows += [APEX_ACCESS(None)] + killswitch(caller) + logrows(caller)
            var.append((f"Origem {ORIG_NOME[o]} · endpoint {e} ({ENDPOINTS[e]})", rows))
    return var

def flow_http(origem="Screen Flow", trig="FLOW"):
    var = []
    for e in NC_E:
        rows, _ = origem_ui("FLOW") if trig == "FLOW" else (None, None)
        rows = list(rows[:3]) if rows else []
        rows += [R("Ação HTTP Callout", "ExternalServiceRegistration", "lê/referencia", "registro gerado pelo assistente de HTTP Callout (método, path, schema de resposta)", "Screen Flow", "Named Credential"),]
        rows += endpoint(e, "Ação HTTP Callout")
        rows += [R("Permission Set (acesso ao Flow)", "PermissionSet", "autoriza", "Run Flows ou acesso ao Flow específico", "plataforma", "—")]
        var.append((f"Endpoint {e} ({ENDPOINTS[e]})", rows))
    return var

def ext_service():
    var = []
    for o in ("FLOW", "APEX"):
        for e in NC_E:
            if o == "FLOW":
                rows, _ = origem_ui("FLOW"); rows = list(rows[:3]); caller = "Screen Flow"
            else:
                rows, _ = origem_ui("LWC"); rows = list(rows); caller = "Controller Apex"
                rows[-1] = rows[-1][:3] + ("chama a classe gerada no namespace `ExternalService`",) + rows[-1][4:5] + ("Registro de External Service",) + rows[-1][6:]
            rows += [R("Registro de External Service", "ExternalServiceRegistration", "lê/referencia", "schema OpenAPI registrado; gera ações invocáveis e classes Apex", caller, "Named Credential")]
            rows += endpoint(e, "Registro de External Service")
            var.append((f"Origem {'Screen Flow' if o=='FLOW' else 'LWC + Apex'} · endpoint {e}", rows))
    return var

def wsdl():
    var = []
    for o in ("LWC", "FLOW"):
        for e in ALL_E:
            rows, entry = origem_ui(o); rows = list(rows)
            rows += [R("Stub gerado (WSDL2Apex)", "ApexClass", "executa", "classe gerada a partir do WSDL; serializa SOAP e faz `WebServiceCallout.invoke`. O `endpoint_x` pode ser sobrescrito", entry, "Sistema externo")]
            rows += endpoint(e, "Stub gerado (WSDL2Apex)")
            rows += [APEX_ACCESS(None)]
            var.append((f"Origem {ORIG_NOME[o]} · endpoint {e}", rows))
    return var

def continuation():
    var = []
    for e in ALL_E:
        rows, entry = origem_ui("LWC"); rows = list(rows)
        rows[-1] = rows[-1][:3] + ("método `@AuraEnabled(continuation=true)` que devolve um `Continuation` (C25)",) + rows[-1][4:5] + ("Sistema externo",) + rows[-1][6:]
        rows += endpoint(e, "Controller Apex")
        rows += [R("Método de callback", "ApexClass", "executa", "recebe a resposta quando o sistema externo responde e devolve ao LWC", "plataforma (ao chegar a resposta)", "Componente LWC")]
        var.append((f"Endpoint {e}", rows))
    return var

def omni_flexcard(com_dm):
    var = []
    for e in ("E1", "E2", "E3"):
        rows = [USER,
          R("Página Lightning", "FlexiPage", "lê/referencia", "exibe a FlexCard", "Usuário", "FlexCard", "Opcional"),
          R("FlexCard", "OmniUiCard", "executa", "fonte de dados do tipo Integration Procedure", "Página Lightning", "Integration Procedure"),
          R("Integration Procedure", "OmniIntegrationProcedure", "executa", "orquestra; o elemento HTTP Action faz a chamada", "FlexCard", "Sistema externo")]
        if com_dm:
            rows.append(R("Data Mapper / DataRaptor Transform", "OmniDataTransform", "executa", "transforma a resposta externa no formato da FlexCard", "Integration Procedure", "—"))
        if e in ("E1", "E2"):
            rows += endpoint(e, "Integration Procedure")
        else:
            rows += [R("Remote Site Setting", "RemoteSiteSetting", "autoriza", "libera a URL fixa configurada na HTTP Action", "plataforma", "—"), ator(EXT, "responde", "Integration Procedure", "—")]
        var.append((f"{'Com' if com_dm else 'Sem'} Data Mapper · endpoint {'E3 (URL fixa na HTTP Action + Remote Site)' if e=='E3' else e}", rows))
    return var

def omniscript():
    var = []
    for via in ("IP", "RA"):
        for e in (("E1", "E2", "E3") if via == "IP" else ALL_E):
            rows = [USER,
              R("Página Lightning / Experience", "FlexiPage", "lê/referencia", "exibe o OmniScript", "Usuário", "OmniScript", "Opcional"),
              R("OmniScript", "OmniScript", "executa", "guia o usuário; chama a etapa de integração", "Página", "Integration Procedure" if via == "IP" else "Classe Remote Action")]
            if via == "IP":
                rows.append(R("Integration Procedure", "OmniIntegrationProcedure", "executa", "HTTP Action faz a chamada", "OmniScript", "Sistema externo"))
                if e == "E3":
                    rows += [R("Remote Site Setting", "RemoteSiteSetting", "autoriza", "libera a URL fixa", "plataforma", "—"), ator(EXT, "responde", "Integration Procedure", "—")]
                else:
                    rows += endpoint(e, "Integration Procedure")
            else:
                rows.append(R("Classe Remote Action", "ApexClass", "executa", "implementa `Callable` (ou a interface do pacote); faz o callout", "OmniScript", "Sistema externo"))
                rows += endpoint(e, "Classe Remote Action") + [APEX_ACCESS(None)]
            var.append((f"Via {'Integration Procedure' if via=='IP' else 'Remote Action (Apex)'} · endpoint {e}", rows))
    return var

def browser_fetch():
    var = []
    for src in ("JS", "LABEL", "CMDT"):
        rows = [USER, R("Componente LWC", "LightningComponentBundle", "executa", "chama a API externa com `fetch()` direto do navegador", "Página", "Sistema externo")]
        if src == "LABEL":
            rows.append(R("Custom Label", "CustomLabels", "lê/referencia", "URL importada via `@salesforce/label`", "Componente LWC", "—"))
        if src == "CMDT":
            rows += [R("Controller Apex", "ApexClass", "executa", "devolve ao LWC a URL lida do CMDT", "Componente LWC", "Registro de Custom Metadata"),
                     R("Registro de Custom Metadata", "CustomMetadata (+ CustomObject __mdt)", "lê/referencia", "URL por ambiente", "Controller Apex", "—")]
        rows += [R("CSP Trusted Site", "CspTrustedSite", "autoriza", "libera o domínio em `connect-src` no navegador", "navegador", "—"),
                 ator(EXT, "responde; precisa liberar CORS para o domínio Lightning", "Componente LWC", "—")]
        var.append(({"JS": "URL no JavaScript", "LABEL": "URL em Custom Label", "CMDT": "URL em Custom Metadata via Apex"}[src], rows))
    return var

def sf_connect(adapter):
    var = []
    codes = ALL_E if adapter else ("PROPRIA", "NC")
    for e in codes:
        rows = [USER,
          R("Layout / Página / Aba", "Layout, FlexiPage ou CustomTab", "lê/referencia", "exibe os registros externos", "Usuário", "External Object"),
          R("External Object", "CustomObject (__x)", "lê/referencia", "representa a tabela externa; cada leitura gera consulta remota", "Página", "External Data Source"),
          R("Campos e relacionamentos externos", "CustomField", "lê/referencia", "colunas; External Lookup / Indirect Lookup ligam a objetos do Salesforce", "External Object", "—"),
          R("External Data Source", "ExternalDataSource", "lê/referencia", "tipo OData 2.0/4.0, cross-org ou Apex; URL e modo de identidade", "External Object", "adaptador" if adapter else "Sistema externo"),
          R("Permission Set", "PermissionSet", "autoriza", "acesso ao External Object e à External Data Source (identidade por usuário)", "plataforma", "—")]
        if adapter:
            rows += [R("Provider do adaptador", "ApexClass", "executa", "estende `DataSource.Provider`: declara capacidades e autenticação", "External Data Source", "Connection"),
                     R("Connection do adaptador", "ApexClass", "executa", "estende `DataSource.Connection`: `sync`, `query`, `search`; faz o callout", "Provider", "Sistema externo")]
            rows += endpoint(e, "Connection do adaptador")
            label = f"Adaptador Apex · endpoint {e}"
        elif e == "NC":
            rows += endpoint("E1", "External Data Source"); label = "Autenticação via Named Credential"
        else:
            rows += [ator(EXT, "serviço OData; responde às consultas", "External Data Source", "—")]; label = "Autenticação na própria External Data Source"
        var.append((label, rows))
    return var

def quick_action():
    var = []
    for o in ("FLOW", "LWC"):
        for e in ALL_E:
            rows = [USER, R("Quick Action", "QuickAction", "executa", "botão na página do registro; tipo Flow ou LWC", "Usuário", "Screen Flow" if o == "FLOW" else "Componente LWC"),
                    R("Layout / Página (onde a ação aparece)", "Layout ou FlexiPage", "lê/referencia", "expõe a ação", "plataforma", "—")]
            if o == "FLOW":
                rows += [R("Screen Flow", "Flow", "executa", "recebe `recordId`, chama o Apex e grava o retorno", "Quick Action", "Classe invocável"),
                         R("Classe invocável", "ApexClass", "executa", "faz o callout", "Screen Flow", "Sistema externo")]
                c = "Classe invocável"
            else:
                rows += [R("Componente LWC (screen ou headless action)", "LightningComponentBundle", "executa", "recebe `recordId` e chama o Apex", "Quick Action", "Controller Apex"),
                         R("Controller Apex", "ApexClass", "executa", "faz o callout", "Componente LWC", "Sistema externo")]
                c = "Controller Apex"
            rows += endpoint(e, c)
            rows += [R("Objeto do registro", "CustomObject + CustomField", "executa (DML)", "recebe os dados de enriquecimento", c, "triggers/flows do objeto"), APEX_ACCESS(None)]
            var.append((f"Quick Action → {ORIG_NOME[o]} · endpoint {e}", rows))
    return var

OUT_SYNC = [
 D("b.1", "LWC / Screen Flow → cadeia de classes → callout", "O usuário aciona a tela; o servidor passa por service e client antes do callout. O usuário espera a resposta.", ui_callout(True)),
 D("b.2", "LWC / Screen Flow → uma classe que faz o callout", "Mesmo desenho do b.1, mas o próprio ponto de entrada faz a chamada.", ui_callout(False)),
 D("b.3", "Screen Flow → ação HTTP Callout (declarativa)", "Sem Apex. O assistente de HTTP Callout gera um registro de External Service.", flow_http(), obs=["HTTP Callout exige Named Credential: as variantes E3–E6 não existem para este desenho.", "No XML, o registro gerado pelo HTTP Callout tem `registrationProviderType`=SchemaInferred (API 57.0+) [MA-ESR]."]),
 D("b.4", "Flow ou Apex → External Service (OpenAPI)", "A API é registrada por um schema OpenAPI; Flow e Apex usam as ações geradas.", ext_service(), obs=["External Services exigem Named Credential."]),
 D("b.5", "LWC / Screen Flow → stub SOAP gerado (WSDL2Apex)", "Callout SOAP com classes geradas a partir do WSDL.", wsdl()),
 D("b.6", "LWC → Apex Continuation", "Chamada longa (até 120 s) sem prender thread do servidor.", continuation(), obs=["Confirmado [AX-CONTL]: até 3 callouts paralelos, 3 encadeados, timeout máximo de 120 s por continuation.", "Confirmado [LWC-CONT]: o método é anotado com `@AuraEnabled(continuation=true)` (pode ter `cacheable=true`); o LWC processa uma Continuation por vez [LWC-CONTL]."]),
 D("c.1", "FlexCard → Integration Procedure → HTTP Action", "Exibição de dado externo via OmniStudio.", omni_flexcard(False) + omni_flexcard(True), validar=["`OmniUiCard`, `OmniIntegrationProcedure`, `OmniDataTransform` e `OmniScript` não constam na lista de Metadata Types do Metadata API Developer Guide (API 68.0) [MA-TYPES]. Confirmar na documentação do OmniStudio. No pacote gerenciado (Vlocity) esses itens são registros/DataPacks."]),
 D("c.2", "OmniScript → Integration Procedure ou Remote Action", "Processo guiado com etapa de integração.", omniscript(), validar=["Mesmos pontos do c.1; interface da Remote Action depende do runtime (padrão ou pacote)."]),
 D("d.1", "LWC → fetch direto do navegador", "Sem servidor Salesforce no meio. Só para APIs públicas ou com token do próprio usuário.", browser_fetch(), obs=["Não usa Named Credential nem Remote Site Setting: quem autoriza é a CSP (`CspTrustedSite`) e o CORS do sistema externo."]),
 D("e.1", "Salesforce Connect (OData / cross-org)", "Virtualização: dado externo lido sob demanda, sem cópia.", sf_connect(False)),
 D("e.2", "Salesforce Connect com adaptador Apex", "Virtualização de APIs que não são OData.", sf_connect(True)),
 D("f.1", "Quick Action → Flow ou LWC → callout → atualiza o registro", "Enriquecimento sob demanda, iniciado pelo usuário.", quick_action()),
]

# =========================== IN SYNC ===========================
def ext_start(api):
    return [ator(EXT, f"obtém o token e chama a {api}", "—", "Connected App / External Client App")]

def dados_destino(caller, upsert=True):
    rows = [R("Objeto de destino", "CustomObject (padrão ou __c)", "executa (DML)", "recebe a criação/alteração/consulta", caller, "triggers e flows do objeto"),
            R("Campos", "CustomField", "lê/referencia", "campos gravados ou lidos", caller, "—")]
    if upsert:
        rows.append(R("Campo External ID", "CustomField (externalId=true)", "lê/referencia", "chave de correlação para upsert entre sistemas", caller, "—", "Opcional (obrigatório em upsert)"))
    rows += [R("Trigger do objeto", "ApexTrigger", "executa", "efeitos colaterais da gravação", "plataforma (DML)", "classes handler", "Opcional"),
             R("Flow record-triggered", "Flow", "executa", "efeitos colaterais declarativos", "plataforma (DML)", "—", "Opcional")]
    return rows

def in_api(api, extra_fn, upsert=True):
    var = []
    for a, f in in_variants():
        rows = ext_start(api) + app_in(a, f)
        rows += [ator(api, "endpoint padrão da plataforma", EXT, extra_fn[0] if extra_fn else "Objeto de destino")]
        if extra_fn:
            rows += extra_fn[1]
        else:
            rows += dados_destino(api, upsert)
        var.append((f"{APPS[a]} · {FLOWS[f]}", rows))
    return var

APEX_REST = ("Classe Apex REST", [
  R("Classe Apex REST", "ApexClass", "executa", "`@RestResource(urlMapping=...)` com `@HttpPost/@HttpGet...`: valida payload e aplica regra de negócio", "Apex REST (/services/apexrest)", "Objeto de destino"),
  R("Classes de serviço / DTO", "ApexClass", "executa", "regra de negócio, desserialização", "Classe Apex REST", "Objeto de destino", "Opcional"),
  R("Permission Set (acesso à classe)", "PermissionSet", "autoriza", "libera a classe Apex REST ao usuário de integração", "plataforma", "—")] + dados_destino("Classe Apex REST"))
APEX_SOAP = ("Classe Apex SOAP", [
  R("Classe Apex SOAP", "ApexClass", "executa", "`global` com métodos `webservice`; WSDL gerado pela plataforma", "SOAP API customizada (/services/Soap/class)", "Objeto de destino"),
  R("Permission Set (acesso à classe)", "PermissionSet", "autoriza", "libera a classe", "plataforma", "—")] + dados_destino("Classe Apex SOAP"))
FLOW_REST = ("Flow autolaunched", [
  R("Flow autolaunched", "Flow", "executa", "invocado por `/actions/custom/flow/<Nome>`; recebe variáveis de entrada", "REST API (Actions)", "Objeto de destino"),
  R("Permission Set (Run Flows / acesso ao Flow)", "PermissionSet", "autoriza", "libera a execução do Flow", "plataforma", "—")] + dados_destino("Flow autolaunched"))

def webhook():
    var = []
    for site in ("SITE", "EXP"):
        for val in ("NENHUMA", "CMDT", "CS"):
            rows = [ator(EXT, "envia o webhook (POST) sem OAuth", "—", "Site")]
            if site == "SITE":
                rows += [R("Site público", "CustomSite", "lê/referencia", "domínio público que expõe `/services/apexrest`", EXT, "Classe Apex REST")]
            else:
                rows += [R("Site Experience Cloud", "Network + ExperienceBundle/DigitalExperienceBundle + CustomSite", "lê/referencia", "site do Experience com acesso guest", EXT, "Classe Apex REST")]
            rows += [R("Perfil guest do site", "Profile", "autoriza", "acesso da classe e dos objetos para o usuário guest", "plataforma", "—"),
                     R("Classe Apex REST", "ApexClass", "executa", "recebe o webhook, valida, grava ou enfileira", "Site", "Objeto de destino")]
            if val == "CMDT":
                rows += [R("Registro de Custom Metadata (protegido)", "CustomMetadata (+ CustomObject __mdt)", "lê/referencia", "segredo/token para validar assinatura HMAC. Risco: ver README", "Classe Apex REST", "—")]
            if val == "CS":
                rows += [R("Custom Setting protegido", "CustomObject (Custom Setting)", "lê/referencia", "segredo para validar assinatura", "Classe Apex REST", "—")]
            rows += dados_destino("Classe Apex REST")
            var.append((f"{'Site público' if site=='SITE' else 'Experience Cloud'} · validação {'nenhuma (não recomendado)' if val=='NENHUMA' else ('segredo em Custom Metadata' if val=='CMDT' else 'segredo em Custom Setting')}", rows))
    return var

IN_SYNC = [
 D("g.1", "Sistema externo → REST/SOAP API padrão (CRUD)", "Sem código na org; o sistema externo grava ou lê objetos diretamente.", in_api("REST/SOAP API padrão", None)),
 D("g.2", "Sistema externo → Composite / sObject Tree / Collections", "Várias operações em uma chamada.", in_api("Composite API", None)),
 D("g.3", "Sistema externo → Apex REST customizado", "Endpoint próprio com regra de negócio.", in_api("Apex REST (/services/apexrest)", APEX_REST)),
 D("g.4", "Sistema externo → Apex SOAP customizado", "Equivalente SOAP com WSDL gerado.", in_api("SOAP API customizada (/services/Soap/class)", APEX_SOAP)),
 D("g.5", "Sistema externo → Flow via REST (Actions)", "Dispara um autolaunched Flow.", in_api("REST API (Actions)", FLOW_REST)),
 D("g.6", "Webhook público → Site → Apex REST", "Sem OAuth: a confiança vem de assinatura/token no payload.", webhook(), obs=["Usuário guest tem restrições de compartilhamento e de acesso; avalie o risco antes de usar."]),
 D("g.7", "Sistema externo → GraphQL API", "Consultas de leitura flexíveis.", in_api("GraphQL API", None, upsert=False), validar=["Escopo atual de mutations na GraphQL API do Salesforce."]),
]

# =========================== OUT ASYNC ===========================
def gatilho_trigger():
    return [ator("Gravação do registro", "insert/update/delete por usuário, API ou automação", "—", "Trigger"),
            R("Objeto de origem", "CustomObject + CustomField", "lê/referencia", "registro que dispara a integração", "—", "Trigger"),
            R("Trigger", "ApexTrigger", "executa", "detecta a mudança (após commit lógico) e delega", "plataforma (DML)", "Classe handler"),
            R("Classe handler", "ApexClass", "executa", "filtra registros elegíveis e enfileira o processamento assíncrono", "Trigger", "processamento assíncrono")]

def async_apex(mech, caller):
    if mech == "FUTURE":
        return [R("Método @future", "ApexClass", "executa", "`@future(callout=true)`: recebe IDs, consulta e faz o callout fora da transação", caller, "Sistema externo")], "Método @future"
    return [R("Classe Queueable", "ApexClass", "executa", "implementa `Queueable, Database.AllowsCallouts`; faz o callout", caller, "Sistema externo"),
            R("Finalizer", "ApexClass", "executa", "implementa `System.Finalizer`: trata falha e reenfileira", "plataforma (fim do Queueable)", "Classe Queueable", "Opcional")], "Classe Queueable"

WRITEBACK = lambda c: R("Atualização do registro de origem", "CustomObject + CustomField", "executa (DML)", "grava o retorno (enriquecimento, ID externo, status). Exige proteção contra recursão do trigger", c, "Trigger (de novo)", "Opcional")

def trig_async():
    var = []
    for m in ("FUTURE", "QUEUE"):
        for e in ALL_E:
            rows = gatilho_trigger()
            a, c = async_apex(m, "Classe handler")
            rows += a + endpoint(e, c) + [WRITEBACK(c)] + killswitch("Classe handler") + logrows(c)
            var.append((f"{'@future' if m=='FUTURE' else 'Queueable'} · endpoint {e}", rows))
    return var

def flow_rt_start():
    return [ator("Gravação do registro", "insert/update", "—", "Flow"),
            R("Objeto de origem", "CustomObject + CustomField", "lê/referencia", "registro que dispara", "—", "Flow"),
            R("Flow record-triggered (Run Asynchronously)", "Flow", "executa", "o caminho assíncrono roda após o commit e permite callout", "plataforma (DML)", "ação")]

def flow_async():
    var = []
    for acao in ("HTTP", "ES", "APEX"):
        for e in (NC_E if acao != "APEX" else ALL_E):
            rows = flow_rt_start()
            if acao == "APEX":
                rows += [R("Classe invocável", "ApexClass", "executa", "`@InvocableMethod` que faz o callout", "Flow", "Sistema externo")]
                c = "Classe invocável"
            else:
                rows += [R("Ação HTTP Callout" if acao == "HTTP" else "Registro de External Service", "ExternalServiceRegistration", "lê/referencia", "define a operação chamada", "Flow", "Named Credential")]
                c = "Flow"
            rows += endpoint(e, c) + [WRITEBACK(c)]
            var.append((f"Ação {'HTTP Callout' if acao=='HTTP' else ('External Service' if acao=='ES' else 'Apex invocável')} · endpoint {e}", rows))
    return var

def pe_def(c="publicador"):
    return [R("Platform Event", "CustomObject (__e)", "lê/referencia", "contrato da mensagem", c, "assinantes"),
            R("Campos do evento", "CustomField", "lê/referencia", "payload", c, "—")]

def pe_callout():
    var = []
    for pub in ("TRIGGER", "FLOW"):
        for sub in ("APEX", "FLOW"):
            for e in (ALL_E if sub == "APEX" else NC_E):
                if pub == "TRIGGER":
                    rows = gatilho_trigger()[:3] + [R("Classe handler", "ApexClass", "executa", "monta e publica o evento (`EventBus.publish`)", "Trigger", "Platform Event")]
                else:
                    rows = flow_rt_start()[:2] + [R("Flow record-triggered", "Flow", "executa", "elemento Create Records no evento `__e`", "plataforma (DML)", "Platform Event")]
                rows += pe_def("publicador")
                if sub == "APEX":
                    rows += [R("Trigger do evento", "ApexTrigger", "executa", "`after insert` no `__e`; não pode fazer callout direto: enfileira", "barramento de eventos", "Classe Queueable"),
                             R("Configuração do assinante", "PlatformEventSubscriberConfig", "lê/referencia", "usuário de execução e tamanho do lote do trigger", "plataforma", "—", "Opcional")]
                    a, c = async_apex("QUEUE", "Trigger do evento")
                    rows += a + endpoint(e, c)
                else:
                    rows += [R("Flow disparado por evento", "Flow", "executa", "Platform Event–Triggered Flow; caminho assíncrono com HTTP Callout/External Service", "barramento de eventos", "Named Credential"),
                             R("Ação HTTP Callout / External Service", "ExternalServiceRegistration", "lê/referencia", "operação chamada", "Flow disparado por evento", "Named Credential")]
                    rows += endpoint(e, "Flow disparado por evento")
                rows += logrows("assinante")
                var.append((f"Publica {'Apex' if pub=='TRIGGER' else 'Flow'} · assina {'Apex Trigger + Queueable' if sub=='APEX' else 'Flow'} · endpoint {e}", rows))
    return var

def outbound_msg():
    var = []
    for origem in ("WF", "FLOW"):
        for cert in (False, True):
            rows = [ator("Gravação do registro", "insert/update", "—", "regra"),
                    R("Objeto de origem", "CustomObject + CustomField", "lê/referencia", "campos enviados na mensagem", "—", "regra")]
            if origem == "WF":
                rows += [R("Regra de workflow", "Workflow (WorkflowRule)", "executa", "critério que dispara a mensagem (legado)", "plataforma (DML)", "Outbound Message")]
            else:
                rows += [R("Flow record-triggered", "Flow", "executa", "ação Outbound Message", "plataforma (DML)", "Outbound Message")]
            rows += [R("Outbound Message", "Workflow (WorkflowOutboundMessage)", "lê/referencia", "endpoint, campos, usuário de envio; fila com retry até 24 h", "regra", "Sistema externo"),
                     ator("Usuário de envio", "usuário cujo contexto define a visibilidade dos campos", "Outbound Message", "—")]
            if cert:
                rows.append(R("Certificate", "Certificate", "autoriza", "certificado de cliente para mutual TLS", "Outbound Message", "—"))
            rows.append(ator(EXT, "listener SOAP que devolve `ack=true`", "Outbound Message", "—"))
            var.append((f"{'Workflow Rule' if origem=='WF' else 'Flow'} · {'com' if cert else 'sem'} certificado", rows))
    return var

def ext_subscriber(app):
    rows = [ator("Pub/Sub API (ou CometD)", "entrega os eventos ao assinante", "barramento", EXT),
            ator(EXT, "assinante gRPC/CometD; trata replay ID", "—", "Pub/Sub API"),
            R("Assinatura gerenciada", "ManagedEventSubscription", "lê/referencia", "`topicName`, `defaultReplay`, `state` para a RPC ManagedSubscribe (Beta, API 60.0+)", EXT, "—", "Opcional")]
    rows += app_in(app, "JWT")
    rows += [R("Permission Set (leitura do evento / do objeto)", "PermissionSet", "autoriza", "Read no `__e` ou no objeto do CDC", "plataforma", "—")]
    return rows

def pe_external():
    var = []
    for pub in ("APEX", "FLOW", "API"):
        for app in ("CA", "ECA"):
            rows = {"APEX": [R("Classe publicadora", "ApexClass", "executa", "`EventBus.publish`", "trigger/serviço", "Platform Event")],
                    "FLOW": [R("Flow publicador", "Flow", "executa", "Create Records no `__e`", "plataforma", "Platform Event")],
                    "API": [ator("Outro sistema", "publica via REST/Pub/Sub API", "—", "Platform Event")]}[pub]
            rows += pe_def() + ext_subscriber(app)
            var.append((f"Publicador {pub} · assinante autenticado por {APPS[app]}", rows))
    return var

def cdc():
    var = []
    for sub in ("EXT_CA", "EXT_ECA", "APEX"):
        for e in (["-"] if sub != "APEX" else ALL_E):
            rows = [ator("Gravação do registro", "qualquer DML", "—", "plataforma"),
                    R("Objeto monitorado", "CustomObject", "lê/referencia", "objeto cujas mudanças viram eventos", "—", "Change Event"),
                    R("Membro do canal ChangeEvents", "PlatformEventChannelMember", "lê/referencia", "habilita o CDC do objeto (`selectedEntity`, ex.: AccountChangeEvent)", "plataforma", "Change Event"),
                    ator("Change Event", "evento gerado pela plataforma (`<Objeto>ChangeEvent`); não é metadata próprio", "plataforma", "assinantes")]
            if sub == "APEX":
                rows += [R("Trigger do change event", "ApexTrigger", "executa", "`after insert` no ChangeEvent; enfileira o callout", "barramento", "Classe Queueable"),
                         R("Configuração do assinante", "PlatformEventSubscriberConfig", "lê/referencia", "usuário e lote", "plataforma", "—", "Opcional")]
                a, c = async_apex("QUEUE", "Trigger do change event")
                rows += a + endpoint(e, c)
                lab = f"Assinante interno (Apex) · endpoint {e}"
            else:
                app = sub.split("_")[1]
                rows += ext_subscriber(app); lab = f"Assinante externo · {APPS[app]}"
            var.append((lab, rows))
    return var

def custom_channel():
    var = []
    for tipo in ("CDC", "PE"):
        for app in ("CA", "ECA"):
            rows = [R("Canal customizado", "PlatformEventChannel", "lê/referencia", f"canal do tipo {'data' if tipo=='CDC' else 'event'} que agrupa eventos", "plataforma", "assinantes"),
                    R("Membro do canal", "PlatformEventChannelMember", "lê/referencia", "inclui o evento/objeto; define campos de enriquecimento e filtro", "Canal", "—")]
            rows += (pe_def() if tipo == "PE" else [R("Objeto monitorado", "CustomObject", "lê/referencia", "origem do change event", "—", "Canal")])
            rows += ext_subscriber(app)
            var.append((f"{tipo} · {APPS[app]}", rows))
    return var

def relay():
    var = []
    for tipo in ("PE", "CDC"):
        rows = (pe_def() if tipo == "PE" else [R("Objeto monitorado", "CustomObject", "lê/referencia", "origem do change event", "—", "Canal")])
        rows += [R("Canal customizado", "PlatformEventChannel", "lê/referencia", "canal que o relay lê", "plataforma", "Event Relay"),
                 R("Membro do canal", "PlatformEventChannelMember", "lê/referencia", "eventos incluídos no canal", "Canal", "—"),
                 R("Event Relay", "EventRelayConfig", "executa", "retransmite os eventos do canal ao destino", "plataforma", "Named Credential"),
                 R("Named Credential (destino AWS)", "NamedCredential", "lê/referencia", "aponta para a conta/região AWS (EventBridge partner event source)", "Event Relay", "Amazon EventBridge"),
                 ator("Amazon EventBridge", "recebe os eventos; regras roteiam para outros serviços", "Event Relay", "—")]
        var.append((tipo, rows))
    return var

def sched_batch(tipo):
    var = []
    for sentido in ("ENVIA", "BUSCA"):
        for e in ALL_E:
            rows = [ator("Agendamento", "job agendado (CronTrigger) via Setup ou `System.schedule`; registro, não metadata", "—", "Classe Schedulable"),
                    R("Classe Schedulable", "ApexClass", "executa", "`execute(SchedulableContext)` inicia o processamento", "Agendamento", "Batch" if tipo == "BATCH" else "Queueable")]
            if tipo == "BATCH":
                rows += [R("Classe Batch", "ApexClass", "executa", "`Database.Batchable, Database.AllowsCallouts`: `start` seleciona, `execute` faz o callout por lote", "Classe Schedulable", "Sistema externo")]
                c = "Classe Batch"
            else:
                rows += [R("Classe Queueable encadeada", "ApexClass", "executa", "busca uma página e enfileira a próxima (`System.enqueueJob`)", "Classe Schedulable / ela mesma", "Sistema externo")]
                c = "Classe Queueable encadeada"
            rows += endpoint(e, c)
            rows += [R("Objeto de destino/origem", "CustomObject + CustomField (External ID)", "executa (DML)", "registros enviados ou gravados com o retorno", c, "—")]
            rows += logrows(c) + killswitch(c)
            var.append((f"{'Envia dados' if sentido=='ENVIA' else 'Busca dados'} · endpoint {e}", rows))
    return var

def sched_flow():
    var = []
    for acao in ("HTTP", "ES", "APEX"):
        for e in (NC_E if acao != "APEX" else ALL_E):
            rows = [R("Flow agendado", "Flow (Schedule-Triggered)", "executa", "roda na frequência configurada sobre os registros que atendem ao filtro", "plataforma (agenda)", "ação")]
            if acao == "APEX":
                rows += [R("Classe invocável", "ApexClass", "executa", "faz o callout", "Flow agendado", "Sistema externo")]; c = "Classe invocável"
            else:
                rows += [R("Ação HTTP Callout / External Service", "ExternalServiceRegistration", "lê/referencia", "operação chamada", "Flow agendado", "Named Credential")]; c = "Flow agendado"
            rows += endpoint(e, c)
            var.append((f"Ação {acao} · endpoint {e}", rows))
    return var

def cross_org_bulk():
    var = []
    for m in ("BATCH", "QUEUE"):
        for e in ("E1", "E2", "E5"):
            rows = [R("Classe de carga", "ApexClass", "executa", f"{'Batch' if m=='BATCH' else 'Queueable'} que cria o job Bulk API 2.0 na org de destino", "agenda/trigger", "org de destino")]
            rows += endpoint(e, "Classe de carga", "Org Salesforce de destino")
            rows += [R("Connected App / External Client App (na org de destino)", "ConnectedApp ou ExternalClientApplication", "autoriza", "emite o token aceito pela org de destino", "Named Credential", "—")]
            var.append((f"{m} · endpoint {e}", rows))
    return var

def staging():
    var = []
    for proc in ("BATCH", "QUEUE"):
        for e in ALL_E:
            rows = gatilho_trigger()[:3] + [
                R("Classe handler", "ApexClass", "executa", "grava um registro de fila com o payload/estado PENDENTE", "Trigger", "Objeto de fila"),
                R("Objeto de fila / staging", "CustomObject (__c) + CustomField", "executa (DML)", "fila persistente: status, tentativas, payload, erro", "Classe handler", "processador"),
                ator("Agendamento", "CronTrigger", "—", "processador")]
            if proc == "BATCH":
                rows += [R("Classe Schedulable + Batch", "ApexClass", "executa", "lê os PENDENTES, faz callout, atualiza status e tentativas", "Agendamento", "Sistema externo")]
            else:
                rows += [R("Classe Queueable", "ApexClass", "executa", "processa a fila e reenfileira enquanto houver itens", "Classe handler ou Schedulable", "Sistema externo")]
            c = "processador"
            rows += endpoint(e, c) + [R("Notificação de falha", "CustomNotificationType ou EmailTemplate", "executa", "alerta após esgotar tentativas", c, "—", "Opcional")]
            var.append((f"Processador {proc} · endpoint {e}", rows))
    return var

OUT_ASYNC = [
 D("D.1", "Trigger Apex → @future ou Queueable → callout", "Callout fora da transação do registro (callout síncrono em trigger não é permitido). Serve para atualizar o externo ou buscar dados e enriquecer o registro.", trig_async()),
 D("D.2", "Flow record-triggered → caminho assíncrono → callout", "Versão declarativa do D.1.", flow_async()),
 D("D.3", "Trigger/Flow publica Platform Event → assinante faz o callout", "Desacopla a transação de origem do callout.", pe_callout(), obs=["Confirmado [PE-SUB]: em trigger de Platform Event, \"with some exceptions, you generally can’t make Apex callouts\" — por isso o assinante Apex enfileira um Queueable."], validar=["Callout em Platform Event–Triggered Flow: não encontrado nas páginas consultadas."]),
 D("D.4", "Outbound Message (SOAP com retry)", "Legado; ainda comum em orgs antigas.", outbound_msg(), obs=["Não usa Named Credential nem Remote Site Setting.", "No XML [MA-WF]: `workflows/Objeto.workflow` → `outboundMessages` (`endpointUrl`, `fields`, `integrationUser`, `includeSessionId`) e ação `type`=OutboundMessage na regra."], validar=["Ação Outbound Message em Flow: o valor não aparece na lista de `actionType` (InvocableActionType) da página Flow [MA-FLOW]. Criação de novas Workflow Rules: não verificado."]),
 D("E.1", "Platform Event publicado → sistema externo assina", "O Salesforce publica; o externo consome via Pub/Sub API.", pe_external()),
 D("E.2", "Change Data Capture", "Mudanças em registros viram eventos sem código de publicação.", cdc()),
 D("E.3", "Canal customizado com enriquecimento e filtro", "Seleciona eventos, adiciona campos e filtra antes de entregar.", custom_channel()),
 D("E.4", "Event Relay → Amazon EventBridge", "Ponte nativa de eventos com a AWS.", relay(), obs=["Envia eventos para fora do Salesforce (AWS).", "Confirmado [MA-ERC]: `destinationResourceName` é o nome da Named Credential com prefixo `callout:` e guarda a conta AWS; `eventChannel` é um canal `X__chn`."], validar=["Tipo (`namedCredentialType`) exigido para essa Named Credential: não informado na página."]),
 D("F.1", "Schedulable → Batch Apex com callout", "Sincronização periódica em lotes.", sched_batch("BATCH")),
 D("F.2", "Schedulable → Queueable encadeado (paginação)", "Percorre APIs paginadas.", sched_batch("QUEUE")),
 D("F.3", "Flow agendado → callout", "Versão declarativa do F.1.", sched_flow(), validar=["Suporte a HTTP Callout em Schedule-Triggered Flow: não encontrado nas páginas consultadas."]),
 D("F.4", "Apex → Bulk API 2.0 de outra org", "Carga entre orgs.", cross_org_bulk()),
 D("G.1", "Fila de integração em objeto (staging) + processador", "Resiliência com status, tentativas e reprocessamento.", staging()),
]

# =========================== IN ASYNC ===========================
def bulk_in():
    var = []
    for a, f in in_variants(flows=("JWT", "CC", "WS")):
        for op in ("INSERT", "UPSERT"):
            rows = ext_start("Bulk API 2.0") + app_in(a, f) + [ator("Bulk API 2.0", "recebe o CSV e processa o job em lotes assíncronos", EXT, "Objeto de destino")]
            rows += dados_destino("Bulk API 2.0", upsert=(op == "UPSERT"))
            var.append((f"{APPS[a]} · {FLOWS[f]} · {op.lower()}", rows))
    return var

def pe_in():
    var = []
    for a, f in in_variants(flows=("JWT", "CC")):
        for via in ("REST", "PUBSUB"):
            for sub in ("APEX", "FLOW"):
                rows = [ator(EXT, "publica o evento", "—", "API")] + app_in(a, f)
                rows += [ator("REST API (sObject __e)" if via == "REST" else "Pub/Sub API (Publish)", "recebe a publicação", EXT, "Platform Event")]
                rows += pe_def("API") + [R("Permission Set (Create no evento)", "PermissionSet", "autoriza", "permite publicar o `__e`", "plataforma", "—")]
                if sub == "APEX":
                    rows += [R("Trigger do evento", "ApexTrigger", "executa", "`after insert` no `__e`; processa e grava", "barramento", "Objeto de destino"),
                             R("Configuração do assinante", "PlatformEventSubscriberConfig", "lê/referencia", "usuário e lote", "plataforma", "—", "Opcional")]
                    c = "Trigger do evento"
                else:
                    rows += [R("Flow disparado por evento", "Flow", "executa", "processa e grava", "barramento", "Objeto de destino")]; c = "Flow disparado por evento"
                rows += dados_destino(c)
                var.append((f"{APPS[a]} · {FLOWS[f]} · publica via {via} · assinante {sub}", rows))
    return var

def rest_enqueue():
    var = []
    for a, f in in_variants(flows=("JWT", "CC")):
        for m in ("QUEUE", "PE"):
            rows = ext_start("Apex REST") + app_in(a, f) + [
                ator("Apex REST (/services/apexrest)", "endpoint", EXT, "Classe Apex REST"),
                R("Classe Apex REST", "ApexClass", "executa", "valida o payload, responde 202 e delega", "Apex REST", "Queueable" if m == "QUEUE" else "Platform Event")]
            if m == "QUEUE":
                rows += [R("Classe Queueable", "ApexClass", "executa", "processa depois da resposta", "Classe Apex REST", "Objeto de destino")]; c = "Classe Queueable"
            else:
                rows += pe_def("Classe Apex REST") + [R("Trigger do evento", "ApexTrigger", "executa", "processa", "barramento", "Objeto de destino")]; c = "Trigger do evento"
            rows += dados_destino(c) + logrows(c)
            var.append((f"{APPS[a]} · {FLOWS[f]} · delega para {'Queueable' if m=='QUEUE' else 'Platform Event'}", rows))
    return var

def email_in():
    var = []
    for dest in ("DML", "QUEUE"):
        rows = [ator(EXT, "envia e-mail ao endereço do serviço", "—", "Email Service"),
                R("Email Service", "EmailServicesFunction", "executa", "endereço, remetentes aceitos, usuário de contexto, ação em falha", EXT, "Classe handler"),
                R("Classe handler", "ApexClass", "executa", "implementa `Messaging.InboundEmailHandler`; lê corpo e anexos", "Email Service", "Objeto de destino" if dest == "DML" else "Queueable")]
        if dest == "QUEUE":
            rows.append(R("Classe Queueable", "ApexClass", "executa", "processamento pesado posterior", "Classe handler", "Objeto de destino"))
        rows += dados_destino("Classe handler", upsert=False)
        var.append(("Processa direto" if dest == "DML" else "Enfileira processamento", rows))
    return var

def files_in():
    var = []
    for a, f in in_variants(flows=("JWT", "CC")):
        for sub in ("APEX", "FLOW"):
            rows = ext_start("REST API (ContentVersion)") + app_in(a, f) + [
                ator("REST API (ContentVersion)", "recebe o arquivo (multipart/base64)", EXT, "ContentVersion"),
                ator("ContentVersion / ContentDocumentLink", "objetos padrão de arquivo (registros, não metadata)", "REST API", "processador")]
            rows += [R("Trigger em ContentVersion" if sub == "APEX" else "Flow record-triggered em ContentVersion", "ApexTrigger" if sub == "APEX" else "Flow", "executa", "lê/valida o conteúdo e vincula ao registro", "plataforma (DML)", "Objeto de destino")]
            rows += dados_destino("processador", upsert=False)
            var.append((f"{APPS[a]} · {FLOWS[f]} · processador {sub}", rows))
    return var

IN_ASYNC = [
 D("H.1", "Sistema externo → Bulk API 2.0", "Cargas de grande volume em jobs assíncronos.", bulk_in()),
 D("H.2", "Sistema externo publica Platform Event → assinante na org", "O externo entrega a mensagem; a org processa quando o evento chega.", pe_in()),
 D("H.3", "Apex REST que recebe e enfileira", "Entrada síncrona, processamento assíncrono.", rest_enqueue()),
 D("H.4", "E-mail inbound (Email Service)", "Integração por e-mail.", email_in()),
 D("H.5", "Arquivos via ContentVersion", "O externo envia arquivo; automação processa.", files_in()),
]

# =========================== MID ===========================
MULE = "MuleSoft / middleware (Experience/Process/System API)"

def mid_out_sync():
    var = []
    for o in ("LWC", "FLOW"):
        for e in ALL_E:
            rows, entry = origem_ui(o); rows = list(rows)
            rows += endpoint(e, entry, MULE)
            rows += [ator("Sistema de destino final", "chamado pelo middleware (ERP, legado etc.)", MULE, "—")]
            var.append((f"Origem {ORIG_NOME[o]} · endpoint {e}", rows))
    for m in ("FUTURE", "QUEUE"):
        for e in ALL_E:
            rows = gatilho_trigger(); a, c = async_apex(m, "Classe handler")
            rows += a + endpoint(e, c, MULE) + [ator("Sistema de destino final", "chamado pelo middleware", MULE, "—")]
            var.append((f"Origem Trigger + {'@future' if m=='FUTURE' else 'Queueable'} · endpoint {e}", rows))
    return var

def mid_sub():
    var = []
    for tipo in ("PE", "CDC"):
        for app in ("CA", "ECA"):
            rows = (pe_def() if tipo == "PE" else [R("Membro do canal ChangeEvents", "PlatformEventChannelMember", "lê/referencia", "habilita o CDC do objeto", "plataforma", "Change Event"), R("Objeto monitorado", "CustomObject", "lê/referencia", "origem", "—", "Change Event")])
            rows += [ator("Pub/Sub API", "entrega os eventos", "barramento", MULE), ator(MULE, "conector Salesforce assina o canal e roteia", "—", "sistemas de destino")]
            rows += app_in(app, "JWT", MULE)
            rows += [R("Permission Set (leitura do evento/objeto)", "PermissionSet", "autoriza", "Read no evento ou objeto", "plataforma", "—")]
            var.append((f"{tipo} · {APPS[app]}", rows))
    return var

def mid_in(api_kind):
    var = []
    for a, f in in_variants(flows=("JWT", "CC")):
        kinds = ("PADRAO", "APEXREST") if api_kind == "SYNC" else ("BULK",)
        for k in kinds:
            rows = [ator(MULE, "orquestra e chama a org", "sistema de origem", "Salesforce")] + app_in(a, f, MULE)
            if k == "APEXREST":
                rows += [ator("Apex REST", "endpoint", MULE, "Classe Apex REST")] + APEX_REST[1]
            else:
                api = {"PADRAO": "REST/Composite API padrão", "BULK": "Bulk API 2.0"}[k]
                rows += [ator(api, "endpoint", MULE, "Objeto de destino")] + dados_destino(api)
            var.append((f"{APPS[a]} · {FLOWS[f]} · {k}", rows))
    return var

def mid_poll():
    var = []
    for a, f in in_variants(flows=("JWT", "CC")):
        for ctrl in ("LMD", "CAMPO"):
            rows = [ator(MULE, "executa SOQL periodicamente", "agenda do middleware", "REST API (query)")] + app_in(a, f, MULE)
            rows += [ator("REST API (query)", "executa a SOQL", MULE, "Objeto consultado"),
                     R("Objeto consultado", "CustomObject + CustomField", "lê/referencia", "dados lidos", "REST API", "—")]
            if ctrl == "CAMPO":
                rows += [R("Campo de controle", "CustomField", "lê/referencia + executa (DML)", "flag/status 'enviado'; o middleware atualiza após processar", MULE, "triggers do objeto")]
            var.append((f"{APPS[a]} · {FLOWS[f]} · controle por {'LastModifiedDate' if ctrl=='LMD' else 'campo customizado'}", rows))
    return var

def mid_ip():
    var = []
    for caller in ("OMNISCRIPT", "FLEXCARD", "APEX", "APEXREST"):
        for e in ("E1", "E2", "E3"):
            ent = {"OMNISCRIPT": [R("OmniScript", "OmniScript", "executa", "chama a IP", "Usuário", "Integration Procedure")],
                   "FLEXCARD": [R("FlexCard", "OmniUiCard", "executa", "fonte de dados IP", "Usuário", "Integration Procedure")],
                   "APEX": [R("Classe Apex", "ApexClass", "executa", "invoca a IP pela API Apex do OmniStudio", "trigger/serviço", "Integration Procedure")],
                   "APEXREST": [ator(EXT, "chama a org", "—", "Apex REST")] + app_in("CA", "JWT") + [R("Classe Apex REST", "ApexClass", "executa", "expõe a IP como endpoint", "Apex REST", "Integration Procedure")]}[caller]
            rows = ent + [R("Integration Procedure", "OmniIntegrationProcedure", "executa", "orquestra várias chamadas, condições e cache", caller, "HTTP Actions / Data Mappers"),
                          R("Data Mapper (Extract/Load/Transform)", "OmniDataTransform", "executa", "lê/grava objetos e transforma payloads", "Integration Procedure", "objetos")]
            if e == "E3":
                rows += [R("Remote Site Setting", "RemoteSiteSetting", "autoriza", "URL fixa", "plataforma", "—"), ator(EXT, "responde", "Integration Procedure", "—")]
            else:
                rows += endpoint(e, "Integration Procedure")
            var.append((f"Chamador {caller} · endpoint {e}", rows))
    return var

def mule_es():
    var = []
    for prov in ("MuleSoft", "Anypoint"):
        for o in ("FLOW", "APEX"):
            for e in NC_E:
                if o == "FLOW":
                    rows = [R("Flow", "Flow", "executa", "`actionCalls` com `actionType`=externalService", "gatilho do Flow", "Registro de External Service")]; c = "Flow"
                else:
                    rows = [R("Classe Apex", "ApexClass", "executa", "chama `ExternalService.<Servico>`", "trigger/serviço/UI", "Registro de External Service")]; c = "Classe Apex"
                rows += [R("Registro de External Service", "ExternalServiceRegistration", "lê/referencia", f"`registrationProviderType`={prov}; operações da API do MuleSoft", c, "Named Credential")]
                rows += endpoint(e, "Registro de External Service", MULE)
                var.append((f"Fonte {prov} · chamador {'Flow' if o=='FLOW' else 'Apex'} · endpoint {e}", rows))
    return var

MID = [
 D("M.1", "Org → middleware (síncrono ou via Apex assíncrono)", "Igual aos desenhos b e D, com o endpoint apontando para o middleware.", mid_out_sync()),
 D("M.2", "Middleware assina Platform Event / CDC", "O conector do middleware consome eventos via Pub/Sub API.", mid_sub()),
 D("M.3", "Middleware → org (REST padrão ou Apex REST)", "O middleware chama a org.", mid_in("SYNC")),
 D("M.4", "Middleware → org (Bulk API 2.0)", "Batch Data Synchronization.", mid_in("BULK")),
 D("M.5", "Middleware faz polling na org", "Sem evento; consulta periódica.", mid_poll()),
 D("M.6", "Integration Procedure como middleware dentro da org", "Orquestração e transformação sem middleware externo.", mid_ip(), validar=["Metadata types OmniStudio ausentes da lista de Metadata Types (API 68.0) [MA-TYPES]; API Apex de invocação de Integration Procedure não confirmada."]),
 D("M.7", "API MuleSoft registrada como External Service → Flow ou Apex", "A especificação vem do MuleSoft/Anypoint; Flow e Apex chamam as operações geradas.", mule_es(), obs=["Confirmado [MA-ESR]: `registrationProviderType` = MuleSoft ou Anypoint (API 63.0+)."]),
]

# =========================== OUTRAS ===========================
def org_org():
    var = []
    var.append(("Salesforce Connect cross-org", [USER,
        R("External Object", "CustomObject (__x)", "lê/referencia", "objetos da org remota", "Página", "External Data Source"),
        R("External Data Source (cross-org)", "ExternalDataSource", "lê/referencia", "URL e identidade da org remota", "External Object", "Org remota"),
        R("Permission Set", "PermissionSet", "autoriza", "acesso ao External Object", "plataforma", "—"),
        ator("Org Salesforce remota", "responde às consultas via API", "External Data Source", "—")]))
    for e in ("E1", "E2", "E5"):
        rows = [R("Classe cliente (org A)", "ApexClass", "executa", "faz o callout para a org B", "trigger/UI/agenda", "Org B")]
        rows += endpoint(e, "Classe cliente (org A)", "Org B")
        rows += [R("Connected App / External Client App (org B)", "ConnectedApp ou ExternalClientApplication", "autoriza", "emite o token", "Named Credential", "—"),
                 R("Classe Apex REST (org B)", "ApexClass", "executa", "recebe e processa", "Org A", "objetos da org B", "Opcional (ou API padrão)")]
        var.append((f"Apex REST org→org · endpoint {e}", rows))
    return var

def ui_int():
    var = []
    var.append(("Botão/link de URL", [USER, R("Botão ou link", "WebLink", "executa", "abre o sistema externo com parâmetros do registro na URL", "Usuário", "Sistema externo"), R("Layout", "Layout", "lê/referencia", "expõe o botão", "plataforma", "—"), ator(EXT, "abre no navegador", "WebLink", "—")]))
    var.append(("Web Tab", [USER, R("Aba web", "CustomTab", "executa", "carrega a URL externa", "Usuário", "Sistema externo"), R("App", "CustomApplication", "lê/referencia", "inclui a aba", "plataforma", "—"), ator(EXT, "exibido em frame", "CustomTab", "—")]))
    for host in ("VF", "PAGE"):
        rows = [USER]
        rows += ([R("Página Visualforce", "ApexPage", "executa", "`<apex:canvasApp>`", "Usuário", "Canvas App")] if host == "VF" else [R("Página Lightning", "FlexiPage", "executa", "componente padrão Canvas App", "Usuário", "Canvas App")])
        rows += [R("Connected App com Canvas", "ConnectedApp", "autoriza + lê", "URL do Canvas, método de acesso (signed request/OAuth), locais permitidos", "host", "Sistema externo"), ator(EXT, "app web que recebe o signed request", "Canvas", "—")]
        var.append((f"Canvas em {'Visualforce' if host=='VF' else 'Lightning Page'}", rows))
    var.append(("Canvas via External Client App", [USER, R("Página Lightning", "FlexiPage", "executa", "componente Canvas App", "Usuário", "Canvas App"),
        R("External Client App", "ExternalClientApplication", "autoriza", "app registrado", "host", "—"),
        R("Configuração Canvas do app", "ExtlClntAppCanvasSettings", "autoriza + lê", "URL e acesso do Canvas (API 66.0+)", "External Client App", "Sistema externo"), ator(EXT, "app web", "Canvas", "—")]))
    var.append(("iframe em LWC", [USER, R("Componente LWC", "LightningComponentBundle", "executa", "renderiza `<iframe>`", "Página", "Sistema externo"), R("CSP Trusted Site", "CspTrustedSite", "autoriza", "libera o domínio em `frame-src`", "navegador", "—"), ator(EXT, "precisa permitir ser emoldurado (X-Frame-Options/CSP)", "LWC", "—")]))
    return var

def sso():
    return [
     ("SAML com IdP externo", [ator("IdP externo", "autentica o usuário", "Usuário", "Salesforce"), R("Configuração SAML", "SamlSsoConfig", "autoriza", "emissor, certificado, mapeamento de identidade", "IdP", "—"), R("Certificate", "Certificate", "autoriza", "valida/assina asserções", "SAML", "—", "Opcional")]),
     ("OpenID Connect via Auth Provider", [ator("Provedor externo", "autentica", "Usuário", "Salesforce"), R("Auth Provider", "AuthProvider", "autoriza", "configuração OIDC", "login", "Registration Handler"), R("Registration Handler", "ApexClass", "executa", "cria/atualiza o usuário a partir dos dados do provedor", "Auth Provider", "User")]),
     ("Salesforce como IdP", [ator("App externo", "pede login", "Usuário", "Salesforce"), R("Connected App (SAML/OIDC)", "ConnectedApp", "autoriza", "app de serviço; Salesforce emite asserção/token", "App externo", "—")]),
    ]

OUTRAS = [
 D("N.1", "Org ↔ org", "Integração entre orgs Salesforce.", org_org(), validar=["Salesforce to Salesforce (legado) não incluído: verificar se há metadata associada."]),
 D("N.2", "Integração de UI", "O usuário vê ou usa outro sistema; pouca ou nenhuma troca de dados no servidor.", ui_int()),
 D("N.3", "Identidade (SSO)", "Integra o login, não os dados.", sso()),
 D("N.4", "Data Cloud", "Ingestão e ativação de dados.", [("A validar", [ator("Data Cloud", "metadata types de data streams, data sources e ativações a confirmar", "—", "—")])], validar=["Toda a família de metadata do Data Cloud."]),
]

SECOES = [
 ("out-sync", "OUT SYNC — Salesforce chama o externo e espera", OUT_SYNC),
 ("in-sync", "IN SYNC — externo chama o Salesforce e espera", IN_SYNC),
 ("out-async", "OUT ASYNC — Salesforce envia sem esperar", OUT_ASYNC),
 ("in-async", "IN ASYNC — externo envia; Salesforce processa depois", IN_ASYNC),
 ("mid", "MID — middleware / MuleSoft", MID),
 ("outras", "Outras dinâmicas", OUTRAS),
]

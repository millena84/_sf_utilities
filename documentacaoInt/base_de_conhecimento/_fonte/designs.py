from blocks import *

def D(id, titulo, resumo, variantes, obs=None, validar=None):
    return dict(id=id, titulo=titulo, resumo=resumo, variantes=variantes, obs=obs or [], validar=validar or [])

USER = ator("Usuário", "Pessoa que usa o Salesforce e dispara a integração ao clicar em algo na tela. Ela fica esperando a resposta.", "—", "página")

def origem_ui(kind):
    """Linhas de entrada para desenhos iniciados por usuário."""
    if kind == "LWC":
        return [USER,
         R("Página Lightning", "FlexiPage", "lê/referencia", "Página do Salesforce (de registro, app ou home) onde o componente foi colocado. É por ela que o usuário chega ao componente.", "Usuário", "LWC", "Opcional (ou CustomTab / QuickAction)"),
         R("Componente LWC", "LightningComponentBundle", "executa", "Componente de tela (LWC). Mostra a interface, captura o clique e chama um método Apex no servidor (import `@salesforce/apex`).", "Página Lightning", "Controller Apex"),
         R("Controller Apex", "ApexClass", "executa", "Classe Apex que recebe o pedido da tela. O método marcado com `@AuraEnabled` é a porta de entrada no servidor.", "Componente LWC", "próximo componente")], "Controller Apex"
    if kind == "FLOW":
        return [USER,
         R("Ponto de entrada", "FlexiPage, QuickAction ou CustomTab", "lê/referencia", "Lugar onde o usuário encontra o Screen Flow: uma página, um botão de ação ou uma aba.", "Usuário", "Screen Flow", "Opcional"),
         R("Screen Flow", "Flow", "executa", "Fluxo com telas, montado sem código. Coleta dados do usuário e chama uma ação Apex para falar com o sistema externo.", "Ponto de entrada", "Classe invocável"),
         R("Versão ativa do Flow", "FlowDefinition", "lê/referencia", "Arquivo antigo que só indica qual versão do Flow está ativa.", "plataforma", "—", "Opcional"),
         R("Classe invocável", "ApexClass", "executa", "Classe Apex que o Flow consegue chamar. O método marcado com `@InvocableMethod` é a porta de entrada no servidor.", "Screen Flow", "próximo componente")], "Classe invocável"
    raise KeyError(kind)

APEX_ACCESS = lambda por: R("Permission Set (acesso às classes Apex)", "PermissionSet", "autoriza", "Dá ao usuário permissão para executar as classes Apex chamadas pela tela. Sem isso, a tela mostra erro de acesso.", "plataforma", "—")
ORIG_NOME = {"LWC": "LWC", "FLOW": "Screen Flow"}

def ui_callout(cadeia):
    var = []
    for o in ("LWC", "FLOW"):
        for e in ALL_E:
            rows, entry = origem_ui(o)
            rows = list(rows)
            caller = entry
            if cadeia:
                rows += [R("Classe de serviço", "ApexClass", "executa", "Camada intermediária: aplica as regras de negócio e monta os dados que serão enviados.", entry, "Classe cliente HTTP"),
                         R("Classe cliente HTTP", "ApexClass", "executa", "Classe que efetivamente chama o sistema externo: monta a requisição HTTP (`HttpRequest`), envia e interpreta a resposta.", "Classe de serviço", "Sistema externo"),
                         R("Classes de DTO / wrapper", "ApexClass", "lê/referencia", "Classes que só representam os dados: convertem objetos Apex em JSON para enviar e o JSON recebido de volta em objetos.", "Classe cliente HTTP", "—", "Opcional")]
                caller = "Classe cliente HTTP"
            else:
                rows[-1] = rows[-1][:3] + (rows[-1][3] + " Nesta variante, ela mesma chama o sistema externo (`HttpRequest`), sem classes intermediárias.",) + rows[-1][4:5] + ("Sistema externo",) + rows[-1][6:]
            rows += endpoint(e, caller)
            rows += [APEX_ACCESS(None)] + killswitch(caller) + logrows(caller)
            var.append((f"Origem {ORIG_NOME[o]} · endpoint {e} ({ENDPOINTS[e]})", rows))
    return var

def flow_http(origem="Screen Flow", trig="FLOW"):
    var = []
    for e in NC_E:
        rows, _ = origem_ui("FLOW") if trig == "FLOW" else (None, None)
        rows = list(rows[:3]) if rows else []
        rows += [R("Ação HTTP Callout", "ExternalServiceRegistration", "lê/referencia", "Cadastro criado automaticamente quando alguém configura um HTTP Callout no Flow Builder. Guarda o que chamar (método e caminho) e o formato da resposta, para o Flow usar sem código.", "Screen Flow", "Named Credential"),]
        rows += endpoint(e, "Ação HTTP Callout")
        rows += [R("Permission Set (acesso ao Flow)", "PermissionSet", "autoriza", "Dá ao usuário permissão para rodar o Flow.", "plataforma", "—")]
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
                rows[-1] = rows[-1][:3] + ("Classe Apex que recebe o pedido da tela e chama a operação da API pelas classes geradas automaticamente (`ExternalService.<Servico>`).",) + rows[-1][4:5] + ("Registro de External Service",) + rows[-1][6:]
            rows += [R("Registro de External Service", "ExternalServiceRegistration", "lê/referencia", "Cadastro da API externa a partir do contrato dela (OpenAPI). A plataforma transforma cada operação da API em uma ação que o Flow ou o Apex pode chamar, sem montar HTTP à mão.", caller, "Named Credential")]
            rows += endpoint(e, "Registro de External Service")
            var.append((f"Origem {'Screen Flow' if o=='FLOW' else 'LWC + Apex'} · endpoint {e}", rows))
    return var

def wsdl():
    var = []
    for o in ("LWC", "FLOW"):
        for e in ALL_E:
            rows, entry = origem_ui(o); rows = list(rows)
            rows += [R("Stub gerado (WSDL2Apex)", "ApexClass", "executa", "Classe gerada automaticamente a partir do contrato SOAP (WSDL) do sistema externo. Monta a mensagem SOAP e faz a chamada (`WebServiceCallout.invoke`). O endereço fica em `endpoint_x` e pode ser trocado pelo código.", entry, "Sistema externo")]
            rows += endpoint(e, "Stub gerado (WSDL2Apex)")
            rows += [APEX_ACCESS(None)]
            var.append((f"Origem {ORIG_NOME[o]} · endpoint {e}", rows))
    return var

def continuation():
    var = []
    for e in ALL_E:
        rows, entry = origem_ui("LWC"); rows = list(rows)
        rows[-1] = rows[-1][:3] + ("Classe Apex que inicia uma chamada demorada sem prender o servidor: devolve um objeto `Continuation` (método `@AuraEnabled(continuation=true)`) e a plataforma espera a resposta por ela.",) + rows[-1][4:5] + ("Sistema externo",) + rows[-1][6:]
        rows += endpoint(e, "Controller Apex")
        rows += [R("Método de callback", "ApexClass", "executa", "Método chamado automaticamente quando a resposta chega. Ele trata o retorno e entrega o resultado para a tela.", "plataforma (ao chegar a resposta)", "Componente LWC")]
        var.append((f"Endpoint {e}", rows))
    return var

def omni_flexcard(com_dm):
    var = []
    for e in ("E1", "E2", "E3"):
        rows = [USER,
          R("Página Lightning", "FlexiPage", "lê/referencia", "Página onde o cartão (FlexCard) aparece para o usuário.", "Usuário", "FlexCard", "Opcional"),
          R("FlexCard", "OmniUiCard", "executa", "Cartão de tela do OmniStudio que mostra informações. Ele busca os dados chamando uma Integration Procedure.", "Página Lightning", "Integration Procedure"),
          R("Integration Procedure", "OmniIntegrationProcedure", "executa", "Roteiro de integração do OmniStudio, montado sem código. Um passo do tipo HTTP Action chama o sistema externo.", "FlexCard", "Sistema externo")]
        if com_dm:
            rows.append(R("Data Mapper / DataRaptor Transform", "OmniDataTransform", "executa", "Ferramenta de mapeamento do OmniStudio: converte a resposta do sistema externo no formato que o cartão espera.", "Integration Procedure", "—"))
        if e in ("E1", "E2"):
            rows += endpoint(e, "Integration Procedure")
        else:
            rows += [R("Remote Site Setting", "RemoteSiteSetting", "autoriza", "Lista de domínios externos permitidos. Como a URL foi escrita direto na HTTP Action (sem Named Credential), o domínio **precisa** estar cadastrado aqui.", "plataforma", "—"), ator(EXT, "O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta.", "Integration Procedure", "—")]
        var.append((f"{'Com' if com_dm else 'Sem'} Data Mapper · endpoint {'E3 (URL fixa na HTTP Action + Remote Site)' if e=='E3' else e}", rows))
    return var

def omniscript():
    var = []
    for via in ("IP", "RA"):
        for e in (("E1", "E2", "E3") if via == "IP" else ALL_E):
            rows = [USER,
              R("Página Lightning / Experience", "FlexiPage", "lê/referencia", "Página onde o processo guiado (OmniScript) aparece.", "Usuário", "OmniScript", "Opcional"),
              R("OmniScript", "OmniScript", "executa", "Processo guiado de várias telas do OmniStudio. Em uma das etapas, chama a integração.", "Página", "Integration Procedure" if via == "IP" else "Classe Remote Action")]
            if via == "IP":
                rows.append(R("Integration Procedure", "OmniIntegrationProcedure", "executa", "Roteiro de integração do OmniStudio. Um passo do tipo HTTP Action chama o sistema externo.", "OmniScript", "Sistema externo"))
                if e == "E3":
                    rows += [R("Remote Site Setting", "RemoteSiteSetting", "autoriza", "Lista de domínios externos permitidos. Como a URL é fixa (sem Named Credential), o domínio **precisa** estar cadastrado aqui.", "plataforma", "—"), ator(EXT, "O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta.", "Integration Procedure", "—")]
                else:
                    rows += endpoint(e, "Integration Procedure")
            else:
                rows.append(R("Classe Remote Action", "ApexClass", "executa", "Classe Apex chamada pelo OmniScript (implementa `Callable` ou a interface do pacote). Ela chama o sistema externo.", "OmniScript", "Sistema externo"))
                rows += endpoint(e, "Classe Remote Action") + [APEX_ACCESS(None)]
            var.append((f"Via {'Integration Procedure' if via=='IP' else 'Remote Action (Apex)'} · endpoint {e}", rows))
    return var

def browser_fetch():
    var = []
    for src in ("JS", "LABEL", "CMDT"):
        rows = [USER, R("Componente LWC", "LightningComponentBundle", "executa", "Componente de tela que chama a API externa direto do navegador do usuário (`fetch()`), sem passar pelo servidor Salesforce.", "Página", "Sistema externo")]
        if src == "LABEL":
            rows.append(R("Custom Label", "CustomLabels", "lê/referencia", "Texto configurável (Custom Label) com a URL da API, lido pelo componente.", "Componente LWC", "—"))
        if src == "CMDT":
            rows += [R("Controller Apex", "ApexClass", "executa", "Classe Apex que só lê a URL na configuração e entrega ao componente.", "Componente LWC", "Registro de Custom Metadata"),
                     R("Registro de Custom Metadata", "CustomMetadata (+ CustomObject __mdt)", "lê/referencia", "Registro de configuração com a URL da API em cada ambiente.", "Controller Apex", "—")]
        rows += [R("CSP Trusted Site", "CspTrustedSite", "autoriza", "Lista de domínios que o **navegador** pode acessar a partir de páginas do Salesforce (regra de segurança CSP). Aqui não se usa Remote Site Setting: ele vale só para chamadas feitas pelo servidor (Apex).", "navegador", "—"),
                 ator(EXT, "O sistema de fora do Salesforce. Como a chamada vem do navegador, ele precisa permitir (CORS) chamadas vindas do domínio do Salesforce.", "Componente LWC", "—")]
        var.append(({"JS": "URL no JavaScript", "LABEL": "URL em Custom Label", "CMDT": "URL em Custom Metadata via Apex"}[src], rows))
    return var

def sf_connect(adapter):
    var = []
    codes = ALL_E if adapter else ("PROPRIA", "NC")
    for e in codes:
        rows = [USER,
          R("Layout / Página / Aba", "Layout, FlexiPage ou CustomTab", "lê/referencia", "Tela onde os dados externos aparecem como se fossem registros do Salesforce.", "Usuário", "External Object"),
          R("External Object", "CustomObject (__x)", "lê/referencia", "Objeto \"espelho\" (sufixo `__x`): representa uma tabela do sistema externo. Os dados não são copiados; cada vez que alguém abre a tela, o Salesforce consulta o sistema externo.", "Página", "External Data Source"),
          R("Campos e relacionamentos externos", "CustomField", "lê/referencia", "Colunas da tabela externa. Campos especiais (External Lookup, Indirect Lookup) ligam esses dados a registros do Salesforce.", "External Object", "—"),
          R("External Data Source", "ExternalDataSource", "lê/referencia", "Cadastro da fonte de dados externa: qual protocolo usa (OData, outra org Salesforce ou adaptador Apex), o endereço e com qual identidade consultar.", "External Object", "adaptador" if adapter else "Sistema externo"),
          R("Permission Set", "PermissionSet", "autoriza", "Dá ao usuário permissão para ver o objeto externo e usar a fonte de dados.", "plataforma", "—")]
        if adapter:
            rows += [R("Provider do adaptador", "ApexClass", "executa", "Classe Apex que \"apresenta\" o adaptador à plataforma: diz o que ele sabe fazer e como autentica.", "External Data Source", "Connection"),
                     R("Connection do adaptador", "ApexClass", "executa", "Classe Apex que faz o trabalho: descreve as tabelas e, a cada consulta ou busca, chama o sistema externo.", "Provider", "Sistema externo")]
            rows += endpoint(e, "Connection do adaptador")
            label = f"Adaptador Apex · endpoint {e}"
        elif e == "NC":
            rows += endpoint("E1", "External Data Source"); label = "Autenticação via Named Credential"
        else:
            rows += [ator(EXT, "Serviço externo no padrão OData que responde às consultas.", "External Data Source", "—")]; label = "Autenticação na própria External Data Source"
        var.append((label, rows))
    return var

def quick_action():
    var = []
    for o in ("FLOW", "LWC"):
        for e in ALL_E:
            rows = [USER, R("Quick Action", "QuickAction", "executa", "Botão de ação na página do registro. Ao clicar, abre um Flow ou um componente LWC.", "Usuário", "Screen Flow" if o == "FLOW" else "Componente LWC"),
                    R("Layout / Página (onde a ação aparece)", "Layout ou FlexiPage", "lê/referencia", "Configuração da página que faz o botão aparecer.", "plataforma", "—")]
            if o == "FLOW":
                rows += [R("Screen Flow", "Flow", "executa", "Fluxo com tela que recebe o registro atual, chama o Apex e grava no registro o que voltou do sistema externo.", "Quick Action", "Classe invocável"),
                         R("Classe invocável", "ApexClass", "executa", "Classe Apex que chama o sistema externo.", "Screen Flow", "Sistema externo")]
                c = "Classe invocável"
            else:
                rows += [R("Componente LWC (screen ou headless action)", "LightningComponentBundle", "executa", "Componente de tela aberto pelo botão; recebe o registro atual e chama o Apex.", "Quick Action", "Controller Apex"),
                         R("Controller Apex", "ApexClass", "executa", "Classe Apex que chama o sistema externo.", "Componente LWC", "Sistema externo")]
                c = "Controller Apex"
            rows += endpoint(e, c)
            rows += [R("Objeto do registro", "CustomObject + CustomField", "executa (DML)", "Registro que recebe os dados trazidos do sistema externo (\"enriquecimento\").", c, "triggers/flows do objeto"), APEX_ACCESS(None)]
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
    return [ator(EXT, f"O sistema de fora do Salesforce. Primeiro pede um token (login) e depois chama a {api}.", "—", "Connected App / External Client App")]

def dados_destino(caller, upsert=True):
    rows = [R("Objeto de destino", "CustomObject (padrão ou __c)", "executa (DML)", "Objeto (tabela) do Salesforce onde a integração cria, altera ou consulta registros.", caller, "triggers e flows do objeto"),
            R("Campos", "CustomField", "lê/referencia", "Campos que a integração lê ou preenche.", caller, "—")]
    if upsert:
        rows.append(R("Campo External ID", "CustomField (externalId=true)", "lê/referencia", "Campo que guarda o identificador do registro no outro sistema. Com ele, o Salesforce sabe se deve criar um registro novo ou atualizar um existente (upsert), sem duplicar.", caller, "—", "Opcional (obrigatório em upsert)"))
    rows += [R("Trigger do objeto", "ApexTrigger", "executa", "Código que roda sozinho quando a integração grava o registro. Pode disparar outras ações (inclusive outras integrações).", "plataforma (DML)", "classes handler", "Opcional"),
             R("Flow record-triggered", "Flow", "executa", "Automação sem código que roda quando a integração grava o registro.", "plataforma (DML)", "—", "Opcional")]
    return rows

def in_api(api, extra_fn, upsert=True):
    var = []
    for a, f in in_variants():
        rows = ext_start(api) + app_in(a, f)
        rows += [ator(api, "Endereço padrão do Salesforce (API pronta, sem código na org) que o sistema externo chama.", EXT, extra_fn[0] if extra_fn else "Objeto de destino")]
        if extra_fn:
            rows += extra_fn[1]
        else:
            rows += dados_destino(api, upsert)
        var.append((f"{APPS[a]} · {FLOWS[f]}", rows))
    return var

APEX_REST = ("Classe Apex REST", [
  R("Classe Apex REST", "ApexClass", "executa", "Classe Apex que vira um endereço (endpoint) que o sistema externo pode chamar (`@RestResource`). Recebe os dados, confere se estão corretos e aplica a regra de negócio.", "Apex REST (/services/apexrest)", "Objeto de destino"),
  R("Classes de serviço / DTO", "ApexClass", "executa", "Classes de apoio: aplicam a regra de negócio e convertem o JSON recebido em objetos Apex.", "Classe Apex REST", "Objeto de destino", "Opcional"),
  R("Permission Set (acesso à classe)", "PermissionSet", "autoriza", "Dá ao usuário de integração permissão para chamar a classe Apex REST. Sem isso, a chamada é recusada.", "plataforma", "—")] + dados_destino("Classe Apex REST"))
APEX_SOAP = ("Classe Apex SOAP", [
  R("Classe Apex SOAP", "ApexClass", "executa", "Classe Apex que vira um serviço SOAP (métodos `webservice` em classe `global`). A plataforma gera o contrato (WSDL) que o sistema externo usa para chamar.", "SOAP API customizada (/services/Soap/class)", "Objeto de destino"),
  R("Permission Set (acesso à classe)", "PermissionSet", "autoriza", "Dá ao usuário de integração permissão para chamar a classe.", "plataforma", "—")] + dados_destino("Classe Apex SOAP"))
FLOW_REST = ("Flow autolaunched", [
  R("Flow autolaunched", "Flow", "executa", "Automação sem código que o sistema externo dispara pela API (`/actions/custom/flow/<Nome>`), mandando os dados de entrada.", "REST API (Actions)", "Objeto de destino"),
  R("Permission Set (Run Flows / acesso ao Flow)", "PermissionSet", "autoriza", "Dá ao usuário de integração permissão para rodar o Flow.", "plataforma", "—")] + dados_destino("Flow autolaunched"))

def webhook():
    var = []
    for site in ("SITE", "EXP"):
        for val in ("NENHUMA", "CMDT", "CS"):
            rows = [ator(EXT, "O sistema de fora do Salesforce. Avisa sobre um acontecimento enviando um POST (webhook), sem login OAuth.", "—", "Site")]
            if site == "SITE":
                rows += [R("Site público", "CustomSite", "lê/referencia", "Site público do Salesforce. Permite que o sistema externo chame o endpoint sem fazer login (como usuário convidado/guest).", EXT, "Classe Apex REST")]
            else:
                rows += [R("Site Experience Cloud", "Network + ExperienceBundle/DigitalExperienceBundle + CustomSite", "lê/referencia", "Site do Experience Cloud com acesso de convidado (guest), usado para receber a chamada sem login.", EXT, "Classe Apex REST")]
            rows += [R("Perfil guest do site", "Profile", "autoriza", "Perfil do usuário convidado do site: define o que a chamada sem login pode executar e acessar. Deve ser o mínimo possível.", "plataforma", "—"),
                     R("Classe Apex REST", "ApexClass", "executa", "Classe que recebe o aviso (webhook) do sistema externo, confere se é legítimo e grava os dados ou os coloca numa fila para processar depois.", "Site", "Objeto de destino")]
            if val == "CMDT":
                rows += [R("Registro de Custom Metadata (protegido)", "CustomMetadata (+ CustomObject __mdt)", "lê/referencia", "Guarda o segredo usado para conferir a assinatura do webhook. Atenção: segredo em Custom Metadata é risco (anti-padrão A01).", "Classe Apex REST", "—")]
            if val == "CS":
                rows += [R("Custom Setting protegido", "CustomObject (Custom Setting)", "lê/referencia", "Guarda o segredo usado para conferir a assinatura do webhook.", "Classe Apex REST", "—")]
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
    return [ator("Gravação do registro", "Alguém (usuário, outra integração ou automação) cria, altera ou exclui um registro. É isso que dispara tudo.", "—", "Trigger"),
            R("Objeto de origem", "CustomObject + CustomField", "lê/referencia", "Objeto cujos registros, ao serem criados ou alterados, disparam a integração.", "—", "Trigger"),
            R("Trigger", "ApexTrigger", "executa", "Código que roda sozinho quando o registro é gravado. Não pode chamar o sistema externo direto (a plataforma não deixa callout síncrono em trigger), então só repassa o trabalho.", "plataforma (DML)", "Classe handler"),
            R("Classe handler", "ApexClass", "executa", "Escolhe quais registros precisam ir para o sistema externo e agenda o envio para rodar em segundo plano.", "Trigger", "processamento assíncrono")]

def async_apex(mech, caller):
    if mech == "FUTURE":
        return [R("Método @future", "ApexClass", "executa", "Método que roda em segundo plano (`@future(callout=true)`), depois que o registro já foi salvo. Recebe os IDs, busca os dados e chama o sistema externo.", caller, "Sistema externo")], "Método @future"
    return [R("Classe Queueable", "ApexClass", "executa", "Tarefa que roda em segundo plano (Queueable com `Database.AllowsCallouts`). É ela que chama o sistema externo. Permite encadear tarefas e tratar falhas melhor que o `@future`.", caller, "Sistema externo"),
            R("Finalizer", "ApexClass", "executa", "Código que roda sempre ao final da tarefa Queueable, mesmo se ela falhar. Usado para registrar o erro e tentar de novo.", "plataforma (fim do Queueable)", "Classe Queueable", "Opcional")], "Classe Queueable"

WRITEBACK = lambda c: R("Atualização do registro de origem", "CustomObject + CustomField", "executa (DML)", "Grava no registro o que voltou do sistema externo (dados, ID externo, status). Cuidado: essa gravação dispara o trigger de novo, então é preciso uma proteção para não entrar em loop.", c, "Trigger (de novo)", "Opcional")

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
    return [ator("Gravação do registro", "Alguém cria ou altera um registro. É isso que dispara tudo.", "—", "Flow"),
            R("Objeto de origem", "CustomObject + CustomField", "lê/referencia", "Objeto cujos registros disparam a integração.", "—", "Flow"),
            R("Flow record-triggered (Run Asynchronously)", "Flow", "executa", "Automação sem código disparada pela gravação do registro. O trecho \"Run Asynchronously\" roda depois que o registro foi salvo e, por isso, pode chamar o sistema externo.", "plataforma (DML)", "ação")]

def flow_async():
    var = []
    for acao in ("HTTP", "ES", "APEX"):
        for e in (NC_E if acao != "APEX" else ALL_E):
            rows = flow_rt_start()
            if acao == "APEX":
                rows += [R("Classe invocável", "ApexClass", "executa", "Classe Apex chamada pelo Flow (`@InvocableMethod`) que chama o sistema externo.", "Flow", "Sistema externo")]
                c = "Classe invocável"
            else:
                rows += [R("Ação HTTP Callout" if acao == "HTTP" else "Registro de External Service", "ExternalServiceRegistration", "lê/referencia", "Cadastro da operação da API externa que o Flow chama (criado pelo HTTP Callout ou pelo External Services).", "Flow", "Named Credential")]
                c = "Flow"
            rows += endpoint(e, c) + [WRITEBACK(c)]
            var.append((f"Ação {'HTTP Callout' if acao=='HTTP' else ('External Service' if acao=='ES' else 'Apex invocável')} · endpoint {e}", rows))
    return var

def pe_def(c="publicador"):
    return [R("Platform Event", "CustomObject (__e)", "lê/referencia", "Platform Event: o \"formato\" de uma mensagem que um sistema publica e outros recebem. Funciona como um aviso: quem publica não espera resposta.", c, "assinantes"),
            R("Campos do evento", "CustomField", "lê/referencia", "Campos da mensagem: os dados que viajam no evento.", c, "—")]

def pe_callout():
    var = []
    for pub in ("TRIGGER", "FLOW"):
        for sub in ("APEX", "FLOW"):
            for e in (ALL_E if sub == "APEX" else NC_E):
                if pub == "TRIGGER":
                    rows = gatilho_trigger()[:3] + [R("Classe handler", "ApexClass", "executa", "Monta a mensagem e a publica (`EventBus.publish`). A partir daí, quem assina o evento faz o resto.", "Trigger", "Platform Event")]
                else:
                    rows = flow_rt_start()[:2] + [R("Flow record-triggered", "Flow", "executa", "Automação sem código que publica o evento criando um registro do Platform Event (`__e`).", "plataforma (DML)", "Platform Event")]
                rows += pe_def("publicador")
                if sub == "APEX":
                    rows += [R("Trigger do evento", "ApexTrigger", "executa", "Código que roda quando o evento chega. A plataforma não deixa ele chamar o sistema externo direto, então ele agenda uma tarefa em segundo plano.", "barramento de eventos", "Classe Queueable"),
                             R("Configuração do assinante", "PlatformEventSubscriberConfig", "lê/referencia", "Define com qual usuário o trigger do evento roda e quantos eventos ele processa de uma vez.", "plataforma", "—", "Opcional")]
                    a, c = async_apex("QUEUE", "Trigger do evento")
                    rows += a + endpoint(e, c)
                else:
                    rows += [R("Flow disparado por evento", "Flow", "executa", "Automação sem código disparada quando o evento chega; chama o sistema externo por HTTP Callout ou External Service.", "barramento de eventos", "Named Credential"),
                             R("Ação HTTP Callout / External Service", "ExternalServiceRegistration", "lê/referencia", "Cadastro da operação da API externa que o Flow chama.", "Flow disparado por evento", "Named Credential")]
                    rows += endpoint(e, "Flow disparado por evento")
                rows += logrows("assinante")
                var.append((f"Publica {'Apex' if pub=='TRIGGER' else 'Flow'} · assina {'Apex Trigger + Queueable' if sub=='APEX' else 'Flow'} · endpoint {e}", rows))
    return var

def outbound_msg():
    var = []
    for origem in ("WF", "FLOW"):
        for cert in (False, True):
            rows = [ator("Gravação do registro", "Alguém cria ou altera um registro. É isso que dispara tudo.", "—", "regra"),
                    R("Objeto de origem", "CustomObject + CustomField", "lê/referencia", "Objeto cujos registros disparam o envio; os campos escolhidos vão na mensagem.", "—", "regra")]
            if origem == "WF":
                rows += [R("Regra de workflow", "Workflow (WorkflowRule)", "executa", "Regra de workflow (recurso antigo) que decide quando enviar a mensagem.", "plataforma (DML)", "Outbound Message")]
            else:
                rows += [R("Flow record-triggered", "Flow", "executa", "Automação sem código que dispara o envio da mensagem.", "plataforma (DML)", "Outbound Message")]
            rows += [R("Outbound Message", "Workflow (WorkflowOutboundMessage)", "lê/referencia", "Configuração do Outbound Message: para onde enviar, quais campos e com qual usuário. A plataforma envia em SOAP e tenta de novo por até 24 h se o sistema externo não confirmar.", "regra", "Sistema externo"),
                     ator("Usuário de envio", "Usuário em nome de quem a mensagem é enviada; define quais campos podem ser lidos.", "Outbound Message", "—")]
            if cert:
                rows.append(R("Certificate", "Certificate", "autoriza", "Certificado digital que prova a identidade do Salesforce para o sistema externo na conexão.", "Outbound Message", "—"))
            rows.append(ator(EXT, "O sistema de fora do Salesforce. Recebe a mensagem SOAP e confirma o recebimento (`ack=true`); sem a confirmação, o Salesforce tenta de novo.", "Outbound Message", "—"))
            var.append((f"{'Workflow Rule' if origem=='WF' else 'Flow'} · {'com' if cert else 'sem'} certificado", rows))
    return var

def ext_subscriber(app):
    rows = [ator("Pub/Sub API (ou CometD)", "API do Salesforce que entrega os eventos para sistemas externos que estão assinando.", "barramento", EXT),
            ator(EXT, "O sistema de fora do Salesforce que assina os eventos. Guarda a posição do último evento lido (replay ID) para retomar se cair.", "—", "Pub/Sub API"),
            R("Assinatura gerenciada", "ManagedEventSubscription", "lê/referencia", "Assinatura de eventos administrada pela plataforma: guarda qual evento o cliente externo assina e de onde retomar se ele cair (recurso Beta).", EXT, "—", "Opcional")]
    rows += app_in(app, "JWT")
    rows += [R("Permission Set (leitura do evento / do objeto)", "PermissionSet", "autoriza", "Dá ao usuário de integração permissão para ler o evento ou o objeto monitorado.", "plataforma", "—")]
    return rows

def pe_external():
    var = []
    for pub in ("APEX", "FLOW", "API"):
        for app in ("CA", "ECA"):
            rows = {"APEX": [R("Classe publicadora", "ApexClass", "executa", "Classe Apex que publica o evento (`EventBus.publish`).", "trigger/serviço", "Platform Event")],
                    "FLOW": [R("Flow publicador", "Flow", "executa", "Automação sem código que publica o evento criando um registro dele.", "plataforma", "Platform Event")],
                    "API": [ator("Outro sistema", "Outro sistema que publica o evento pela API.", "—", "Platform Event")]}[pub]
            rows += pe_def() + ext_subscriber(app)
            var.append((f"Publicador {pub} · assinante autenticado por {APPS[app]}", rows))
    return var

def cdc():
    var = []
    for sub in ("EXT_CA", "EXT_ECA", "APEX"):
        for e in (["-"] if sub != "APEX" else ALL_E):
            rows = [ator("Gravação do registro", "Qualquer criação, alteração ou exclusão de registro do objeto monitorado.", "—", "plataforma"),
                    R("Objeto monitorado", "CustomObject", "lê/referencia", "Objeto cujas alterações (criar, editar, excluir, restaurar) viram eventos automaticamente.", "—", "Change Event"),
                    R("Membro do canal ChangeEvents", "PlatformEventChannelMember", "lê/referencia", "Liga o Change Data Capture (CDC) para o objeto: a partir daí, toda alteração gera um evento (ex.: AccountChangeEvent) sem nenhum código.", "plataforma", "Change Event"),
                    ator("Change Event", "Evento criado automaticamente pela plataforma a cada alteração (`<Objeto>ChangeEvent`). Não aparece como arquivo no projeto.", "plataforma", "assinantes")]
            if sub == "APEX":
                rows += [R("Trigger do change event", "ApexTrigger", "executa", "Código que roda quando chega o evento de mudança. Agenda uma tarefa em segundo plano para chamar o sistema externo.", "barramento", "Classe Queueable"),
                         R("Configuração do assinante", "PlatformEventSubscriberConfig", "lê/referencia", "Define com qual usuário o trigger roda e quantos eventos processa de uma vez.", "plataforma", "—", "Opcional")]
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
            rows = [R("Canal customizado", "PlatformEventChannel", "lê/referencia", f"Canal próprio (tipo {'data' if tipo=='CDC' else 'event'}) que junta só os eventos que interessam a quem vai assinar.", "plataforma", "assinantes"),
                    R("Membro do canal", "PlatformEventChannelMember", "lê/referencia", "Coloca um evento ou objeto no canal e pode acrescentar campos extras (enriquecimento) ou filtrar quais eventos passam.", "Canal", "—")]
            rows += (pe_def() if tipo == "PE" else [R("Objeto monitorado", "CustomObject", "lê/referencia", "Objeto cujas alterações geram os eventos de mudança.", "—", "Canal")])
            rows += ext_subscriber(app)
            var.append((f"{tipo} · {APPS[app]}", rows))
    return var

def relay():
    var = []
    for tipo in ("PE", "CDC"):
        rows = (pe_def() if tipo == "PE" else [R("Objeto monitorado", "CustomObject", "lê/referencia", "Objeto cujas alterações geram os eventos de mudança.", "—", "Canal")])
        rows += [R("Canal customizado", "PlatformEventChannel", "lê/referencia", "Canal de onde o Event Relay pega os eventos para repassar.", "plataforma", "Event Relay"),
                 R("Membro do canal", "PlatformEventChannelMember", "lê/referencia", "Indica quais eventos entram no canal.", "Canal", "—"),
                 R("Event Relay", "EventRelayConfig", "executa", "Repassa automaticamente os eventos do canal para a AWS (Amazon EventBridge), sem código.", "plataforma", "Named Credential"),
                 R("Named Credential (destino AWS)", "NamedCredential", "lê/referencia", "Guarda a conta e a região da AWS para onde os eventos vão.", "Event Relay", "Amazon EventBridge"),
                 ator("Amazon EventBridge", "Serviço da AWS que recebe os eventos e os distribui para outros serviços, conforme regras.", "Event Relay", "—")]
        var.append((tipo, rows))
    return var

def sched_batch(tipo):
    var = []
    for sentido in ("ENVIA", "BUSCA"):
        for e in ALL_E:
            rows = [ator("Agendamento", "Agendamento que diz quando a classe roda. É feito na tela ou por código e não fica no projeto (N01).", "—", "Classe Schedulable"),
                    R("Classe Schedulable", "ApexClass", "executa", "Classe que a plataforma executa no horário agendado; ela só dá a partida no processamento.", "Agendamento", "Batch" if tipo == "BATCH" else "Queueable")]
            if tipo == "BATCH":
                rows += [R("Classe Batch", "ApexClass", "executa", "Processamento em lotes (Batch Apex): seleciona os registros e os processa em blocos; em cada bloco chama o sistema externo. Bom para grandes volumes.", "Classe Schedulable", "Sistema externo")]
                c = "Classe Batch"
            else:
                rows += [R("Classe Queueable encadeada", "ApexClass", "executa", "Tarefa em segundo plano que busca uma página de dados e agenda a próxima, até acabar. Bom para APIs que devolvem os dados em páginas.", "Classe Schedulable / ela mesma", "Sistema externo")]
                c = "Classe Queueable encadeada"
            rows += endpoint(e, c)
            rows += [R("Objeto de destino/origem", "CustomObject + CustomField (External ID)", "executa (DML)", "Objeto cujos registros são enviados ao sistema externo ou atualizados com o que voltou. O campo External ID evita duplicidade.", c, "—")]
            rows += logrows(c) + killswitch(c)
            var.append((f"{'Envia dados' if sentido=='ENVIA' else 'Busca dados'} · endpoint {e}", rows))
    return var

def sched_flow():
    var = []
    for acao in ("HTTP", "ES", "APEX"):
        for e in (NC_E if acao != "APEX" else ALL_E):
            rows = [R("Flow agendado", "Flow (Schedule-Triggered)", "executa", "Automação sem código que roda em horários definidos sobre os registros que atendem a um filtro.", "plataforma (agenda)", "ação")]
            if acao == "APEX":
                rows += [R("Classe invocável", "ApexClass", "executa", "Classe Apex que chama o sistema externo.", "Flow agendado", "Sistema externo")]; c = "Classe invocável"
            else:
                rows += [R("Ação HTTP Callout / External Service", "ExternalServiceRegistration", "lê/referencia", "Cadastro da operação da API externa que o Flow chama.", "Flow agendado", "Named Credential")]; c = "Flow agendado"
            rows += endpoint(e, c)
            var.append((f"Ação {acao} · endpoint {e}", rows))
    return var

def cross_org_bulk():
    var = []
    for m in ("BATCH", "QUEUE"):
        for e in ("E1", "E2", "E5"):
            rows = [R("Classe de carga", "ApexClass", "executa", f"Tarefa em segundo plano ({'Batch' if m=='BATCH' else 'Queueable'}) que envia uma carga grande de dados para a outra org pela Bulk API 2.0.", "agenda/trigger", "org de destino")]
            rows += endpoint(e, "Classe de carga", "Org Salesforce de destino")
            rows += [R("Connected App / External Client App (na org de destino)", "ConnectedApp ou ExternalClientApplication", "autoriza", "Cadastro, na outra org, que permite que esta org entre lá com um token.", "Named Credential", "—")]
            var.append((f"{m} · endpoint {e}", rows))
    return var

def staging():
    var = []
    for proc in ("BATCH", "QUEUE"):
        for e in ALL_E:
            rows = gatilho_trigger()[:3] + [
                R("Classe handler", "ApexClass", "executa", "Em vez de chamar o sistema externo na hora, grava um pedido numa fila (objeto próprio) com status PENDENTE.", "Trigger", "Objeto de fila"),
                R("Objeto de fila / staging", "CustomObject (__c) + CustomField", "executa (DML)", "Objeto que funciona como fila: guarda o que precisa ser enviado, o status, quantas tentativas já houve e o último erro. Permite reprocessar com segurança.", "Classe handler", "processador"),
                ator("Agendamento", "Agendamento que diz quando o processamento roda. Não fica no projeto (N01).", "—", "processador")]
            if proc == "BATCH":
                rows += [R("Classe Schedulable + Batch", "ApexClass", "executa", "Processa a fila em lotes: pega os pendentes, chama o sistema externo e atualiza o status e o número de tentativas.", "Agendamento", "Sistema externo")]
            else:
                rows += [R("Classe Queueable", "ApexClass", "executa", "Processa a fila em segundo plano e agenda a si mesma de novo enquanto houver itens.", "Classe handler ou Schedulable", "Sistema externo")]
            c = "processador"
            rows += endpoint(e, c) + [R("Notificação de falha", "CustomNotificationType ou EmailTemplate", "executa", "Avisa alguém (notificação ou e-mail) quando um item falhou em todas as tentativas.", c, "—", "Opcional")]
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
            rows = ext_start("Bulk API 2.0") + app_in(a, f) + [ator("Bulk API 2.0", "API do Salesforce para cargas grandes: recebe um arquivo CSV e processa em lotes, em segundo plano.", EXT, "Objeto de destino")]
            rows += dados_destino("Bulk API 2.0", upsert=(op == "UPSERT"))
            var.append((f"{APPS[a]} · {FLOWS[f]} · {op.lower()}", rows))
    return var

def pe_in():
    var = []
    for a, f in in_variants(flows=("JWT", "CC")):
        for via in ("REST", "PUBSUB"):
            for sub in ("APEX", "FLOW"):
                rows = [ator(EXT, "O sistema de fora do Salesforce. Publica o evento pela API.", "—", "API")] + app_in(a, f)
                rows += [ator("REST API (sObject __e)" if via == "REST" else "Pub/Sub API (Publish)", "API do Salesforce que recebe a publicação do evento.", EXT, "Platform Event")]
                rows += pe_def("API") + [R("Permission Set (Create no evento)", "PermissionSet", "autoriza", "Dá ao usuário de integração permissão para publicar o evento.", "plataforma", "—")]
                if sub == "APEX":
                    rows += [R("Trigger do evento", "ApexTrigger", "executa", "Código que roda quando o evento chega; processa os dados e grava no Salesforce.", "barramento", "Objeto de destino"),
                             R("Configuração do assinante", "PlatformEventSubscriberConfig", "lê/referencia", "Define com qual usuário o trigger roda e quantos eventos processa de uma vez.", "plataforma", "—", "Opcional")]
                    c = "Trigger do evento"
                else:
                    rows += [R("Flow disparado por evento", "Flow", "executa", "Automação sem código que roda quando o evento chega; processa os dados e grava no Salesforce.", "barramento", "Objeto de destino")]; c = "Flow disparado por evento"
                rows += dados_destino(c)
                var.append((f"{APPS[a]} · {FLOWS[f]} · publica via {via} · assinante {sub}", rows))
    return var

def rest_enqueue():
    var = []
    for a, f in in_variants(flows=("JWT", "CC")):
        for m in ("QUEUE", "PE"):
            rows = ext_start("Apex REST") + app_in(a, f) + [
                ator("Apex REST (/services/apexrest)", "Endereço do Salesforce chamado pelo sistema externo.", EXT, "Classe Apex REST"),
                R("Classe Apex REST", "ApexClass", "executa", "Recebe a chamada, confere os dados e responde na hora \"recebido\" (202). O processamento pesado fica para depois, em segundo plano.", "Apex REST", "Queueable" if m == "QUEUE" else "Platform Event")]
            if m == "QUEUE":
                rows += [R("Classe Queueable", "ApexClass", "executa", "Tarefa em segundo plano que faz o processamento depois que o sistema externo já recebeu a resposta.", "Classe Apex REST", "Objeto de destino")]; c = "Classe Queueable"
            else:
                rows += pe_def("Classe Apex REST") + [R("Trigger do evento", "ApexTrigger", "executa", "Código que roda quando o evento chega e faz o processamento.", "barramento", "Objeto de destino")]; c = "Trigger do evento"
            rows += dados_destino(c) + logrows(c)
            var.append((f"{APPS[a]} · {FLOWS[f]} · delega para {'Queueable' if m=='QUEUE' else 'Platform Event'}", rows))
    return var

def email_in():
    var = []
    for dest in ("DML", "QUEUE"):
        rows = [ator(EXT, "O sistema de fora do Salesforce. Manda um e-mail para o endereço do Email Service.", "—", "Email Service"),
                R("Email Service", "EmailServicesFunction", "executa", "Cria um endereço de e-mail no Salesforce. Define quem pode enviar, com qual usuário o processamento roda e o que fazer em caso de erro.", EXT, "Classe handler"),
                R("Classe handler", "ApexClass", "executa", "Classe Apex que recebe cada e-mail que chega ao endereço (`Messaging.InboundEmailHandler`) e lê o texto e os anexos.", "Email Service", "Objeto de destino" if dest == "DML" else "Queueable")]
        if dest == "QUEUE":
            rows.append(R("Classe Queueable", "ApexClass", "executa", "Tarefa em segundo plano para o processamento mais pesado.", "Classe handler", "Objeto de destino"))
        rows += dados_destino("Classe handler", upsert=False)
        var.append(("Processa direto" if dest == "DML" else "Enfileira processamento", rows))
    return var

def files_in():
    var = []
    for a, f in in_variants(flows=("JWT", "CC")):
        for sub in ("APEX", "FLOW"):
            rows = ext_start("REST API (ContentVersion)") + app_in(a, f) + [
                ator("REST API (ContentVersion)", "API do Salesforce que recebe o arquivo enviado pelo sistema externo.", EXT, "ContentVersion"),
                ator("ContentVersion / ContentDocumentLink", "Objetos padrão que guardam arquivos e o vínculo com os registros. São dados, não aparecem no projeto.", "REST API", "processador")]
            rows += [R("Trigger em ContentVersion" if sub == "APEX" else "Flow record-triggered em ContentVersion", "ApexTrigger" if sub == "APEX" else "Flow", "executa", "Roda quando o arquivo chega: confere o conteúdo e o vincula ao registro certo.", "plataforma (DML)", "Objeto de destino")]
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
            rows += [ator("Sistema de destino final", "Sistema final (ERP, legado etc.) que o middleware chama. O Salesforce não fala com ele direto.", MULE, "—")]
            var.append((f"Origem {ORIG_NOME[o]} · endpoint {e}", rows))
    for m in ("FUTURE", "QUEUE"):
        for e in ALL_E:
            rows = gatilho_trigger(); a, c = async_apex(m, "Classe handler")
            rows += a + endpoint(e, c, MULE) + [ator("Sistema de destino final", "Sistema final que o middleware chama. O Salesforce não fala com ele direto.", MULE, "—")]
            var.append((f"Origem Trigger + {'@future' if m=='FUTURE' else 'Queueable'} · endpoint {e}", rows))
    return var

def mid_sub():
    var = []
    for tipo in ("PE", "CDC"):
        for app in ("CA", "ECA"):
            rows = (pe_def() if tipo == "PE" else [R("Membro do canal ChangeEvents", "PlatformEventChannelMember", "lê/referencia", "Liga o Change Data Capture para o objeto: toda alteração vira um evento, sem código.", "plataforma", "Change Event"), R("Objeto monitorado", "CustomObject", "lê/referencia", "Objeto cujas alterações geram os eventos.", "—", "Change Event")])
            rows += [ator("Pub/Sub API", "API do Salesforce que entrega os eventos ao middleware.", "barramento", MULE), ator(MULE, "Middleware (ex.: MuleSoft). Assina os eventos com o conector do Salesforce e repassa para os sistemas internos.", "—", "sistemas de destino")]
            rows += app_in(app, "JWT", MULE)
            rows += [R("Permission Set (leitura do evento/objeto)", "PermissionSet", "autoriza", "Dá ao usuário do middleware permissão para ler o evento ou o objeto.", "plataforma", "—")]
            var.append((f"{tipo} · {APPS[app]}", rows))
    return var

def mid_in(api_kind):
    var = []
    for a, f in in_variants(flows=("JWT", "CC")):
        kinds = ("PADRAO", "APEXREST") if api_kind == "SYNC" else ("BULK",)
        for k in kinds:
            rows = [ator(MULE, "Middleware (ex.: MuleSoft). Organiza o fluxo entre sistemas e chama o Salesforce.", "sistema de origem", "Salesforce")] + app_in(a, f, MULE)
            if k == "APEXREST":
                rows += [ator("Apex REST", "Endereço do Salesforce chamado pelo sistema externo.", MULE, "Classe Apex REST")] + APEX_REST[1]
            else:
                api = {"PADRAO": "REST/Composite API padrão", "BULK": "Bulk API 2.0"}[k]
                rows += [ator(api, "Endereço do Salesforce chamado pelo sistema externo.", MULE, "Objeto de destino")] + dados_destino(api)
            var.append((f"{APPS[a]} · {FLOWS[f]} · {k}", rows))
    return var

def mid_poll():
    var = []
    for a, f in in_variants(flows=("JWT", "CC")):
        for ctrl in ("LMD", "CAMPO"):
            rows = [ator(MULE, "Middleware (ex.: MuleSoft) que, de tempos em tempos, consulta o Salesforce em busca de novidades.", "agenda do middleware", "REST API (query)")] + app_in(a, f, MULE)
            rows += [ator("REST API (query)", "API do Salesforce que executa a consulta pedida.", MULE, "Objeto consultado"),
                     R("Objeto consultado", "CustomObject + CustomField", "lê/referencia", "Objeto que o middleware consulta periodicamente.", "REST API", "—")]
            if ctrl == "CAMPO":
                rows += [R("Campo de controle", "CustomField", "lê/referencia + executa (DML)", "Campo que marca o que já foi enviado. O middleware lê os registros não marcados e marca depois de processar.", MULE, "triggers do objeto")]
            var.append((f"{APPS[a]} · {FLOWS[f]} · controle por {'LastModifiedDate' if ctrl=='LMD' else 'campo customizado'}", rows))
    return var

def mid_ip():
    var = []
    for caller in ("OMNISCRIPT", "FLEXCARD", "APEX", "APEXREST"):
        for e in ("E1", "E2", "E3"):
            ent = {"OMNISCRIPT": [R("OmniScript", "OmniScript", "executa", "Processo guiado do OmniStudio que chama a Integration Procedure.", "Usuário", "Integration Procedure")],
                   "FLEXCARD": [R("FlexCard", "OmniUiCard", "executa", "Cartão de tela do OmniStudio que busca os dados na Integration Procedure.", "Usuário", "Integration Procedure")],
                   "APEX": [R("Classe Apex", "ApexClass", "executa", "Classe Apex que chama a Integration Procedure.", "trigger/serviço", "Integration Procedure")],
                   "APEXREST": [ator(EXT, "O sistema de fora do Salesforce que chama a org.", "—", "Apex REST")] + app_in("CA", "JWT") + [R("Classe Apex REST", "ApexClass", "executa", "Classe Apex REST que deixa a Integration Procedure ser chamada de fora do Salesforce.", "Apex REST", "Integration Procedure")]}[caller]
            rows = ent + [R("Integration Procedure", "OmniIntegrationProcedure", "executa", "Roteiro de integração do OmniStudio, montado sem código: encadeia chamadas, decisões e cache. Faz o papel de um middleware dentro do Salesforce.", caller, "HTTP Actions / Data Mappers"),
                          R("Data Mapper (Extract/Load/Transform)", "OmniDataTransform", "executa", "Ferramenta de mapeamento do OmniStudio: lê e grava registros e converte dados de um formato para outro.", "Integration Procedure", "objetos")]
            if e == "E3":
                rows += [R("Remote Site Setting", "RemoteSiteSetting", "autoriza", "Lista de domínios externos permitidos. Como a URL é fixa (sem Named Credential), o domínio **precisa** estar cadastrado aqui.", "plataforma", "—"), ator(EXT, "O sistema de fora do Salesforce. Recebe a chamada e devolve a resposta.", "Integration Procedure", "—")]
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
                    rows = [R("Flow", "Flow", "executa", "Automação sem código que chama a operação da API do MuleSoft como se fosse uma ação pronta.", "gatilho do Flow", "Registro de External Service")]; c = "Flow"
                else:
                    rows = [R("Classe Apex", "ApexClass", "executa", "Classe Apex que chama a operação da API do MuleSoft pelas classes geradas automaticamente (`ExternalService.<Servico>`).", "trigger/serviço/UI", "Registro de External Service")]; c = "Classe Apex"
                rows += [R("Registro de External Service", "ExternalServiceRegistration", "lê/referencia", f"Cadastro da API do MuleSoft (origem {prov}). A plataforma transforma cada operação em ação para Flow e classe para Apex.", c, "Named Credential")]
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
        R("External Object", "CustomObject (__x)", "lê/referencia", "Objetos \"espelho\" (`__x`) que mostram dados da outra org sem copiar.", "Página", "External Data Source"),
        R("External Data Source (cross-org)", "ExternalDataSource", "lê/referencia", "Cadastro da outra org: endereço e com qual identidade consultar.", "External Object", "Org remota"),
        R("Permission Set", "PermissionSet", "autoriza", "Dá ao usuário permissão para ver os objetos espelho.", "plataforma", "—"),
        ator("Org Salesforce remota", "A outra org Salesforce, que responde às consultas.", "External Data Source", "—")]))
    for e in ("E1", "E2", "E5"):
        rows = [R("Classe cliente (org A)", "ApexClass", "executa", "Classe Apex desta org (A) que chama a outra org (B).", "trigger/UI/agenda", "Org B")]
        rows += endpoint(e, "Classe cliente (org A)", "Org B")
        rows += [R("Connected App / External Client App (org B)", "ConnectedApp ou ExternalClientApplication", "autoriza", "Cadastro, na org B, que permite que a org A entre lá com um token.", "Named Credential", "—"),
                 R("Classe Apex REST (org B)", "ApexClass", "executa", "Endpoint na org B que recebe a chamada e processa os dados.", "Org A", "objetos da org B", "Opcional (ou API padrão)")]
        var.append((f"Apex REST org→org · endpoint {e}", rows))
    return var

def ui_int():
    var = []
    var.append(("Botão/link de URL", [USER, R("Botão ou link", "WebLink", "executa", "Botão ou link que abre o sistema externo em outra aba, levando dados do registro na URL. Não há troca de dados no servidor.", "Usuário", "Sistema externo"), R("Layout", "Layout", "lê/referencia", "Configuração da página que faz o botão aparecer.", "plataforma", "—"), ator(EXT, "O sistema externo, aberto no navegador do usuário.", "WebLink", "—")]))
    var.append(("Web Tab", [USER, R("Aba web", "CustomTab", "executa", "Aba do menu que mostra o sistema externo dentro do Salesforce.", "Usuário", "Sistema externo"), R("App", "CustomApplication", "lê/referencia", "App que contém a aba.", "plataforma", "—"), ator(EXT, "O sistema externo, mostrado dentro do Salesforce.", "CustomTab", "—")]))
    for host in ("VF", "PAGE"):
        rows = [USER]
        rows += ([R("Página Visualforce", "ApexPage", "executa", "Página Visualforce que mostra o sistema externo dentro do Salesforce (Canvas).", "Usuário", "Canvas App")] if host == "VF" else [R("Página Lightning", "FlexiPage", "executa", "Página Lightning com o componente Canvas, que mostra o sistema externo dentro do Salesforce.", "Usuário", "Canvas App")])
        rows += [R("Connected App com Canvas", "ConnectedApp", "autoriza + lê", "Cadastro do sistema externo como Canvas: endereço, como o Salesforce passa a identidade do usuário (signed request ou OAuth) e onde ele pode aparecer.", "host", "Sistema externo"), ator(EXT, "Aplicação web externa que recebe do Salesforce a identidade do usuário (signed request).", "Canvas", "—")]
        var.append((f"Canvas em {'Visualforce' if host=='VF' else 'Lightning Page'}", rows))
    var.append(("Canvas via External Client App", [USER, R("Página Lightning", "FlexiPage", "executa", "Página Lightning com o componente Canvas.", "Usuário", "Canvas App"),
        R("External Client App", "ExternalClientApplication", "autoriza", "Cadastro (modelo novo) do sistema externo no Salesforce.", "host", "—"),
        R("Configuração Canvas do app", "ExtlClntAppCanvasSettings", "autoriza + lê", "Parte do External Client App com o endereço e o acesso do Canvas.", "External Client App", "Sistema externo"), ator(EXT, "Aplicação web externa mostrada dentro do Salesforce.", "Canvas", "—")]))
    var.append(("iframe em LWC", [USER, R("Componente LWC", "LightningComponentBundle", "executa", "Componente de tela que mostra o sistema externo numa moldura (`<iframe>`).", "Página", "Sistema externo"), R("CSP Trusted Site", "CspTrustedSite", "autoriza", "Lista de domínios que o **navegador** pode mostrar em moldura nas páginas do Salesforce (regra CSP).", "navegador", "—"), ator(EXT, "O sistema externo. Precisa permitir ser mostrado em moldura dentro de outro site.", "LWC", "—")]))
    return var

def sso():
    return [
     ("SAML com IdP externo", [ator("IdP externo", "Provedor de identidade externo que faz o login do usuário.", "Usuário", "Salesforce"), R("Configuração SAML", "SamlSsoConfig", "autoriza", "Configuração do login único (SSO) via SAML: quem é o provedor de identidade, o certificado e como achar o usuário correspondente.", "IdP", "—"), R("Certificate", "Certificate", "autoriza", "Certificado usado para conferir ou assinar as mensagens de login.", "SAML", "—", "Opcional")]),
     ("OpenID Connect via Auth Provider", [ator("Provedor externo", "Provedor de login externo que confirma quem é o usuário.", "Usuário", "Salesforce"), R("Auth Provider", "AuthProvider", "autoriza", "Cadastro do provedor de login externo (OpenID Connect).", "login", "Registration Handler"), R("Registration Handler", "ApexClass", "executa", "Classe Apex que cria ou atualiza o usuário do Salesforce com os dados vindos do provedor de login.", "Auth Provider", "User")]),
     ("Salesforce como IdP", [ator("App externo", "Aplicação externa que pede ao Salesforce para confirmar quem é o usuário.", "Usuário", "Salesforce"), R("Connected App (SAML/OIDC)", "ConnectedApp", "autoriza", "Cadastro do sistema externo que vai usar o Salesforce como provedor de login; o Salesforce emite a confirmação de identidade.", "App externo", "—")]),
    ]

OUTRAS = [
 D("N.1", "Org ↔ org", "Integração entre orgs Salesforce.", org_org(), validar=["Salesforce to Salesforce (legado) não incluído: verificar se há metadata associada."]),
 D("N.2", "Integração de UI", "O usuário vê ou usa outro sistema; pouca ou nenhuma troca de dados no servidor.", ui_int()),
 D("N.3", "Identidade (SSO)", "Integra o login, não os dados.", sso()),
 D("N.4", "Data Cloud", "Ingestão e ativação de dados.", [("A validar", [ator("Data Cloud", "Data Cloud: os metadata types envolvidos (fluxos de dados, fontes e ativações) ainda precisam ser confirmados.", "—", "—")])], validar=["Toda a família de metadata do Data Cloud."]),
]

SECOES = [
 ("out-sync", "OUT SYNC — Salesforce chama o externo e espera", OUT_SYNC),
 ("in-sync", "IN SYNC — externo chama o Salesforce e espera", IN_SYNC),
 ("out-async", "OUT ASYNC — Salesforce envia sem esperar", OUT_ASYNC),
 ("in-async", "IN ASYNC — externo envia; Salesforce processa depois", IN_ASYNC),
 ("mid", "MID — middleware / MuleSoft", MID),
 ("outras", "Outras dinâmicas", OUTRAS),
]

# Blocos reutilizáveis de componentes. Cada linha:
# (componente, metadata_type, relacao, papel, acionado_por, aciona, obrigatoriedade)
NM = "não é metadata"
EXT = "Sistema externo"

def R(c, t, rel, papel, por, aciona, ob="Obrigatório"):
    return (c, t, rel, papel, por, aciona, ob)

def ator(c, papel, por, aciona, ob="Obrigatório"):
    return (c, NM, "ator", papel, por, aciona, ob)

# ---------- Fontes de endpoint/autenticação para callout Apex (OUT) ----------
ENDPOINTS = {
 "E1": "Named Credential (namedCredentialType=SecuredEndpoint) + External Credential",
 "E2": "Named Credential legada (namedCredentialType=Legacy, autenticação embutida)",
 "E3": "URL fixa no código Apex + Remote Site Setting",
 "E4": "Custom Metadata (endpoint, client_id etc.) + Remote Site Setting; token obtido por callout próprio",
 "E5": "Custom Metadata guarda o NOME da Named Credential + Named Credential + External Credential",
 "E6": "Custom Setting ou Custom Label (endpoint) + Remote Site Setting",
}

def endpoint(code, caller, alvo=EXT):
    if code == "E1":
        return [
         R("Named Credential", "NamedCredential", "lê/referencia", "Guarda o endereço (URL) do sistema externo. O código não escreve a URL: usa `callout:Nome` e a plataforma troca pelo endereço cadastrado aqui. Como o domínio já está cadastrado na Named Credential, **não é preciso Remote Site Setting**.", caller, "External Credential"),
         R("External Credential", "ExternalCredential", "autoriza", "Guarda **como** se autenticar no sistema externo (OAuth, JWT, usuário e senha ou cabeçalho próprio). A plataforma gera o token ou o cabeçalho e o coloca na requisição; o código não vê a credencial.", "Named Credential", alvo),
         R("Permission Set (acesso ao principal)", "PermissionSet", "autoriza", "Dá permissão para o usuário que está rodando o código usar a credencial (campo `externalCredentialPrincipalAccesses`). Sem isso, o callout falha por falta de acesso.", "plataforma (no momento do callout)", "—"),
         R("Certificate", "Certificate", "autoriza", "Certificado digital usado quando o sistema externo exige: assina o token JWT ou prova a identidade do Salesforce na conexão (mutual TLS).", "External Credential", "—", "Opcional"),
         ator(alvo, "O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta.", caller, "—")]
    if code == "E2":
        return [
         R("Named Credential (legada)", "NamedCredential", "lê/referencia + autoriza", "Modelo antigo de Named Credential: guarda no mesmo cadastro o endereço e a autenticação (senha, OAuth ou JWT). Assim como no modelo novo, **dispensa Remote Site Setting**.", caller, alvo),
         R("Auth Provider", "AuthProvider", "autoriza", "Quando a autenticação é OAuth, é ele que conversa com o servidor de login do sistema externo para conseguir o token.", "Named Credential", "—", "Opcional"),
         R("Certificate", "Certificate", "autoriza", "Certificado digital usado quando o sistema externo exige assinatura do JWT ou mutual TLS.", "Named Credential", "—", "Opcional"),
         ator(alvo, "O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta.", caller, "—")]
    if code == "E3":
        return [
         R("Remote Site Setting", "RemoteSiteSetting", "autoriza", "Lista de domínios externos que o Apex pode chamar. Como a URL está escrita direto no código (sem Named Credential), o domínio **precisa** estar cadastrado aqui, senão a plataforma bloqueia a chamada.", "plataforma (no momento do callout)", "—"),
         R("Certificate", "Certificate", "autoriza", "Certificado digital apresentado ao sistema externo na conexão (mutual TLS), indicado no código por `setClientCertificateName`.", caller, "—", "Opcional"),
         ator(alvo, "O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta.", caller, "—")]
    if code == "E4":
        return [
         R("Tipo de Custom Metadata", "CustomObject (__mdt) + CustomField", "lê/referencia", "É a \"tabela\" de configuração da integração: define quais campos existem (URL, caminho, client_id, timeout, ligado/desligado).", caller, "registro de Custom Metadata"),
         R("Registro de Custom Metadata", "CustomMetadata", "lê/referencia", "É a \"linha\" dessa tabela com os valores do ambiente (URL, client_id). O código lê daqui para saber onde chamar. Atenção: guardar senha ou client_secret aqui é risco (anti-padrão A01).", caller, "—"),
         R("Classe de token", "ApexClass", "executa", "Como não há Named Credential para cuidar do login, o próprio código chama o servidor de autenticação do sistema externo e obtém o token antes da chamada principal.", caller, "endpoint de token do sistema externo", "Opcional"),
         R("Partição de cache", "PlatformCachePartition", "lê/referencia", "Memória temporária da plataforma. Guarda o token até ele vencer, para não pedir um token novo a cada chamada.", "Classe de token", "—", "Opcional"),
         R("Remote Site Setting", "RemoteSiteSetting", "autoriza", "Lista de domínios que o Apex pode chamar. Como a URL vem de configuração (e não de uma Named Credential), cada domínio usado **precisa** estar cadastrado aqui — normalmente um por ambiente.", "plataforma (no momento do callout)", "—"),
         ator(alvo, "O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta.", caller, "—")]
    if code == "E5":
        return [
         R("Tipo de Custom Metadata", "CustomObject (__mdt) + CustomField", "lê/referencia", "É a \"tabela\" de configuração: tem um campo com o **nome** da Named Credential a usar e outros parâmetros não sensíveis.", caller, "registro de Custom Metadata"),
         R("Registro de Custom Metadata", "CustomMetadata", "lê/referencia", "É a \"linha\" de configuração do ambiente: diz qual Named Credential usar e os parâmetros (caminho, timeout, ligado/desligado). Trocar de ambiente é só mudar esse registro.", caller, "—"),
         R("Named Credential", "NamedCredential", "lê/referencia", "Guarda o endereço do sistema externo. O código monta `callout:` + o nome lido do Custom Metadata. Por ser Named Credential, **dispensa Remote Site Setting**.", caller, "External Credential"),
         R("External Credential", "ExternalCredential", "autoriza", "Guarda como se autenticar no sistema externo; a plataforma aplica a credencial na requisição sem o código ver o segredo.", "Named Credential", alvo),
         R("Permission Set (acesso ao principal)", "PermissionSet", "autoriza", "Dá permissão para o usuário que roda o código usar a credencial. Sem isso, o callout falha.", "plataforma (no momento do callout)", "—"),
         ator(alvo, "O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta.", caller, "—")]
    if code == "E6":
        return [
         R("Custom Setting ou Custom Label", "CustomObject (Custom Setting) ou CustomLabels", "lê/referencia", "Guarda a URL do sistema externo por ambiente. Custom Label fica no repositório; o valor de Custom Setting é dado e não fica (N06).", caller, "—"),
         R("Remote Site Setting", "RemoteSiteSetting", "autoriza", "Lista de domínios que o Apex pode chamar. Como a URL vem de configuração, o domínio **precisa** estar cadastrado aqui.", "plataforma (no momento do callout)", "—"),
         ator(alvo, "O sistema de fora do Salesforce. Recebe a chamada, processa e devolve a resposta.", caller, "—")]
    raise KeyError(code)

ALL_E = ["E1", "E2", "E3", "E4", "E5", "E6"]
NC_E = ["E1", "E2"]  # Flow HTTP Callout / External Services exigem Named Credential

# ---------- Autenticação de entrada (IN) ----------
APPS = {"CA": "Connected App", "ECA": "External Client App"}
FLOWS = {
 "JWT": "OAuth 2.0 JWT Bearer",
 "CC": "OAuth 2.0 Client Credentials",
 "WS": "OAuth 2.0 Web Server + Refresh Token",
 "UP": "OAuth 2.0 Username-Password (legado, desaconselhado)",
}

def app_in(app, flow, caller=EXT):
    if app == "CA":
        extra = " (`isClientCredentialEnabled` + `oauthClientCredentialUser`)" if flow == "CC" else ""
        rows = [R("Connected App", "ConnectedApp", "autoriza", f"Cadastro do sistema externo no Salesforce (modelo antigo). Diz quem pode pedir token, por qual fluxo ({FLOWS[flow]}{extra}) e com quais permissões (`scopes`). Sem ele, o sistema externo não consegue entrar.", caller, "Salesforce (emissão do token)")]
    else:
        rows = [
         R("External Client App", "ExternalClientApplication", "autoriza", "Cadastro do sistema externo no Salesforce (modelo novo, recomendado). Sem ele, o sistema externo não consegue obter token para chamar a org.", caller, "Salesforce (emissão do token)"),
         R("Configurações OAuth do app", "ExtlClntAppOauthSettings", "autoriza", f"Diz o que o token poderá fazer (escopos, campo `commaSeparatedOauthScopes`) no fluxo {FLOWS[flow]}.", "External Client App", "—"),
         R("Configurações OAuth globais", "ExtlClntAppGlobalOauthSettings", "autoriza", "Identificação do app: client_id (`consumerKey`), client_secret (`consumerSecret`, segredo: nunca copiar), certificado e quais fluxos estão ligados.", "External Client App", "—"),
         R("Políticas OAuth configuráveis", "ExtlClntAppOauthConfigurablePolicies", "autoriza", "Regras definidas pelo admin: quais perfis/Permission Sets podem usar o app, restrição de IP e o usuário em nome de quem o fluxo Client Credentials roda.", "External Client App", "—"),
         R("Políticas gerais", "ExtlClntAppConfigurablePolicies", "autoriza", "Liga ou desliga o app e suas partes (plugins) nesta org.", "External Client App", "—")]
    if flow == "JWT":
        rows.append(R("Certificate (público, do cliente)", "Certificate", "autoriza", "No fluxo JWT, o sistema externo assina o pedido de token com a chave privada dele; o Salesforce confere a assinatura com este certificado público, guardado no próprio app.", "app", "—", "Obrigatório (no app)"))
    if flow == "CC":
        rows.append(ator("Usuário run-as", "No fluxo Client Credentials não há login de pessoa: tudo roda em nome deste usuário, configurado no app.", "app", "—"))
    else:
        rows.append(ator("Usuário de integração", "Usuário em nome de quem a integração entra no Salesforce. O que ele pode ver e fazer é o que a integração pode ver e fazer.", "app", "—"))
    rows += [
     R("Perfil do usuário de integração", "Profile", "autoriza", "Perfil base do usuário de integração. O recomendado é um perfil mínimo, só com acesso via API.", "plataforma", "—"),
     R("Permission Set / Permission Set Group", "PermissionSet / PermissionSetGroup", "autoriza", "Dá ao usuário de integração só os acessos de que ele precisa: objetos, campos, classes Apex e o app.", "plataforma", "—"),
     R("Escopo OAuth customizado", "OauthCustomScope", "autoriza", "Escopo criado pela empresa para limitar ainda mais o que o token pode acessar.", "app", "—", "Opcional")]
    return rows

def in_variants(apps=("CA", "ECA"), flows=("JWT", "CC", "WS", "UP")):
    return [(a, f) for a in apps for f in flows]

def logrows(caller):
    return [R("Objeto de log de integração", "CustomObject (__c) + CustomField", "executa (DML)", "Objeto criado pela empresa para guardar o histórico de cada chamada (o que foi enviado, o que voltou, se deu erro). Ajuda a investigar falhas.", caller, "—", "Opcional")]

def killswitch(caller):
    return [R("Interruptor (kill switch)", "CustomMetadata ou CustomPermission", "lê/referencia", "Chave liga/desliga: permite parar a integração sem mexer no código.", caller, "—", "Opcional")]

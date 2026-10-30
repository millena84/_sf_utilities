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
         R("Named Credential", "NamedCredential", "lê/referencia", "resolve a URL base usada em `callout:Nome`", caller, "External Credential"),
         R("External Credential", "ExternalCredential", "autoriza", "fornece o protocolo de autenticação (OAuth, JWT, Basic, Custom) e os principals", "Named Credential", alvo),
         R("Permission Set (acesso ao principal)", "PermissionSet", "autoriza", "`externalCredentialPrincipalAccesses` dá ao usuário que executa o callout acesso ao principal da External Credential", "plataforma (no momento do callout)", "—"),
         R("Certificate", "Certificate", "autoriza", "assina o JWT ou faz mutual TLS, quando o protocolo exige", "External Credential", "—", "Opcional"),
         ator(alvo, "recebe a requisição e devolve a resposta", caller, "—")]
    if code == "E2":
        return [
         R("Named Credential (legada)", "NamedCredential", "lê/referencia + autoriza", "resolve a URL e injeta a autenticação (senha, OAuth via Auth Provider, JWT)", caller, alvo),
         R("Auth Provider", "AuthProvider", "autoriza", "obtém o token OAuth quando a Named Credential legada usa OAuth", "Named Credential", "—", "Opcional"),
         R("Certificate", "Certificate", "autoriza", "assina JWT ou mutual TLS", "Named Credential", "—", "Opcional"),
         ator(alvo, "recebe a requisição e devolve a resposta", caller, "—")]
    if code == "E3":
        return [
         R("Remote Site Setting", "RemoteSiteSetting", "autoriza", "libera o domínio fixo no código para callout", "plataforma (no momento do callout)", "—"),
         R("Certificate", "Certificate", "autoriza", "mutual TLS (`setClientCertificateName`)", caller, "—", "Opcional"),
         ator(alvo, "recebe a requisição e devolve a resposta", caller, "—")]
    if code == "E4":
        return [
         R("Tipo de Custom Metadata", "CustomObject (__mdt) + CustomField", "lê/referencia", "define os campos de configuração (endpoint, path, client_id, timeout, ativo)", caller, "registro de Custom Metadata"),
         R("Registro de Custom Metadata", "CustomMetadata", "lê/referencia", "fornece os valores do ambiente (URL, client_id). Segredo aqui é risco: ver README", caller, "—"),
         R("Classe de token", "ApexClass", "executa", "faz o callout de autenticação (ex.: client_credentials) e devolve o token", caller, "endpoint de token do sistema externo", "Opcional"),
         R("Partição de cache", "PlatformCachePartition", "lê/referencia", "guarda o token até expirar, evitando um callout de token por chamada", "Classe de token", "—", "Opcional"),
         R("Remote Site Setting", "RemoteSiteSetting", "autoriza", "libera o domínio lido do Custom Metadata (um por ambiente)", "plataforma (no momento do callout)", "—"),
         ator(alvo, "recebe a requisição e devolve a resposta", caller, "—")]
    if code == "E5":
        return [
         R("Tipo de Custom Metadata", "CustomObject (__mdt) + CustomField", "lê/referencia", "define o campo com o nome da Named Credential e parâmetros não sensíveis", caller, "registro de Custom Metadata"),
         R("Registro de Custom Metadata", "CustomMetadata", "lê/referencia", "indica qual Named Credential usar e os parâmetros (path, timeout, ativo)", caller, "—"),
         R("Named Credential", "NamedCredential", "lê/referencia", "resolve a URL base (`callout:` + nome lido do CMDT)", caller, "External Credential"),
         R("External Credential", "ExternalCredential", "autoriza", "fornece a autenticação", "Named Credential", alvo),
         R("Permission Set (acesso ao principal)", "PermissionSet", "autoriza", "dá ao usuário executor acesso ao principal", "plataforma (no momento do callout)", "—"),
         ator(alvo, "recebe a requisição e devolve a resposta", caller, "—")]
    if code == "E6":
        return [
         R("Custom Setting ou Custom Label", "CustomObject (Custom Setting) ou CustomLabels", "lê/referencia", "fornece o endpoint por ambiente", caller, "—"),
         R("Remote Site Setting", "RemoteSiteSetting", "autoriza", "libera o domínio lido", "plataforma (no momento do callout)", "—"),
         ator(alvo, "recebe a requisição e devolve a resposta", caller, "—")]
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
        rows = [R("Connected App", "ConnectedApp", "autoriza", f"`oauthConfig`: registra o cliente externo e libera o fluxo {FLOWS[flow]}{extra} e os `scopes`", caller, "Salesforce (emissão do token)")]
    else:
        rows = [
         R("External Client App", "ExternalClientApplication", "autoriza", "registra o cliente externo", caller, "Salesforce (emissão do token)"),
         R("Configurações OAuth do app", "ExtlClntAppOauthSettings", "autoriza", f"escopos (`commaSeparatedOauthScopes`) do fluxo {FLOWS[flow]}", "External Client App", "—"),
         R("Configurações OAuth globais", "ExtlClntAppGlobalOauthSettings", "autoriza", "`callbackUrl`, `consumerKey`, `consumerSecret` (segredo: não versionar), `certificate`, `isClientCredentialsFlowEnabled`", "External Client App", "—"),
         R("Políticas OAuth configuráveis", "ExtlClntAppOauthConfigurablePolicies", "autoriza", "`commaSeparatedPermissionSet`/`commaSeparatedProfile`, `ipRelaxationPolicyType`, `clientCredentialsFlowUser`", "External Client App", "—"),
         R("Políticas gerais", "ExtlClntAppConfigurablePolicies", "autoriza", "habilita o app e seus plugins na org", "External Client App", "—")]
    if flow == "JWT":
        rows.append(R("Certificate (público, do cliente)", "Certificate", "autoriza", "o Salesforce valida a assinatura do JWT com o certificado carregado no app (fica no próprio app, não necessariamente como metadata Certificate)", "app", "—", "Obrigatório (no app)"))
    if flow == "CC":
        rows.append(ator("Usuário run-as", "usuário em nome do qual o token Client Credentials executa", "app", "—"))
    else:
        rows.append(ator("Usuário de integração", "usuário autenticado pelo fluxo", "app", "—"))
    rows += [
     R("Perfil do usuário de integração", "Profile", "autoriza", "base do usuário (ex.: Minimum Access, API Enabled)", "plataforma", "—"),
     R("Permission Set / Permission Set Group", "PermissionSet / PermissionSetGroup", "autoriza", "acesso a objetos, campos, classes Apex e ao app", "plataforma", "—"),
     R("Escopo OAuth customizado", "OauthCustomScope", "autoriza", "restringe o que o token pode fazer", "app", "—", "Opcional")]
    return rows

def in_variants(apps=("CA", "ECA"), flows=("JWT", "CC", "WS", "UP")):
    return [(a, f) for a in apps for f in flows]

def logrows(caller):
    return [R("Objeto de log de integração", "CustomObject (__c) + CustomField", "executa (DML)", "registra requisição, resposta, status e erro", caller, "—", "Opcional")]

def killswitch(caller):
    return [R("Interruptor (kill switch)", "CustomMetadata ou CustomPermission", "lê/referencia", "liga/desliga a integração sem deploy de código", caller, "—", "Opcional")]

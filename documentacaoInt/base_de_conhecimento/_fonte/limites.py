# O que o repositório não mostra (item 4). Fonte "nv" = conhecimento da plataforma não conferido nesta coleta.
LIMITES = [
 # (id, informação, por que não está no repositório / onde fica, efeito na documentação, fonte)
 ("N01", "Agendamento de Apex (quando roda)", "o agendamento é feito na tela Schedule Apex ou por `System.schedule`; a classe Schedulable está no projeto, o agendamento não", "F.1/F.2: registrar a classe e marcar a frequência como \"Não informado\"", "AX-SCH"),
 ("N02", "Agendamento de Flow agendado", "fica no próprio Flow (`start`), então **está** no projeto", "F.3: frequência pode ser documentada", "MA-FLOW"),
 ("N03", "Segredos de Named Credential, External Credential e Connected App", "credenciais ficam criptografadas na org; campos como `password` e `consumerSecret` podem vir vazios ou mascarados", "nunca copiar valor; registrar só que existe credencial", "MA-NC"),
 ("N04", "Quais usuários têm cada Permission Set", "atribuição é dado (PermissionSetAssignment), não metadata", "não afirmar qual usuário executa a integração; só o Permission Set exigido", "nv"),
 ("N05", "Usuário de integração (registro, licença, perfil efetivo)", "o XML guarda apenas o nome de usuário (`user`, `runAsUser`, `integrationUser`, `clientCredentialsFlowUser`)", "registrar que há usuário configurado, sem o nome (proteção de dados)", "MA-PESC, MA-ESF, MA-WF, MA-ECAOP"),
 ("N06", "Valores de Custom Setting", "registros de Custom Setting são dados; a definição está no projeto, os valores não", "E6 com Custom Setting: endpoint \"Não informado\"", "nv"),
 ("N07", "Valores de Custom Metadata e Custom Labels", "**estão** no projeto (`customMetadata/*.md`, `labels/CustomLabels.labels`)", "E4/E5/E6 com Label: endpoint pode ser resolvido", "MA-CMD, MA-LBL"),
 ("N08", "Assinantes externos de Platform Event/CDC (Pub/Sub, CometD, middleware)", "a conexão é feita pelo cliente externo; o projeto só mostra o evento e, se houver, `ManagedEventSubscription`", "E.1/E.2/M.2: assinante externo \"presumido\"", "MA-MES"),
 ("N09", "Publicadores externos de Platform Event", "publicação via API não deixa rastro no projeto", "H.2: publicador \"presumido\"", "PE-SUB"),
 ("N10", "Quem usa as APIs padrão (REST, SOAP, Bulk, Composite, GraphQL)", "chamadas de entrada não exigem código na org", "g.1/g.2/g.7/H.1/M.3/M.4: só INBOUND_PRESUMIDO (campo External ID, app de entrada)", "nv"),
 ("N11", "Fluxo OAuth usado pelo cliente (Web Server × Username-Password)", "a escolha é do cliente externo; o XML do app não distingue", "registrar \"não determinado\"", "MA-CA"),
 ("N12", "Comportamento do sistema externo e do middleware", "configuração do MuleSoft, contratos e regras do outro lado ficam fora da org", "documentar só o lado Salesforce e o host", "—"),
 ("N13", "Volume, frequência real, erros e logs", "dados de execução (logs, Event Monitoring, fila de Outbound Message, uso de API)", "não estimar volumetria", "nv"),
 ("N14", "Componentes de pacote gerenciado", "Flows de pacote gerenciado não são acessíveis via Metadata API (exceto templates); código de pacote não vem no projeto", "registrar a dependência do pacote sem detalhar o conteúdo", "MA-FLOW"),
 ("N15", "Componentes que nunca passaram pelo repositório", "o repositório só tem o que foi versionado ou recuperado; configurações feitas direto na org podem faltar", "ausência no projeto não prova ausência na org", "—"),
 ("N16", "Status ativo/inativo efetivo em produção", "o XML traz o status versionado (ex.: Flow `status`, RemoteSiteSetting `isActive`), que pode divergir da org", "registrar o status do XML e a data do repositório", "MA-FLOW, MA-RSS"),
 ("N17", "Itens OmniStudio", "formato no projeto não confirmado (ausentes da lista de Metadata Types da API 68.0); no pacote gerenciado são dados (DataPacks)", "registrar o que houver nos arquivos, sem afirmar estrutura", "MA-TYPES"),
]

# Prompt-base — criação de utilitário Salesforce

## Papel

Você é uma pessoa engenheira de software com conhecimento avançado em Bash, Python, Robot Framework e Salesforce.

## Objetivo

Criar ou evoluir um utilitário para extrair, normalizar, comparar e documentar o metadata `{TIPO_METADATA}` em projetos Salesforce.

## Fontes

Analise separadamente XML Salesforce, tabela interna consultada com `sf data query`, API padrão ou Metadata API, Tooling API quando aplicável, código, configuração, snapshots e documentação.

## Procedimento SDD

1. Leia os conhecimentos e instruções do projeto.
2. Identifique as particularidades do metadata.
3. Crie ou atualize a SPEC.
4. Defina entradas, saídas, fontes, campos, segurança e critérios de aceitação.
5. Separe Bash para CLI/precheck/logs/exit codes; Python para parsing/normalização/comparação/renderização; Robot Framework para testes; Salesforce para semântica, APIs e metadata.
6. Implemente e teste.
7. Valide contra a SPEC.

## Regras

- Não assuma que todos os metadata types têm a mesma identidade ou estrutura XML.
- Não trate tabela interna como estado atual da org.
- Não trate XML local antigo como estado atual.
- Confirme disponibilidade, campos e permissões da Tooling API.
- Use `describe` quando necessário.
- Prefira campos explícitos a `FIELDS(ALL)` quando houver limitações.
- Trate paginação e limites.
- Use somente leitura por padrão.
- Nunca exponha secrets, tokens, senhas, consumer secrets, client secrets, chaves privadas ou certificados privados.

## Critérios de aceitação

- [ ] metadata identificado;
- [ ] fontes separadas;
- [ ] campos específicos extraídos;
- [ ] dados sensíveis protegidos;
- [ ] evidências registradas;
- [ ] snapshots comparáveis;
- [ ] documentação gerada;
- [ ] testes executados;
- [ ] limitações e fontes oficiais documentadas.

considere integrações outbound salesforce e explique:
1) para que serve o certificado
2) passos para criação de um certificado
3) passos para renovação de um certificado
4) papel dos arquivos crt, csr, key na criação e na renovação de um certificado
5) papel do access token nesse processo
6) o que é gerado em linha de comando usando openssl e curl + endereçoss

explique didaticamente e considerando conceitos (pois criação em renovação em ambientes controlados terao seus proprios passos)

---

## Resposta curta

A chave privada (.key) aparece em dois momentos e nunca é enviada pela rede:

1. **Na criação:** ela assina o CSR.
2. **Em cada chamada:** ela assina a "prova de identidade". Pode ser no handshake mTLS ou num JWT para pedir o token.

Na analogia: o .crt é o passaporte, que você mostra para todo mundo. A .key é a sua digital, que você usa para provar que o passaporte é seu, mas nunca entrega a ninguém.

---

## Momento 1: na criação

```
[.key nasce] ──assina──> [.csr] ──vai para──> [CA] ──devolve──> [.crt]
```

- A .key é a primeira coisa gerada. Dela sai a chave pública.
- O CSR leva a chave pública e é assinado com a .key. Assim a CA sabe que quem pediu tem mesmo a chave correspondente.
- O .crt que volta da CA contém a chave pública e só "funciona" junto com aquela .key. É por isso que a Salesforce recusa o upload de um certificado que não corresponde ao registro criado. [help.salesforce](https://help.salesforce.com/s/articleView?id=xcloud.security_keys_uploading_signed_cert.htm&language=en_US&type=5)

## Momento 2: em cada chamada outbound

### a) No handshake mTLS
1. A Salesforce envia o .crt, que é público.
2. O servidor do parceiro pergunta, na prática: "prove que esse certificado é seu".
3. A Salesforce assina os dados do handshake com a .key.
4. O parceiro confere essa assinatura com a chave pública que está no .crt.

A chave fica parada. Só a assinatura viaja.

### b) No pedido de token via JWT (quando o parceiro usa esse modelo)
1. A Salesforce monta um JWT ("sou o cliente X, válido por 5 min").
2. Assina o JWT com a .key.
3. O parceiro valida com o .crt que recebeu antes e devolve o access token.

Ou seja, a .key não é o token. Ela é o que permite conseguir o token.

---

## Onde ela fica guardada

| Cenário | Onde a .key mora | Cuidado |
|---|---|---|
| Caminho A: a Salesforce gera o certificado | Dentro da org. A Salesforce cria o certificado e as chaves automaticamente [help.salesforce](https://help.salesforce.com/s/articleView?id=xcloud.security_keys_uploading_signed_cert.htm&language=en_US&type=5) | Você nem vê a chave. É o cenário mais seguro |
| Caminho B: gerada fora (OpenSSL) | Na sua máquina ou num cofre. Depois entra na Salesforce dentro do keystore JKS por **Import from Keystore** [help.salesforce](https://help.salesforce.com/s/articleView?id=ind.fsc_admin_tdm_cnfgr_certi_visa_trxn_dspt.htm&language=en_US&type=5) | Proteja e apague as cópias soltas. O JKS tem senha por isso |
| Testes com curl/openssl | Arquivo local, informado em `--key` | Ela é usada só localmente para assinar e não é enviada |

## Na renovação

- **Recomendado:** gerar uma .key nova, depois um CSR novo e um .crt novo.
- **Por quê:** se a chave antiga tiver vazado em algum momento, quem a tem perde o acesso quando o certificado antigo é desativado.
- **Se a .key vazar:** isso não espera a renovação. Revogue o certificado na CA, gere um par novo e avise o parceiro.

---

## Para fixar

- **.key:** é secreta, nasce primeiro e assina.
- **.csr:** é o pedido, assinado pela .key.
- **.crt:** é público e confere as assinaturas feitas pela .key.
- **Token:** é obtido graças às assinaturas da .key, mas é outra coisa.

Frase-âncora: "O certificado diz quem eu sou; a chave privada prova que sou eu; o token diz o que posso fazer."

<br>

---

<br>

Imagine a seguinte situação.

Eu tenho um certificado crt na Salesforce q vence 18/11.
Recebi um client_id e um client_secret.

Com os dados de um portal de aplicação interno, rodei um comando openasl pra gerar o arquivo .csr e um .key

Ai, com client_id e client_secret, acessei um site interno pra gerar o access token.
Configurei o certificado anterior (eh uma renovacao) no insomnia junto com sua chave.
Colei o conteúdo do arquivo .csr numa chamada de outro site interno, com o access token no formato Authorization Bearer. 

Retornou um erro que o CN do certificado q estava sendo renovado eh diferente do client_id.


O q vc entende que isso significa?

---

## O que o erro significa

O serviço interno de renovação está conferindo se as suas duas identidades são a mesma pessoa:

| Identidade | De onde vem | O que diz |
|---|---|---|
| **OAuth** | access token, gerado com o client_id/secret | "Sou a aplicação **client_id = X**" |
| **PKI** | certificado antigo, enviado pelo Insomnia no mTLS | "Sou o **CN = Y**" |

A regra provável é: só pode renovar um certificado quem é o dono dele. Para isso, o serviço exige que o CN do certificado antigo seja igual ao client_id do token. Como X ≠ Y, ele recusou.

É como renovar o passaporte no balcão: você mostra o passaporte antigo e o RG. Se os nomes forem diferentes, o atendente não renova, porque não sabe se você é o dono daquele passaporte.

O mecanismo em si está funcionando como deveria. O problema está em algum dos dados que entraram na chamada.

---

## Hipóteses, da mais à menos provável

1. **O client_id/secret é de outra aplicação ou de outro ambiente.** Por exemplo, um client_id de homologação usado contra um certificado de produção, ou o client_id de uma aplicação vizinha.
2. **O Insomnia enviou outro certificado.** No Insomnia, o certificado de cliente fica amarrado a um host. Se houver outro certificado cadastrado para o mesmo domínio, ou se o host/porta não bater exatamente, ele pode enviar o certificado errado.
3. **O certificado antigo segue uma convenção antiga de CN.** Por exemplo, CN = nome do sistema ou hostname, enquanto a regra atual exige CN = client_id. Nesse caso não dá para renovar, e o caminho é uma emissão nova pelo processo interno.
4. **O CN do CSR novo está diferente.** Pela mensagem, o serviço está olhando o certificado antigo, mas alguns serviços validam os três (certificado antigo, CSR e token). Vale conferir.

---

## Como diagnosticar

Compare três valores lado a lado.

```bash
# 1. CN do certificado antigo (o que está no Insomnia / na Salesforce)
openssl x509 -in certificado_antigo.crt -noout -subject -enddate

# 2. CN do CSR novo
openssl req -in novo.csr -noout -subject

# 3. Confirma que a chave no Insomnia é mesmo do certificado antigo (hashes iguais)
openssl x509 -noout -modulus -in certificado_antigo.crt | openssl md5
openssl rsa  -noout -modulus -in chave_antiga.key      | openssl md5
```

Depois, veja o client_id:
- **No token:** se o token for um JWT (formato `xxx.yyy.zzz`), a parte do meio, decodificada em base64, costuma ter um campo como `client_id`, `azp` ou `sub`. Decodifique localmente. Não cole o token em sites públicos.
- **No que você recebeu:** compare com o client_id que foi entregue a você.

Como ler o resultado:
- **CN antigo = client_id, mas o erro continua:** o Insomnia provavelmente enviou outro certificado (hipótese 2). Revise a configuração de Client Certificates para o host exato da API de renovação.
- **CN antigo ≠ client_id:** confirme com o time dono do portal ou da PKI qual client_id corresponde a esse certificado (hipóteses 1 e 3).
- **CN do CSR diferente dos dois:** gere o CSR de novo com o CN correto (hipótese 4).

---

## Atenção ao prazo

O certificado vence em 18/11, então faltam cerca de 3 semanas. Se o caminho for "emissão nova" (hipótese 3), isso costuma envolver aprovação e o parceiro ou a Salesforce cadastrando o certificado novo. Vale abrir a conversa com o time da PKI já.

Se você me mandar só os `subject` (CN) que o openssl mostrar e o client_id, mascarando parte se quiser, eu te digo qual hipótese é. Não envie a .key, o secret nem o token.


<br>

---

<br>

E se por ventura, a ideia foi criar um novo certificado do zero?

---

## Se a ideia era criar do zero, o erro faz ainda mais sentido

Você recebeu um client_id novo. Isso sugere que a intenção era criar uma identidade nova, com um certificado novo cujo CN é esse client_id. Mas a chamada foi montada como renovação:

- Você enviou o certificado antigo no Insomnia.
- Pela mensagem, o serviço entendeu como renovação, seja pelo endpoint usado, seja pela presença do certificado antigo.

Então o serviço comparou o CN antigo com o client_id novo, e eles não batem. Esse resultado é esperado, porque o client_id novo não é o dono do certificado antigo.

Na analogia: você foi tirar o primeiro passaporte de uma pessoa nova, mas entregou no balcão o passaporte de outra pessoa como se fosse uma renovação.

---

## Renovação x emissão nova

| | Renovação | Emissão nova (do zero) |
|---|---|---|
| Quem prova a identidade | Certificado antigo (mTLS) + token | Só o token (client_id/secret) |
| Certificado antigo no Insomnia | Sim | Não. Remova-o para esse host |
| Endpoint | De renovação | De emissão (normalmente outro). Confira no portal interno |
| CN do CSR | O mesmo do certificado antigo | O que a regra interna pedir, provavelmente = client_id novo |
| Do lado do parceiro | Às vezes nada muda | É uma identidade nova, que pode precisar ser cadastrada no truststore dele |

Confirme com o time dono do portal se esse client_id é mesmo de uma aplicação nova, e qual é o endpoint de emissão.

---

## Caminho do zero, passo a passo

### 1. Decidir onde a chave privada vai nascer
É a decisão mais importante:
- **Na Salesforce:** você cria um CA-Signed Certificate, preenche o CN com o client_id e baixa o CSR. A chave nunca sai da org e você não lida com arquivo .key. [help.salesforce](https://help.salesforce.com/s/articleView?id=xcloud.security_keys_uploading_signed_cert.htm&language=en_US&type=5)
- **No OpenSSL (o que você fez):** você tem o .key em mãos, então depois vai precisar levá-lo para a Salesforce num keystore JKS.

Se a Salesforce é quem vai usar o certificado, gerar o CSR nela costuma ser o caminho mais simples e seguro. Só não é possível se o portal exigir algum campo que a Salesforce não permite preencher.

### 2. Gerar o CSR com o CN certo (se for pelo OpenSSL)
```bash
openssl req -new -newkey rsa:2048 -nodes \
  -keyout novo.key -out novo.csr \
  -subj "/CN=<CLIENT_ID>/O=<EMPRESA>/C=BR"

# confere antes de enviar
openssl req -in novo.csr -noout -subject
```
Use os campos que o portal interno exigir. O formato acima é só um exemplo.

### 3. Emitir o certificado
1. Gere o token com o client_id/secret.
2. No Insomnia, sem certificado de cliente para esse host, chame o endpoint de emissão com `Authorization: Bearer <token>` e o conteúdo do CSR.
3. Guarde o .crt e a cadeia (intermediários e raiz) que voltarem.

### 4. Levar para a Salesforce
- **Se o CSR foi gerado na Salesforce:** use **Upload Signed Certificate** no mesmo registro.
- **Se foi gerado no OpenSSL:** monte o keystore e use **Import from Keystore**. [help.salesforce](https://help.salesforce.com/s/articleView?id=ind.fsc_admin_tdm_cnfgr_certi_visa_trxn_dspt.htm&language=en_US&type=5)

```bash
openssl pkcs12 -export -inkey novo.key -in novo.crt -certfile cadeia.crt \
  -name novo_cert -out novo.p12
keytool -importkeystore -srckeystore novo.p12 -srcstoretype PKCS12 \
  -destkeystore novo.jks -deststoretype JKS
```
Depois disso, apague as cópias soltas do .key.

### 5. Virada antes de 18/11
1. Garanta que o parceiro aceita o certificado novo (truststore ou cadastro).
2. Troque a referência na Named Credential/External Credential.
3. Teste o fluxo: token, depois a chamada à API.
4. Só então desative o certificado antigo.

---

## Para fixar

- **Renovar** é provar que você é o dono do certificado antigo e pedir outro igual.
- **Criar do zero** é provar quem você é (pelo token) e pedir o primeiro certificado dessa identidade.

O certificado antigo só entra na renovação. Na criação do zero ele atrapalha.

<br>

---

<br>

Entao, pois bem
Eu tentei a renovação sem sucesso.

Tentei a renovação via portal interno, mas ao informar os dados, retornou "nao pode renovação antes de 30 dias" (mas falta menos, lembra, vence 18/11). 

Entao tentei o passo a passo da criação. 

O erro agora nao vou lembrar, mas tbm nao consegui seguir pq a aplicação nao eh reconnecida. 

Possivelmente, o client ID com os comandos do OpenSsl (q informa dados do portal interno de aplicacoes) tem Relação com isso?

---

## Resposta curta

Sim, é bem provável. Os dois erros apontam para a mesma causa: as identidades usadas não estão amarradas entre si no portal interno.

O portal precisa que três coisas apontem para a mesma aplicação:

```
[Aplicação cadastrada no portal]  ←→  [client_id do token]  ←→  [Dados do CSR (CN, OU, O...)]
```

Se qualquer um desses elos estiver quebrado, aparece um erro como "aplicação não reconhecida", "CN diferente do client_id" ou uma regra de prazo aplicada ao certificado errado.

---

## Os dois erros novos

### "Não pode renovar antes de 30 dias"
Hoje é 27/10 e o certificado vence em 18/11, ou seja, faltam 22 dias. Se a regra é "só renova nos últimos 30 dias", você já estaria dentro do prazo. Então algo não fecha. As hipóteses principais são:

1. **O portal está olhando outro certificado.** Os dados que você informou levaram a um certificado com outro vencimento, por exemplo um da mesma aplicação em outro ambiente ou outro certificado ligado a esse client_id.
2. **A regra é sobre a emissão, não sobre o vencimento.** Por exemplo, "não pode emitir de novo menos de 30 dias depois da última emissão". Isso aconteceria se alguém, ou alguma tentativa anterior, já tiver gerado um certificado recente para essa aplicação.
3. **A mensagem está mal redigida** e a regra real é outra. Só o time dono do portal confirma.

Para testar: o portal mostra qual certificado ou qual data de vencimento ele encontrou? Se mostrar uma data diferente de 18/11, a hipótese 1 está confirmada.

### "Aplicação não reconhecida"
Aqui a relação com o OpenSSL é direta. Os campos do `-subj` (CN, OU, O) são lidos pelo portal como "quem está pedindo". Se eles não batem exatamente com o cadastro da aplicação, ele não reconhece. Isso inclui:
- maiúsculas e minúsculas;
- espaços;
- a sigla do sistema;
- o ambiente (homologação ou produção).

Outra possibilidade: o client_id existe, mas ainda não está vinculado a essa aplicação no portal, ou não tem permissão para emitir certificado.

---

## Monte uma "matriz de identidade"

Coloque os valores lado a lado. Pode mascarar o meio dos IDs, o que importa é comparar.

| Fonte | Como obter | Valor |
|---|---|---|
| Aplicação no portal (ID/sigla, ambiente) | Tela do portal interno | |
| client_id recebido | O que te entregaram | |
| client_id dentro do token | Parte do meio do JWT, decodificada localmente | |
| CN/OU do certificado antigo | `openssl x509 -in antigo.crt -noout -subject -enddate` | |
| CN/OU do CSR novo | `openssl req -in novo.csr -noout -subject` | |
| Certificado que o portal encontrou (vencimento) | Tela ou mensagem do portal | |

A linha que destoar das outras é a causa.

---

## O que eu faria agora

1. **Parar de tentar várias vezes.** Cada tentativa pode criar pedidos órfãos ou reiniciar a contagem dos 30 dias, se a hipótese 2 for verdadeira.
2. **Preencher a matriz** acima.
3. **Abrir um chamado com o time do portal/PKI ainda esta semana.** Informe:
   - o vencimento em 18/11;
   - as duas mensagens de erro;
   - a matriz preenchida, sem secret, sem token e sem .key.

   Faça três perguntas objetivas:
   - "Qual certificado o portal associa a essa aplicação e a esse client_id?"
   - "A regra dos 30 dias é contada a partir de quê?"
   - "Para essa aplicação, o caminho certo é renovação ou emissão nova, e quais valores exatos de CN/OU devo usar no CSR?"
4. **Pedir um caminho de exceção** se o prazo apertar. Ambientes controlados costumam ter um fluxo de urgência para certificados prestes a vencer.

---

## Para fixar

- O CSR não é só um arquivo técnico: os campos dele são um documento de identidade.
- O portal só aceita se o que está no CSR, o que está no token e o que está no cadastro forem a mesma "pessoa".

Se me mandar a matriz preenchida, mascarada, eu te ajudo a apontar qual elo quebrou.

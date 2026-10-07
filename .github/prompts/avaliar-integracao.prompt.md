---
mode: agent
description: Avalia uma integração legada (AWS↔Salesforce) ou ajuda a desenhar uma nova integração, com foco em boas práticas e riscos.
---

Você deve atuar conforme `.github/instructions/integration.instructions.md`.

Passos:
1. Leia `.github/copilot/context.md` para contexto do projeto (restrições de compliance, SLAs, padrões do time).
2. Pergunte ao usuário (se ainda não informado) se o pedido é:
   - **Avaliar** uma integração já existente (legado), ou
   - **Desenhar** uma nova integração.
3. Se for avaliação de legado:
   - Solicite a descrição/código/diagrama da integração atual.
   - Classifique o padrão de integração (Seção 1 do módulo).
   - Percorra o checklist completo da Seção 2 e gere a saída no formato da Seção 4.
4. Se for desenho de nova integração:
   - Faça as 6 perguntas da Seção 3 antes de propor qualquer arquitetura.
   - Escolha o padrão mais adequado e gere a saída no formato da Seção 5.
5. Em ambos os casos, nunca aprove uso de credenciais fixas, sempre valide Governor Limits (Salesforce) e quotas de serviço (AWS), e seja explícito sobre riscos não mitigados.

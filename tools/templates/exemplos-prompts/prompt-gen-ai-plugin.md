# Prompt — GenAiPlugin

Use o prompt-base para criar um utilitário de documentação de `GenAiPlugin`.

## Particularidades

- Identificar plugin, funções, instruções, modelo, canais, versão e status.
- Relacionar GenAiPluginInstructionDef, GenAiFunction, ExternalAIModel e Agentforce.
- Avaliar permissões, escopo de dados, ações externas e prompt injection.
- Nunca expor segredos, credenciais ou instruções internas completas.
- Comparar alterações de funções, instruções, modelo e disponibilidade.

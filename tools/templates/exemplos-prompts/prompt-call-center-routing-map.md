# Prompt — CallCenterRoutingMap

Use o prompt-base para criar um utilitário de documentação de `CallCenterRoutingMap`.

## Particularidades

- Identificar regras de roteamento, filas, agentes, regiões, prioridades e condições.
- Relacionar CallCenter, Queue, User, ServiceChannel e PresenceStatus.
- Não expor identificadores de usuários ou critérios que fragilizem o roteamento.
- Diferenciar mapa configurado de chamada roteada em produção.
- Avaliar risco de transbordo, distribuição desigual e indisponibilidade.

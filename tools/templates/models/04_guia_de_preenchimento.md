# Guia de uso dos modelos

## 1. Escolha do documento

- Triagem: quando a natureza ou o encaminhamento ainda não estiverem claros.
- Avaliação: quando houver necessidade de analisar uma evolução, alternativa ou mudança antes de decidir seu avanço.
- MASP: quando a investigação e o tratamento estruturado de causas forem proporcionais ao impacto, à recorrência ou à complexidade.

Não preencher todos os modelos automaticamente. A triagem pode ser breve e o MASP completo não é obrigatório para todo defeito.

## 2. Princípios de preenchimento

1. Entender a necessidade antes de aceitar a solução proposta.
2. Separar fatos, premissas, hipóteses e recomendações.
3. Usar a profundidade necessária para sustentar a decisão, sem duplicar conteúdo.
4. Registrar evidências e limitações, não apenas conclusões.
5. Dar responsável, prazo e condição de avanço às pendências relevantes.
6. Distinguir parecer técnico, prontidão, prioridade e autorização.
7. Referenciar registros existentes em vez de copiar toda a documentação.
8. Manter o documento atualizado e indicar se a conclusão é provisória ou final.

## 3. Avaliação: checklist de consulta

> Use para revisar a análise. Registre no parecer apenas impactos relevantes, ou exclusões cuja justificativa seja importante.

### Necessidade e alternativas

- O resultado esperado está claro e verificável?
- O benefício tem evidência ou ainda é uma hipótese?
- A solução proposta é uma restrição real ou pode ser negociada?
- Há alternativa de processo, configuração, reutilização ou manutenção da situação atual?
- O custo de não fazer e eventual obrigação foram esclarecidos?

### Impacto funcional e técnico

- Jornada, regras, exceções e perfis de usuário.
- Componentes, automações, execução assíncrona e dependências.
- APIs, contratos, eventos, integrações e consumidores.
- Modelo de dados, qualidade, migração, retenção e reconciliação.
- Permissões, segurança, privacidade e controles.
- Performance, capacidade e limites da plataforma.
- Compatibilidade, testes funcionais, integração e regressão.
- Monitoramento, alertas, suporte e documentação.
- Implantação coordenada, reversão e recuperação de dados.

### Critérios de classificação sugeridos

| Dimensão | Referência para justificar |
|---|---|
| Valor | Benefício, alcance, obrigação e evidência disponível |
| Viabilidade | Restrições, capacidade, dependências e validações realizadas |
| Complexidade | Quantidade e acoplamento de componentes, incerteza, dados e coordenação |
| Risco | Probabilidade, consequência, controles e risco residual |

Não confundir complexidade com risco ou esforço. Informar o que não é conhecido; evitar classificações sem justificativa.

## 4. Relação com os frameworks discutidos

- Double Diamond: referência para explorar e definir a necessidade, considerar alternativas e validar a solução. O parecer não pretende representar sozinho todo o ciclo de design.
- INVEST: checklist de qualidade das user stories resultantes; não exigir que uma demanda ampla já nasça pequena e independente.
- Análise de impacto: identificar efeitos e dependências da mudança.
- Análise de valor, risco e viabilidade: sustentar a decisão sobre avanço e condições.
- MASP: estruturar investigação, ações, verificação e prevenção.
- 5 Porquês, Ishikawa e análise técnica: possíveis apoios à investigação; selecionar conforme o caso e validar hipóteses com evidências.
- Gestão do conhecimento: reaproveitar respostas e aprendizados, especialmente em dúvidas recorrentes.

## 5. Prontidão de um incremento, quando aplicável

- [ ] Necessidade e resultado compreendidos.
- [ ] Escopo do incremento delimitado.
- [ ] Critérios de aceitação verificáveis.
- [ ] Regras e exceções relevantes registradas.
- [ ] Impactos principais analisados.
- [ ] Dependências identificadas e bloqueios tratados.
- [ ] Riscos relevantes com tratamento definido.
- [ ] Incertezas compatíveis com a execução pretendida.
- [ ] Responsáveis e condições para avanço conhecidos.

Esta revisão não substitui priorização, autorização nem critérios específicos da equipe. Descobertas, investigações e atividades técnicas podem exigir formatos diferentes de user story.

## 6. Evidências e proteção da informação

- Usar apenas referências cujo compartilhamento seja autorizado.
- Não inserir credenciais, tokens, segredos, dados pessoais ou conteúdo de produção nos modelos compartilhados.
- Preferir dados sintéticos e descrições genéricas nos exemplos.
- Remover identificadores e metadados desnecessários de capturas, logs e anexos.
- Manter evidências sensíveis no repositório autorizado e registrar apenas referência e conclusão permitidas.
- Não tratar anonimização superficial como garantia de que um conjunto de dados possa ser compartilhado.

## 7. Revisão final

- A conclusão responde à pergunta da demanda?
- É possível distinguir o que foi observado do que foi inferido?
- Há um próximo passo concreto com responsável?
- O documento repete informações já registradas?
- Existe conteúdo sensível que não deveria estar aqui?
- A decisão e suas limitações estão claras para quem não participou da análise?

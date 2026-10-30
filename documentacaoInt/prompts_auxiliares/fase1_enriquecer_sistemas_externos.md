# Fase 1 — Enriquecer os sistemas externos

Sem alterar `fase1/integration_points.csv`, gere `fase1/revisao/sistemas_externos_pistas.md` para ajudar a revisora a nomear cada sistema de `fase1/sistemas_externos_proposto.csv`.

Para cada sistema (inclusive `SIS::DESCONHECIDO` e os pontos `DINAMICO`), reúna as pistas encontradas no repositório, com evidência `arquivo:linha`:
1. Domínio(s) e credenciais (Named Credential, External Credential, Remote Site, registro de Custom Metadata).
2. `label` e `description` dos XML dessas credenciais e registros.
3. Nomes das classes, triggers, Flows e LWC que formam os pontos de integração do sistema, e os métodos/recursos chamados (ex.: `POST /cobrancas`).
4. Comentários no código que mencionem o sistema, o fornecedor ou o produto.
5. Para pontos INBOUND: Connected Apps / External Client Apps, Permission Sets e usuários de integração ligados às classes expostas (`@RestResource`, `webservice`).
6. Assuntos de `fase0/glossario_aprovado.csv` cujos termos aparecem nesses componentes.

Ao final de cada sistema:
- **Nome sugerido** (nome de negócio provável) e o motivo, em 1 frase.
- **Confiança** da sugestão (alta/média/baixa).
- Se parecer que **dois sistemas propostos são o mesmo**, ou que **um sistema junta dois diferentes**, diga isso.

Também acrescente ao `sistemas_externos_proposto.csv` as colunas `nome_sugerido` e `confianca_sugestao`, **sem alterar** `status_revisao` (continua `pendente`). Não crie o `_aprovado`. Registre em `decisions.md`.

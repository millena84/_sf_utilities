# Bash para utilitários Salesforce

## Responsabilidade

Use Bash para entrada CLI, precheck, descoberta de caminhos, chamada de `sf`, chamada de Python, logs e exit codes.

## Regras

- usar `set -Eeuo pipefail`;
- não depender do diretório atual;
- validar argumentos e dependências;
- preservar códigos de saída;
- não fazer parsing XML complexo;
- não colocar regra de negócio Salesforce espalhada em shell;
- não mascarar falhas.

## Contrato de saída

- `0`: sucesso;
- `1`: erro;
- `2`: nada a fazer;
- `3`: precheck falhou;
- `4`: autorização necessária.

## Fonte

- [Salesforce CLI Reference](https://developer.salesforce.com/docs/platform/salesforce-cli-reference)

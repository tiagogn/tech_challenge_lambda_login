# Lambda Function for Cognito Authentication

Este projeto é uma função AWS Lambda que autentica usuários com base no CPF usando o Amazon Cognito. Ele permite criar e autenticar usuários no pool de usuários do Cognito, verificando e validando o CPF fornecido.

## Estrutura do Projeto

- *lambda_function.py*: Contém a função Lambda principal e as funções auxiliares para autenticação e criação de usuários.
- *cognito_utils.py*: Contém funções para interagir com o Amazon Cognito.
- *cpf_utils.py*: Contém a função para validar o CPF.
- *utils.py*: Contém a função para gerar respostas HTTP.

## Requisitos

- Python 3.7 ou superior
- Bibliotecas AWS: boto3
- Variáveis de ambiente configuradas:
  - USER_POOL_ID
  - CLIENT_ID
  - CLIENT_SECRET
  - TEMP_PASSWORD

## Funções Principais

### lambda_handler

Função principal da Lambda que é chamada quando o evento é acionado. Ela valida o CPF, tenta autenticar o usuário no Cognito ou cria um novo usuário se o CPF não for encontrado.

### get_cognito_user

Verifica se um usuário com o CPF fornecido existe no pool de usuários do Cognito.

### create_cognito_user

Cria um novo usuário no pool de usuários do Cognito com um CPF fornecido.

### validar_cpf

Valida o CPF fornecido de acordo com as regras brasileiras.

### generate_response

Gera uma resposta HTTP para retornar o status e a mensagem apropriada.

## Variáveis de Ambiente

- USER_POOL_ID: ID do Pool de Usuários do Cognito.
- CLIENT_ID: ID do Cliente no Cognito.
- CLIENT_SECRET: Segredo do Cliente no Cognito.
- TEMP_PASSWORD: Senha temporária usada para autenticação.

## Exemplo de Evento

```json
{
  "cpf": "12345678909"
}

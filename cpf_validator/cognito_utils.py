import boto3
import base64
import hashlib
import hmac
import os
from botocore.exceptions import ClientError

# Inicializando o cliente Cognito
cognito_client = boto3.client('cognito-idp')
USER_POOL_ID = os.environ['USER_POOL_ID']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
TEMP_PASSWORD = os.environ['TEMP_PASSWORD']

def get_cognito_user(cpf):
    try:
        response = cognito_client.admin_get_user(
            UserPoolId=USER_POOL_ID,
            Username=cpf
        )
        return response
    except cognito_client.exceptions.UserNotFoundException:
        return None
    except ClientError as e:
        raise ClientError(f'Erro ao verificar o usuario: {str(e)}')

def create_cognito_user(cpf):
    try:
        cognito_client.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=cpf,
            TemporaryPassword=TEMP_PASSWORD,
            MessageAction='SUPPRESS'
        )
        return True
    except ClientError as e:
        raise ClientError(f'Erro ao criar o usuario: {str(e)}')

def authenticate_user(cpf):
    try:
        secret_hash = calculate_secret_hash(cpf, CLIENT_ID, CLIENT_SECRET)
        
        auth_response = cognito_client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            ClientId=CLIENT_ID,
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': cpf,
                'PASSWORD': TEMP_PASSWORD,
                'SECRET_HASH': secret_hash
            }
        )
        
        if 'ChallengeName' in auth_response and auth_response['ChallengeName'] == 'NEW_PASSWORD_REQUIRED':
            response = cognito_client.admin_respond_to_auth_challenge(
                UserPoolId=USER_POOL_ID,
                ClientId=CLIENT_ID,
                ChallengeName='NEW_PASSWORD_REQUIRED',
                Session=auth_response['Session'],
                ChallengeResponses={
                    'USERNAME': cpf,
                    'NEW_PASSWORD': TEMP_PASSWORD,
                    'SECRET_HASH': secret_hash,
                }
            )
            return extract_token(response)
        
        return extract_token(auth_response)
    
    except ClientError as e:
        # Levanta uma exceção
        raise Exception(f"Erro na autenticacao: {str(e)}")


def extract_token(auth_response):
    if 'AuthenticationResult' in auth_response:
        return auth_response['AuthenticationResult']['IdToken']
    raise Exception("Erro ao obter o token: resposta de autenticacao inválida")

def calculate_secret_hash(username, client_id, client_secret):
    message = username + client_id
    dig = hmac.new(
        bytes(client_secret , 'utf-8'), 
        msg = bytes(message , 'utf-8'), 
        digestmod = hashlib.sha256
    )
    secret_hash = base64.b64encode(dig.digest()).decode()
    return secret_hash

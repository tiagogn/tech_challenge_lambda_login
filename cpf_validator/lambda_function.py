import os
import json
import re
from botocore.exceptions import ClientError
from cognito_utils import get_cognito_user, create_cognito_user, authenticate_user
from cpf_utils import validar_cpf
from utils import generate_response

# Inicializando o cliente Cognito
import boto3
cognito_client = boto3.client('cognito-idp')

USER_POOL_ID = os.environ['USER_POOL_ID']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
TEMP_PASSWORD = os.environ['TEMP_PASSWORD']

def lambda_handler(event, context):
    cpf = re.sub(r'\D', '', event.get('cpf', ''))
    
    if not cpf:
        return generate_response(400, 'CPF obrigatorio!')
    
    if not validar_cpf(cpf):
        return generate_response(400, 'CPF invalido!')
    
    try:
        cognito_user = get_cognito_user(cpf)
        
        if cognito_user:
            token = authenticate_user(cpf)
            return generate_response(200, 'CPF encontrado!', token)
        
        create_user_response = create_cognito_user(cpf)
        if create_user_response:
            token = authenticate_user(cpf)
            return generate_response(201, f'Novo usuario criado para o CPF: {cpf}', token)
        
    except ClientError as e:
        return generate_response(500, f'Erro interno: {str(e)}')

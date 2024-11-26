import json

def generate_response(status_code, message, token=None):
    response_body = {
        'message': message,
        'token': token if token else None
    }
    return {
        'statusCode': status_code,
        'body': json.dumps(response_body)
    }

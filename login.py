import json
import boto3
import hashlib
import uuid
import time

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla_usuarios = dynamodb.Table('usuarios')
tabla_sesiones = dynamodb.Table('sesiones')

def hashear_password(password, salt):
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        email = body.get('email', '').strip().lower()
        password = body.get('password', '')

        if not email or not password:
            return respuesta(400, {'error': 'Email y password son requeridos'})

        usuario = tabla_usuarios.get_item(Key={'email': email}).get('Item')

        if not usuario:
            return respuesta(401, {'error': 'Credenciales inválidas'})

        hash_calculado = hashear_password(password, usuario['salt'])

        if hash_calculado != usuario['password_hash']:
            return respuesta(401, {'error': 'Credenciales inválidas'})

        token = str(uuid.uuid4())

        tabla_sesiones.put_item(Item={
            'token': token,
            'email': email
        })

        return respuesta(200, {
            'token': token,
            'email': email,
            'nombre': usuario.get('nombre', '')
        })

    except Exception as e:
        print(f"Error en login: {e}")
        return respuesta(500, {'error': 'Error interno del servidor'})

def respuesta(status, body):
    return {
        'statusCode': status,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }
import json
import boto3
import hashlib
import os
import re

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla_usuarios = dynamodb.Table('usuarios')

def hashear_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    hash_resultado = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000 
    ).hex()
    return hash_resultado, salt

def email_valido(email):
    patron = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    return re.match(patron, email) is not None

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        email = body.get('email', '').strip().lower()
        password = body.get('password', '')
        nombre = body.get('nombre', '')

        if not email or not password:
            return respuesta(400, {'error': 'Email y password son requeridos'})

        if not email_valido(email):
            return respuesta(400, {'error': 'Email inválido'})

        if len(password) < 8:
            return respuesta(400, {'error': 'La contraseña debe tener al menos 8 caracteres'})

        existente = tabla_usuarios.get_item(Key={'email': email})
        if 'Item' in existente:
            return respuesta(409, {'error': 'Ya existe usuarion con ese Email'})

        password_hash, salt = hashear_password(password)

        tabla_usuarios.put_item(Item={
            'email': email,
            'nombre': nombre,
            'password_hash': password_hash,
            'salt': salt
        })

        return respuesta(201, {'mensaje': 'Usuario registrado correctamente', 'email': email})

    except Exception as e:
        print(f"Error en registro: {e}")
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
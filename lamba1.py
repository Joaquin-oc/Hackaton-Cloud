import json
import boto3
import csv
import io
import uuid
import os

sqs = boto3.client('sqs', region_name='us-east-1')
SQS_URL = os.environ['SQS_URL']

def lambda_handler(event, context):
    body = json.loads(event['body'])
    csv_content = body['csv']
    perfil_usuario = body['perfil']
    sesion_id = str(uuid.uuid4())

    reader = csv.DictReader(io.StringIO(csv_content))
    ofertas = list(reader)

    for i, oferta in enumerate(ofertas):
        mensaje = {
            'sesion_id': sesion_id,
            'oferta_id': str(i),
            'empresa': oferta.get('empresa', ''),
            'cargo': oferta.get('cargo', ''),
            'modalidad': oferta.get('modalidad', ''),
            'lugar': oferta.get('lugar', ''),
            'salario': oferta.get('salario', ''),
            'horas_semanales': oferta.get('horas_semanales', ''),
            'requerimientos': oferta.get('requerimientos', ''),
            'descripcion': oferta.get('descripcion', ''),
            'perfil_usuario': perfil_usuario
        }
        sqs.send_message(
            QueueUrl=SQS_URL,
            MessageBody=json.dumps(mensaje)
        )

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({
            'sesion_id': sesion_id,
            'total': len(ofertas)
        })
    }
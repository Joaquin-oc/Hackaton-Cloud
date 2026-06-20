import json
import boto3
import urllib.request
import os

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
tabla = dynamodb.Table('resultados-ofertas')

GROQ_API_KEY = os.environ['GROQ_API_KEY']
GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions'

def llamar_groq(oferta_texto, perfil):
    prompt = f"""Analiza esta oferta de trabajo para el siguiente candidato.

OFERTA:
{oferta_texto}

PERFIL DEL CANDIDATO:
{perfil}

Responde SOLO con un JSON con esta estructura exacta, sin texto adicional:
{{
  "match_score": número del 0 al 100,
  "nivel_requerido": "Junior/Mid/Senior",
  "salario_estimado": "rango estimado en dólares o 'No especificado'",
  "habilidades_requeridas": ["lista", "de", "habilidades"],
  "brechas": ["qué le falta al candidato"],
  "veredicto": "una frase explicando si debe aplicar o no"
}}"""

    data = json.dumps({
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }).encode('utf-8')

    req = urllib.request.Request(
        GROQ_URL,
        data=data,
        headers={
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            resultado = json.loads(response.read())
            texto = resultado['choices'][0]['message']['content']
            return json.loads(texto)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise Exception("RATE_LIMIT")
        raise e

def lambda_handler(event, context):
    for record in event['Records']:
        mensaje = json.loads(record['body'])

        oferta_texto = f"Empresa: {mensaje['empresa']}\nCargo: {mensaje['cargo']}\nDescripción: {mensaje['descripcion']}"

        try:
            resultado = llamar_groq(oferta_texto, mensaje['perfil_usuario'])

            tabla.put_item(Item={
                'sesion_id': mensaje['sesion_id'],
                'oferta_id': mensaje['oferta_id'],
                'empresa': mensaje['empresa'],
                'cargo': mensaje['cargo'],
                'match_score': str(resultado.get('match_score', 0)),
                'nivel_requerido': resultado.get('nivel_requerido', ''),
                'salario_estimado': resultado.get('salario_estimado', ''),
                'habilidades': json.dumps(resultado.get('habilidades_requeridas', [])),
                'brechas': json.dumps(resultado.get('brechas', [])),
                'veredicto': resultado.get('veredicto', ''),
                'estado': 'completado'
            })

        except Exception as e:
            if 'RATE_LIMIT' in str(e):
                raise e 
            print(f"Error procesando oferta: {e}")
            raise e

    return {'statusCode': 200}
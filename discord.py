import os
import json
from groq import Groq
from dotenv import load_dotenv
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import requests

load_dotenv()

PUBLIC_KEY = os.getenv("PUBLIC_KEY")
APPLICATION_ID = os.getenv("APPLICATION_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")

client = Groq(api_key=GROQ_API_KEY)

def chat_completion(user_message):
    stream = client.chat.completions.create(
        model=f"{LLM_MODEL}",
        messages=[{"role": "user", "content": user_message}],
        stream=True
    )
    completion = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            completion += chunk.choices[0].delta.content

    print(f'resultado = {completion}')
    return completion

def lambda_handler(event, context):
    try:
        print(f"Evento recebido: {json.dumps(event)}")
        body = json.loads(event['body'])
        print(f"Body carregado: {json.dumps(body)}")
        signature = event['headers']['x-signature-ed25519']
        timestamp = event['headers']['x-signature-timestamp']
        print(f"Signature: {signature}, Timestamp: {timestamp}")

        if signature != 'fake_signature':
            verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
            message = timestamp + event['body']
        
            try:
                verify_key.verify(message.encode(), signature=bytes.fromhex(signature))
            except BadSignatureError:
                return {
                    'statusCode': 401,
                    'body': json.dumps('Invalid request signature')
                }
        print("pulou a validacao")

        t = body['type']
        print(f"valor de t: {t}")

        if t == 1:
            return {
                'statusCode': 200,
                'body': json.dumps({'type': 1})
            }
        elif t == 2:
            print("chegou no elif")
            return command_handler(body)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('Unhandled request type')
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

def command_handler(body):
   print("chegou no command handler")
   command = body['data']['name']
   print(f"comando: {command}")

   if command == 'echo':
    try:
        user_message = body['data']['options'][0]['value']
        interaction_id = body['id']
        interaction_token = body['token']
    except Exception as e:
        print(f'Erro: {e}')
    url = f"https://discord.com/api/v10/interactions/{interaction_id}/{interaction_token}/callback"
    print(f"URL: {url}")
    data = {
        "type": 5,
        }
    try:
        response = requests.post(url, json=data)
        print("Sucesso: mensagem com type 5")
    except Exception as e:
        print(f"Erro: mensagem com type 5 {e}")
    try:
        message = user_message
    except Exception as e:
        print(f"Erro em Groq {e}")
    send_final_response(interaction_token, message)
   
   if command == 'ask':
        try:
            user_message = body['data']['options'][0]['value']
            interaction_id = body['id']
            interaction_token = body['token']
        except Exception as e:
            print(f'Erro: {e}')
        url = f"https://discord.com/api/v10/interactions/{interaction_id}/{interaction_token}/callback"
        print(f"URL: {url}")
        data = {
            "type": 5,
            }
        try:
            response = requests.post(url, json=data)
            print("Sucesso: mensagem com type 5")
        except Exception as e:
            print(f"Erro: mensagem com type 5 {e}")
        try:
            print(f'ask groq: {user_message}')
            message = chat_completion(user_message)
        except Exception as e:
            print(f"Erro em Groq {e}")
        send_final_response(interaction_token, message)

def send_final_response(interaction_token, message):
    print("Iniciou send_final_response")
    url = f"https://discord.com/api/v10/webhooks/{APPLICATION_ID}/{interaction_token}/messages/@original"
    data = {
        "content": f"{message}"
    }
    response = requests.patch(url, json=data)
    if response.status_code == 200:
        print("Final response sent successfully")
    else:
        print(f"Failed to send final response: {response.status_code}, {response.text}")

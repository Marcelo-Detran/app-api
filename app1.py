from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

# Configurações de ambiente
os.environ['FLASK_ENV'] = 'development'  # Modo desenvolvimento
os.environ['FLASK_DEBUG'] = '1'         # Ativa debug

# Função de teste para verificar se a API está funcionando
def handler(request, context):
    # Rota principal
    if request.path == "/":
        return jsonify({'message': 'API hospedada no Netlify com sucesso!'})
    
    # Rota para consultar documentos no SEI
    if request.path == "/consultar_documento":
        documento_id = request.args.get('id')
        if not documento_id:
            return jsonify({'error': 'Parâmetro "id" é obrigatório'}), 400

        sei_url = f'https://sei.sp.gov.br/api/documento/{documento_id}'
        headers = {'Authorization': 'Bearer seu_token'}

        try:
            # Requisição à API do SEI
            response = requests.get(sei_url, headers=headers, timeout=10)
            response.raise_for_status()  # Levanta erro se status não for 200-299
            return jsonify(response.json())
        except requests.exceptions.RequestException as e:
            return jsonify({'error': 'Erro ao acessar o SEI', 'details': str(e)}), 400
    
    # Rota para assinar documentos
    if request.path == "/assinar_documento":
        try:
            documento_id = request.json.get('documento_id')
            assinatura_data = request.json.get('assinatura_data')

            if not documento_id or not assinatura_data:
                return jsonify({'error': 'Parâmetros "documento_id" e "assinatura_data" são obrigatórios'}), 400

            print(f"Documento {documento_id} assinado com os dados {assinatura_data}")

            return jsonify({
                'status': 'documento assinado com sucesso',
                'documento_id': documento_id
            })
        except Exception as e:
            return jsonify({'error': 'Erro no processamento da assinatura', 'details': str(e)}), 500

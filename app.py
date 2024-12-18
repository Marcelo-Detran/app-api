from flask import Flask, jsonify, request
import requests  # Para fazer requisições HTTP ao SEI
import os

app = Flask(__name__)

# Configurações de ambiente
os.environ['FLASK_ENV'] = 'development'  # Modo desenvolvimento
os.environ['FLASK_DEBUG'] = '1'         # Ativa debug

# Rota de teste para verificar se o servidor Flask está funcionando
@app.route('/')
def home():
    return jsonify({'message': 'API hospedada no Heroku com sucesso!'})

# Rota para consultar documentos no SEI
@app.route('/consultar_documento', methods=['GET'])
def consultar_documento():
    # Parâmetros e URL da API SEI
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
        print(f"Erro ao acessar o SEI: {e}")
        return jsonify({'error': 'Erro ao acessar o SEI', 'details': str(e)}), 400

# Rota para assinatura digital (exemplo simplificado)
@app.route('/assinar_documento', methods=['POST'])
def assinar_documento():
    try:
        # Parâmetros enviados na requisição JSON
        documento_id = request.json.get('documento_id')
        assinatura_data = request.json.get('assinatura_data')

        if not documento_id or not assinatura_data:
            return jsonify({'error': 'Parâmetros "documento_id" e "assinatura_data" são obrigatórios'}), 400

        # Aqui seria chamada a API do SEI ou lógica para assinar o documento
        print(f"Documento {documento_id} assinado com os dados {assinatura_data}")

        return jsonify({
            'status': 'documento assinado com sucesso',
            'documento_id': documento_id
        })
    except Exception as e:
        return jsonify({'error': 'Erro no processamento da assinatura', 'details': str(e)}), 500

# Iniciar servidor Flask com host configurado para 0.0.0.0 e porta 10000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)

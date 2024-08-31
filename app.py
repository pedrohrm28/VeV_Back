from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import quote as url_quote


app = Flask(__name__)
CORS(app)

# Dados simulados (em um sistema real, isso estaria em um banco de dados)
pix_keys = {}

@app.route('/criar_chave_pix', methods=['POST'])
def criar_chave_pix():
    chave = request.json.get('chave')
    if chave in pix_keys:
        return jsonify({"message": "Chave Pix já existe!"}), 400
    pix_keys[chave] = {"valor": 0.0}
    return jsonify({"message": "Chave Pix criada com sucesso!"}), 201

@app.route('/validar_chave_pix', methods=['POST'])
def validar_chave_pix():
    chave = request.json.get('chave')
    if chave not in pix_keys:
        return jsonify({"message": "Chave Pix inválida!"}), 404
    return jsonify({"message": "Chave Pix validada com sucesso!"}), 200

@app.route('/validar_valor_pix', methods=['POST'])
def validar_valor_pix():
    valor = request.json.get('valor')
    if valor <= 0:
        return jsonify({"message": "Valor do Pix inválido!"}), 400
    return jsonify({"message": "Valor do Pix validado com sucesso!"}), 200

@app.route('/realizar_pix', methods=['POST'])
def realizar_pix():
    chave = request.json.get('chave')
    valor = request.json.get('valor')

    if chave not in pix_keys:
        return jsonify({"message": "Chave Pix inválida!"}), 404
    if valor <= 0:
        return jsonify({"message": "Valor do Pix inválido!"}), 400

    # Simula a operação de Pix
    pix_keys[chave]["valor"] += valor
    return jsonify({"message": "Pix realizado com sucesso!", "chave": chave, "valor": valor}), 200

if __name__ == '__main__':
    app.run(debug=True)


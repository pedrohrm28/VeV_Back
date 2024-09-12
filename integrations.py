# test_app.py
import json
from datetime import datetime

def test_criar_chave_pix(client):
    response = client.post('/criar_chave_pix', json={'chave': '123456789'})
    assert response.status_code == 201
    assert json.loads(response.data)['message'] == "Chave Pix criada com sucesso!"

def test_validar_chave_pix(client):
    client.post('/criar_chave_pix', json={'chave': '123456789'})
    response = client.post('/validar_chave_pix', json={'chave': '123456789'})
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == "Chave Pix validada com sucesso!"

def test_validar_valor_pix(client):
    response = client.post('/validar_valor_pix', json={'valor': 500})
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == "Valor do Pix validado com sucesso!"

def test_realizar_pix(client):
    client.post('/criar_chave_pix', json={'chave': '123456789'})
    response = client.post('/realizar_pix', json={'chave': '123456789', 'valor': 500})
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == "Pix realizado com sucesso!"
    assert json.loads(response.data)['valor'] == '500.00'

def test_extrato(client):
    client.post('/criar_chave_pix', json={'chave': '123456789'})
    client.post('/realizar_pix', json={'chave': '123456789', 'valor': 500})
    response = client.post('/extrato', json={'chave': '123456789'})
    assert response.status_code == 200
    assert len(json.loads(response.data)['transacoes']) == 1
    assert json.loads(response.data)['transacoes'][0]['valor'] == '500.00'

def test_verificar_limite_diario(client):
    client.post('/criar_chave_pix', json={'chave': '123456789'})
    client.post('/realizar_pix', json={'chave': '123456789', 'valor': 500})
    response = client.get('/verificar_limite_diario', query_string={'chave': '123456789'})
    assert response.status_code == 200
    assert json.loads(response.data)['total_diario'] == 500.00
    assert json.loads(response.data)['limite_maximo'] == 1000.00
    assert json.loads(response.data)['excedido'] == False

def test_login(client):
    client.post('/register', json={'username': 'testuser', 'password': 'password'})
    response = client.post('/login', json={'username': 'testuser', 'password': 'password'})
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == "Login bem-sucedido!"

def test_register(client):
    response = client.post('/register', json={'username': 'newuser', 'password': 'newpassword'})
    assert response.status_code == 201
    assert json.loads(response.data)['message'] == "Cadastro bem-sucedido!"

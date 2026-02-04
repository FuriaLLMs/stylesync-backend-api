import pytest
import sys
import os

# Adiciona o diretório raiz ao path para importar 'app' corretamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def get_auth_header(client):
    rv = client.post('/login', json={"username": "admin", "password": "123"})
    token = rv.json['access_token']
    return {'Authorization': f'Bearer {token}'}

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.json == {"message": "Bem-vindo à API da StyleSync!"}

def test_login_success(client):
    rv = client.post('/login', json={"username": "admin", "password": "123"})
    assert rv.status_code == 200
    assert "access_token" in rv.json

def test_create_product_authorized(client):
    headers = get_auth_header(client)
    product_data = {
        "name": "Mouse Gamer Protected",
        "sku": "MOUSE-PROT-001",
        "price": 250.00,
        "stock": 15,
        "description": "Mouse de teste protegido"
    }
    rv = client.post('/products', json=product_data, headers=headers)
    assert rv.status_code == 201
    return rv.json['_id'] # Return ID for other tests

def test_update_product(client):
    # Primeiro cria
    product_id = test_create_product_authorized(client)
    headers = get_auth_header(client)
    
    # Atualiza apenas preço
    update_data = {"price": 199.99}
    rv = client.put(f'/product/{product_id}', json=update_data, headers=headers)
    
    assert rv.status_code == 200
    assert rv.json['price'] == 199.99
    assert rv.json['name'] == "Mouse Gamer Protected" # Nome deve permanecer

def test_delete_product(client):
    # Primeiro cria
    product_id = test_create_product_authorized(client)
    headers = get_auth_header(client)
    
    # Deleta
    rv = client.delete(f'/product/{product_id}', headers=headers)
    assert rv.status_code == 204
    
    # Tenta buscar (deve ser 404)
    rv = client.get(f'/product/{product_id}')
    assert rv.status_code == 404

def test_delete_product_unauthorized(client):
    # Não vamos criar, mas tentar deletar algo
    rv = client.delete('/product/507f1f77bcf86cd799439011')
    assert rv.status_code == 401

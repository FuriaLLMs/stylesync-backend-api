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

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.json == {"message": "Bem-vindo à API da StyleSync!"}

def test_login_success(client):
    rv = client.post('/login', json={"username": "admin", "password": "123"})
    assert rv.status_code == 200
    assert rv.json == {"message": "Login bem-sucedido!"}

def test_login_invalid_credentials(client):
    rv = client.post('/login', json={"username": "admin", "password": "wrong"})
    assert rv.status_code == 401
    assert rv.json == {"message": "Credenciais invalidas!"}

def test_login_missing_field(client):
    rv = client.post('/login', json={"username": "admin"})
    assert rv.status_code == 400
    assert "error" in rv.json

def test_get_products(client):
    rv = client.get('/products')
    assert rv.status_code == 200
    # Agora retorna uma lista de produtos, não uma mensagem
    assert isinstance(rv.json, list) 
    # Podemos verificar se a lista não está vazia se tivermos garantias do seed
    # assert len(rv.json) > 0 

def test_create_product(client):
    product_data = {
        "name": "Mouse Gamer",
        "sku": "MOUSE-TEST-001",
        "price": 250.00,
        "stock": 15,
        "description": "Mouse de teste"
    }
    rv = client.post('/products', json=product_data)
    assert rv.status_code == 201
    assert rv.json["message"] == "Produto criado com sucesso!"
    assert "_id" in rv.json
    assert rv.json["data"]["sku"] == "MOUSE-TEST-001"

def test_get_product_by_id_not_found(client):
    # Testando com um ObjectId válido mas inexistente (provavelmente)
    fake_id = "507f1f77bcf86cd799439011" 
    rv = client.get(f'/product/{fake_id}')
    # Esperamos 404 pois esse ID não deve existir, ou 200 se existir. 
    # O teste original usava int=1, que agora falha pois não é ObjectId valido (400)
    assert rv.status_code == 404

def test_get_product_invalid_id_format(client):
    product_id = "invalid-id"
    rv = client.get(f'/product/{product_id}')
    assert rv.status_code == 400
    assert "error" in rv.json

def test_update_product(client):
    product_id = 1
    rv = client.put(f'/product/{product_id}')
    assert rv.status_code == 200
    assert rv.json == {"message": f"Esta é a rota de atualizacao do produto com o id {product_id}"}

def test_delete_product(client):
    product_id = 1
    rv = client.delete(f'/product/{product_id}')
    assert rv.status_code == 200
    assert rv.json == {"message": f"Esta é a rota de deleção do produto com o id {product_id}"}

def test_upload_sales(client):
    rv = client.post('/sales/upload')
    assert rv.status_code == 200
    assert rv.json == {"message": "Esta é a rota de upload do arquivo de vendas"}

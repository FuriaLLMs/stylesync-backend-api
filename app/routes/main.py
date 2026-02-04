from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.models.user import LoginPayload
from app.models.product import Product, ProductDBModel
from app import db # Importa a conexão do banco
from bson import ObjectId # Para trabalhar com o ID do Mongo

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    return jsonify({"message": "Bem-vindo à API da StyleSync!"})

# RF: O sistema deve permitir que um usuário se autentique para obter um token
@main_bp.route('/login', methods=['POST'])
def login():
    try:
        # 1. Captura os dados enviados na requisição (JSON)
        raw_data = request.get_json()
        
        # 2. Valida os dados usando o Pydantic (LoginPayload)
        # O **raw_data desempacota o dicionário para preencher a classe
        user_data = LoginPayload(**raw_data)

        # 3. Simula a verificação de credenciais (Hardcoded conforme a aula)
        if user_data.username == 'admin' and user_data.password == '123':
            return jsonify({"message": "Login bem-sucedido!"})
        else:
            # Retorna 401 (Não Autorizado) se a senha estiver errada
            return jsonify({"message": "Credenciais invalidas!"}), 401

    except ValidationError as e:
        # 4. Retorna erro 400 se os dados não seguirem o modelo (ex: faltou senha)
        return jsonify({"error": e.errors()}), 400
        
    except Exception as e:
        # Retorna erro 500 para qualquer outro problema interno
        return jsonify({"error": "Erro durante a requisição do dado"}), 500

# RF: O sistema deve permitir listagem de todos os produtos
@main_bp.route('/products', methods=['GET'])
def get_products():
    # Busca todos os documentos na coleção 'products'
    # TODO: Error handling if db is None?
    if db is None:
         return jsonify({"error": "Database not connected"}), 500

    products_cursor = db.products.find()
    
    # List comprehension poderosa que valida e serializa cada item numa linha só
    products_list = [
        ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True) 
        for product in products_cursor
    ]
        
    return jsonify(products_list)

# RF: O sistema deve permitir a criacao de um novo produto
@main_bp.route('/products', methods=['POST'])
def create_product():
    if db is None:
         return jsonify({"error": "Database not connected"}), 500

    try:
        # 1. Captura os dados JSON enviados
        raw_data = request.get_json()
        
        # 2. Valida os dados usando o modelo Pydantic
        # Se faltar campo obrigatório ou tipo errado, o Pydantic lança ValidationError
        product = Product(**raw_data)
        
        # 3. Prepara os dados para salvar (converte para dicionário Python)
        product_dict = product.model_dump()
        
        # 4. Insere no MongoDB
        result = db.products.insert_one(product_dict)
        
        # 5. Retorna sucesso com o ID gerado pelo banco
        # Importante converter ObjectId para string antes de serializar o próprio dicionário se formos retorná-lo
        product_dict['_id'] = str(result.inserted_id)

        return jsonify({
            "message": "Produto criado com sucesso!",
            "_id": str(result.inserted_id), 
            "data": product_dict
        }), 201 # Status 201 Created
        
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
        
    except Exception as e:
        return jsonify({"error": f"Erro ao criar produto: {e}"}), 500

# RF: O sistema deve permitir a visualizacao dos detalhes de um unico produto
@main_bp.route('/product/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    if db is None:
         return jsonify({"error": "Database not connected"}), 500

    try:
        # Converte a string da URL para ObjectId
        oid = ObjectId(product_id)
        
        # Busca um único documento pelo _id
        product = db.products.find_one({"_id": oid})
        
        if product:
             # Usa o modelo para serializar corretamente
            product_model = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
            return jsonify(product_model)
        else:
            return jsonify({"error": f"Produto com o id: {product_id} - Não encontrado"}), 404
            
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar o produto: {e}"}), 400

# RF: O sistema deve permitir a atualizacao de um unico produto e produto existente
@main_bp.route('/product/<product_id>', methods=['PUT'])
def update_product(product_id):
    # TODO Update for mongo
    return jsonify({"message": f"Esta é a rota de atualizacao do produto com o id {product_id}"})

# RF: O sistema deve permitir a delecao de um unico produto e produto existente
@main_bp.route('/product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    # TODO Update for mongo
    return jsonify({"message": f"Esta é a rota de deleção do produto com o id {product_id}"})

# RF: O sistema deve permitir a importacao de vendas através de um arquivo
@main_bp.route('/sales/upload', methods=['POST'])
def upload_sales():
    return jsonify({"message": "Esta é a rota de upload do arquivo de vendas"})

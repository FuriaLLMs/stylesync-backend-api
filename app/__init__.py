from flask import Flask
from pymongo import MongoClient

# Variável global para ser importada nos outros arquivos
db = None

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    global db
    try:
        # Conecta ao MongoDB usando a URI do config
        client = MongoClient(app.config['MONGO_URI'])
        db = client.get_default_database()
        print("Conexão com MongoDB realizada com sucesso!")
    except Exception as e:
        print(f"Erro ao realizar a conexao com o banco de dados: {e}")

    # Importações movidas para cá para evitar Ciclo de Importação
    from .routes.main import main_bp
    from .routes.category_routes import category_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(category_bp)
    
    return app

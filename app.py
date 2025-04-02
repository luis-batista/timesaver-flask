from flask import Flask
from models.database import init_db
from controllers import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Inicializar banco de dados
    with app.app_context():
        init_db()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'])
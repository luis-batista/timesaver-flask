from controllers.agendamento import agendamento_bp
from controllers.cliente import cliente_bp

def register_blueprints(app):
    app.register_blueprint(agendamento_bp)
    app.register_blueprint(cliente_bp)
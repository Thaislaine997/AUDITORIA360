from flask import Flask

def register_blueprints(app: Flask):
    """
    Registra todos os blueprints da aplicação.
    """
    from .empresas_routes import empresas_bp
    from .folhas_routes import folhas_bp
    from .dashboard_routes import dashboard_bp

    app.register_blueprint(empresas_bp, url_prefix='/api/v1/empresas')
    app.register_blueprint(folhas_bp, url_prefix='/api/v1/folhas')
    app.register_blueprint(dashboard_bp, url_prefix='/api/v1/dashboard')
    
    # Adicione aqui outros blueprints se necessário
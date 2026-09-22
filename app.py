from flask import Flask, render_template
from config import Config
from models import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    from routes.business import business_bp
    app.register_blueprint(business_bp)

    from routes.assets import assets_bp
    app.register_blueprint(assets_bp)

    from routes.threats import threats_bp
    app.register_blueprint(threats_bp)

    from routes.assessment import assessment_bp
    app.register_blueprint(assessment_bp)

    from routes.reports import reports_bp
    app.register_blueprint(reports_bp)

    from utils.auth_utils import get_current_business
    @app.context_processor
    def inject_business():
        return dict(current_business=get_current_business())

    @app.route('/')
    def index():
        return render_template('landing.html')

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=4444)

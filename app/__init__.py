from flask import Flask, render_template
from config import Config
from app.database.db import close_db
from app.routes.admin import teams, matches,scorers,scores,seasons,stadiums,standings,users,coaches,referees,faculties,decorators,leagues,players
from app.routes.admin_routes import admin_bp
from app.routes.user_routes import user_bp
from app.routes.auth_bp import auth_bp  



def create_app():
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY

    # Registrar blueprints
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)

    # Manejo de teardown
    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

    # Error handler
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return app

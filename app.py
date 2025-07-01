from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from models import User, init_db

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    app.config['DB_NAME'] = 'expenses.db'
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    bcrypt = Bcrypt(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    # Database setup
    init_db()

    # Register blueprints
    from auth import auth_bp
    from expenses import expenses_bp
    from budgets import budgets_bp
    from incomes import incomes_bp
    from dashboard import dashboard_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(budgets_bp)
    app.register_blueprint(incomes_bp)
    app.register_blueprint(dashboard_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) 
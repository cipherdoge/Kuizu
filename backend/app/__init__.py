from .models import db, User
from .routes import api
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from datetime import datetime


def create_app():
    app = Flask(__name__)
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    app.config['JWT_SECRET_KEY'] = 'himitsu'  
    jwt = JWTManager(app)

    db.init_app(app)
    initialize_admin(app)
    app.register_blueprint(api, url_prefix='/api')

    with app.app_context():
        db.create_all()

    return app




def initialize_admin(app1):
    with app1.app_context():
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            print("No admin found, creating one.")
            new_admin = User(username='admin', password=generate_password_hash('your_secure_password', method='scrypt'), is_admin = True, dob = datetime.strptime("15/11/1999", '%d/%m/%Y').date(),qualification = "B.Tech")
            db.session.add(new_admin)
            db.session.commit()
        else:
            print("Admin already exists.")


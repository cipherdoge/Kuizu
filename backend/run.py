from app import create_app, db
from app.routes import api

app = create_app()
app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

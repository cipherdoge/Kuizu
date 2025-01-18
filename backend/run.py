from app.routes import api
from app.models import db
from flask_cors import CORS
from app import create_app

app = create_app()
CORS(app)


if __name__ == '__main__':
    app.run(port=5000,debug=True)


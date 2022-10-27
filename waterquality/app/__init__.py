from flask import Flask

flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = 'sh...-keep-this-a-secret'
flask_app.secret_key="123"

from app import routes

from flask import Flask
from flask_cors import CORS

flask_app = Flask(__name__)
CORS(flask_app)

flask_app.config['SECRET_KEY'] = 'sh...-keep-this-a-secret'
flask_app.secret_key="123"

from app import routes

from tkinter import *
import _tkinter
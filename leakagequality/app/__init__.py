from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'sh...-keep-this-a-secret'
app.secret_key="123"

from app import routes

from tkinter import *
import _tkinter

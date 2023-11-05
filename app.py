from flask import Flask
from config import app, jwt
from routes import *

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from xrpl.clients import JsonRpcClient

app = Flask(__name__)

testnet_url = "https://s.altnet.rippletest.net:51234"
xrpl_client = JsonRpcClient(testnet_url)

app.config['MONGO_URI'] = 'mongodb+srv://tauseefahmad:tauseef12@cluster0.ivlps4o.mongodb.net/payment_processor'
mongo = PyMongo(app)
app.config['JWT_SECRET_KEY'] = '123'
jwt = JWTManager(app)

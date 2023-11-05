from flask import Flask
from models import payment_processor_api
from config import app

# All routes here
app.add_url_rule('/register', 'register', payment_processor_api.register, methods=['POST'])
app.add_url_rule('/login', 'login', payment_processor_api.login, methods=['POST'])
app.add_url_rule('/balance', 'get_balance', payment_processor_api.get_balance, methods=['GET'])
app.add_url_rule('/send_payment', 'send_payment', payment_processor_api.send_payment, methods=['POST'])
app.add_url_rule('/xrpl_send_payment', 'xrpl_send_payment', payment_processor_api.xrpl_send_payment, methods=['POST'])

app.add_url_rule('/add_money', 'add_money', payment_processor_api.add_money, methods=['POST'])
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from xrpl.models.transactions import Payment
import xrpl.transaction
from config import *
from xrpl.wallet import generate_faucet_wallet


app = Flask(__name__)
bcrypt = Bcrypt(app)

#PaymentProcessorAPI class
class PaymentProcessorAPI:
    def register(self):
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        
        if self.find_user_by_username(username):
            return jsonify({'message': 'Username already exists'}), 400
        # Generate an XRPL wallet for the user
        client = xrpl.clients.JsonRpcClient(testnet_url)
        xrpl_wallet = generate_faucet_wallet(client)
        if xrpl_wallet is None:
            return jsonify({'error': 'Failed to generate XRPL wallet'}), 500
        xrpl_address = xrpl_wallet.classic_address

        user = {
            'username': username,
            'email': email,
            'password': password,
            'balance': 0,
            'xrpl_address': xrpl_address
        }
        self.save_user(user)
        
        return jsonify({'message': 'User registered successfully','xrpl_address': xrpl_address}), 201

    def login(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        user = self.find_user_by_username(username)
        
        if user and bcrypt.check_password_hash(user['password'], password):
            access_token = create_access_token(identity=username)
            return jsonify({'access_token': access_token}), 200
        
        return jsonify({'message': 'Invalid credentials'}), 401
    
    ########### Add More Routes #################
    def add_money(self):
        data = request.get_json()
        username = data['username']
        amount = data['amount']
        user = self.find_user_by_username(username)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        user['balance'] += amount
        self.update_user_balance(user)
        return jsonify({'message': 'Money added successfully'}), 200
#####################################################################

    @jwt_required()
    def get_balance(self):
        current_user = get_jwt_identity()
        user = self.find_user_by_username(current_user)
        
        return jsonify({'balance': user['balance']}), 200
    
    @jwt_required()
    def send_payment(self):
        current_user = get_jwt_identity()
        data = request.get_json()
        recipient_username = data['recipient_username']
        amount = data['amount']

        # Check if the recipient exists
        recipient = self.find_user_by_username(recipient_username)
        if not recipient:
            return jsonify({'message': 'Recipient not found'}), 404

        # Check if the sender has enough balance
        sender = self.find_user_by_username(current_user)
        if sender['balance'] < amount:
            return jsonify({'message': 'Insufficient balance'}), 400

        # Perform the transaction
        sender['balance'] -= amount
        recipient['balance'] += amount

        # Update balances in the database
        self.update_user_balance(sender)
        self.update_user_balance(recipient)

        return jsonify({'message': 'Payment sent successfully'}), 200

    def find_user_by_username(self, username):
        return mongo.db.users.find_one({'username': username})

    def save_user(self, user):
        mongo.db.users.insert_one(user)

    def update_user_balance(self, user):
        mongo.db.users.update_one({'username': user['username']}, {'$set': {'balance': user['balance']}})

    ####################  PART 2  #############################
    @jwt_required()
    def xrpl_send_payment(self):
        current_user = get_jwt_identity()
        data = request.get_json()
        recipient_username = data['recipient_username']
        amount = data['amount']
        recipient = self.find_user_by_username(recipient_username)
        if not recipient:
            return jsonify({'error': 'Recipient not found'}), 404
        
        # Check if the sender has enough balance
        sender = self.find_user_by_username(current_user)

        if sender['balance'] < amount:
            return jsonify({'error': 'Insufficient balance'}), 400
        sender_wallet = xrpl.wallet.generate_faucet_wallet(xrpl_client)
        sender_wallet_secret = sender_wallet.seed
        sender_address = sender_wallet.classic_address

        payment = xrpl.models.transactions.Payment(
        account=sender_address,
        amount=xrpl.utils.xrp_to_drops(amount),
        destination=recipient['xrpl_address']
    )
        response = xrpl.transaction.submit_and_wait(payment, xrpl_client, sender_wallet)
        if response.is_successful():
            sender['balance'] -= amount
            self.update_user_balance(sender)
            return jsonify({'message': 'XRP payment sent successfully'}), 200
        return jsonify({'error': 'XRP transaction failed'}), 500

# Initialize the API
payment_processor_api = PaymentProcessorAPI()
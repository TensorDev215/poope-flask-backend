from flask import Blueprint, jsonify, request
from .models import Wallet, db, Transaction, User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
from decimal import Decimal
from flask_socketio import SocketIO, send, emit
from .extensions import socketio, cache
from sqlalchemy import event

import random
from datetime import datetime

from flask_caching import Cache

from pycoingecko import CoinGeckoAPI


main = Blueprint('main', __name__)

@main.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify(message="Hello from Flask")

@event.listens_for(Transaction, 'after_insert')
def send_notification(mapper, connection, target):
    socketio.emit('new_notification', {
        'id': target.id,
        'wallet_id': target.wallet_id,
        'amount': str(target.amount),
        'date': target.date.isoformat(),
        'type': target.type
    })


@main.route('/api/connect', methods=['POST'])
def connect():
    wallet_address = request.json.get('address')

    if not wallet_address:
        return jsonify({"message": "Wallet address is required"}), 400
    
    wallet = Wallet.query.filter_by(address=wallet_address).first()

    if wallet:
        wallet_id = str(wallet.id)
        access_token = create_access_token(identity=str(wallet.id))
        return jsonify(access_token=access_token, address=wallet.address, amount=wallet.amount)
    else:
        new_wallet = Wallet(address=wallet_address, amount=2000)
        db.session.add(new_wallet)
        db.session.commit()

        access_token = create_access_token(identity=str(new_wallet.id))
        return jsonify(access_token=access_token, amount=new_wallet.amount)
    
@main.route('/api/user_info', methods=['POST'])
@jwt_required()
def create_user():
    request_wallet_id = get_jwt_identity()

    request_wallet = Wallet.query.filter_by(id=request_wallet_id).first()

    if not request_wallet:
        return jsonify({"message": "wallet is not found"}), 404
    
    user = User.query.filter_by(wallet_id=request_wallet_id).first()

    if user:
        user.name = request.json.get("name")
        user.email = request.json.get("email")

        db.session.commit()
        return jsonify({"message": "User is updated successfully"}), 200
    else:
        new_user = User(
            wallet_id = request_wallet_id,
            name = request.json.get('name'),
            email = request.json.get('email')
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User is created successfully"}), 201
    
@main.route('/api/get_user', methods=['GET'])
@jwt_required()
def get_user():
    req_wallet_id = get_jwt_identity()

    user = User.query.filter_by(wallet_id=req_wallet_id).first()

    if user:
        return jsonify({
            "name": user.name,
            "email": user.email,
            "image": user.image,
        }), 200
    else:
        return jsonify({"message": "User is not founded."}), 404



@main.route('/api/wallets', methods=['GET'])
@jwt_required()
def get_wallets():
    wallets = Wallet.query.all()
    return jsonify([wallet.address for wallet in wallets]), 200

@main.route('/api/history', methods=['GET'])
@jwt_required()
def get_history():
    wallets = Wallet.query.all()

    all_transactions = []

    for wallet in wallets:
        transactions = Transaction.query.filter_by(wallet_id=wallet.id).all()

        for tx in transactions:
            all_transactions.append({
                'id': tx.id,
                'address': wallet.address,
                'amount': str(tx.amount),
                'date': tx.date.strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'Buy' if tx.type == 0 else 'Swap'
            })

    return jsonify(all_transactions), 200



@main.route('/api/transact', methods=['POST'])
@jwt_required()
def transact_poope():
    wallet_id = get_jwt_identity()

    amount = request.json.get('amount')
    type = request.json.get('type')


    if (request.json.get('type')):
        type = 0
    else:
        type = 1

    if not amount:
        return jsonify({"message: Amount is required."}), 400
    
    wallet = Wallet.query.get(wallet_id)

    if not wallet:
        return jsonify({"message": "Wallet is not found."}), 404
    
    transaction = Transaction(
        wallet_id=wallet.id,
        amount=amount,
        date=datetime.datetime.utcnow(),
        type=type
    )

    match type:
        case 0:
            db.session.add(transaction)
            wallet.amount += Decimal(amount)
            db.session.commit()
        case 1:
            if (wallet.amount > amount):
                db.session.add(transaction)
                wallet.amount -= Decimal(amount)
                db.session.commit()
            else:
                return jsonify({
                    "message": "The wallet doesn't contain much coin."
                })

    return jsonify({
        "message": "Transaction is successful.",
    }), 201


@cache.cached(key_prefix="binary")
def random_binary():
    return [random.randrange(0, 2) for i in range(500)]


@main.route("/api/get/binary")
def get_binary():
    return jsonify({"data": random_binary()})

@main.route("/api/clear-cache")
def clear_cache():
    cache.clear()
    
@cache.cached(key_prefix="coin")
def coin_data():
    cg = CoinGeckoAPI()
    ohlc = cg.get_coin_ohlc_by_id(id = 'ethereum', vs_currency="usd", days="30") 

    ohlc_with_dates = []

    for entry in ohlc:
        timestamp = entry[0]
        date = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        ohlc_with_dates.append([date] + entry[1:])
    return ohlc_with_dates

@main.route("/api/coin", methods=['GET'])
@jwt_required()
def get_coin():
    return jsonify({'data': coin_data()})
# id = 'ethereum'
# vs_currency = 'usd'
# days = '30'  # '1', '7', '30', '365', 'max'



    


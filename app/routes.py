from flask import Blueprint, jsonify, request
from .models import Wallet, db, Transaction
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
from decimal import Decimal

main = Blueprint('main', __name__)

@main.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify(message="Hello from Flask")

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
    


@main.route('/api/wallets', methods=['GET'])
@jwt_required()
def get_wallets():
    wallets = Wallet.query.all()
    return jsonify([wallet.address for wallet in wallets])

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

    return jsonify(all_transactions)



@main.route('/api/transact', methods=['POST'])
@jwt_required()
def transact_poope():
    wallet_id = get_jwt_identity()

    print(request) 
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
        return jsonify({"message": "Wallet not found."}), 404
    
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
                    "message": "The wallet doesn't contain much."
                })

    return jsonify({
        "message": "Transaction successful.",
        # "tranaction_id": transaction.id,
        # "wallet_id": transaction.wallet_id,
        # "amount": str(transaction.amount),
        # "date": transaction.date.isoformat(),
        # "type": transaction.type
    }), 201

    


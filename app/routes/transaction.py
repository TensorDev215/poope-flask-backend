from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Wallet, Transaction
from ..extensions import db

from datetime import datetime
from decimal import Decimal


transaction_bp = Blueprint("transaction", __name__, url_prefix="/api")


@transaction_bp.route("/history", methods=["GET"])
@jwt_required()
def get_history():
    wallets = Wallet.query.all()

    all_transactions = []

    for wallet in wallets:
        transactions = Transaction.query.filter_by(wallet_id=wallet.id).all()

        for tx in transactions:
            all_transactions.append({
                "id": tx.id,
                "address": wallet.address,
                "amount": str(tx.amount),
                "date": tx.date.strftime("%Y-%m-%d %H:%M:%S"),
                "type": "Buy" if tx.type == 0 else "Swap"
            })

    return jsonify(all_transactions), 200


@transaction_bp.route("/transact", methods=["POST"])
@jwt_required()
def transact_poope():
    wallet_id = get_jwt_identity()

    amount = request.json.get("amount")
    tx_type = request.json.get("type")

    if not amount:
        return jsonify({"message": "Amount is required"}), 400

    amount = Decimal(amount)

    # Convert type properly
    tx_type = 0 if tx_type else 1

    wallet = Wallet.query.get(wallet_id)

    if not wallet:
        return jsonify({"message": "Wallet not found"}), 404

    transaction = Transaction(
        wallet_id=wallet.id,
        amount=amount,
        date=datetime.utcnow(),
        type=tx_type
    )

    if tx_type == 0:
        db.session.add(transaction)
        wallet.amount += amount
        db.session.commit()

    else:
        if wallet.amount >= amount:
            db.session.add(transaction)
            wallet.amount -= amount
            db.session.commit()
        else:
            return jsonify({
                "message": "The wallet doesn't contain enough coins."
            }), 400

    return jsonify({"message": "Transaction successful"}), 201
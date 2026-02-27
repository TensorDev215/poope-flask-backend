from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..models import Wallet, User
from ..extensions import db

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

@auth_bp.route("/connect", methods=['POST'])
def connect():
    wallet_address = request.json.get('address')

    if not wallet_address:
        return jsonify({"message": "Wallet address is required"}), 400
    
    wallet = Wallet.query.filter_by(address=wallet_address).first()

    if wallet:
        access_token = create_access_token(identity=str(wallet.id))
        user_image = ""
        user = User.query.filter_by(wallet_id=wallet.id).first()

        if user:
            user_image = user.image

        return jsonify(access_token=access_token, address=wallet.address, amount=wallet.amount, image=user_image)
    else:
        new_wallet = Wallet(address=wallet_address, amount=2000)
        db.session.add(new_wallet)
        db.session.commit()

        access_token = create_access_token(identity=str(new_wallet.id))
        return jsonify(access_token=access_token, amount=new_wallet.amount, image="")
    


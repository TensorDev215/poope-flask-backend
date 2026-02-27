from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, Wallet
from ..extensions import db

user_bp = Blueprint("user", __name__, url_prefix="/api")

@user_bp.route('/user_info', methods=['POST'])
@jwt_required()
def create_or_update_user():
    request_wallet_id = get_jwt_identity()

    request_wallet = Wallet.query.filter_by(id=request_wallet_id).first()

    user = User.query.filter_by(wallet_id=request_wallet_id).first()

    if user:
        user.name = request.json.get("name")
        user.email = request.json.get("email")

        db.session.commit()

        return jsonify({"message": "User is updated successfully"}), 200
    else:
        new_user=User(
            wallet_id = request_wallet_id,
            name = request.json.get("name"),
            email = request.json.get("email")
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User is created successfully"}), 201

@user_bp.route('/get_user', methods=['GET'])
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
    

        
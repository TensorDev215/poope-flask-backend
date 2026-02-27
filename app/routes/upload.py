from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, Wallet
from ..extensions import db 
from datetime import datetime
import os
from ..utils import allowed_file
from flask import send_from_directory

from werkzeug.utils import secure_filename

upload_bp = Blueprint("upload", __name__)

@upload_bp.route('/api/upload', methods=['POST'])
@jwt_required()
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selelcted file"}), 400
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    original_filename = file.filename
    file_extension = os.path.splitext(original_filename)[1]

    new_filename = f"{timestamp}_{original_filename}"

    if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
        filename = secure_filename(new_filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        request_wallet_id = get_jwt_identity()
        request_wallet = Wallet.query.filter_by(id=request_wallet_id).first()
        user = User.query.filter_by(wallet_id=request_wallet_id).first()

        if user:
            user.image = filename
            db.session.commit()
        else:
            new_user = User(
                wallet_id = request_wallet_id,
                image = filename
            )
            db.session.add(new_user)
            db.session.commit()

        return jsonify({"message": "File uploaded successfully", "filename": filename})
    
    else:
        return jsonify({"error": "File type not allowed"}), 400
    
@upload_bp.route('/static/uploads/<filename>', methods=['GET'])
def serve_uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)



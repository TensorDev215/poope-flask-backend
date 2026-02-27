from flask import Blueprint, jsonify, request, Flask, current_app
from flask_jwt_extended import jwt_required
from ..extensions import cache, db
from pycoingecko import CoinGeckoAPI
import datetime


cache_bp = Blueprint("cache", __name__, url_prefix='/api')

@cache.cached(key_prefix="coin")
def coin_data():
    cg = CoinGeckoAPI()
    ohlc = cg.get_coin_ohlc_by_id(id = 'ethereum', vs_currency="usd", days="30")

    ohlc_with_dates = []

    for entry in ohlc:
        timestemp = entry[0]
        date = datetime.utcdate = datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
        ohlc_with_dates.append([date] + entry[1:])

    return ohlc_with_dates

@cache_bp.route("/coin", methods=['GET'])
@jwt_required()
def get_coin():
    return jsonify({'data': coin_data()})

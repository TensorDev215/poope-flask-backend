"""
wallets table

id
address
amount

transactions table

id
wallet_id
amount
date
type

"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2), unique=False, nullable=True)

    def __repr__(self):
        return f"<Wallet {self.address}>"
    
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.id'), nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2), unique=False, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.Integer, nullable=False) # type=0: Buy, type=1: Swap

    def __repr__(self):
        return f"<Transaction wallet_id={self.wallet_id}, amount={self.amount}, date={self.date}, type={self.type}"
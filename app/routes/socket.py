from sqlalchemy import event
from ..models import Transaction
from ..extensions import db, socketio

@event.listens_for(Transaction, 'after_insert')
def send_notification(mapper, connection, target):
    socketio.emit('new_notification', {
        'id': target.id,
        'wallet_id': target.wallet_id,
        'amount': str(target.amount),
        'date': target.date.isoformat(),
        'type': target.type
    })
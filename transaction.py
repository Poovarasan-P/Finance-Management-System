# backend/app/routes/transactions.py
from flask import Blueprint, request, jsonify
from ..models import db, Transaction
from datetime import datetime

transactions = Blueprint('transactions', __name__)

@transactions.route('/', methods=['POST'])
def create_transaction():
    data = request.get_json()
    new_transaction = Transaction(
        user_id=data['user_id'],
        amount=data['amount'],
        type=data['type'],
        category=data['category'],
        description=data.get('description'),
        transaction_date=data['transaction_date']
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify(new_transaction)

@transactions.route('/<int:id>', methods=['GET'])
def get_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    return jsonify(transaction)

@transactions.route('/<int:id>', methods=['PUT'])
def update_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    data = request.get_json()

    transaction.amount = data['amount']
    transaction.type = data['type']
    transaction.category = data['category']
    transaction.description = data.get('description')
    transaction.transaction_date = data['transaction_date']
    transaction.updated_at = datetime.utcnow()

    db.session.commit()
    return jsonify(transaction)

@transactions.route('/<int:id>', methods=['DELETE'])
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction deleted"})

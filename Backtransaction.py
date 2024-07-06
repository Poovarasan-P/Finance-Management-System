# backend/app/routes/transactions.py
from flask import Blueprint, request, jsonify
from ..models import db, Transaction
from ..middleware import token_required

transactions = Blueprint('transactions', __name__)

@transactions.route('/', methods=['POST'])
@token_required
def create_transaction(current_user):
    data = request.get_json()
    new_transaction = Transaction(user_id=current_user.id, amount=data['amount'], category=data['category'], description=data.get('description', ''))
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({"message": "Transaction created successfully!"}), 201

@transactions.route('/', methods=['GET'])
@token_required
def get_transactions(current_user):
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    result = []
    for transaction in transactions:
        transaction_data = {
            'id': transaction.id,
            'amount': transaction.amount,
            'category': transaction.category,
            'description': transaction.description,
            'transaction_date': transaction.transaction_date
        }
        result.append(transaction_data)
    return jsonify(result)

@transactions.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_transaction(current_user, id):
    transaction = Transaction.query.get_or_404(id)
    if transaction.user_id != current_user.id:
        return jsonify({"message": "Permission denied!"}), 403

    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction deleted!"})

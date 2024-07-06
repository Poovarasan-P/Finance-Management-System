### Project 4: Personal Finance Management System
#### Day-by-Day Instructions

#### Day 4: Transaction Management System

**Objective**: Implement a basic transaction management system including creating, retrieving, and deleting transactions.

**Tasks**:

1. **Set Up Transaction Model**
   - **Create `Transaction` model in `backend/app/models.py`:**
     python
     from . import db

     class Transaction(db.Model):
         id = db.Column(db.Integer, primary_key=True)
         user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
         amount = db.Column(db.Float, nullable=False)
         category = db.Column(db.String(255), nullable=False)
         description = db.Column(db.String(255), nullable=True)
         transaction_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

         user = db.relationship('User', back_populates='transactions')

     User.transactions = db.relationship('Transaction', order_by=Transaction.id, back_populates='user')
     

2. **Create Transaction Routes**
   - **Create `routes/transactions.py` and set up routes for transaction management:**
     python
     from flask import Blueprint, request, jsonify
     from ..models import db, Transaction
     from ..middleware import token_required

     transactions = Blueprint('transactions', _name_)

     @transactions.route('/', methods=['POST'])
     @token_required
     def create_transaction(current_user):
         data = request.get_json()
         new_transaction = Transaction(user_id=current_user.id, amount=data['amount'], category=data['category'], description=data['description'])
         db.session.add(new_transaction)
         db.session.commit()
         return jsonify({"message": "Transaction created successfully!"}), 201

     @transactions.route('/', methods=['GET'])
     @token_required
     def get_transactions(current_user):
         transactions = Transaction.query.filter_by(user_id=current_user.id).all()
         result = []
         for transaction in transactions:
             transaction_data = {'id': transaction.id, 'amount': transaction.amount, 'category': transaction.category, 'description': transaction.description, 'transaction_date': transaction.transaction_date}
             result.append(transaction_data)
         return jsonify(result)

     @transactions.route('/<id>', methods=['DELETE'])
     @token_required
     def delete_transaction(current_user, id):
         transaction = Transaction.query.get_or_404(id)
         if transaction.user_id != current_user.id:
             return jsonify({"message": "Permission denied!"}), 403

         db.session.delete(transaction)
         db.session.commit()
         return jsonify({"message": "Transaction deleted!"})
     

3. **Integrate Transaction Routes**
   - **Update `backend/app/__init__.py` to include transaction routes:**
     python
     from flask import Flask
     from .models import db
     from .routes.users import users
     from .routes.transactions import transactions

     app = Flask(_name_)
     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://finance_user:yourpassword@localhost/personal_finance'
     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

     db.init_app(app)

     app.register_blueprint(users, url_prefix='/users')
     app.register_blueprint(transactions, url_prefix='/transactions')

     @app.route('/')
     def hello_world():
         return 'Hello, World!'

     if _name_ == '_main_':
         app.run(debug=True)
     

4. **Commit and Push Changes to GitHub**
   - Stage and commit the changes:
     bash
     git add .
     git commit -m "Implement transaction management system"
     
   - Push to the GitHub repository:
     bash
     git push origin main
     

**Outcome**: By the end of Day 4, the basic transaction management system will be implemented, including routes for creating, retrieving, and deleting transactions. All changes will be committed and pushed to GitHub.

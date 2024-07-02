from flask import Flask
from .models import db
from .routes.users import users
from .routes.transactions import transactions
from .middleware import token_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://finance_user:yourpassword@localhost/personal_finance'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(transactions, url_prefix='/transactions')

@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': f'Welcome {current_user.username}'})

if __name__ == '__main__':
    app.run(debug=True)

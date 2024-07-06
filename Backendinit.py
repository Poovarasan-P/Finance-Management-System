# backend/app/__init__.py
from flask import Flask
from .models import db
from .routes.users import users
from .routes.transactions import transactions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://finance_user:yourpassword@localhost/personal_finance'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(transactions, url_prefix='/transactions')

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)

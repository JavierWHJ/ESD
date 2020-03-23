from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from os import environ
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@localhost:8889/customers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class Customer(db.Model):
    __tablename__ = 'customers'

    customerID = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    postalcode = db.Column(db.String(512), nullable=False)

    def __init__(self, customerID, name, email, phone, postalcode):
        self.customerID = customerID
        self.name = name
        self.email = email
        self.phone = phone
        self.postalcode = postalcode

    def json(self):
        return {"customerID": self.customerID, "name": self.name, "email": self.email, "phone": self.phone, "postalcode": self.postalcode}


@app.route('/customer', methods=['GET'])
def get_all_customer():
    return jsonify({"customers": [customer.json() for customer in Customer.query.all()]})


@app.route('/customer/<string:customerID>', methods=['GET'])
def get_customer_by_id(customerID):
    customer = Customer.query.filter_by(customerID=customerID).first()
    if customer:
        return jsonify(customer.json())
    return jsonify({"message": "customer ID not found."}), 404


if __name__ == '__main__':
    # if want to build the image use 0.0.0.0
    # localhost is for testing locally
    # app.run(host='localhost', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

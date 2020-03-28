from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from os import environ
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://is213@localhost:8889/prescriptions"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class Prescription(db.Model):
    __tablename__ = 'prescription'
    bookingID = db.Column(db.Integer, primary_key=True)
    doctorID = db.Column(db.String(2), nullable=False)
    customerID = db.Column(db.String(2), nullable=False)
    prescription = db.Column(db.String(500), nullable=False)

    def __init__(self, bookingID, doctorID, customerID, prescription):
        self.bookingID = bookingID
        self.doctorID = doctorID
        self.customerID = customerID
        self.prescription = prescription

    def json(self):
        return {"bookingID": self.bookingID, "doctorID": self.doctorID, "customerID": self.customerID, "prescription": self.prescription}


@app.route("/prescription")
def get_all():
    return jsonify({"prescriptions": [prescription.json() for prescription in Prescription.query.all()]}), 200


@app.route("/prescription/cid=<string:cid>")
def get_prescription_by_cid(cid):
    return jsonify({
        "prescriptions": [prescription.json() for prescription in Prescription.query.filter_by(customerID=cid).all()]
    }), 200


@app.route("/prescription", methods=['POST'])
def add_prescription():
    data = request.get_json()
    prescription = Prescription(data['bookingID'], data['doctorID'], data['customerID'], data['prescription'])

    try:
        db.session.add(prescription)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the record."}), 500

    return jsonify(prescription.json()), 200


@app.route("/prescription", methods=['DELETE'])
def delete_prescription():
    data = request.get_json()
    cid = data['customerID']
    did = data['doctorID']
    bid = data['bookingID']
    prescription = Prescription.query.filter_by(
        bookingID=bid, customerID=cid, doctorID=did).first()

    try:
        db.session.delete(prescription)
        db.session.commit()
        return jsonify({"message": "Successfully deleted record."}), 200
    except:
        return jsonify({"message": "An error occurred while trying to delete record."}), 500


@app.route("/prescription", methods=['PUT'])
def update_prescription():
    data = request.get_json()
    # print(data)
    cid = data['customerID']
    did = data['doctorID']
    bid = data['bookingID']
    prescription = Prescription.query.filter_by(
        bookingID=bid, customerID=cid, doctorID=did).first()
    prescription.prescription = data['prescription']
    try:
        db.session.commit()
        return jsonify({"message": "Successfully updated record."}), 200
    except:
        return jsonify({"message": "An error occurred while trying to update record."}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/doctors'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class Doctor(db.Model):
    __tablename__ = 'doctors'

    doctorID = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(256), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    postalcode = db.Column(db.String(512), nullable=False)
    services = db.Column(db.String(64), nullable=False)

    def __init__(self, doctorID, name, email, sex, price, phone, postalcode, services):
        self.doctorID = doctorID
        self.name = name
        self.email = email
        self.sex = sex
        self.price = price
        self.phone = phone
        self.postalcode = postalcode
        self.services = services

    def json(self):
        return {"doctorID": self.doctorID, "name": self.name, "email": self.email, "sex": self.sex, "price": self.price, "phone": self.phone, "postalcode": self.postalcode, "services": self.services}


@app.route("/doctor")
def get_all():
    return jsonify({"doctors": [doctor.json() for doctor in Doctor.query.all()]})


@app.route("/doctor/<string:doctorID>")
def find_by_doctorID(doctorID):
    doctor = Doctor.query.filter_by(doctorID=doctorID).first()
    if doctor:
        return jsonify(doctor.json())
    return jsonify({"message": "Doctor ID not found."}), 404

@app.route("/doctor/name=<string:name>")
def find_by_name(name):
    doctor = Doctor.query.filter_by(name=name).first()
    if doctor:
        return jsonify(doctor.json())
    return jsonify({"message": "Doctor name not found."}), 404

@app.route("/doctor/name=<string:email>")
def find_by_email(email):
    doctor = Doctor.query.filter_by(email=email).first()
    if doctor:
        return jsonify(doctor.json())
    return jsonify({"message": "Doctor email not found."}), 404


@app.route("/doctor/sex=<string:sex>")
def find_by_sex(sex):
    doctor = Doctor.query.filter_by(sex=sex).all()
    if doctor:
        return jsonify({"doctors": [doctor.json() for doctor in Doctor.query.filter_by(sex=sex).all()]})
    return jsonify({"message": "sex not found."}), 404


@app.route("/doctor/location=<string:location>")
def find_by_location(location):
    doctor = Doctor.query.filter_by(location=location).all()
    if doctor:
        return jsonify({"doctors": [doctor.json() for doctor in Doctor.query.filter_by(location=location).all()]})
    return jsonify({"message": "postal code location not found."}), 404


@app.route("/doctor/services=<string:services>")
def find_by_services(services):
    doctor = Doctor.query.filter_by(services=services).all()
    if doctor:
        return jsonify({"doctors": [doctor.json() for doctor in Doctor.query.filter_by(services=services).all()]})
    return jsonify({"message": "services not found."}), 404


@app.route("/doctor/<int:doctorID>", methods=['POST'])
def create_doctor(doctorID):
    if (Doctor.query.filter_by(doctorID=doctorID).first()):
        return jsonify({"message": "A doctor with doctorID '{}' already exists.".format(doctorID)}), 400

    data = request.get_json()
    doctor = Doctor(doctorID, **data)

    try:
        db.session.add(doctor)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the doctor."}), 500

    return jsonify(doctor.json()), 201


@app.route("/delete-doctor/<int:doctorID>", methods=['DELETE'])
# delete doctor by passing the doctorID through the URL
def delete_doctor(doctorID):
    doctor = Doctor.query.filter_by(doctorID=doctorID).first()

    try:
        db.session.delete(doctor)
        db.session.commit()
        return jsonify({"message": "Successfully deleted record."}), 200
    except:
        return jsonify({"message": "An error occurred while trying to delete record."}), 500


@app.route("/update-doctor", methods=['PUT'])
# pass through the whole JSON Doctor's Object (including doctorID) and update doctorID
def update_doctor():
    data = request.get_json()

    doctorID = data['doctorID']

    doctor = Doctor.query.filter_by(doctorID=doctorID).first()
    if(doctor):
        if('name' in data):
            doctor.name = data['name']
        if('email' in data):
            doctor.email = data['email']
        if('sex' in data):
            doctor.sex = data['sex']
        if('price' in data):
            doctor.price = data['price']
        if('phone' in data):
            doctor.phone = data['phone']
        if('postalcode' in data):
            doctor.location = data['postalcode']
        if('services' in data):
            doctor.services = data['services']
    else:
        return jsonify({"message": "Doctor ID not found."}), 404

    try:
        db.session.commit()
        return jsonify({"message": "Successfully updated record."}), 200
    except:
        return jsonify({"message": "An error occurred while trying to update record."}), 500


if __name__ == '__main__':
    # if want to build the image use 0.0.0.0
    # localhost is for testing locally
    # app.run(host='localhost', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

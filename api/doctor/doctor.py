from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/doctors'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class Doctor(db.Model):
    __tablename__ = 'doctors'

    doctorID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(64), nullable=False)
    services = db.Column(db.String(64), nullable=False)

    def __init__(self, doctorID, name, sex, price, phone, location, services):
        self.doctorID = doctorID
        self.name = name
        self.sex = sex
        self.price = price
        self.phone = phone
        self.location = location
        self.services = services

    def json(self):
        return {"doctorID": self.doctorID, "name": self.name, "sex": self.sex, "price": self.price, "phone": self.phone, "location": self.location, "services": self.services}


@app.route("/doctor")
def get_all():
    return jsonify({"doctors": [doctor.json() for doctor in Doctor.query.all()]})


@app.route("/doctor/<int:doctorID>")
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
#delete doctor by passing the doctorID through the URL
def delete_doctor(doctorID):
    doctor = Doctor.query.filter_by(doctorID=doctorID).first()

    try:
        db.session.delete(doctor)
        db.session.commit()
        return jsonify({"message": "Successfully deleted record."}), 200
    except:
        return jsonify({"message": "An error occurred while trying to delete record."}), 500

@app.route("/update-doctor", methods=['PUT'])
#pass through the whole JSON Doctor's Object (including doctorID) and update doctorID
def update_doctor():
    data = request.get_json()

    doctorID = data['doctorID']
 
    doctor = Doctor.query.filter_by(doctorID=doctorID).first()

    try:
        doctor.name = data['name']
        doctor.sex = data['sex']
        doctor.price = data['price']
        doctor.phone = data['phone']
        doctor.location = data['location']
        doctor.services = data['services']

        db.session.commit()
        return jsonify({"message": "Successfully updated record."}), 200
    except:
        return jsonify({"message": "An error occurred while trying to update record."}), 500
    

    




if __name__ == '__main__':
    app.run(port=5000, debug=True)

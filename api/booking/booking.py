from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/bookings'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class Booking(db.Model):
    __tablename__ = 'bookings'

    bookingID = db.Column(db.integer, primary_key=True)
    customerID = db.Column(db.String(2), nullable=False)
    doctorID = db.Column(db.String(2), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(45), nullable=False)
    services = db.Column(db.String(45), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, bookingID, customerID, doctorID, datetime, location, services, status, price):
        self.bookingID = bookingID
        self.customerID = customerID
        self.doctorID = doctorID
        self.datetime = datetime
        self.location = location
        self.services = services
        self.status = status
        self.price = price

    def json(self):
        return {"bookingID": self.bookingID, "customerID": self.customerID, "doctorID": self.doctorID, "datetime": self.datetime, "location": self.location, "services": self.services, "status": self.status, "price": self.price}


@app.route("/bookings")
def get_all():
    return jsonify({"bookings": [booking.json() for booking in Booking.query.all()]})


@app.route("/bookings/<int:bookingID>")
def find_by_bookingID(bookingID):
    booking = Booking.query.filter_by(bookingID=bookingID).first()
    if booking:
        return jsonify(booking.json())
    return jsonify({"message": "booking ID not found."}), 404


@app.route("/bookings/<int:customerID>")
def find_by_customer(customerID):
    booking = Booking.query.filter_by(customerID=customerID).all()
    if booking:
        return jsonify({"bookings": [booking.json() for booking in Booking.query.filter_by(customerID=customerID).all()]})
    return jsonify({"message": "customer ID not found."}), 404


@app.route("/bookings/<int:doctorID>")
def find_by_doctor(doctorID):
    booking = booking.query.filter_by(doctorID=doctorID).all()
    if booking:
        return jsonify({"bookings": [booking.json() for booking in Booking.query.filter_by(doctorID=doctorID).all()]})
    return jsonify({"message": "doctor ID not found."}), 404


@app.route("/bookings/<string:bookingID>", methods=['POST'])
def create_booking(bookingID):
    if (Booking.query.filter_by(bookingID=bookingID).first()):
        return jsonify({"message": "A booking with bookingID '{}' already exists.".format(bookingID)}), 400

    data = request.get_json()
    booking = Booking(bookingID, **data)

    try:
        db.session.add(booking)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the booking."}), 500

    return jsonify(booking.json()), 201


@app.route("/bookings", methods=['DELETE'])
def delete_booking():
    data = request.get_json()
    bid = data['bookingID']
    booking = Booking.query.filter_by(
        bookingID=bid).first()

    try:
        db.session.delete(booking)
        db.session.commit()
        return jsonify({"message": "Successfully deleted record."}), 200
    except:
        return jsonify({"message": "An error occurred while trying to delete record."}), 500


@app.route("/bookings", methods=['PUT'])
def update_booking():
    data = request.get_json()
    bid = data['bookingID']
    booking = Booking.query.filter_by(
        bookingID=bid).first()
    if(booking):
        if('customerID' in data):
            booking.customerID = data['customerID']
        if('doctorID' in data):
            booking.doctorID = data['doctorID']
        if('datetime' in data):
            booking.datetime = data['datetime']
        if('location' in data):
            booking.location = data['location']
        if('services' in data):
            booking.services = data['services']        
        if('status' in data):
            booking.status = data['status']
        if('price' in data):
            booking.price = data['price']
    try:
        db.session.commit()
        return jsonify({"message": "Successfully updated record."}), 200
    except:
        return jsonify({"message": "An error occurred while trying to update record."}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)

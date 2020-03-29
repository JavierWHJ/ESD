from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import pika
import requests
app = Flask(__name__)

CORS(app)
bookingURL = "http://booking:5000/bookings"
notificationURL = "http://notification:5000/notifications"

def send_to_booking(data):
    # data is json {"booking_id" ,  "customer_id" , "status" : "booked", "service"}
    booking = json.loads(json.dumps(data, default=str))
    r = requests.put(bookingURL, json=booking)
    if r.status_code == 200:
        result = json.loads(r.text.lower())
        return(result)
    else:
        return jsonify({
            "message": "error sending to booking"
        }), 500


@app.route('/make_booking', methods=['POST'])
def make_booking():
    # booking and notification
    # no need entire booking object. bookingid, customerid, doctorid, status, service, notificationID
    data = request.get_data()
    booking = json.loads(data)
    r = requests.put(bookingURL, json=booking)
    if r.status_code != 200:
        return jsonify({
            "message": "error sending to booking"
        }), 500
    else:
        # no error so send notification to doctor
        doctorID = booking['doctorID']
        customerID = booking['customerID']
        hostname = "host.docker.internal"  # change to host.docker.internal before building image
        port = 5672  # port of rabbitmq
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        channel = connection.channel()

        # set up exchange name
        exchangename="notification_topic"
        channel.exchange_declare(exchange=exchangename, exchange_type='topic')

        r = requests.get(notificationURL).json()
        if len(r['notifications']) == 0:
            nid = 1
        else:
            nid = r['notifications'][-1]['nid'] + 1
        notification = {
            "nid" : nid,
            "sender" : customerID,
            "receiver": doctorID,
            "message" : "You have a new booking created",
        }
        notification = json.dumps(notification, default=str)
        channel.basic_publish(exchange=exchangename, routing_key="booking.notification", body=notification, properties=pika.BasicProperties(delivery_mode = 2))
        connection.close()
        return jsonify({
            "message": "Booking successful"
        }), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
